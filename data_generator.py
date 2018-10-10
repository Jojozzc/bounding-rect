import bounding_core
import os
import re
from scipy.misc import *

def batch_process_div_by_rate(source_dir, roi_dir_path, save_dir, img_file_format=['bmp', 'jpg', 'jpeg', 'png'],
                              div_method=lambda img, x, y: img[x][y] != 0):
    if source_dir is None or not os.path.exists(source_dir):
        print('源目录不存在')
        return None
    for file in os.listdir(source_dir):
        lower_name = file.lower()
        name_div = lower_name.split('.')
        if name_div[len(name_div) - 1] in img_file_format:
            single_process_div_by_rate(os.path.join(source_dir, file),
                                       os.path.join(roi_dir_path, file),
                                       os.path.join(save_dir, file),
                                       div_method)


def single_process_div_by_rate(source_img_path, roi_path, save_path, div_method):
    source_img = imread(source_img_path)
    roi_img = imread(roi_path)
    bound_rect = bounding_core.get_bounding_rectangle(roi_img,
                                                      div_method=div_method)
    # 切成正方形
    result = bounding_core.img_seg_by_rate(source_img, bound_rect, hw_rate=1)
    imsave(save_path, result)

if __name__ == '__main__':
    source_good_dir = '/media/jojo/Code/multi-task/samples/good'
    source_bad_dir = '/media/jojo/Code/multi-task/samples/bad'

    roi_good_dir = '/media/jojo/Code/multi-task/samples/goodROI'
    roi_bad_dir = '/media/jojo/Code/multi-task/samples/badROI'

    good_save_dir = '/media/jojo/Code/multi-task/samples/bound-rate/good'
    bad_save_dir = '/media/jojo/Code/multi-task/samples/bound-rate/bad'
    batch_process_div_by_rate(source_dir=source_bad_dir,
                              roi_dir_path=roi_bad_dir,
                              save_dir=bad_save_dir)
