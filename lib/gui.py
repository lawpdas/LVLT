import os
import numpy as np
import cv2
from tkinter import *
import tkinter as tk
from lib import load_votlt
from PIL import Image, ImageDraw, ImageFont, ImageTk


class AnnotationToolkit(object):
    def __init__(self, init_window: Tk):
        self.init_window = init_window
        self.init_window.title("Language Description Annotator")

        # -------------------------------
        self.var_description = StringVar(init_window)
        self.var_description.set('None')

        self.var_description_show = StringVar(init_window)
        self.var_description_show.set('None')

        self.var_video_name = StringVar(init_window)
        self.var_video_name.set('None')

        self.var_frame_id = StringVar(init_window)
        self.var_frame_id.set('None')

        # -------------------------------
        self.show_name = Label(init_window, textvariable=self.var_video_name, font=8)
        self.show_name.grid(row=0, column=0, columnspan=2, sticky=tk.N + tk.E + tk.W)

        self.show_id = Label(init_window, textvariable=self.var_frame_id, font=8)
        self.show_id.grid(row=0, column=1, columnspan=2, sticky=tk.N + tk.E + tk.W)

        # -------------------------------
        self.canvas = Canvas(init_window, height=600, width=750, bd=2)
        self.canvas.grid(row=1, column=0, columnspan=5, padx=2)

        # There is bug in PhotoImage which removes image from memory (so it is not displayed)
        # when it is assigned to local variable created in function or class method.
        # https://blog.furas.pl/python-tkinter-how-to-load-display-and-replace-image-on-label-button-or-canvas-gb.html
        # It has to be assigned to global variable or class variable or using self. in class
        img = Image.fromarray(np.zeros([600, 750, 3], dtype=np.uint8))
        self.img = ImageTk.PhotoImage(img)
        self.img_show = self.canvas.create_image((0, 0), anchor='nw', image=self.img)

        # -------------------------------
        self.text_show = Entry(init_window, width=100, bd=2, textvariable=self.var_description_show, font=8)
        self.text_show.grid(row=2, column=0, columnspan=5, padx=2, sticky=tk.N + tk.E + tk.W)

        # -------------------------------
        self.text_entry = Entry(init_window, width=100, bd=2, textvariable=self.var_description, font=8)
        self.text_entry.grid(row=3, column=0, columnspan=5, padx=2, sticky=tk.N + tk.E + tk.W)

        # -------------------------------
        self.backward_video_button = Button(init_window, text='|<', command=self.backward_video, width=2, bd=2)
        self.backward_video_button.grid(row=4, column=0, sticky=tk.N + tk.E + tk.W)

        self.backward_frame_button = Button(init_window, text='<', command=self.backward_frame, width=2, bd=2)
        self.backward_frame_button.grid(row=4, column=1, sticky=tk.N + tk.E + tk.W)

        self.save_button = Button(init_window, text='Save', command=self.change_description, width=10, bd=2)
        self.save_button.grid(row=4, column=2, sticky=tk.N + tk.E + tk.W)

        self.forward_frame_button = Button(init_window, text='>', command=self.forward_frame, width=2, bd=2)
        self.forward_frame_button.grid(row=4, column=3, sticky=tk.N + tk.E + tk.W)

        self.forward_video_button = Button(init_window, text='>|', command=self.forward_video, width=2, bd=2)
        self.forward_video_button.grid(row=4, column=4, sticky=tk.N + tk.E + tk.W)

        self.init_window.bind("<Up>", self.up_fun)
        self.init_window.bind("<Left>", self.left_fun)
        self.init_window.bind("<Enter>", self.enter_fun)
        self.init_window.bind("<Right>", self.right_fun)
        self.init_window.bind("<Down>", self.down_fun)

        # #################################
        self.video_name = 'None'
        self.frame_id = 0
        self.video_id = 0

        self.video_list = []

        self.current_video = None
        self.frame_list = []
        self.boxes_list = []
        self.description_list = []

        self.load_dataset_info()
        self.init_video()

    def load_dataset_info(self):
        self.video_list = load_votlt('/data1/Datasets/VOT/LTB50')
        self.video_id = 0

    def load_language(self):
        with open(os.path.join('./RefLTB50', self.video_name, 'language.txt'), 'r') as f:
            tmp = f.readlines()
        self.description_list = [f.strip() for f in tmp]

    def save_language(self):
        with open(os.path.join('./RefLTB50', self.video_name, 'language.txt'), 'w') as f:
            for tmp in self.description_list:
                f.write(tmp + '\n')
        print('save ...', self.video_name)

    def update_description_show(self):
        self.var_description.set(self.description_list[self.frame_id])
        if len(self.description_list[self.frame_id]) > 0:
            self.var_description_show.set(self.description_list[self.frame_id])

        self.text_entry.icursor(len(self.description_list[self.frame_id]))

    def init_video(self):
        self.current_video = self.video_list[self.video_id]

        self.video_name = self.current_video[0]
        self.var_video_name.set('Name: {:<20s}'.format(self.video_name))

        self.description_list = self.current_video[3]
        self.boxes_list = self.current_video[2]
        self.frame_list = self.current_video[1]
        self.load_language()

        self.frame_id = 0
        self.var_frame_id.set('Frame: {:>6d} / {:>6d}'.format(self.frame_id + 1, len(self.frame_list)))

        assert len(self.video_list) > 0
        assert len(self.frame_list) > 0
        assert len(self.description_list) == len(self.frame_list)

        self.update_description_show()

        img = cv2.imread(self.frame_list[self.frame_id])
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = self.img_plot(img, self.boxes_list[self.frame_id])
        self.img = ImageTk.PhotoImage(img)

        self.canvas.itemconfig(self.img_show, image=self.img)

    def up_fun(self, event):
        self.backward_video()

    def left_fun(self, event):
        self.backward_frame()

    def enter_fun(self, event):
        self.change_description()

    def right_fun(self, event):
        self.forward_frame()

    def down_fun(self, event):
        self.forward_video()

    @staticmethod
    def img_plot(img, gt, lang=None):
        imh, imw = img.shape[:2]
        img = cv2.resize(img, (750, 600), interpolation=cv2.INTER_CUBIC)
        sh, sw = 600 / imh, 750 / imw

        img = Image.fromarray(img)
        # img = img.convert("RGBA")
        draw = ImageDraw.ImageDraw(img)

        gt = np.array(gt)  # [x y w h]
        gt[2:] = gt[2:] + gt[:2] - 1
        gt[0::2] *= sw
        gt[1::2] *= sh
        gt_box = gt.astype(int)
        draw.rectangle(((gt_box[0], gt_box[1]), (gt_box[2], gt_box[3])), outline=(255, 0, 0), width=2)

        # draw.rectangle(((0, 0), (750, 40)), fill=(0, 0, 0, 230))  # (y, x)

        if lang is not None:
            font = ImageFont.truetype('/data2/Documents/Experiments/BaseT/plot_tools/Sarai.ttf', size=25)
            draw.text((10, 5), lang, fill=(255, 255, 255), font=font)

        # img = img.convert("RGB")

        return img

    def change_description(self):
        new_description = self.var_description.get()
        self.description_list[self.frame_id] = new_description

        self.update_description_show()

    def forward_frame(self):
        self.frame_id += 1
        self.frame_id = np.clip(self.frame_id, 0, len(self.frame_list) - 1)
        self.var_frame_id.set('Frame: {:>6d} / {:>6d}'.format(self.frame_id + 1, len(self.frame_list)))

        self.update_description_show()

        img = cv2.imread(self.frame_list[self.frame_id])
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = self.img_plot(img, self.boxes_list[self.frame_id])
        self.img = ImageTk.PhotoImage(img)

        self.canvas.itemconfig(self.img_show, image=self.img)

        print(self.var_description.get() + '>', self.video_id, self.var_video_name.get(), self.var_frame_id.get())

    def backward_frame(self):
        self.frame_id -= 1
        self.frame_id = np.clip(self.frame_id, 0, len(self.frame_list) - 1)
        self.var_frame_id.set('Frame: {:>6d} / {:>6d}'.format(self.frame_id + 1, len(self.frame_list)))

        self.update_description_show()

        img = cv2.imread(self.frame_list[self.frame_id])
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = self.img_plot(img, self.boxes_list[self.frame_id])
        self.img = ImageTk.PhotoImage(img)

        self.canvas.itemconfig(self.img_show, image=self.img)

        print(self.var_description.get() + '<', self.video_id, self.var_video_name.get(), self.var_frame_id.get())

    def forward_video(self):
        self.video_id += 1
        self.video_id = np.clip(self.video_id, 0, len(self.video_list) - 1)
        self.save_language()

        self.init_video()

        print(self.var_description.get() + '>|', self.video_id, self.var_video_name.get(), self.var_frame_id.get())

    def backward_video(self):
        self.video_id -= 1
        self.video_id = np.clip(self.video_id, 0, len(self.video_list) - 1)
        self.save_language()

        self.init_video()

        print(self.var_description.get() + '|<', self.video_id, self.var_video_name.get(), self.var_frame_id.get())


if __name__ == '__main__':
    root = Tk()
    toolkit = AnnotationToolkit(root)
    root.mainloop()
    toolkit.save_language()

