import numpy as np
import os
from scipy.misc import *
import re

def img_seg_by_rate(source_img, bound_rect, hw_rate=1):
    """

    :param source_img: numpy array of source image
    :param wh_rate: height / width
    :param margin:Margin pixel
    :param bound_rect: [[most_up, most_left], [most_down, most_right]]

    :return target image numpy array
    """
    if hw_rate == 0:
        return None
    most_up = int(bound_rect[0][0])
    most_left = int(bound_rect[0][1])
    most_down = int(bound_rect[1][0])
    most_right = int(bound_rect[1][1])

    source_img = np.array(source_img)
    bound_height = most_right - most_left
    bound_width = most_down - most_up

    bound_rate = bound_height / bound_width

    result_height = bound_height
    result_width = bound_width

    if bound_rate == hw_rate:
        return img_segmentation(source_img, bound_rect)
    if bound_rate < hw_rate: # height is smaller
        result_height = result_width * hw_rate
    else:
        result_width = result_height / hw_rate

    result_np = np.zeros(shape=(result_height, result_width, 3))
    source_x1 = max(0, most_up - (result_height - bound_height) / 2)
    source_x2 = min(source_img.shape[0] - 1, most_down + (result_height - bound_height) / 2)
    source_y1 = max(0, most_left - (result_width - bound_width) / 2)
    source_y2 = min(source_img.shape[1] - 1, most_right + (result_width - bound_width) / 2)



def abs2relatively(abs_x, abs_y, bias_x, bias_y):
    """

    :param abs_x: 绝对坐标x
    :param abs_y: 绝对坐标y
    :param bias_x: 相对参考系x方向的偏移
    :param bias_y: 相对参考系y方向的偏移

    :return 相对参考系中的坐标对(x_r, y_r)
    """
    x_r = abs_x + bias_x
    y_r = abs_y + bias_y
    return (x_r, y_r)



# img:图像矩阵
# divMethod: 分割依据
# return : 外接矩阵左上角和右下角的坐标
def get_bounding_rectangle(img, div_method):
    img = np.array(img)
    img_shape = img.shape
    rows = img_shape[0]
    cols = img_shape[1]
    most_up = rows
    most_down = 0
    most_left = cols
    most_right = 0
    for i in range(rows):
        for j in range(cols):
            if(div_method(img, i, j)):
                most_up = min(i, most_up)
                most_down = max(i, most_down)
                most_left = min(j, most_left)
                most_right = max(j, most_right)
    return [[most_up, most_left], [most_down, most_right]]

def get_bounding_rectangle2(img, div_method, inc_rate=0.16):
    """
    :param img: 图片
    :param div_method: 分割方法
    :param inc_rate: 期望的扩充比例
    在原有的基础上向外扩张
    """
    img = np.array(img)
    [[most_up, most_left], [most_down, most_right]] = get_bounding_rectangle(img, div_method)
    width = most_right - most_left
    height = most_down - most_up
    width_inc = width * inc_rate
    height_inc = height * inc_rate
    horizontal_half = width_inc / 2.0
    vertical_half = height_inc / 2.0
    most_left = max(0, most_left - int(horizontal_half))
    most_right = min(img.shape[1] - 1, most_right + int(horizontal_half))
    most_up = max(0, most_up - int(vertical_half))
    most_down = min(img.shape[0] - 1, most_down + int(vertical_half))
    return [[most_up, most_left], [most_down, most_right]]


def img_segmentation(img_data, bounding_rect):
    print(img_data.shape)
    print(bounding_rect)
    start_x = bounding_rect[0][0]
    start_y = bounding_rect[0][1]
    end_x = bounding_rect[1][0]
    end_y = bounding_rect[1][1]
    rows = end_x - start_x + 1
    cols = end_y - start_y + 1
    result = np.zeros(shape=(rows, cols, 3))
    print("result shape:" + str(result.shape))
    for i in range(rows):
        for j in range(cols):
            result[i][j] = img_data[start_x + i][start_y + j]
    return result

# 原图和答案图需要保持名称一致
# origin_img_dir: 原图像路径
# roi_img_dir: 分割答案图像路径
# target_dir:  结果路径，结果图像的名称与原图像一致
# div_method:  像素分类方法 div_method(img, x, y)
def batch_process(origin_img_dir, roi_img_dir, target_dir, div_method):
    for file in os.listdir(origin_img_dir):
        lower_name = file.lower()
        if re.search('\.bmp$', lower_name) or re.search('\.png$', lower_name) or \
            re.search('\.jpg$', lower_name) or re.search('\.jpeg', lower_name):
            single_process(os.path.join(origin_img_dir, file),
                           os.path.join(roi_img_dir, file), target_dir + '/' + file, div_method)

def single_process(origin_img_path, roi_img_path, target_path, div_method):
    img_roi = imread(roi_img_path)
    img_org = imread(origin_img_path)
    bounding_rect = get_bounding_rectangle2(np.array(img_roi), div_method, 0.1)
    seg_data = img_segmentation(np.array(img_org), bounding_rect)
    imsave(target_path, seg_data)