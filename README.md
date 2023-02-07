# stitch_nd2

Script for performing tile stitching of Nikon ND2 data, and converting the result to OME-TIFF format. Used in the following project about co-registration of multiplexed images:

https://biifsweden.github.io/projects/2022/11/15/ShahrzadShiraziFard2022-1/


## Example screenshots

![Screenshot](screenshot.png?raw=true "Screenshot")


## Python installation (via Anaconda and pip):

1. Install the Anaconda (Miniconda) package manager for Python 3.9 from [here](https://docs.conda.io/en/latest/miniconda.html). On Linux, you can also install it like this:
```
    curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh  
    sh Miniconda3-latest-Linux-x86_64.sh
```
2. Create a new virtual environment (stitch_nd2), from the terminal or Anaconda command line:
```
    conda create --name stitch_nd2 python=3.9
```
3. Activate the virtual environment and install the required Python dependendecies (via pip):
```
    conda activate stitch_nd2
    pip install -r requirements.txt
```

## Basic usage

To stitch and convert a single ND2-dataset (`.nd2` file) to OME-TIFF, run

    ./stitch_nd2.py input_filename [max|center|first]

or (alternatively)

    python stitch_nd2.py input_filename [max|center|first]

The first argument input_filename must be and .nd2 image file. The second optional argument controls what projection type should be used to project Z-stacks from 3D to 2D:

    max: Use maximum intensity projection along the Z-axis
    center: Use center slice from the Z-stack (default)
    first: Use first slice from the Z-stack (for fast preview)

The output OME-TIFF will be written to a `.ome.tif` having same prefix and location as `input_filename`.


## Code style

This project uses the [Black code style](https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html). For automatic formatting, the [black code formatter](https://pypi.org/project/black/) can be installed via pip,

    pip install black

and then applied to a source file like this:

    black sourcefile.py


## License

The code is provided under the MIT license (see LICENSE.md).
