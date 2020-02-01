import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from skimage import filters, color, io
from scipy.ndimage import median_filter, distance_transform_edt
from scipy.signal import argrelextrema

# extra packages for a progress bar
from ipywidgets import FloatProgress
from IPython.display import display


def eucledean_distance_map(img, thresh_block_size = 21, denoise_level = 9):
    '''creates an Eucledean distance map for an input image'''
    img_gray = color.rgb2gray(img) #convert to gray scale
    adaptive_thresh = filters.threshold_local(img_gray, block_size = thresh_block_size, offset=0) # sets the thershold values    img_gray_thres = img_gray > adaptive_thresh # applies the threshold values
    img_gray_thres = img_gray > adaptive_thresh # applies the threshold values
    img_denoise = median_filter(img_gray_thres, size = denoise_level) # reduce image noise by despeckle
    img_EDM = distance_transform_edt(img_denoise) # estimate eucldean distance to the closest dark pixel
    return img_EDM, img_denoise

def find_peaks_to_bundle_width(img_EDM, pixel_size): 
    '''finds the peak intensity of all lines and columns on the EDM image
       and returns the distribution of values, the mean and std pixel_size: in microns'''
    
    peaks = [] #empty list to save all the peaks for each line and each column

    for line in range(img_EDM.shape[0]):
        peaks_lines = argrelextrema(img_EDM[line,: ], np.greater, order =1)[0] # finds the peak positions for each line
        peaks_lines_dist = [img_EDM[line,: ][i] for i in peaks_lines] # saves peak 'intensity' for each position = distance from dark pixel
        peaks.append(peaks_lines_dist) # save each array of peaks for each line in the 'peak' list

    for column in range(img_EDM.shape[1]):
        peaks_columns = argrelextrema(img_EDM[:,column], np.greater, order =1)[0] # finds the peak positions for each line
        peaks_columns_dist = [img_EDM[:, column ][i] for i in peaks_columns] # saves peak 'intensity' for each position = distance from dark pixel
        peaks.append(peaks_columns_dist) # save each array of peaks for each line in the 'peak' list
    
    # pull all the peaks into a single array, discard NA values and correct for pixel size
    # width is equal to peak distance * 2
    
    width_dist = pd.Series(np.concatenate(peaks)).dropna() * pixel_size * 2
    width_mean = np.mean(width_dist)
    width_std = np.std(width_dist)
        
    return width_mean, width_std, width_dist

def analyze_movie(filename, time_per_frame, cutoff = -1, step = 10, pixel_size = 1, show_images = True, save_files = False):
    ''' filename: path/filename of the movie to analyze; time_per_frame: in seconds; 
        cutoff: run analysis up to this frame number, runs for the whole movie by default (-1);
        step: frame interval to analyze (every frame is time consuming)
        pixel_size: in microns (1 micron by default - dummy calibration);
        show_images: show a pre-processed frame as example
        save_files: True to save final results as txt'''
    
    mov = io.imread(filename)
    mov = mov[ :cutoff:step]

    means = []  # list to save means from different frames
    stds  = []  # list to save std from different frames
    sems  = []  # list to save sems (std/sqrt(n)) from different frames
    hists = []  # list to save all histograms from different frames

    # build a progress bar // fancy!
    bar = FloatProgress(description = 'Processing ...', bar_style= 'info', max = mov.shape[0])
    display(bar)

    for frame in mov:
        img_EDM, img_denoised = eucledean_distance_map(frame) # pre-processed function defined above
        mean, std, histogram = find_peaks_to_bundle_width(img_EDM, pixel_size) # function defined above

        means.append(mean)
        stds.append(std)
        sems.append(std/np.sqrt(len(histogram)))
        hists.append(histogram)
        
        bar.value += 1
    
    # show the pre-processing images if needed
    if show_images == True:     
        frame_to_show = mov[int(len(mov)/2)] #show the frame at the middle of the movie as example 
        img_EDM, img_denoised = eucledean_distance_map(frame_to_show) # pre-processed function defined above
        
        fig, ax = plt.subplots(1, 3, figsize = (10,5), dpi = 120)
        ax[0].imshow(frame_to_show); ax[0].set_title('original image (frame '+ str(int(len(mov)/2)) + ')', fontsize = 8);ax[0].axis('off')
        ax[1].imshow(img_EDM); ax[1].set_title('threshold + denoise', fontsize = 8);ax[1].axis('off')
        ax[2].imshow(img_denoised); ax[2].set_title('EDM', fontsize = 8 );ax[2].axis('off');
        
    # save values in organized tables
    
    time_array = np.array(range(0,len(mov))) * time_per_frame * step
    
    hists = pd.DataFrame(hists).T # all histograms as a data frame, each column = one time point in seconds 
    hists.columns = [time_array]
    
    bundle_width_table = pd.DataFrame([time_array, means, stds, sems]).T
    bundle_width_table.columns = ['time','bundle_mean','bundle_std', 'bundle_sem']
    
    if save_files == True:
        bundle_width_table.to_csv(str(filename)[:-4] + '_bundle_width_table.txt', index=False)
        hists.to_csv(str(filename)[:-4] + '_all_histograms.txt', index = False)
        print('results saved as txt in same dir')
        
    time  = bundle_width_table.time
    means = bundle_width_table.bundle_mean
    stds  = bundle_width_table.bundle_std
    sems  = bundle_width_table.bundle_sem

    # plot mean bundle width over time
    
    plt.figure(figsize = (8,3), dpi = 120)
    plt.subplot(1,2,1)
    plt.errorbar(time, means, color = 'darkblue', lw = 2, label = 'mean')
    plt.fill_between(time, means - stds, means + stds, #define upper and lower error
                 color = 'blue', alpha=0.1, label = 'std');

    plt.xlabel('time (s)', fontsize = 10)
    plt.ylabel('bundle width ($\mu$m)', fontsize = 10)
    plt.tick_params(direction = 'in', top = False, right = False)
    plt.xticks(fontsize = 10)
    plt.yticks(fontsize = 10)
    plt.legend(frameon  = True, fontsize = 8)
          
    # plot all histograms 
    
    plt.subplot(1,2,2)

    nCurves = 0
    for col in hists:
        nCurves = nCurves + 1
        counts, bins = np.histogram(hists[col].dropna(), density = True) # how to iterate over columns in pandas
        plt.plot(bins[:-1], counts, '-', lw = 0.5, color = plt.cm.Blues(nCurves*10))

    plt.xlabel('bundle width ($\mu$m)', fontsize = 10)
    plt.ylabel('PDF', fontsize = 10)
    plt.tick_params(direction = 'in', top = False, right = False)
    plt.xticks(fontsize = 10)
    plt.yticks(fontsize = 10);
    plt.subplots_adjust(wspace = 0.3)
      
    # and save plots!
    plt.savefig(filename +'_Bundle_width_results.png', bbox_inches="tight", transparent = True)
    
    return bundle_width_table, hists