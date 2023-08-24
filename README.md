# Co-registration of multiplexed images


## File structure

- `stitch_nd2` Python script for performing tile stitching of Nikon ND2 data and converting the result to OME-TIFF format.
- `coregistration_qupath` Tutorial describing how to perform co-registration of a mix of single-channel and multi-channel OME-TIFF files using Warpy in QuPath.


## Python installation (via Anaconda and pip):

1. Install the Anaconda (Miniconda) package manager for Python 3.9 from [here](https://docs.conda.io/en/latest/miniconda.html). On Linux, you can also install it like this:
```
    curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh  
    sh Miniconda3-latest-Linux-x86_64.sh
```
2. Create a new virtual environment (`coregistration`) for the application, from the terminal or Anaconda command line:
```
    conda create --name coregistration python=3.9
```
3. Activate the virtual environment and install the required Python dependendecies (via pip):
```
    conda activate coregistration
    pip install -r requirements.txt
```


## Usage

See the respective README.md file or documentation in each subfolder.


## License

The code is provided under the MIT license (see LICENSE.md).
