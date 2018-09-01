import cv2
import numpy as np
from os.path import join, exists
import threading
import os

#PatchDirection
#PatchLength
#PatchWidth
#VarianceThresh
#OpenClose vs CloseOpen
#OpenKernel
#CloseKernel


def adjustCoordinates(l1,  l2, w1, w2, width, length):
    if l1 < 0:
        l1 = 0
    if l2 >= width:
        l2 = width - 1
    if w1 < 0:
        w1 = 0
    if w2 >= length:
        w2 = length - 1
    return l1, l2, w1, w2

def adjustPixels(m, n, length):
    if m < 0:
        m = 0
    if n >= length:
        n = length - 1
    if n < 0:
        n = 0
    return m, n

def getSqPatchWhitePixels(img, l1, l2, w1, w2, width, length):
    l1, l2, w1, w2 = adjustCoordinates(l1, l2, w1, w2, width, length)
    patch_rows_white_pixels = []
    for m in range(l1, l2):
        white_pixels = 0
        for n in range(w1, w2):
            if img[m][n] == 255:
                white_pixels += 1
        patch_rows_white_pixels.append(white_pixels)

    return patch_rows_white_pixels

def rowsNsUniform(img, i, j, c, length_of_patch, width_of_patch, paths, width, length):
    max_white_row = []
    for k in range(2 * length_of_patch):
        m = i - length_of_patch + k
        n = j - length_of_patch + width_of_patch + k if c == 0 else j + length_of_patch - width_of_patch - k
        row = []
        for z in range(width_of_patch):
            if m >= width:
                break
            m, n = adjustPixels(m, n)
            row.append(img[m][n])
            m += 1
            n = n - 1 if c == 0 else n + 1

        if row.count(255) > max_white_row.count(255):
            max_white_row = row

    for k in range(2 * length_of_patch):
        m = i - length_of_patch + k
        n = j - length_of_patch + width_of_patch + k if c == 0 else j + length_of_patch - width_of_patch - k

        for z in range(width_of_patch):
            if m >= width or z >= len(max_white_row):
                break
            m, n = adjustPixels(m, n)
            if max_white_row[z] == 255:
                paths[m][n] = 255
                if m + 1 < width:
                    paths[m + 1][n] = 255
            else:
                paths[m][n] = 1
                if m + 1 < width:
                    paths[m + 1][n] = 1
            m += 1
            n = n - 1 if c == 0 else n + 1

def getNsPatchWhitePixels(img, i, j, c, length_of_patch, width_of_patch, width):
    patch_rows_white_pixels = []
    for k in range(2 * length_of_patch):
        m = i - length_of_patch + k
        n = j - length_of_patch + width_of_patch + k if c == 0 else j + length_of_patch - width_of_patch - k
        white_pixels = 0
        for z in range(width_of_patch):
            if m >= width:
                break
            m, n = adjustPixels(m, n)
            if img[m][n] == 255:
                white_pixels += 1
            m += 1
            n = n - 1 if c == 0 else n + 1
        patch_rows_white_pixels.append(white_pixels)
    return patch_rows_white_pixels

def makePatchUniform(img, l1, l2, w1, w2, paths, width, length):
    l1, l2, w1, w2 = adjustCoordinates(l1, l2, w1, w2, width, length)
    result = list(map(sum, img[l1:l2, w1:w2]))
    max_white_row = img[l1 + result.index(max(result)), w1:w2]

    for i in range(l1, l2):
        for j in range(w1, w2):
            if max_white_row[j - w1] == 255:
                paths[i][j] = 255
            else:
                paths[i][j] = 1
    return paths


def getMinVariancePatch(img, i, j, length_of_patch, width_of_patch, width, length):
    p1_white_pixels = getSqPatchWhitePixels(img, i - length_of_patch, i + length_of_patch, j - width_of_patch, j + width_of_patch, width, length)
    return np.var(p1_white_pixels)
    '''    
    p2_white_pixels = getSqPatchWhitePixels(i - width_of_patch, i + width_of_patch, j - length_of_patch, j + length_of_patch)
    patch_variances.append(np.var(p2_white_pixels))
    
    p3_white_pixels = getNsPatchWhitePixels(i , j, 0)
    patch_variances.append(np.var(p3_white_pixels))
    
    p4_white_pixels = getNsPatchWhitePixels(i, j, 1)
    patch_variances.append(np.var(p4_white_pixels))
    '''

def combine_images(org_image, st_img, rot_img):
    width = len(org_image)
    length = len(org_image[0])
    r = 10
    for i in range(width):
        for j in range(length):
            try:
                if st_img[i][j] == 255 and rot_img[i][j] == 255:
                    org_image[i][j] = 255
                elif st_img[i][j] == 255:
                    org_image[i][j] = 255
                    if st_img[i][j - 1] == 0:
                        for k in range(1, r):
                            if j - k < length:
                                org_image[i][j - k] = 0
                    if st_img[i][j + 1] == 0:
                        for k in range(1, r):
                            if j + k < length:
                                org_image[i][j + k] = 0

                elif rot_img[i][j] == 255:
                    org_image[i][j] = 255
                    if rot_img[i - 1][j] == 0:
                        for k in range(1, r):
                            if i - k < width:
                                org_image[i - k][j] = 0
                    if rot_img[i + 1][j] == 0:
                        for k in range(1, r):
                            if i + k < width:
                                org_image[i + k][j] = 0
            except:
                continue
    return org_image


def worker(tname, ang_images, length_of_patch, width_of_patch, var_thresh, name):
    print('Thread', tname, 'processing Patch Length:', length_of_patch, '   Patch Width:', width_of_patch)
    results = []
    l = 0

    kernel_length = 10
    kernel_width = 2
    kernels = [[kernel_length, kernel_width], [kernel_width, kernel_length]]
    for aimg in ang_images:
        width = len(aimg)
        length = len(aimg[0])
        paths = np.zeros((width, length))

        for i in range(length_of_patch, width, length_of_patch):
            for j in range(width_of_patch, length, width_of_patch):
                if aimg[i][j] == 255 and paths[i][j] == 0:
                    variance = getMinVariancePatch(aimg, i, j, length_of_patch, width_of_patch, width, length)
                    if variance < var_thresh:
                        paths = makePatchUniform(aimg, i - length_of_patch, i + length_of_patch, j - width_of_patch,
                                                 j + width_of_patch, paths, width, length)

        if l == 1:
            paths = paths.transpose()
        #cv2.imwrite(join(DIR, str(l) + '_' + str(length_of_patch) + '_' + str(width_of_patch) + '_' + str(var_thresh) + '_' + name), paths)
        close = cv2.morphologyEx(paths, cv2.MORPH_CLOSE, np.ones((kernels[l][0], kernels[l][1]), np.uint8))
        open = cv2.morphologyEx(close, cv2.MORPH_OPEN, np.ones((kernels[l][0], kernels[l][1] * 2), np.uint8))
        #cv2.imwrite(join(DIR, 'c_' + str(l) + '_' + str(length_of_patch) + '_' + str(width_of_patch) + '_' + str(var_thresh) + '_' + name), open)
        results.append(open)
        l += 1

    combinedImage = combine_images(ang_images[0], results[0], results[1])
    cv2.imwrite(join(DIR, str(length_of_patch) + '_' + str(width_of_patch) + '_' + str(var_thresh) + '.png'), combinedImage)
    print(join(DIR, str(length_of_patch) + '_' + str(width_of_patch) + '_' + str(var_thresh) + '.png'), 'Saved')


def execute(img, name):
    DIR = join('Variance_test', name)
    print('-----------------------------------------------')
    print('        STEP 2: Applying Variance Test         ')
    print('-----------------------------------------------')

    if not exists(DIR):
        os.mkdir(DIR)

    global DIR
    ang_images = [img, img.transpose()]
    patch_length_vals = [20, 30, 40]
    patch_width_vals = [5, 10]
    var_threshes = [2]

    threads = []
    i = 0
    for length_of_patch in patch_length_vals:
        for width_of_patch in patch_width_vals:
            for var_thresh in var_threshes:
                t = threading.Thread(target=worker, args=(str(i), ang_images, length_of_patch, width_of_patch, var_thresh, name))
                threads.append(t)
                t.start()
                i += 1

    for t in threads:
        t.join()
    print('-----------------------------------------------\n')
