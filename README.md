# hdritool
Python script to merge bracketing sequences into 32bit HDR images. 

## how to use
The script needs a path to a foulder containing all images and the amount of exposures per bracketing sequence (typically 3, 5, 7 or 9).

## todos
- currently only *.tif images are accepted, this needs to be dynamic
- `cv.createCalibrateDebevec()` does not produce meaningful results
- the script fails, when the source images do not feature any EXIF metadata. An alternative manual method of inputting exposure times would be nice
- the resulting *.hdr files do not feature any EXIF metadata, at least the used camera and lens could be transferred from the source images
- the script explicity tries to extract the images' metadata by searching for "EXIF ExposureTime". I do not know if the name of this tag is always the same across camera manufacturers, therefore a more robust solution might be needed. (currently tested with Nikon D750, Nikon D800, and Nikon Z9)
- a GUI would be nice in the future
