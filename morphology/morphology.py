import cv2
import numpy as np
from os.path import exists, join
from os import mkdir


def cannyEdgeDetection(image):
    Hthres = 200
    Lthres = 100
    edges = cv2.Canny(image, Lthres, Hthres)

    width = len(image)
    length = len(image[0])
    for i in range(width):
        for j in range(length):
            if edges[i][j] == 255:
                image[i][j] = [255, 255, 0]
    return image

def unsharp_mask(img, blur_size = (9,9), imgWeight = 1.5, gaussianWeight = -0.5):
    gaussian = cv2.GaussianBlur(img, (5,5), 0)
    return cv2.addWeighted(img, imgWeight, gaussian, gaussianWeight, 0)

def HoughLines(thresh, build_image):
    lines = cv2.HoughLines(thresh, 1, np.pi / 30, 2000)
    print('No of lines:', len(lines))
    idx = 0
    for line in lines:
        rho = line[0][0]
        theta = line[0][1]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))

        cv2.line(build_image, (x1, y1), (x2, y2), (255, 255, 0), 3)
        if idx % 1000 == 0:
            print(idx, 'Complete')
        idx += 1

def skeletonization(img):
    size = np.size(img)
    skel = np.zeros(img.shape, np.uint8)
    element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    done = False

    while (not done):
        eroded = cv2.erode(img, element)
        temp = cv2.dilate(eroded, element)
        temp = cv2.subtract(img, temp)
        skel = cv2.bitwise_or(skel, temp)
        img = eroded.copy()

        zeros = size - cv2.countNonZero(img)
        if zeros == size:
            done = True
    return skel

def execute(img, name):
    DIR = join('Morphology', name)
    print('-----------------------------------------------')
    print('           STEP 1: Applying Morphology         ')
    print('-----------------------------------------------')
    if not exists(DIR):
        mkdir(DIR)

    build_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh_image = cv2.threshold(build_gray, 0, 255,
                                 cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    inv = cv2.bitwise_not(thresh_image)
    close = cv2.morphologyEx(inv, cv2.MORPH_CLOSE, np.ones((2, 2), np.uint8))

    print('Kernel Size: 25x25')
    dim = [25, 25]

    print('Applying open close operations...')
    open = cv2.morphologyEx(close, cv2.MORPH_OPEN, np.ones((dim[0], dim[1]), np.uint8))
    open_close = cv2.morphologyEx(open, cv2.MORPH_OPEN, np.ones((dim[0] // 3 + 1, dim[1] // 3 + 1), np.uint8))
    sub = cv2.bitwise_and(close, cv2.bitwise_not(open_close))

    cv2.imwrite(join(DIR, 'OTSU_thresh.png'), inv)
    cv2.imwrite(join(DIR, 'noise.png'), open_close)
    cv2.imwrite(join(DIR, 'noise_free.png'), sub)
    print('Saved OTSU_thresh.png, noise.png, noise_free.png in the directory "', DIR, '"')
    return sub
    print('-----------------------------------------------\n')

    '''
    kernel = np.ones((12, 12), np.uint8)
    nopening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    gradient = cv2.morphologyEx(thresh, cv2.MORPH_GRADIENT, kernel)
    tophat = cv2.morphologyEx(thresh, cv2.MORPH_TOPHAT, kernel)
    skel = skeletonization(tophat)
    denoise = cv2.fastNlMeansDenoising(thresh)
    #blackhat = cv2.morphologyEx(thresh, cv2.MORPH_BLACKHAT, kernel)
    #closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    '''
