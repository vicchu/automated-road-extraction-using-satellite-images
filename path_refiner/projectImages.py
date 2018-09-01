from os.path import join, exists
from os import mkdir, listdir
import cv2
import numpy as np

def execute(img, name):
    DIR1 = join('Results', name, 'Single Pixel Path Results')
    DIR2 = join('Results', name, 'Wide Jump Path Results')
    print('\nProjecting Refined Images onto the Satellite Image...')
    if not exists(join('Results', name)):
        mkdir(join('Results', name))
    if not exists(DIR1):
        mkdir(DIR1)
    if not exists(DIR2):
        mkdir(DIR2)

    files_dir1 = listdir(join('path_refiner', name, 'Single Pixel Path Refined'))
    files_dir2 = listdir(join('path_refiner', name, 'Wide Path Refined'))
    for file in files_dir1:
        path_image = cv2.imread(join('path_refiner', name, 'Single Pixel Path Refined', file))
        path_image[np.where((path_image == [255, 255, 255]).all(axis=2))] = [0, 255, 0]
        cv2.imwrite(join(DIR1, file), cv2.addWeighted(img, 1, path_image, 0.5, 0.0))
    for file in files_dir2:
        path_image = cv2.imread(join('path_refiner', name, 'Wide Path Refined', file))
        path_image[np.where((path_image == [255, 255, 255]).all(axis=2))] = [255, 255, 0]
        cv2.imwrite(join(DIR2, file), cv2.addWeighted(img, 1, path_image, 0.5, 0.0))

    print('All resulting images saved in Results directory\n')
    print('-------------------------------------------------')
