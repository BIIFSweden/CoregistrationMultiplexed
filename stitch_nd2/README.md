# stitch_nd2

Script for performing tile stitching of Nikon ND2 data, and converting the result to OME-TIFF format. Used in the following project about co-registration of multiplexed images:

https://biifsweden.github.io/projects/2022/11/15/ShahrzadShiraziFard2022-1/


## Basic usage

To stitch and convert a single ND2-dataset (`.nd2` file) to OME-TIFF, activate the `coregistration` conda environment from the command prompt or terminal,

    conda activate coregistration

and then run

    ./stitch_nd2.py input_filename [max|center|first]

or (alternatively)

    python stitch_nd2.py input_filename [max|center|first]

The first argument input_filename must be an .nd2 image file. The second optional argument controls what projection type should be used to project Z-stacks from 3D to 2D:

    max: Use maximum intensity projection along the Z-axis
    center: Use center slice from the Z-stack (default)
    first: Use first slice from the Z-stack (useful for quick preview)

The output OME-TIFF will be written to a `.ome.tif` having same prefix and location as `input_filename`.


## Code style

This project uses the [Black code style](https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html). For automatic formatting, the [black code formatter](https://pypi.org/project/black/) can be installed via pip,

    pip install black

and then applied to a source file like this:

    black sourcefile.py
