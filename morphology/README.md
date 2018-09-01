-----------------------------------------------
		STEP 1: Applying Morphology         
-----------------------------------------------

### Description

In this step, OTSU thresholding is applied on the input image to convert it into a binary image. The inverse of the binary image results in having roads appearing as white pixels but with a lot of noise coming from buildings and other objects like trees etc.
To remove large parts of noise from the image, an opening and closing morphological operations are applied using large noise sized kernel. This results in having large areas of noise removed while retaining roads pixels along with inseparable noise parts.


### Operations

- OTSU Threshold Operation
- Bitwise NOT(Inverse)
- Morphology Close
- Morphology Open
- Bitwise AND(Subtract)


### Variables

- Kernel Size: 25x25



	
