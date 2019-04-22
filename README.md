# Bundle Width of Filament Networks

Evaluate the mean bundle width of protein filaments is not always a trivial task. For instance, cytoskeleton filaments tend to form networks of overlapping filaments creating an extremely crowded environment. The absolute value of bundle width is virtually impossible to estimate from simple confocal images. To get an approximation of the value without increasing the complexity of my experimental setup, we use an image segmentation approach followed by distance mapping. On a first approach we implemented this procedure by using a combination of multiple ImageJ plugins and a home-built matlab scipt. Here, I combined all the steps of that routine into a single python script.
Regardless of the true absolute value for bundlw width, this estimation is robust enough to compare amongst samples width a different bundle degree.

Approach: <br>
(i) Fluorescence images are binarized using an adaptive threshold. This corrects for non-homogeneous background intensities, overcoming the limitation of conventional threshold methods; <br>
(ii) binarized time-lapse movies are then processed with a denoise filter to remove small particles; <br>
(iii) The Euclidean Distance Map (EDM) is calculated for every frame. This transformation results in a grey scale image, where the grey value of each pixel represents the shortest distance to the nearest pixel in the background. Accordingly, bundle widths correspond to the local peak intensities multiplied by 2. <br>
(iv) The mean bundle width for every frame of the movie is calculated by identifying the peak intensities for each line and column of the image. This value is then plotted as a function of time. <br>

Code: <br>
(i) Run the script to set all the modules and functions <br>
(ii) Analyze time-lapse and set the experimental parameters <br>
      
      movie_to_analyze = 'path\filename.tif'
      bundle_width_estimation(movie_to_analyze, time_per_frame = 2, pixel_size = 0.108, save_files=True);

      # time_per_frame (sec) & pixel_size (microns) 
      # save_files: saves final figures and data as txt
