# First Assignment - Functional filters and convolution filters

Application with GUI for functional and convolution filters.
Requirments:  
  - Load images from file and display them on the screen.
  - Select filter and apply it to the image.
  - (optional) display before and after images side by side.
  - (optional) option to reset image to the original state (without applied filters).
  - Combine any number of filters: apply new filters to the result of other filter.
  - Implement functional filters: (parameters easily modified in code)
  1. Functional filters:
      * inversion
      * brightness correction
      * contrast enhancement
      * gamma correction
  2. Convolution filters (3x3):
      * blur
      * Gaussian smoothing
      * sharpen
      * edge detection
      * emboss
      
# Second Assignment - Error Diffusion and Uniform Quantization

Application with GUI for Error Diffusion and Uniform Quantization.
Requirments:  
  1. Implement 5 different error diffusion filters:
    * Floyd-Steinberg
    * Burkes Filter
    * Stucky Filter
    * Sierra Filter
    * Atkinson Filter
  2. Apply those filter with param M (number of grey levels - 2, 4, 8, 16)
  3. Apply uniform color quantization with param levels (number of colors in each channel or durection of cube) 