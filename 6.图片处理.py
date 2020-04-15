# -*- coding: utf-8 -*-
"""
@author: Jiang Ke
@contact: jiangke9413@163.com
@software: PyCharm
@file: 图像处理.py
@time: 2020/4/14 17:39
"""

from PIL import Image, ImageFilter

# 读取图像文件
im = Image.open('sourceMaterial/处理前.jpg')
# 展示图像文件
im.show()

# 在图像上应用滤镜
# BLUR  模糊滤镜。会使图片较原先的模糊一些。
# CONTOUR   等高线。也就是轮廓滤波，将图像中的轮廓信息提取出来
# DETALL    细节。也就是细节增强滤波，它会显化图片中细节。
# SHARPEN   锐化。锐化滤波，补偿图像的轮廓，增强图像的边缘及灰度跳变的部分，使图像变得清晰。
im_sharp = im.filter(ImageFilter.SHARPEN)

# 保存已处理图像到新文件
im_sharp.save('./sourceMaterial/处理后.jpg', 'JPEG')

# 分离图像波段（band），即RGB模式的红、绿、蓝波段
r, g, b = im_sharp.split()

# 查看图像中嵌入的EXIF信息
exif_data = im._getexif()
print(exif_data)

if __name__ == "__main__":
    print("OK")
