import os
import numpy as np


video_name_list = list(np.loadtxt('/data1/Datasets/VOT/LTB50/list.txt', dtype=np.str))
for n in video_name_list:
    gts = np.loadtxt(os.path.join('/data1/Datasets/VOT/LTB50', n, 'groundtruth.txt'), delimiter=',')
    disappear = np.isnan(gts.sum(axis=1))

    os.makedirs(os.path.join('/data1/Datasets/VOT/LTB50_language2', n), exist_ok=True)
    with open(os.path.join('/data1/Datasets/VOT/LTB50_language2', n, 'language.txt'), 'w') as f:
        for i, label in enumerate(disappear):
            if bool(label) is True and bool(disappear[i-1]) is False:
                description = '{:>6d} {:5s} | target disappeared\n'.format(i, str(label))
            else:
                description = '{:>6d} {:5s} | \n'.format(i, str(label))
            f.write(description)


# #############################################################
# write
# with open('/home/space/Desktop/VOT/LTB50_language2', 'r') as f:
#     language = f.readlines()
#
# language = [f.split('|') for f in language]
# language = [[ff.strip() for ff in f] for f in language]
#
# for name, _, lang in language:
#     with open(os.path.join('/data2/Datasets/TREK-150_language', name, 'language.txt'), 'w') as f:
#         f.writelines(lang)

