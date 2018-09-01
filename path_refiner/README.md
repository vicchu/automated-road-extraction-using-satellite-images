-----------------------------------------------
			STEP 4: Path Refiner        
-----------------------------------------------

# Description

The paths obtained in the previous steps from both algorithms are further refined using a set of morphological techniques(dilation, erosion, skeletonization). The resulting road network is then projected onto the actual satellite image to obtain the final result.


# Operations

- Dilation
- Erosion
- Morphology Close
- Morphology Skeleton
- Dilation
- Project Path onto Image
	

# Variables

- Kernel Size: 5x4




	