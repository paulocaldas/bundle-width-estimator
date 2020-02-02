## Bundle width estimator for crowded filament networks

Proteins like FtsZ, form networks of filament bundles in vitro. These networks of overlaping filaments tend to be extremely crowded, wich makes the measurement of bundle widths and lengths extremely challenging. Even though the absolute width value of these kind of bundles is virtually impossible to estimate from simple confocal images, we came up with a simple approach to estimate the apparent bundle width combining image segmentation and Eucleadean distance mapping.

### Approach: <br>
(i) Fluorescence images are binarized using an adaptive threshold with a block size of 21 pixels; <br>
(ii) binarized time-lapse movies are then processed with a denoise filter to remove small particles; <br>
(iii) The Euclidean Distance Map (EDM) is calculated for every frame. This transformation results in a grey scale image, where the grey value of each pixel represents the shortest distance to the nearest pixel in the background. Accordingly, bundle widths correspond to the local peak intensities multiplied by 2. All these steps rely on the `skimage` library (check source code inside bkg_func folder). <br>
(iv) The mean bundle width for every frame of the movie is calculated by identifying the peak intensities for each line and column of the image. This value is then plotted as a function of time. All peak distributions are plotted as a function of time (histogram, light to dark blue). Tables and plots are saved in the same directory of the selected movie. <br>

### Instructions: <br>
Simply open the `jupyther` notebook `bundle_width_estimator.ipynb`, insert file_name and run the function with the appropriate parameters.

- `filename`: tif movie to analzye (path/to/filename)
- `time_per_frame`: in seconds
- `cutoff`: truncate analysis by frame number (whole movie = -1)
- `step`: frame interval to analyze (= 1 to analyze every frame)
- `pixel_size`: in microns
- `show_images`: `True` to show pre-processed images as example
- `save_files`: `True` to save final results as txt tables

#### requires this extra package
- `ipywidgets` <br>
(open anaconda prompt and write `pip install ipywidgets`)
