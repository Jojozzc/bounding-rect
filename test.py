# test for demo
from scipy.misc import *

import os
import numpy as np
import bounding_core

def divROI(img, x, y):
    img = np.array(img)
    return img[x][y] != 0


# img:图像数据
# x, y 像素坐标
# 瞎写的，记得改
def div(img, x, y):
    img = np.array(img)
    return img[x][y][0] == 128

if __name__ == '__main__':
    # example1
    bounding_core.batch_process(origin_img_dir="/media/jojo/Code/multi-task/samples/good",
                                roi_img_dir="/media/jojo/Code/multi-task/samples/goodROI",
                                target_dir="/media/jojo/Code/multi-task/samples/bound2/goodBoundingRect2",
                                div_method=divROI)

# example2
# boundingCore.batch_process(origin_img_dir="/media/jojo/Code/BUS/wavelet_test",
#                            roi_img_dir="/media/jojo/Code/BUS/GT_tumor_test",
#                            target_dir="/media/jojo/Code/BUS/target_test",
#                            div_method=div)