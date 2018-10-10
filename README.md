### 使用方法
    修改test.py
    div为分割判断方法
    bounding_core.batch_process中的参数分别为：
    origin_img_dir: 原图像路径
    roi_img_dir: 分割答案图像路径
    target_dir:  结果路径，结果图像的名称与原图像一致
    div_method:  像素分类方法 div_method(img, x, y)
    所有对应图像名称均一致，包括目标图像名称

![example](https://github.com/Jojozzc/bounding-rect/blob/master/example-all.png)
