#!/usr/bin/env python

"""
.. module:: stitch_nd2
   :platform: Linux, Windows
   :synopsis: Script for stitching tiles from ND2 file and writing result to OME-TIFF

.. moduleauthor:: Fredrik Nysjo
"""

import numpy as np
import tifffile
from pims import ND2Reader_SDK

import math
import sys
import os


def rgb_to_hex(color):
    """Helper function for converting color from RGB to hexadecimal int32 format"""
    r = int(color[0] * 255.99)
    g = int(color[1] * 255.99)
    b = int(color[2] * 255.99)
    return np.int32((r << 24) + (g << 16) + (b << 8))


def main():
    if len(sys.argv) <= 1:
        sys.exit("Usage: ./stitch_nd2.py input_filename [max|center|first]")
    input_filename = sys.argv[1]
    z_projection = sys.argv[2] if len(sys.argv) > 2 else "center"
    if ".nd2" not in input_filename:
        sys.exit("Input filename must be an ND2 file")
    output_filename = os.path.splitext(input_filename)[0] + ".ome.tif"

    print("Opening ND2 image " + input_filename + "...")
    with ND2Reader_SDK(input_filename) as nd2:
        print("Reading tile positions...")
        tile_size_pixels = nd2.metadata["width"]
        nd2.iter_axes = "m"
        nd2.bundle_axes = "yx"
        num_tiles = nd2.shape[0]
        tile_offsets_micron = []
        for frame in nd2:
            tile_offsets_micron.append((frame.metadata["x_um"], frame.metadata["y_um"]))

        print("Reading other metadata...")
        nd2.iter_axes = []  # Workaround for zero division bug in pims_nd2 library
        metadata = {
            "Name": "",
            "PhysicalSizeX": nd2.metadata["calibration_um"],
            "PhysicalSizeY": nd2.metadata["calibration_um"],
            "Channel": {
                "Name": nd2.metadata["plane_0"]["name"],
                "Color": rgb_to_hex(nd2.metadata["plane_0"]["rgb_value"]),
            },
        }
        pixels_to_micron = nd2.metadata["calibration_um"]
        micron_to_pixels = 1.0 / pixels_to_micron
        nd2.iter_axes = "m"

        print("Allocating output image large enough to fit stitched tiles...")
        x_min, y_min = 999999, 999999
        x_max, y_max = -999999, -999999
        for i in range(0, num_tiles):
            x0 = int(micron_to_pixels * tile_offsets_micron[i][0])
            y0 = int(micron_to_pixels * tile_offsets_micron[i][1])
            x1 = x0 + tile_size_pixels
            y1 = y0 + tile_size_pixels
            x_min = min(x_min, x0)
            y_min = min(y_min, y0)
            x_max = max(x_max, x1)
            y_max = max(y_max, y1)
        w, h = (x_max - x_min), (y_max - y_min)
        output_image = np.zeros((1, h, w), dtype=np.uint16)
        print(output_image.shape)

        print("Combining tiles into output image...")
        print("Z-projection type:", z_projection)
        nd2.bundle_axes = "yx" if z_projection == "first" else "zyx"
        for i, frame in enumerate(nd2):
            print(str(i) + " ", end="", flush=True)
            x0 = int(micron_to_pixels * tile_offsets_micron[i][0]) - x_min
            y0 = int(micron_to_pixels * tile_offsets_micron[i][1]) - y_min
            x1 = x0 + tile_size_pixels
            y1 = y0 + tile_size_pixels
            if z_projection == "max":
                # Do a maximum projection along the Z-axis
                output_image[0, y0:y1, x0:x1] = np.amax(frame, axis=0)[:, ::-1]
            elif z_projection == "center":
                # Use the Z-slice from the middle of the stack
                z_index = frame.shape[0] // 2
                output_image[0, y0:y1, x0:x1] = frame[z_index, :, ::-1]
            else:
                # Use the first Z-slice from the stack
                output_image[0, y0:y1, x0:x1] = frame[:, ::-1]
        print("")

    print("Saving output image to file %s..." % output_filename)
    tifffile.imwrite(output_filename, output_image, metadata=metadata)

    print("Done")


if __name__ == "__main__":
    main()
