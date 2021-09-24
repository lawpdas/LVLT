import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from typing import List
from lib import load_votlt

strList = List[str]

seqs = load_votlt('/data1/Datasets/VOT/LTB50')

for i, (video_name, im_list, gt_list, _) in enumerate(seqs):
    with open(os.path.join('../RefLTB50', video_name, 'language.txt'), 'r') as f:
        language = f.readlines()

    # language = [f.split('|')[-1].strip() for f in language]
    language = [f.strip() for f in language]
    assert len(gt_list) == len(language)

    for im_i, im_f in enumerate(im_list):
        # print('...', video_name, im_i, '/', len(im_list))

        lang = language[im_i]
        if len(lang) <= 0:
            continue

        print('{:0>6d} |'.format(im_i), lang)

        right_point = im_i + 1
        for _ in range(100):
            right_point = np.clip(right_point + 1, 0, len(im_list)-1)
            if len(language[right_point]) > 0:
                break
        if right_point-1 <= im_i:
            img_id = im_i
        else:
            img_id = np.random.randint(im_i, right_point-1)

        img = cv2.imread(im_list[img_id])
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        imh, imw = img.shape[:2]
        img = cv2.resize(img, (750, 600), interpolation=cv2.INTER_CUBIC)
        sh, sw = 600 / imh, 750 / imw

        img = Image.fromarray(img)
        img = img.convert("RGBA")
        draw = ImageDraw.ImageDraw(img)

        gt = np.array(gt_list[img_id])  # [x y w h]
        gt[2:] = gt[2:] + gt[:2] - 1
        gt[0::2] *= sw
        gt[1::2] *= sh
        gt_box = gt.astype(int)
        draw.rectangle(((gt_box[0], gt_box[1]), (gt_box[2], gt_box[3])), outline=(255, 0, 0), width=5)

        draw.rectangle(((0, 0), (750, 40)), fill=(0, 0, 0, 230))  # (y, x)

        font = ImageFont.truetype('/data2/Documents/Experiments/BaseT/plot_tools/Sarai.ttf', size=25)
        draw.text((10, 5), lang, fill=(255, 255, 255), font=font)

        img = img.convert("RGB")

        save_path = '../tmp'
        # save_path = '../tmp/{}'.format(video_name)
        os.makedirs(save_path, exist_ok=True)
        img.save(os.path.join(save_path, '{}_{:0>6d}.jpg'.format(video_name, img_id)))

    print('######################################################################################################')
