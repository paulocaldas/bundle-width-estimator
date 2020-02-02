## Bundle width estimator for crowded filament networks

Proteins like FtsZ, form networks of filament bundles in vitro. These networks of overllaping filaments tend to be extremely crowded, wich makes the measurement of bundle widths and lengths extremely challenging. Even though the absolute value of bundle width is virtually impossible to estimate from simple confocal images, we can apply a simple approach to estimate the apparent bundle widthcombining image segmentation and Eucleadean distance mapping. 

### Approach: <br>
(i) Fluorescence images are binarized using an adaptive threshold with a block size of 21 pixels; <br>
(ii) binarized time-lapse movies are then processed with a denoise filter to remove small particles; <br>
(iii) The Euclidean Distance Map (EDM) is calculated for every frame. This transformation results in a grey scale image, where the grey value of each pixel represents the shortest distance to the nearest pixel in the background. Accordingly, bundle widths correspond to the local peak intensities multiplied by 2. all these steps rely on the skimage library <br>
(iv) The mean bundle width for every frame of the movie is calculated by identifying the peak intensities for each line and column of the image. This value is then plotted as a function of time. All peak distributions are plotted as a function of time (histogram, light to dark blue). Tables annd plots are saved in the same directory of the analyzed movie. <br>

### Instructions: <br>
Simply open the `jupyther` notebook, insert file_name and run the function with the appropriate parameters.

- `filename`: tif movie to analzye (path/to/filename)
- `time_per_frame`: in seconds
- `cutoff`: set to -1 to analyze the whole movie
- `step`: frame interval
- `pixel_size`: in microns
- `show_images`: `True` to show pre-processed images as example
- `save_files`: `True` to save final results as txt tables

#### requires this extra package
- `ipywidgets` <br>
(open anaconda prompt and write `pip install ipywidgets`)