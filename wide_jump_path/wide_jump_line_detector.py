import cv2
import threading
import math
import numpy as np
from os import mkdir
from os.path import join, exists
from collections import defaultdict

def percent_white_pixel(i, j, gray_image, paths, length):
    num_white_pixels = 1
    total = path_width
    for m in range(j + 1, path_width + j):
        if m >= length or paths[i][m] != 0:
            total = m - j
            break
        if gray_image[i][m] > 200:
            num_white_pixels += 1
    if (num_white_pixels / total * 100) >= white_pixel_thresh:
        return True
    else:
        return False


def locate_WidePath_recursive(i, j, angle_thresh, angle_score, len_score, gray_image, width, length, path_scores, paths):
    if (i, j, angle_score, len_score) in path_scores.keys():
        return path_scores[(i, j, angle_score, len_score)]

    if i + 1 < width and gray_image[i + 1][j] > 200 and percent_white_pixel(i + 1, j, gray_image, paths, length):
        path = locate_WidePath_recursive(i + 1, j, angle_thresh, angle_score, len_score + 1, gray_image, width, length,
                                         path_scores, paths)
    else:
        mscore = 111
        mpixels = []

        for r in range(1, math.ceil(len_score * jmp_factor + 1)):
            if i + r >= width:
                break

            lchk, rchk = 1, 1
            left_pixels, right_pixels = [], []
            lscore, rscore = -111, 111

            for v in range(1, int(angle_thresh / 3) + 1):
                if j - v < 0 or angle_score - v < -angle_thresh:
                    lchk = 0
                if j + v >= length or angle_score + v > angle_thresh:
                    rchk = 0
                if i + r >= width or (lchk == 0 and rchk == 0):
                    break

                if lchk == 1 and j - v >= 0 and i + r < width \
                        and gray_image[i + r][j - v] > 200 and percent_white_pixel(i + r, j - v, gray_image, paths, length):
                    lscore = angle_score - v
                    left_pixels = [i + r, j - v]
                    lchk = 0

                if rchk == 1 and j + v < length and i + r < width \
                        and gray_image[i + r][j + v] > 200 and percent_white_pixel(i + r, j + v, gray_image, paths, length):
                    rscore = angle_score + v
                    right_pixels = [i + r, j + v]
                    rchk = 0

            if len(left_pixels) == 0 and len(right_pixels) == 0:
                continue
            elif -angle_thresh <= lscore <= angle_thresh and (len(right_pixels) == 0 or abs(lscore) <= abs(rscore)):
                if abs(lscore) <= abs(mscore):
                    mscore = lscore
                    mpixels = left_pixels
            elif angle_thresh >= rscore >= -angle_thresh and (len(left_pixels) == 0 or abs(rscore) <= abs(lscore)):
                if abs(rscore) <= abs(mscore):
                    mscore = rscore
                    mpixels = right_pixels

        if len(mpixels) == 0:
            path = []
        else:
            path = locate_WidePath_recursive(mpixels[0], mpixels[1], angle_thresh, mscore, len_score + 1, gray_image,
                                             width, length, path_scores, paths)

    result = [[i, j]] + path
    path_scores[(i, j, angle_score, len_score)] = result
    return result


def worker(tname, gray_image, len_thresh, angle_thresh, name):
    print('Wide Jump   Thread', tname, 'Processing:   Length Thresh:', len_thresh, '   Angle Thresh:', angle_thresh)

    global jmp_factor, path_width, white_pixel_thresh
    path_width = 8
    jmp_factor = 0.2
    white_pixel_thresh = 50
    line_no = 255
    path_scores = defaultdict()
    gray_images = [gray_image, gray_image.transpose()]
    idx = 0

    for img in gray_images:
        width = len(img)
        length = len(img[0])
        paths = np.zeros((width, length))

        angle_score = 0
        len_score = 0
        for i in range(width):
            for j in range(1, length - 1):
                if img[i][j] > 200 and paths[i][j] == 0 and percent_white_pixel(i, j, img, paths, length):
                    path = locate_WidePath_recursive(i, j, angle_thresh, angle_score, len_score + 1, img, width, length,
                                                     path_scores, paths)
                    if len(path) > len_thresh:
                        for point in path:
                            for c in range(path_width):
                                if point[1] + c < length:
                                    paths[point[0]][point[1] + c] = line_no
                    else:
                        for point in path:
                            #for c in range(path_width):
                             #   if point[1] + c < length and \
                            if paths[point[0]][point[1]] != 255:
                                paths[point[0]][point[1]] = -1
        if idx == 0:
            cv2.imwrite(join(DIR, 'Vertical Paths', str(len_thresh) + '_' + str(angle_thresh) + '.png'), paths)
        else:
            cv2.imwrite(join(DIR, 'Horizontal Paths', str(len_thresh) + '_' + str(angle_thresh) + '.png'), paths.transpose())

        path_scores.clear()
        idx += 1
    print(join(DIR, 'Vertical Paths', str(len_thresh) + '_' + str(angle_thresh) + '.png'), 'Processed')
    print(join(DIR, 'Horizontal Paths', str(len_thresh) + '_' + str(angle_thresh) + '.png'), 'Processed')

def execute(gray_image, name):
    global DIR
    print('\n-----------------------------------------------')
    print('       STEP 3(b): Wide Jump Path Detector      ')
    print('-----------------------------------------------\n')

    DIR = join('wide_jump_path', name)
    if not exists(DIR):
        mkdir(DIR)
    if not exists(join(DIR, 'Vertical Paths')):
        mkdir(join(DIR, 'Vertical Paths'))
    if not exists(join(DIR, 'Horizontal Paths')):
        mkdir(join(DIR, 'Horizontal Paths'))

    angle_threshes = [6]
    len_threshes = [80]
    threads = []
    i = 0
    for len_thresh in len_threshes:
        for angle_thresh in angle_threshes:
            t = threading.Thread(target=worker, args=(str(i), gray_image, len_thresh, angle_thresh, name))
            threads.append(t)
            t.start()
            i += 1

    for t in threads:
        t.join()
