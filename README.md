# Bundle Width of Filament Networks

Evaluate the mean bundle width of protein filaments is not always a trivial task. For instance, cytoskeleton filaments tend to form networks of overlapping filaments creating an extremely crowded environment. The absolute value of bundle width is virtually impossible to estimate from simple confocal images. To get at least an approximation of the real value without increasing the complexity of my experimental setups, we use an image segmentation approach followed by distance mapping. Regardless of the true absolute value, this estimation is robust enough to compare amongst samples width a different bundle degree.

Approach: 
(i) Fluorescence images are binarized using an adaptive threshold. This corrects for non-homogeneous background intensities, overcoming the limitation of conventional threshold methods; 
(ii) binarized time-lapse movies are then processed with a denoise filter to remove small particles; 
(iii) The Euclidean Distance Map (EDM) is calculated for every frame. This transformation results in a grey scale image, where the grey value of each pixel represents the shortest distance to the nearest pixel in the background. Accordingly, bundle widths correspond to the local peak intensities multiplied by 2.  
(iv) The mean bundle width for every frame of the movie is calculated by identifying the peak intensities for each line and column of the image. This value is then plotted as a function of time.
