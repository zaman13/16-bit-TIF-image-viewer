# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 11:44:03 2023

@author: Mohammad Asif Zaman
A python script to view 16 bit TIF image files with the option of changing color limits for 
better visibility/contrast. This is useful for viewing low-light images. 
"""
import tkinter as tk 
from tkinter import ttk, filedialog 
from tkinter.filedialog import askopenfile 
import os

import numpy as np
import matplotlib.pyplot as py
import cv2
from matplotlib.widgets import Slider, Button, RadioButtons

# %matplotlib qt


# control variables
blur_order= 5
cmp = 'viridis'


# file path
# path_main = 'C:/Users/Asif/Dropbox/Codes/Python/image viewer 16 bit/Test images'
# folder = ['']
# fullpath = path_main + folder[0] + '/6_image_2023-12-06T16-56-57.826_bead1_120min.tif'        # full path

# function for openfile window
def open_file():
    file = filedialog.askopenfile(mode='r', filetypes=[('TIF', '*.tif')])    
    
    if file:
        global filepath
        global counter 
        filepath = os.path.abspath(file.name)
        update_label(filepath)
        # quit()

# function for closing window after file is selected        
def quit():
    win.destroy()

def update_label(fname):
    global lb
    lb = ttk.Label(text=filepath,foreground='green')
    # lb.place(relx= 20, rely = 20, anchor = 'sw')
    lb.pack()

def delete_label():
    global lb
    lb.destroy()

def display_file():
    delete_label()
   
    # read image and determine min/max value 
    # img = cv2.imread(fullpath, cv2.IMREAD_UNCHANGED)     
    img = cv2.imread(filepath, cv2.IMREAD_UNCHANGED) 
    imb = cv2.medianBlur(img, blur_order)   # the blurring gets rid of pixel defects (i.e., hot pixels)
    bmx = np.max(imb)     # min of the blurred image
    bmn = np.min(img)     # max of the blurred image
    
    
    # setup plotting figure
    fig = py.figure()
    ax = fig.add_subplot(111)
    
    img = ax.imshow(img,cmap = cmp)   # image with cmp
    img.set_clim([bmn,bmx])           # set color range
    
    axcolor = 'lightgoldenrodyellow'
    axmin = fig.add_axes([0.25,  0.05, 0.65, 0.03])
    axmax  = fig.add_axes([0.25, 0.01, 0.65, 0.03])
    
    
    smin = Slider(axmin, 'Min', bmn*0.4, bmn*1.4, valinit=bmn)
    smax = Slider(axmax, 'Max', bmx*0.4, bmx*1.4, valinit=bmx, color = 'red')
    
    def update(val):
        img.set_clim([smin.val,smax.val])
        fig.canvas.draw()    

        
    smin.on_changed(update)
    smax.on_changed(update)
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    py.show()




win = tk.Tk()
win.iconbitmap("logo.ico")

win.geometry("700x200")


# style = ttk.Style()
# style.theme_use('alt')
# style.configure('TButton', background = 'red', foreground = 'white', width = 20, borderwidth=3, focusthickness=3, focuscolor='none')


b1 = ttk.Button(win, text="Browse",  command=open_file).pack(pady=20)

ttk.Button(win, text= "Run",command= display_file).pack()

    
# 
win.title('Hesselink Lab: 16bit TIF Viewer v0.3, Dec. 2023')
win.mainloop()
# display_file()
