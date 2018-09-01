import cv2
from os import mkdir
from os.path import join, exists
import threading
import numpy as np
from collections import defaultdict

def locatePath_recursive(i, j, score, gray_image, length, width, paths, path_scores, thresh1, thresh2, angle):

    if (('90' not in angle or score < thresh1 or score > thresh2) and ('45' not in angle or score > thresh2)
        and ('135' not in angle or score < thresh1)) or \
            (((i + 1 >= width) or (gray_image[i + 1][j] < 200))
             and ((i + 1 >= width) or gray_image[i + 1][j - 1] < 200)
             and ((i + 1 >= width) or (j + 1 >= length) or (gray_image[i + 1][j + 1] < 200))):
        return [[i, j]]
    if (i, j, score) in path_scores.keys():
        return path_scores[(i, j, score)]

    routes = []
    if '45' in angle:
        if (i + 1) < width and gray_image[i + 1][j - 1] > 200:
            path = locatePath_recursive(i + 1, j - 1, score - 0.5, gray_image, length, width, paths, path_scores, thresh1, thresh2, angle)
            routes.append(path)
        if (i + 1) < width and gray_image[i + 1][j] > 200:
            path = locatePath_recursive(i + 1, j, score + 1, gray_image, length, width, paths, path_scores, thresh1, thresh2, angle)
            routes.append(path)
        if (i + 1 < width and j + 1 < length) and gray_image[i + 1][j + 1] > 200:
            path = locatePath_recursive(i + 1, j + 1, score + 2, gray_image, length, width, paths, path_scores, thresh1, thresh2, angle)
            routes.append(path)

    elif '90' in angle:
        if (i + 1) < width and gray_image[i + 1][j] > 200:
            path = locatePath_recursive(i + 1, j, score, gray_image, length, width, paths, path_scores, thresh1, thresh2, angle)
            routes.append(path)
        if (i + 1) < width and gray_image[i + 1][j - 1] > 200:
            path = locatePath_recursive(i + 1, j - 1, score - 1, gray_image, length, width, paths, path_scores, thresh1, thresh2, angle)
            routes.append(path)
        if (i + 1 < width and j + 1 < length) and gray_image[i + 1][j + 1] > 200:
            path = locatePath_recursive(i + 1, j + 1, score + 1, gray_image, length, width, paths, path_scores, thresh1, thresh2, angle)
            routes.append(path)

    elif '135' in angle:
        if (i + 1 < width and j + 1 < length) and gray_image[i + 1][j + 1] > 200:
            path = locatePath_recursive(i + 1, j + 1, score + 1, gray_image, length, width, paths, path_scores, thresh1, thresh2, angle)
            routes.append(path)
        if (i + 1) < width and gray_image[i + 1][j] > 200:
            path = locatePath_recursive(i + 1, j, score - 1, gray_image, length, width, paths, path_scores, thresh1, thresh2, angle)
            routes.append(path)
        if (i + 1) < width and gray_image[i + 1][j - 1] > 200:
            path = locatePath_recursive(i + 1, j - 1, score - 2, gray_image, length, width, paths, path_scores, thresh1, thresh2, angle)
            routes.append(path)


    max, idx = len(routes[0]), 0
    for route in routes:
        if len(route) > max:
            max = len(route)
            idx = routes.index(route)

    for route in routes:
        if routes.index(route) != idx:
            for point in route:
                if paths[point[0]][point[1]] != 255:
                    paths[point[0]][point[1]] = -1

    result = [[i, j]] + routes[idx]
    path_scores[(i, j, score)] = result
    return result

def worker(tname, gray_image, len_thresh, angle_thresh, name):
    #show_plot()
    print('Single Line Thread', tname, 'Processing:   Length Thresh:', len_thresh, '   Angle Thresh:', angle_thresh)

    score = 0
    line_no = 255
    path_scores = defaultdict()
    gray_images = [gray_image, gray_image.transpose()]
    idx = 0

    for img in gray_images:
        width = len(img)
        length = len(img[0])
        paths = np.zeros((width, length))

        for i in range(width):
            for j in range(length):
                if img[i][j] > 200 and paths[i][j] == 0:
                    path = locatePath_recursive(i, j, score, img, length, width, paths, path_scores, -angle_thresh, angle_thresh, '90')
                    if len(path) > len_thresh:
                        for point in path:
                            paths[point[0]][point[1]] = line_no
                    else:
                        for point in path:
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
    print('-----------------------------------------------')
    print('      STEP 3(a): Single Pixel Path Detector    ')
    print('-----------------------------------------------')
    DIR = join('single_pixel_path', name)
    if not exists(DIR):
        mkdir(DIR)
    if not exists(join(DIR, 'Vertical Paths')):
        mkdir(join(DIR, 'Vertical Paths'))
    if not exists(join(DIR, 'Horizontal Paths')):
        mkdir(join(DIR, 'Horizontal Paths'))

    angle_threshes = [6]
    len_threshes = [70]
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
    print('-----------------------------------------------\n')