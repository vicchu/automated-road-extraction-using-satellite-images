-----------------------------------------------
	STEP 3(b): Wide Jump Path Detector        
-----------------------------------------------

# Description

This is an optimized version of single pixel path algorithm. It operates on a patch of multiple pixels at a time. Instead of making multiple recursive calls to white pixels of subsequent row, it makes a single call to the pixel with the best score. Another added factor is that of jump which lets a path to continue looking for pixels down a number of rows if no white pixels are found in the one immediately following it. This factor depends on the continuation of path and its length.


# Operations

- Create a thread for each combination of thresholds(length_thresh, angle_thresh)
- Thread:
	- For each patch with a path width, send call locatePath_recursive function to the best scored white pixel in the immediate following row which in turn send call to its  next best scored pixels.
	- Return on deviation beyond angle threshold or no white pixels in a number of rows(jump factor).
	- Retain path if length of path greater than length threshold.
	

# Variables

- Length Threshold/s: [30, 60]
- Angle Threshold/s:  [18]
- Path Width: 8 pixels
- White Pixel Percetage for wider path: 50%
- Jump factor: 0.2 * length of path




	