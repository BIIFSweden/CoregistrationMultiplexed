# Co-registration in QuPath (Tutorial)


## Pre-requisites

- QuPath v0.4.x
- The Image Combiner Warpy extension v0.2.6

To install the Warpy extension in QuPath, download it from [here](https://github.com/BIOP/qupath-extension-warpy/releases/download/0.2.6/qupath-extension-warpy-0.2.6.zip) and drag and drop the extracted JAR-files from the archive onto the QuPath window. If you have an older version of the extension installed since earlier, you can go to `Extensions->Installed extensions` in the menu in QuPath, select `Open extensions directory`, and remove the `qupath-extension-warpy-*.jar` file for the older version.  


## Using the Image Combiner Warpy extension

Start by creating a new project in QuPath, and add the images (OME-TIFF files) that should be co-registered to the project. In this example, we are going to use the DAPI channels from three different image modalities (DNA, RNA, and protein) for the registration, to find the two transform matrices to align the RNA and protein images against the DNA images. Here is the single-channel `dna_dapi.ome.tif` that will be used as the reference DAPI image for the registration:

![Screenshot](images/screenshot_new_project.png?raw=true)

The Image Combiner Warpy extension uses the multiview feature of QuPath to provide control over the contrast and color (and also channel selection, for multi-channel images) of overlays shown during the registration. Additonal views can be added via `Add row` and `Add column` under `Multi-view` in the menu whown when right-clicking on the image viewport:

![Screenshot](images/screenshot_multiview_menu.png?raw=true)

Here we have added rows and columns for a grid of 2x2 views: 

![Screenshot](images/screenshot_multiview_split.png?raw=true)

To open more images, click on the view to select it, and then on the image in the `Image list` panel. Here we have opened the single-channel image `rna_dapi.ome.tif` and the multi-channel image `protein_cropped.ome.tif` in two of the additional views:

![Screenshot](images/screenshot_multiview_3images.png?raw=true)

(Add text)

![Screenshot](images/screenshot_multiview_grayscale.png?raw=true)

(Add text)

![Screenshot](images/screenshot_hello_warpy.png?raw=true)

(Add text)

![Screenshot](images/screenshot_warpy_rna_selected.png?raw=true)

(Add text)

![Screenshot](images/screenshot_warpy_aligned_coarse.png?raw=true)

(Add text)

![Screenshot](images/screenshot_warpy_estimate_transform.png?raw=true)

(Add text)

![Screenshot](images/screenshot_warpy_aligned_fine.png?raw=true)

(Add text)

![Screenshot](images/screenshot_warpy_matrix.png?raw=true)

(Add text)

![Screenshot](images/screenshot_warpy_scale_rotation1.png?raw=true)

(Add text)

![Screenshot](images/screenshot_warpy_scale_rotation2.png?raw=true)

(Add text)

![Screenshot](images/screenshot_warpy_scale_rotation3.png?raw=true)

(Add text)

![Screenshot](images/screenshot_warpy_enable_channels_before_create.png?raw=true)

(Add text)

![Screenshot](images/screenshot_warpy_created_overlay.png?raw=true)


## Exporting the result to OME-TIFF

(Add text)

![Screenshot](images/screenshot_export_ometiff.png?raw=true)

(Add text)

![Screenshot](images/screenshot_coregistration_result.png?raw=true)