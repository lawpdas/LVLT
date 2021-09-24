import os
import numpy as np
from tqdm import tqdm
from typing import List
strList = List[str]


def load_votlt(root):
    video_name_list = np.loadtxt(os.path.join(root, 'list.txt'), dtype=np.str)

    if len(video_name_list) > 35:
        name = 'VOT19-LT'
    else:
        name = 'VOT18-LT'

    video_list = []
    for v_n in tqdm(video_name_list, ascii=True, desc='loading %s' % name):
        gt_path = os.path.join(root, v_n, 'groundtruth.txt')
        im_dir = os.path.join(root, v_n, 'color')
        lang_path = os.path.join(root + '_language', v_n, 'language.txt')

        im_list: strList = os.listdir(im_dir)
        im_list = sorted(im_list)

        gts = np.loadtxt(gt_path, delimiter=',').tolist()  # [x y w h]
        ims = [os.path.join(im_dir, im_f) for im_f in im_list if 'jpg' in im_f]
        with open(lang_path, 'r') as f:
            lang = f.readline().lower()

        video_list.append([v_n, ims, gts, lang.strip()])

    return video_list
