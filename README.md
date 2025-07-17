# hdritool
Python script to merge bracketing sequences into HDR images. 

## how to use
The script needs apath to a foulder containing all images and the amount of exposures per bracketing sequence (typically 3, 5, 7 or 9).

## todos
- currently only *.tif images are accepted, this needs to be dynamic
- `cv.createCalibrateDebevec()` does not produce meaningful results
- the script fails, when the source images do not feature any EXIF metadata. An alternative manual method of inputting exposure times would be nice
- the resulting *.hdr files do not feature any EXIF metadata, at least the used camera and lens could be transferred from the source images
