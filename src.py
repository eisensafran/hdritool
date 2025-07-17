#!/usr/bin/env python3

# Batch HDR merging for bracketed TIF images using OpenCV.
# Version 0.3 (2025)

import os
import glob
import exifread
import cv2 as cv
import numpy as np

# path to the directory containing the images
INPUT_DIR = ""

# define the amount of exposures per bracket
BRACKET_SIZE = 5

OUTPUT_DIR = os.path.join(INPUT_DIR, "HDR")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# function to read the image exposure times out of the EXIF data
def get_exposure_time(image_path):
    with open(image_path, 'rb') as img_file:
        tags = exifread.process_file(img_file)
    tag = tags.get("EXIF ExposureTime")

    if tag is None:
        raise ValueError(f"No ExposureTime EXIF tag in {image_path}")

    # normally the "inverted exposure times" need to be calculated since OpenCV does not expect "1/400" but rather "400".
    # see the documentation here: http://man.hubwiz.com/docset/OpenCV.docset/Contents/Resources/Documents/d3/db7/tutorial_hdr_imaging.html
    # see also: https://blog.kyleingraham.com/2020/08/23/radiometric-response-functions-in-opencv/
    # inverted_exposure = 1.0/float(tag.values[0])

    # BUT this produces nonsensical results.
    # By trial and error I found out that the times simply need a multiplication.
    corrected_exposure = float(tag.values[0]*10000)
    print("corrected exposure: ", corrected_exposure)
    return corrected_exposure

tif_paths = sorted(glob.glob(os.path.join(INPUT_DIR, '*.tif')))
if not tif_paths:
    print(f"No .tif files found in {INPUT_DIR}.")
    exit(1)

for idx in range(0, len(tif_paths), BRACKET_SIZE):
    group = tif_paths[idx:idx + BRACKET_SIZE]
    if len(group) < BRACKET_SIZE:
        print(f"Skipping last {len(group)} file(s): not a full bracket.")
        break

    # Load images and times
    images = []
    times = []
    for path in group:
        img = cv.imread(path, cv.IMREAD_UNCHANGED)
        if img is None:
            raise IOError(f"Failed to read image {path}")

        # here is the culprit: cv.createMergeDebevec() only accepts 8bit images.
        # this might be a major drawback
        # convert to 8bit if needed
        if img.dtype != np.uint8:
            # handle 16-bit images
            if img.dtype == np.uint16:
                img = cv.convertScaleAbs(img, alpha=(255.0/65535.0))
                print("16bit detected, image", path, "was converted to 8bit")
            # handle 32-bit / float images
            elif img.dtype == np.float32 or img.dtype == np.float64:
                img_norm = cv.normalize(img, None, 0, 255, cv.NORM_MINMAX)
                img = img_norm.astype(np.uint8)
                print("32bit detected, image", path, "was converted to 8bit")
            else:
                # fallback conversion for any other depth
                img = cv.convertScaleAbs(img)
                print("different color depth detected, image", path, "was converted to 8bit")

        images.append(img)
        times.append(get_exposure_time(path))
    times = np.array(times, dtype=np.float32)



    # Estimate camera response
    # currently this does not produce any meaningful results, therefore commented out
    # calibrate = cv.createCalibrateDebevec()
    # response = calibrate.process(images, times)

    # Merge into HDR
    merge_debevec = cv.createMergeDebevec()
    hdr = merge_debevec.process(images, times)

    # Save result
    output_name = f"merged_{idx // BRACKET_SIZE + 1:03d}.hdr"
    output_path = os.path.join(OUTPUT_DIR, output_name)
    cv.imwrite(output_path, hdr)
    print(f"Saved HDR: {output_path}")

