# automated-road-extraction
Automated roads extraction from satellite imagery using a combination of image processing techniques and dynamic path finding algorithms. Read the project description [here](https://drive.google.com/file/d/1zmWoqN7tSay-REJBXZ0SfHSildUCJhYs/view?usp=sharing)

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for use. All sample images are present in
data directory. See a visual representation of each step [here](https://docs.google.com/presentation/d/1oVIDWYQ5ZnVxSbRWyUtYeC2JI6PqkEe9PoX42nhSgx4/edit?usp=sharing)

## REQUIREMENTS
1. Python 3.x
1. Python Libraries: 
    - OpenCV-Python 3.1.0  
    - numpy  
    - scikit-image

## Inputs
- Image name (python run.py --imagename)
- Input image number after completion of step 2. Step 3 requires manual selecting best image from results of step2 variance test for further processing.

## Running the Code
To run the code, use the following command in the main directory  
- python run.py --image_name

## Example Run

python run.py t3  

Processing Image t3


           STEP 1: Applying Morphology          

Kernel Size: 25x25  
Applying open close operations  
Saved OTSU_thresh.png, noise.png, noise_free.png in the directory " Morphology\t3 "


        STEP 2: Applying Variance Test         

Thread 0 processing Patch Length: 30    Patch Width: 5  
Thread 1 processing Patch Length: 30    Patch Width: 10  
Thread 2 processing Patch Length: 40    Patch Width: 5  
Thread 3 processing Patch Length: 40    Patch Width: 10  
Variance_test\t3\30_5_2.png Saved  
Variance_test\t3\30_10_2.png Saved  
Variance_test\t3\40_5_2.png Saved  
Variance_test\t3\40_10_2.png Saved  

Select image from " variance_test\t3 " for further processing  
1 -> 30_5_2.png  
2 -> 30_10_2.png  
3 -> 40_5_2.png  
4 -> 40_10_2.png  
Enter image number: 1  


      STEP 3(a): Single Pixel Path Detector     

Single Line Thread 0     Length Thresh: 50    Angle Thresh: 3  
Wide Jump Thread 0       Length Thresh: 60    Angle Thresh: 6  
Single Line Thread 1     Length Thresh: 50    Angle Thresh: 6  
...  

       STEP 3(b): Wide Jump Path Detector      

...  
wide_jump_path\t3\Vertical Paths\80_12.png Saved  
wide_jump_path\t3\Horizontal Paths\80_12.png Saved  
single_pixel_path\t3\Vertical Paths\70_3.png Saved  
single_pixel_path\t3\Horizontal Paths\70_3.png Saved  


             STEP 4: Path Refiner                


-- Kernel Size: 5x4  

Refining Wide Jump Path Images  
Refining Single Pixel Path Images  

Projecting Refined Images onto the Satellite Image  

Processing Complete  

All resulting images saved in Results directory  
