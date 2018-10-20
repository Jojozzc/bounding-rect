# change rbg image to one-hot
import numpy as np
from scipy.misc import *
import os
import re
'''
ROI image's pixel range from 0 to 255, so we should encode it to one-hot(0-1 or 0-N).
'''


def encode(img, i, j):
    if img[i][j] != 0:
        return 1
    return 0


def rbg2one_hot(img, encode2one_hot):
    """

    :param img: origin image
    :param encode: encode method
    :return: one-hot image
    """
    one_hot_img = np.array(img)
    for i in range(one_hot_img.shape[0]):
        for j in range(one_hot_img.shape[1]):
            one_hot_img[i][j] = encode2one_hot(img, i, j)
    return one_hot_img


def single_file_encode(img_path, encode2one_hot):
    img = imread(img_path)
    return rbg2one_hot(img, encode2one_hot)


def batch_encode(source_path, target_path, encode2one_hot):
    if source_path is None or not os.path.exists(source_path):
        print('源目录不存在')
        return
    for file in os.listdir(source_path):
        lower_name = file.lower()
        if re.search('\.bmp$', lower_name) or re.search('\.png$', lower_name) or \
                re.search('\.jpg$', lower_name) or re.search('\.jpeg', lower_name):
            one_hot_img = single_file_encode(os.path.join(source_path, file),
                                             encode2one_hot)
            imsave(os.path.join(target_path, file), one_hot_img)


def test_one_hot_like():
    img_path = '/media/jojo/Code/multi-task/unet-seg/ImgData/LabelDataF2/case233.png'
    mark = set()
    roi_path = '/media/jojo/Code/multi-task/samples/badROI/case172.bmp'
    roi_img = imread(roi_path)
    save_path = './test.png'
    img = imread(img_path)
    print('label shape:{}'.format(img.shape))
    for i in range(roi_img.shape[0]):
        for j in range(roi_img.shape[1]):
            mark.add(roi_img[i][j])
    print(mark)
    img = rbg2one_hot(img, encode)
    mark = set()
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            mark.add(img[i][j])
    print(mark)
    imsave(save_path, img)


if __name__ == '__main__':
    label_t_dir = '/media/jojo/Code/multi-task/unet-seg/ImgData/LabelDataT'
    label_f_dir = '/media/jojo/Code/multi-task/unet-seg/ImgData/LabelDataF'
    good_roi_dir = '/media/jojo/Code/multi-task/samples/goodROI'
    bad_roi_dir = '/media/jojo/Code/multi-task/samples/badROI'
    batch_encode(good_roi_dir, label_t_dir, encode)
    batch_encode(bad_roi_dir, label_f_dir, encode)