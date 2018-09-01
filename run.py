import cv2
import sys
import threading
from os import mkdir, listdir
from os.path import join, exists
from variance_test import variance_patch
from morphology import morphology
from wide_jump_path import wide_jump_line_detector
from single_pixel_path import single_line_detector
from path_refiner import refiner, projectImages

def image_select(name, dir, c = 0):
    files = listdir(dir)
    print('####################################################')
    print('Select image from "', dir, '" for further processing...')
    for file in files:
        print(files.index(file) + 1, '->' , file)
    num = input('\nEnter image number: ')
    if c == 0:
        build_gray = cv2.imread(join(dir, files[int(num) - 1]), 0)
        image = cv2.threshold(build_gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    else:
        image = cv2.imread(join(dir, files[int(num) - 1]))
    print('\n####################################################')
    return image


def main(argv):
    if not exists('Results'):
        mkdir('Results')
    print('### Processing Image', argv[1], '###')
    name = argv[1]

    img = cv2.resize(cv2.imread(join('Data', name + '.png')), (500,500))

    morphology_res = morphology.execute(img, name)
    variance_patch.execute(morphology_res, name)
    var_image = image_select(name, join('variance_test', name))

    t1 = threading.Thread(target=single_line_detector.execute, args=(var_image, name))
    t2 = threading.Thread(target=wide_jump_line_detector.execute, args=(var_image, name))
    t1.start()
    t2.start()
    t2.join()
    t1.join()

    refiner.execute(name)
    projectImages.execute(img, name)
    print('\n### Processing Complete ###')

if __name__ == '__main__':
    exit(main(['', 't1']))