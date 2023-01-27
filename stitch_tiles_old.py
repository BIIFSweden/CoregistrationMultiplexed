#!/usr/bin/env python

"""
.. module:: stitch_tiles
   :platform: Linux, Windows
   :synopsis: Script for stiching multiple OME-TIFFs with XY-offsets

.. moduleauthor:: Fredrik Nysjo
"""

import numpy as np
import pandas as pd
import tifffile
import ome_types

import sys
import os


TILE_SIZE_PIXELS = 2048
NUM_TILES = 44
#NUM_TILES = 46
NUM_CHANNELS = 1
INPUT_DIR = "./converted/"

if len(sys.argv) <= 2:
    sys.exit("Usage: ./stitch_tiles.py input_filename csv_filename")
input_filename = sys.argv[1]
csv_filename = sys.argv[2]
if ".nd2" not in input_filename:
    sys.exit("Input filename must be an ND2 file")

output_filename = "stitched.ome.tif"

print("Loading tile positions from " + csv_filename + "...")
tile_offsets_micron = [
    (19883.90, 1264.30),
    (19552.50, 1265.10),
    (19221.50, 1597.20),
    (19553.10, 1596.60),
    (19884.60, 1596.10),
    (20216.00, 1595.50),
    (20879.90, 1925.70),
    (20548.10, 1926.20),
    (20216.80, 1926.80),
    (19885.20, 1927.40),
    (19553.70, 1928.00),
    (19222.10, 1928.80),
    (18890.60, 1929.30),
    (18891.20, 2260.80),
    (19222.70, 2260.40),
    (19554.40, 2259.70),
    (19885.90, 2259.10),
    (20217.30, 2258.40),
    (20549.00, 2257.90),
    (20880.50, 2257.20),
    (20881.00, 2588.70),
    (20549.50, 2589.10),
    (20218.00, 2589.80),
    (19886.50, 2590.50),
    (19554.90, 2591.10),
    (19223.30, 2591.70),
    (18891.90, 2592.40),
    (18892.50, 2924.00),
    (19223.80, 2923.30),
    (19555.50, 2922.80),
    (19887.20, 2922.20),
    (20218.70, 2921.50),
    (20550.10, 2920.80),
    (20881.70, 2920.20),
    (20550.70, 3252.40),
    (20219.30, 3252.90),
    (19887.70, 3253.60),
    (19556.20, 3254.10),
    (19224.70, 3254.80),
    (18893.00, 3255.40),
    (19556.90, 3585.80),
    (19888.40, 3585.10),
    (20219.90, 3584.60),
    (20551.40, 3584.00)
]
#tile_offsets_micron = [
#    (20303.70, 346.20),
#    (19972.10, 346.70),
#    (19640.60, 347.40),
#    (19309.10, 347.90),
#    (19309.70, 679.60),
#    (19641.30, 679.00),
#    (19972.70, 678.30),
#    (20304.30, 677.70),
#    (20635.70, 677.00),
#    (20967.40, 676.50),
#    (20967.90, 1007.90),
#    (20636.40, 1008.40),
#    (20305.10, 1009.10),
#    (19973.20, 1009.80),
#    (19641.80, 1010.40),
#    (19310.40, 1011.00),
#    (18978.70, 1011.60),
#    (18647.30, 1012.30),
#    (18647.90, 1344.10),
#    (18979.40, 1343.30),
#    (19310.90, 1342.60),
#    (19642.50, 1342.00),
#    (19973.90, 1341.40),
#    (20305.60, 1340.70),
#    (20637.10, 1340.10),
#    (20968.40, 1339.50),
#    (20969.10, 1671.00),
#    (20637.50, 1671.60),
#    (20306.30, 1672.20),
#    (19974.50, 1672.80),
#    (19643.10, 1673.40),
#    (19311.60, 1674.10),
#    (18980.00, 1674.70),
#    (18648.50, 1675.30),
#    (18980.80, 2006.30),
#    (19312.10, 2005.60),
#    (19643.80, 2005.10),
#    (19975.10, 2004.50),
#    (20306.80, 2003.80),
#    (20638.30, 2003.20),
#    (20969.70, 2002.50),
#    (20638.90, 2334.70),
#    (20307.50, 2335.10),
#    (19975.70, 2335.90),
#    (19644.40, 2336.50),
#    (19312.70, 2337.10)
#]

first_tile = INPUT_DIR + input_filename + "_0.ome.tif"
print("Loading metadata from " + first_tile + "...")
ome = ome_types.from_tiff(first_tile, parser="lxml")
metadata = {
    "Name": "",
    "PhysicalSizeX": ome.images[0].pixels.physical_size_x,
    "PhysicalSizeY": ome.images[0].pixels.physical_size_y,
    "Channel": {
        "Name": ome.images[0].pixels.channels[0].name,
        "Color": ome.images[0].pixels.channels[0].color.as_int32()
    },
}
pixels_to_micron = ome.images[0].pixels.physical_size_x
micron_to_pixels = 1.0 / pixels_to_micron

print("Allocating output image large enough to fit stiched tiles...")
x_min, y_min = 999999, 999999
x_max, y_max = -999999, -999999
for i in range(0, NUM_TILES):
    x0 = int(micron_to_pixels * tile_offsets_micron[i][0])
    y0 = int(micron_to_pixels * tile_offsets_micron[i][1])
    x1 = x0 + TILE_SIZE_PIXELS
    y1 = y0 + TILE_SIZE_PIXELS
    x_min = min(x_min, x0)
    y_min = min(y_min, y0)
    x_max = max(x_max, x1)
    y_max = max(y_max, y1)
w, h = (x_max - x_min), (y_max - y_min)
output_image = np.zeros((NUM_CHANNELS, h, w), dtype=np.uint16)
#print("  ", x_min, y_min, x_max, y_max)
#print("  ", w, h)

print("Combining tiles into output image...")
channel_names = ["DAPI"]  # TODO
for i in range(0, NUM_TILES):
    x0 = int(micron_to_pixels * tile_offsets_micron[i][0]) - x_min
    y0 = int(micron_to_pixels * tile_offsets_micron[i][1]) - y_min
    x1 = x0 + TILE_SIZE_PIXELS
    y1 = y0 + TILE_SIZE_PIXELS
    tile_filename = INPUT_DIR + input_filename + "_" + str(i) + ".ome.tif"
    tile_image = tifffile.imread(tile_filename)
    output_image[0, y0 : y1, x0 : x1] = tile_image[:, ::-1]

print("Saving output image to file %s..." % output_filename)
tifffile.imwrite(output_filename, output_image, metadata=metadata)

print("Done")
