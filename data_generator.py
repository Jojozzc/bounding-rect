import bounding_core
import os
import re
from scipy.misc import *


def GT_div_judge(img, x, y):
    return img[x][y][0] == 128

def batch_process_div_by_rate(source_dir, roi_dir_path, save_dir, img_file_format=['bmp', 'jpg', 'jpeg', 'png'],
                              div_method=lambda img, x, y: img[x][y] != 0):
    '''

    :param source_dir:
    :param roi_dir_path:
    :param save_dir:
    :param img_file_format:
    :param div_method:
    '''
    if source_dir is None or not os.path.exists(source_dir):
        print('源目录不存在')
        return
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    for file in os.listdir(source_dir):
        lower_name = file.lower()
        name_div = lower_name.split('.')
        if name_div[len(name_div) - 1] in img_file_format:
            single_process_div_by_rate(os.path.join(source_dir, file),
                                       os.path.join(roi_dir_path, name_div[0] + '.png'),
                                       os.path.join(save_dir, file),
                                       div_method)


def single_process_div_by_rate(source_img_path, roi_path, save_path, div_method):
    """

    :param source_img_path: 原图路径
    :param roi_path: roi图路径
    :param save_path: 保存结果图片的路径
    :param div_method: 分割方法
    """
    source_img = imread(source_img_path)
    roi_img = imread(roi_path)
    bound_rect = bounding_core.get_bounding_rectangle2(roi_img,
                                                      div_method=div_method, inc_rate=0.26)
    # 切成正方形
    result = bounding_core.img_seg_by_rate(source_img, bound_rect, hw_rate=1)
    imsave(save_path, result)

def single_test():
    img_path = '/run/media/kele/DataSSD/Code/multi-task/newData/samples1-良恶性无重复/samples/wavelet_origin/good/case2.jpg'
    roi_path = '/run/media/kele/DataSSD/Code/multi-task/newData/samples1-良恶性无重复/samples/goodROI/case2.png'
    save_path = './clip.png'
    single_process_div_by_rate(img_path, roi_path, save_path, lambda img, x, y: img[x][y] != 0)


if __name__ == '__main__':
    # single_test()
    # exit(0)
    source_good_dir = 'G:/Code/multi-task/newData/xxx/good'
    source_bad_dir = 'G:/Code/multi-task/newData/xxx/bad'


    roi_good_dir = 'G:/Code/multi-task/newData/xxx/GT'
    roi_bad_dir = 'G:/Code/multi-task/newData/xxx/GT'

    good_save_dir = 'G:/Code/multi-task/newData/xxx/bound/good'
    bad_save_dir = 'G:/Code/multi-task/newData/xxx/bound/bad'

    batch_process_div_by_rate(source_dir=source_bad_dir,
                              roi_dir_path=roi_bad_dir,
                              save_dir=bad_save_dir,
                              div_method=GT_div_judge)

