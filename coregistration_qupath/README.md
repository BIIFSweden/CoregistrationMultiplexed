# Co-registration in QuPath (Tutorial)


## Pre-requisites

- QuPath v0.4.x
- The Image Combiner Warpy extension v0.2.6

To install the Warpy extension in QuPath, download it from [here](https://github.com/BIOP/qupath-extension-warpy/releases/download/0.2.6/qupath-extension-warpy-0.2.6.zip) and drag and drop the extracted JAR-files from the archive onto the QuPath window. The QuPath documentation also recommends restarting QuPath after installing new extensions. If you have an older version of the extension installed already, you need to go to `Extensions->Installed extensions` in the menu in QuPath, select `Open extensions directory`, and remove the `qupath-extension-warpy-*.jar` file for the older version.  


## Using the Image Combiner Warpy extension

Start by creating a new project in QuPath, and then add to the project the images (OME-TIFF files) that should be co-registered. In this example, we are going to use the DAPI channels from images of three different biomarkers (DNA, RNA, and protein) for the registration, to find the two transform matrices that align the RNA and protein biomarker images against the DNA biomarker images. Here is the single-channel `dna_dapi.ome.tif` that will be used as the reference DAPI image for the registration:

![Screenshot](images/screenshot_new_project.png?raw=true)

The Image Combiner Warpy extension uses the multiview feature of QuPath to provide control over contrast and color (and also channel selection, for multi-channel images) of the overlays shown during the registration. Additional views can be added via `Add row` and `Add column` under `Multi-view` in the menu shown when right-clicking on the image viewport:

![Screenshot](images/screenshot_multiview_menu.png?raw=true)

Here we have added rows and columns to create a grid of 2x2 views: 

![Screenshot](images/screenshot_multiview_split.png?raw=true)

To open another image in one of the views, click on the view to select it, and then double-click on the image in the `Image list` panel. Here we have opened the single-channel `rna_dapi.ome.tif` and the multi-channel `protein_cropped.ome.tif` in two of the additional views:

![Screenshot](images/screenshot_multiview_3images.png?raw=true)

To adjust contrast, color, and channel selection, use the `Brightness & contrast` setting on each view. Here all images have been changed to grayscale, and the DAPI channel from the multi-channel `protein_cropped.ome.tif` image has been selected.   

![Screenshot](images/screenshot_multiview_grayscale.png?raw=true)

The Image Combiner Warpy tool should be available in QuPath under `Analyze->Interactive image combiner warpy`. Before opening the tool, we need to select which image that should be the reference for the registration, by clicking on its corresponding view so that it becomes active (indicated by a red outline around the view, and also by bold text in the `Image list` panel); the final co-registered image will have the same pixel size and resolution as this reference image. Here is what the tool looks like when opening it with `dna_dapi.ome.tif` selected:

![Screenshot](images/screenshot_hello_warpy.png?raw=true)

After opening the tool, other images from the project can be added by clicking on `Choose images from project`. An image selected under the `Image & overlays` panel will display as an overlay on top of the reference image in the viewport. Here one of the other DAPI images, `rna_dapi.ome.tif`, has been selected and will be shown as an overlay:

![Screenshot](images/screenshot_warpy_rna_selected.png?raw=true)

The first step is to provide a coarse alignment that will be used as input to the automatic registration in Warpy. Hold the `Shift` key and click + drag to interactively move the overlay on top of the reference image. The opacity of the overlay can be controlled via the `Opacity' slider. (Note: here the overlay is also shown in a different color, for better visibilty)

![Screenshot](images/screenshot_warpy_aligned_coarse.png?raw=true)

Next, after coarse alignment, we use `Estimate transform` to try to calculate the final transform. The `Pixel size` field controls at which level of detail the registration will be performed at, which can affect the quality of the estimate. 

![Screenshot](images/screenshot_warpy_estimate_transform.png?raw=true)

Here is what the registration between the two DAPI images looks like, after decreasing `Pixel size` to 10 and then calculating the transform via `Estimate transform`:

![Screenshot](images/screenshot_warpy_aligned_fine.png?raw=true)

After having found a good registration between the two DAPI images, we can transfer the transform matrix to other RNA biomarker images (`rna_a647.ome.tif` in this example), by simply copying the values in the text field `Current affine transform being displayed` from one image to another:

![Screenshot](images/screenshot_warpy_matrix.png?raw=true)

Next, we want to repeat the registration procedure for the third biomarker type (protein). In this case, the image `protein_cropped.ome.tif` was captured at a different pixel spacing (0.5082 micron instead of the 0.1619 micron) compared to the reference image, and also has a different orientation. The Warpy extension does not take the pixel spacing into account during registration, meaning there will be mismatch in scale, as seen here in the screenshot:

![Screenshot](images/screenshot_warpy_scale_rotation1.png?raw=true)

Correction for scale and rotation can be provided via the `Scale increment` and `Rotation increment` fields; note that changing these fields also affect the translation of the image, which might cause the image to disappear outside the visible view.

![Screenshot](images/screenshot_warpy_scale_rotation2.png?raw=true)

After correcting for scale and rotation, we can proceed in the same way as for the `rna_dapi.ome.tif` image, i.e. by first doing coarse manual alignment followed by automatic registration via `Estimate transform`. 

![Screenshot](images/screenshot_warpy_scale_rotation3.png?raw=true)

Important: before the next step, we also need to enable all channels in `Brightness & contrast` that were previously unchecked for `protein_cropped.ome.tif`. Otherwise, the Image Combiner Warpy extension will not include them in the combined image. 

![Screenshot](images/screenshot_warpy_enable_channels_before_create.png?raw=true)

After done with registration of all the images, the final step is to click on the `Create` button in the tool to generate a co-registered combined overlay: 

![Screenshot](images/screenshot_warpy_created_overlay.png?raw=true)


## Exporting the result to OME-TIFF

To export the co-registered result for processing or visualization in other software, select the view with the combined overlay generated by Image Combiner Warpy. Then go to `File->Export images->OME TIFF` and press `OK`. A message will be displayed after the export has fininshed (note that this can take a very long time, especially for large images with many channels!)    

![Screenshot](images/screenshot_export_ometiff.png?raw=true)

After the result has been exported, we can try to open the created OME-TIFF file in a new window of QuPath for inspection:

![Screenshot](images/screenshot_coregistration_result.png?raw=true)
