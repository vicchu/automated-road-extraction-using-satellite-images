-----------------------------------------------
	STEP 3(a): Single Pixel Path Detector        
-----------------------------------------------

### Description

This path detection algorithm operates on one white pixel of the image at a time. At each pixel, 3 recursive calls are made to the white pixels in the subsequent row which in turn send recursive calls to their next three. The direction of the path is controlled using angle deviation threshold which cuts the path when it deviated beyond the threshold. Further a length threshold is used to separate out road segments from small noise.


### Operations

- Create a thread for each combination of thresholds(length_thresh, angle_thresh)
- Thread:
	- For each pixel, send call locatePath_recursive function to 3 white pixels in the immediate following row which in turn send calls to their next 3 pixels
	- Return on deviation beyond angle threshold or no white pixel found in next row.
	- Retain path if length of path greater than length threshold.
	

### Variables

- Length Threshold/s: [30, 40]
- Angle Threshold/s:  [6]



	
