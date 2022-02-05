import cv2
from PIL import Image, ImageDraw, ImageColor
import numpy as np
import os

PATH_SUCCESS = '/var/www/html/api/oil/oil-found'
PATH_FAIL = '/var/www/html/api/oil/oil-not-found'

def analysis(filename, square_size, part, paint, fn2):
    fn = filename
    square_size = square_size
    cv2img = cv2.imread(fn)
    min_p = (0, 0, 29)
    max_p = (255, 255, 255)

    filter_image = cv2.inRange(cv2img, min_p, max_p)
    cv2.imwrite('filterPicture.png', filter_image)
    path = 'filterPicture.png'

    # block of croping image
    image_list = list()
    res = list()

    # opening the source image and its size
    im = Image.open(path)

    # string to debug and to draw red square
    im = im.convert("RGB")

    width, height = im.size

    # finding the output images  square size
    square_length = int(height * square_size)

    # croping the source image to crop it correctly further
    im = im.crop((0, 0, square_length * int(width / square_length), square_length * int(height / square_length)))
    width, height = im.size

    for i in range(square_length, width, square_length):
        for j in range(square_length, height + 1, square_length):
            im2 = im.crop((i - square_length, j - square_length, i, j))
            image_list.append(im2)

    tmp = np.array(image_list[1])
    one_pic_size = np.sum(tmp)

    for i in range(0, len(image_list)):
        img_arr = np.array(image_list[i])
        n_black_pix = np.sum(img_arr == 0)
        if n_black_pix > part * one_pic_size:
            res.append(i)
    if res:
        print('OIL SPILL DETECTED')
        cv2.imwrite(os.path.join(PATH_SUCCESS, fn2), cv2img)
    else:
        print('NO OIL SPILL')
        cv2.imwrite(os.path.join(PATH_FAIL, fn2), cv2img)
        return

    if paint:
        end = Image.open(fn)
        if len(image_list) > 0:
            square_length = image_list[0].size[0]
        else:
            return 0

        for k in res:
            im = end

            # convert from monochrome to RGB to draw red square
            im = im.convert("RGB")

            # croping the source image to crop it correctly further
            im = im.crop((0, 0, square_length * int(width / square_length), square_length * int(height / square_length)))
            width, height = im.size

            # indices for drawing
            in_height = height / square_length

            i = int(k / in_height) * square_length
            j = int(k % in_height) * square_length

            # drawing red square
            draw = ImageDraw.Draw(im)
            draw.rectangle((i, j, i + square_length, j + square_length), outline=ImageColor.getrgb("red"), width=3)
            end = im

        end.save(os.path.join(PATH_SUCCESS, fn2))
    else:
        return

    return 1