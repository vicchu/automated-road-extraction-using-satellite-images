import os
import cv2
import numpy as np
import threading
from skimage.morphology import skeletonize_3d

def join_broken_paths(broken_image, v1, v2, v3, v4, iter, JOIN):
    if JOIN:
        kernel1 = np.ones((v1, v2), np.uint8)
        kernel2 = np.ones((v3, v4), np.uint8)
        dilation = cv2.dilate(broken_image, kernel1, iterations=iter)
        return cv2.morphologyEx(dilation, cv2.MORPH_CLOSE, kernel2)
    else:
        return broken_image



def worker(tname, dir_name, fol_name, fname, res_fol):
    v1 = 5  #5, 4
    v2 = 2
    ver_kernel = np.ones((v1, v2), np.uint8)
    hor_kernel = np.ones((v2, v1), np.uint8)

    hor_img = cv2.imread(os.path.join(dir_name, fol_name, 'Horizontal Paths', fname), 0)
    ver_img = cv2.imread(os.path.join(dir_name, fol_name, 'Vertical Paths', fname), 0)

    dilation = cv2.dilate(ver_img, ver_kernel, iterations=3)
    erosion = cv2.erode(dilation, ver_kernel, iterations=2)
    join_broken = join_broken_paths(erosion, v1 + 3,  v2 - 1, v1 + 5, v2 + 2, iter=5, JOIN=True)
    skeleton = skeletonize_3d(join_broken)
    ver_refined = cv2.dilate(skeleton, np.ones((v1 + 3, v2 + 2), np.uint8), iterations=1)

    dilation = cv2.dilate(hor_img, hor_kernel, iterations=3)
    erosion = cv2.erode(dilation, hor_kernel, iterations=2)
    join_broken = join_broken_paths(erosion, v2 - 1, v1 + 3, v2 + 2, v1 + 5, iter=5, JOIN=True)
    skeleton = skeletonize_3d(join_broken)
    hor_refined = cv2.dilate(skeleton, np.ones((v2 + 2, v1 + 3), np.uint8), iterations=1)

    refined = cv2.addWeighted(ver_refined, 1, hor_refined, 1, 0.0)
    cv2.imwrite(os.path.join(DIR, res_fol, fname), refined)

def execute(name):
    global DIR
    print('\n-----------------------------------------------')
    print('             STEP 4: Path Refiner                ')
    print('-----------------------------------------------')

    DIR = os.path.join('path_refiner', name)
    if not os.path.exists(DIR):
        os.mkdir(DIR)
    if not os.path.exists(os.path.join(DIR, 'Wide Path Refined')):
        os.mkdir(os.path.join(DIR, 'Wide Path Refined'))
    if not os.path.exists(os.path.join(DIR, 'Single Pixel Path Refined')):
        os.mkdir(os.path.join(DIR, 'Single Pixel Path Refined'))

    print('\n-- Kernel Size: 5x4\n')
    wide_path_files = os.listdir(os.path.join('wide_jump_path', name, 'Horizontal Paths'))
    single_pixel_files = os.listdir(os.path.join('single_pixel_path', name, 'Horizontal Paths'))

    threads = []
    i = 0
    print('Refining Wide Jump Path Images...')
    for file in wide_path_files:
        t = threading.Thread(target=worker, args=(str(i + 1), 'wide_jump_path', name, file, 'Wide Path Refined'))
        threads.append(t)
        t.start()
        i += 1
    print('Refining Single Pixel Path Images...')
    for file in single_pixel_files:
        t = threading.Thread(target=worker, args=(str(i + 1), 'single_pixel_path', name, file, 'Single Pixel Path Refined'))
        threads.append(t)
        t.start()
        i += 1

    for t in threads:
        t.join()



























