-----------------------------------------------
		STEP 2: Applying Variance Test         
-----------------------------------------------

# Description

In this step, to further enhance roads and small alleyways and separate them from noise, a variance test is applied. A small patch is taken from the image at a time and the variance is calculated using counts of white pixels in each row of the patch. If variance of the patch is less than a variance threshold, the number of white pixels is made uniform across all patch rows. The idea behind applying variance test is that variance of a patch belonging to a road tend to be less and have more uniformity across rows as compared to a noisy patch.


# Operations

- Create a thread for each combination of patch variables(length, width, variance_threshold)

- Thread:
	- Iterate the image using the patch
	 	- Calculate patch variance and compare with threshold
	 	- If less than threshold, make patch uniform in terms of white pixels in a row.
	- Morphology Close
	- Morphology Open

# Variables

- Patch length/s: [30, 40]
- Patch width/s:  [5, 10]
- Variance Thresholds: [2, 5]
- Kernel size for open/close: 10x2
