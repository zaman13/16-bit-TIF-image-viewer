# -*- coding: utf-8 -*-
"""
Created on Tue Dec 26 15:15:56 2023

@author: Mohammad Asif Zaman

Stackoverflow Help links:
    - https://stackoverflow.com/questions/59001195/how-to-update-a-graph-created-by-matplotlib-in-tkinter

"""

# import tkinter as tk
# from tkinter import *
import ttkbootstrap as tk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

from tkinter.filedialog import askopenfile 
from ttkbootstrap.dialogs import Messagebox

import numpy as np
import cv2


# Function to update slider labels when sliders are updated
def scale_update(evnt):
    # Function to update slider labels when sliders are updated

    # update the text near the sliders
    lbl_min1.config(text = str(int(sld_min1.get())))
    lbl_max1.config(text = str(int(sld_max1.get())))
    lbl_min2.config(text = str(int(sld_min2.get())))
    lbl_max2.config(text = str(int(sld_max2.get())))

    # Call function to draw the figures
    draw_figure()

# ==========================================================
# Update and draw/display figure
# ==========================================================
def draw_figure():
    # Update and draw/display figure    
    # clear figure
    fig.clear()
    
    ax = fig.add_subplot(111)
    
    # display image 1 with appropriate color scale and transparency
    img = img1
    im_obj = ax.imshow(img,cmap = spn_cmp1.get(), alpha = float(mtr_alp1.amountusedvar.get()/100))
    im_obj.set_clim([sld_min1.get(), sld_max1.get()])

    
    # display image 2 with appropriate color scale and transparency
    img = img2
    im_obj = ax.imshow(img,cmap = spn_cmp2.get(), alpha = float(mtr_alp2.amountusedvar.get()/100))
    im_obj.set_clim([sld_min2.get(), sld_max2.get()])
    
    # Turn axis labels off
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
 
    # print('sld_min1 = %i' % sld_min1.get())
    
    # Draw canvas
    canvas.draw_idle()
# ==========================================================



# ==========================================================
# Auto set functions. Set slider values. The draw_figure
# function would be autocalled through the slider command
# functions
# ==========================================================
def auto_set1():
    sld_min1.set(bmn1)
    sld_max1.set(bmx1)

def auto_set2():
    sld_min2.set(bmn2)
    sld_max2.set(bmx2)
# ==========================================================


# ==========================================================
# Manual set functions. Similar to the auto_set functions.
# ==========================================================
def man_set1():
    sld_min1.set(ent_min1.get())
    sld_max1.set(ent_max1.get())
    

def man_set2():
    sld_min2.set(ent_min2.get())
    sld_max2.set(ent_max2.get())

# ==========================================================
    
def load_img():
    global img1
    global img2
    
    global bmn1
    global bmx1
    global bmn2
    global bmx2
    
    global mn1L
    global mn1H
    global mx1L
    global mx1H
    
    global mn2L
    global mn2H
    global mx2L
    global mx2H
    
    
    # ==========================================================
    # Load images
    # ==========================================================
    img1 = cv2.imread(path1, cv2.IMREAD_UNCHANGED)
    img2 = cv2.imread(path2, cv2.IMREAD_UNCHANGED)
    # ==========================================================



    # ==========================================================
    # calculate the blurred image and min/max color range of the blurred images
    # ==========================================================
    imb = cv2.medianBlur(img1, blur_order)   # the blurring gets rid of pixel defects (i.e., hot pixels)
    bmx1 = np.max(imb)     # min of the blurred image
    bmn1 = np.min(imb)     # max of the blurred image

    imb = cv2.medianBlur(img2, blur_order)   # the blurring gets rid of pixel defects (i.e., hot pixels)
    bmx2 = np.max(imb)     # min of the blurred image
    bmn2 = np.min(imb)     # max of the blurred image
    
    mn1L = bmn1*mn_fct
    mn1H = bmn1*mx_fct
    mx1L = bmx1*mn_fct
    mx1H = bmx1*mx_fct
    
    mn2L = bmn2*mn_fct
    mn2H = bmn2*mx_fct
    mx2L = bmx2*mn_fct
    mx2H = bmx2*mx_fct
    
    # print(sld_min1.winfo_exists())            
    try:
        sld_min1.configure(from_=mn1L, to = mn1H)
    except:
        pass
            
    try:
        sld_max1.configure(from_=mx1L, to = mx1H)
    except:
        pass
    
    try:
        sld_min2.configure(from_=mn2L, to = mn2H)
    except:
        pass
            
    try:
        sld_max2.configure(from_=mx2L, to = mx2H)
    except:
        pass
    
# ==========================================================

    

# =============================================================================    
# Function for when the browse button is clicked. Assigns path, enables run button, populates ifname_list
# =============================================================================    
def open_file1():
    # Function for when the browse button is clicked. It assigns the global path variable and populates the global ifname_list list. 
    # Enables run button. Edits the file path label for the output_frame. 
    file = askopenfile(mode='r', filetypes=[('TIF', '*.tif')])    # Open file explorer to select file
    
    if file:
        global path1
        path1 = file.name
        lbl_path1.config(text = 'File 1 = ' + path1)
    print('Selected file 1 path = %s' %path1)
    print('Selected file 2 path = %s' %path2)
    load_img()
    draw_figure()
        
def open_file2():
    # Function for when the browse button is clicked. It assigns the global path variable and populates the global ifname_list list. 
    # Enables run button. Edits the file path label for the output_frame. 
    
    file = askopenfile(mode='r', filetypes=[('TIF', '*.tif')])    # Open file explorer to select file
    
    if file:
        global path2
        path2 = file.name   
        lbl_path2.config(text = 'File 2 = ' + path2)
    print('Selected file 1 path = %s' %path1)
    print('Selected file 2 path = %s' %path2)
    load_img()
    draw_figure()
# =============================================================================    


# =============================================================================    
# Quit program function with confirmation message box
# =============================================================================    
def quit_program():
    # Quit program function with confirmation message box
    
    # create messagebox
    mb_quit = Messagebox.yesno('Do you want to quit eclypse?', 'Quit',parent = output_frame)
    
    if mb_quit == 'Yes':
      
        print('\nThank you for using the program. Longer strands!\n')
        root.quit()     # Added this in vb0.2. Sometimes, the terminal gets stuck when quitting the program. This might help.
        root.destroy()
    else:
        pass
# =============================================================================    



# ==========================================================
# Main Program
# ==========================================================
    

    
# =============================================================================
# Window and frame parameters
# =============================================================================
window_width = 1400
window_height = 900    
posx = window_width/8    # x position of the window
posy = window_height/20  # y position of the window

ctrl_width_fraction = 3/8   # what fraction of the total window is the ctrl_frame
top_frame_height = 100
bottom_frame_height = 50
# ==========================================================


# ==========================================================
# Control parameters. Currently GUI doesn't have access to it.
# ==========================================================
blur_order = 5
mn_fct = 0.25
mx_fct = 3
# =============================================================================

# =============================================================================
# Default values of parameters
# =============================================================================
mn1L, mn1H = 100, 600
mx1L, mx1H = 800, 10000
bmn1, bmx1 = 400, 4000


mn2L, mn2H = mn1L, mn1H
mx2L, mx2H = mx1L, mx1H
bmn2, bmx2 = bmn1, bmx1

path1 = 's1.tif'
path2 = 's2.tif'

im1_style = 'info'
im2_style = 'success'

# =============================================================================

# =============================================================================
# root window
# =============================================================================

root = tk.Window(themename="journal")    # set root windows and theme

root.title('16 bit Image: View and Superimpose')    # Set title of the root frame
root.geometry(("%dx%d+%d+%d" % (window_width, window_height, posx, posy)))

# Icon not working in linux builds. Work on this later
# my_icon = ttb.PhotoImage('icon.ico')
# root.iconphoto(my_icon)  

root.update()  # get window dimensiosn
root.minsize(root.winfo_width(), root.winfo_height())   # set minimum size of the program window

# =============================================================================



# =============================================================================
# define frames
# =============================================================================
# total 4 frames. 
ctrl_frame = tk.Labelframe(root)
output_frame = tk.Labelframe(root)
top_frame = tk.Frame(root)
bottom_frame = tk.Frame(root)

# place/pack the 4 frames
ctrl_frame.place(x=0,y=0,relheight=1, width = window_width*ctrl_width_fraction)
top_frame.place(x=window_width*ctrl_width_fraction, y=0, height = top_frame_height, relwidth = 1 )
output_frame.place(x=window_width*ctrl_width_fraction,y=top_frame_height, relheight=1, relwidth = 1)
bottom_frame.pack(side= 'bottom',anchor = 'e')


# st.configure('top_frame.TFrame', background = 'green')

# =============================================================================





# =============================================================================
# Define and load figures
# ==========================================================

img_logoM = tk.PhotoImage(file = 'ec_logo_80px.png')
lbl_logoM = tk.Label(top_frame,  image = img_logoM)
lbl_version = tk.Label(top_frame, text = 'Mohammad Asif Zaman \nVersion b_0.1 \nDec. 2023', bootstyle = 'secondary')
bt_quit = tk.Button(top_frame, text = 'Quit', bootstyle = 'primary', command = quit_program)


lbl_path1 = tk.Label(output_frame,text = 'File 1 = ' + path1, bootstyle = im1_style)
lbl_path2 = tk.Label(output_frame,text = 'File 2 = ' + path2, bootstyle = im2_style)

# Pack output frame texts immediately so that they appear on the top (above the figure)
lbl_path1.pack(side = 'top', anchor = 'nw', padx = 10)
lbl_path2.pack(side =  'top', anchor = 'nw', padx = 10)




bt_browse1 = tk.Button(ctrl_frame, text = 'Browse', bootstyle = im1_style, command = open_file1)
bt_browse2 = tk.Button(ctrl_frame, text = 'Browse', bootstyle = im2_style, command = open_file2)


fig = Figure(figsize=(4, 3), dpi=150)
ax = fig.add_subplot(111)

fig.tight_layout()


# ==========================================================
# Display figure and toolbar
# ==========================================================
canvas = FigureCanvasTkAgg(fig, master=output_frame)  # A tk.DrawingArea.
canvas.get_tk_widget().pack(anchor = 'nw')
toolbar = NavigationToolbar2Tk(canvas, bottom_frame)
# ==========================================================

# ==========================================================
# ==========================================================

# initialize labels
lbl_min1 = tk.Label(ctrl_frame, text = '')
lbl_max1 = tk.Label(ctrl_frame, text = '')
lbl_min2 = tk.Label(ctrl_frame, text = '')
lbl_max2 = tk.Label(ctrl_frame, text = '')

# Header labels
lbl_header1 =tk.Label(ctrl_frame,text = 'Image 1 control', font = ('bold', 12))
lbl_header2 =tk.Label(ctrl_frame,text = 'Image 2 control', font = ('bold', 12))



mtr_alp1 = tk.Meter(ctrl_frame, 
                    bootstyle = im1_style, 
                    subtextstyle= im1_style,
                    subtext = 'Opacity',
                    interactive = True,
                    stripethickness=6,
                    meterthickness=4,
                    metersize = 80,
                    amounttotal = 100,
                    amountused = 100,
                    textright = '%',
                    stepsize=1,
                    textfont='-size 10 -weight bold',
                    subtextfont='-size 7 -weight normal',)


mtr_alp2 = tk.Meter(ctrl_frame, 
                    bootstyle = im2_style, 
                    subtextstyle = im2_style,
                    subtext = 'Opacity',
                    interactive = True,
                    stripethickness=6,
                    meterthickness=4,
                    metersize = 80,
                    amounttotal = 100,
                    amountused = 60,
                    textright = '%',
                    stepsize=1,
                    textfont='-size 10 -weight bold',
                    subtextfont='-size 7 -weight normal',
                    )

lbl_cmp1 = tk.Label(ctrl_frame,text = 'Colormap 1', bootstyle = im1_style)
spn_cmp1  = tk.Spinbox(ctrl_frame, 
                       bootstyle= im1_style,
                       values = ['viridis', 'jet', 'Greys', 'cividis', 'Blues'], state= 'readonly',
                       wrap = True,
                       command = draw_figure,
                       )
spn_cmp1.set('Blues')



lbl_cmp2 = tk.Label(ctrl_frame,text = 'Colormap 2', bootstyle = im2_style)
spn_cmp2  = tk.Spinbox(ctrl_frame, 
                       bootstyle= im2_style,
                       values = ['hot', 'Reds', 'PuRd','Greens'], state= 'readonly',
                       wrap = True,
                       command = draw_figure,
                       )
spn_cmp2.set('Greens')


# Load image
load_img()

sld_min1 = tk.Scale(ctrl_frame, 
                    bootstyle = im1_style, 
                    from_ = np.round(mn1L,2),
                    to = np.round(mn1H,2),
                    command = scale_update,
                    )

sld_max1 = tk.Scale(ctrl_frame, 
                    from_ = np.round(mx1L,2),
                    to = np.round(mx1H,2),
                    bootstyle = im1_style,
                    command = scale_update,
                    )

sld_min2 = tk.Scale(ctrl_frame, 
                    bootstyle = im2_style,
                    from_ = np.round(mn2L,2),
                    to = np.round(mn2H,2),
                    command = scale_update,
                    )

sld_max2 = tk.Scale(ctrl_frame, 
                    bootstyle = im2_style,
                    from_ = np.round(mx2L,2),
                    to = np.round(mx2H,2),
                    command = scale_update,
                    )

# set slider values
sld_min1.set(bmn1)
sld_max1.set(bmx1)
sld_min2.set(bmn2)
sld_max2.set(bmx2)

# display slider text
lbl_min1 = tk.Label(ctrl_frame, text = sld_min1.get(), bootstyle = im1_style)
lbl_max1 = tk.Label(ctrl_frame, text = sld_max1.get(), bootstyle = im1_style)
lbl_min2 = tk.Label(ctrl_frame, text = sld_min2.get(), bootstyle = im2_style)
lbl_max2 = tk.Label(ctrl_frame, text = sld_max2.get(), bootstyle = im2_style)

# labels for entry widgets
lbl_ent_min1 = tk.Label(ctrl_frame, text = 'Img 1 min', bootstyle = im1_style)
lbl_ent_max1 = tk.Label(ctrl_frame, text = 'Img 1 max', bootstyle = im1_style)
lbl_ent_min2 = tk.Label(ctrl_frame, text = 'Img 2 min', bootstyle = im2_style)
lbl_ent_max2 = tk.Label(ctrl_frame, text = 'Img 2 max', bootstyle = im2_style)

# entry widgets for min/max values of the image. Used for manual setting.
ent_min1 = tk.Entry(ctrl_frame, bootstyle = im1_style )
ent_max1 = tk.Entry(ctrl_frame, bootstyle = im1_style )
ent_min2 = tk.Entry(ctrl_frame, bootstyle = im2_style )
ent_max2 = tk.Entry(ctrl_frame, bootstyle = im2_style )

ent_min1.insert(0, sld_min1.get())
ent_max1.insert(0, sld_max1.get())
ent_min2.insert(0, sld_min2.get())
ent_max2.insert(0, sld_max2.get())

# Button for setting slider to auto range
btn_auto_set1 = tk.Button(ctrl_frame, text = 'Auto Set', bootstyle = im1_style, command = auto_set1)
btn_auto_set2 = tk.Button(ctrl_frame, text = 'Auto Set', bootstyle = im2_style, command = auto_set2)

# Button for setting slider to manual range
btn_man_set1 = tk.Button(ctrl_frame, text = 'Set', bootstyle = im1_style, command = man_set1)
btn_man_set2 = tk.Button(ctrl_frame, text = 'Set', bootstyle = im2_style, command = man_set2)

# Buttons for setting opacity
btn_set_mtr1 = tk.Button(ctrl_frame, bootstyle = im1_style, text = 'Set Opacity', command = draw_figure)
btn_set_mtr2 = tk.Button(ctrl_frame, bootstyle = im2_style, text = 'Set Opacity', command = draw_figure)






# =============================================================================
# Layout (mostly grid)
# =============================================================================

# =============================================================================
# Ctrl_frame fill
# =============================================================================
ctrl_frame.columnconfigure(0, weight = 1)
ctrl_frame.columnconfigure(1, weight = 1)
ctrl_frame.columnconfigure(2, weight = 1)

ctrl_frame.rowconfigure((0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16, 17, 18,19,20,21,22,23,24), weight = 1)
ctrl_frame.rowconfigure(25, weight = 1000)   # this will stay an empty row. The large height will pack the other rows tight..


# the count variable makes it easy to reposition widgets in the frame without having to change grid indices of all following entries

count = 0
# lbl_test.grid(row = count, column = 1, stick = 'nw', padx = 10)
# count = count + 1
# count = count + 1
# tk.Separator(ctrl_frame, bootstyle='secondary').grid(row=count, column = 0, columnspan=3, pady = 10, sticky = 'nsew')
# count = count + 1



# Image 1 controls
# -----------------------------------
lbl_header1.grid(row = count, column = 0, columnspan = 2,  stick = 'nw', padx = 10)
count = count + 1
bt_browse1.grid(row = count, column = 0, stick = 'nw', padx = 10, pady = 10)
# count = count + 1

btn_set_mtr1.grid(row = count, column = 1, stick ='ne', pady = 10, padx = 10)
count = count + 1
mtr_alp1.grid(row = count, column = 0, columnspan = 2, rowspan = 4, stick = 'ne', padx = 10)

count = count + 1


lbl_cmp1.grid(row = count, column = 0, stick = 'nw', padx = 10)

count = count + 1
spn_cmp1.grid(row = count, column = 0,  stick = 'nw', padx = 10)

count = count + 1
# count = count + 1

lbl_min1.grid(row = count, column = 0,  stick = 'nw', padx = 10)
count = count + 1
sld_min1.grid(row = count, column = 0, columnspan = 2,  stick = 'nwe', padx = 10)
# lbl_test.grid(row = count, column = 3, stick = 'nw', padx = 10)
count = count + 1

lbl_max1.grid(row = count, column = 0,  stick = 'nw', padx = 10)
count = count + 1
sld_max1.grid(row = count, column = 0, columnspan = 2,  stick = 'nwe', padx = 10)
count = count + 1

lbl_ent_min1.grid(row = count, column = 0, stick = 'nw', padx = 10)
lbl_ent_max1.grid(row = count, column = 1, stick = 'nw', padx = 10)
count = count + 1
ent_min1.grid(row = count, column = 0, stick = 'nw', padx = 10)
ent_max1.grid(row = count, column = 1, stick = 'nw', padx = 10)
count = count + 1

btn_man_set1.grid(row = count, column = 0, stick = 'nw', padx = 10, pady = 10)
btn_auto_set1.grid(row = count, column = 1, stick = 'nw', padx = 10, pady = 10)

count = count + 1




tk.Separator(ctrl_frame, bootstyle='secondary').grid(row=count, column = 0, columnspan=3, pady = 10, sticky = 'nsew')
count = count + 1


#------------------------------------------
# Image 2 controls
#------------------------------------------

lbl_header2.grid(row = count, column = 0, columnspan = 2,  stick = 'nw', padx = 10)
count = count + 1
bt_browse2.grid(row = count, column = 0, stick = 'nw', padx = 10, pady = 10)
# count = count + 1

btn_set_mtr2.grid(row = count, column = 1, stick ='ne',pady = 10, padx = 10)
count = count + 1
mtr_alp2.grid(row = count, column = 0, columnspan = 2, rowspan = 4, stick = 'ne', padx = 10)

count = count + 1

lbl_cmp2.grid(row = count, column = 0, stick = 'nw', padx = 10)

count = count + 1
spn_cmp2.grid(row = count, column = 0,  stick = 'nw', padx = 10)

count = count + 1


lbl_min2.grid(row = count, column = 0,  stick = 'nw', padx = 10)
count = count + 1
sld_min2.grid(row = count, column = 0, columnspan = 2,  stick = 'nwe', padx = 10)
# lbl_test.grid(row = count, column = 3, stick = 'nw', padx = 10)
count = count + 1

lbl_max2.grid(row = count, column = 0,  stick = 'nw', padx = 10)
count = count + 1
sld_max2.grid(row = count, column = 0, columnspan = 2,  stick = 'nwe', padx = 10)
count = count + 1

lbl_ent_min2.grid(row = count, column = 0, stick = 'nw', padx = 10)
lbl_ent_max2.grid(row = count, column = 1, stick = 'nw', padx = 10)
count = count + 1
ent_min2.grid(row = count, column = 0, stick = 'nw', padx = 10)
ent_max2.grid(row = count, column = 1, stick = 'nw', padx = 10)
count = count + 1

btn_man_set2.grid(row = count, column = 0, stick = 'nw', padx = 10, pady = 10)
btn_auto_set2.grid(row = count, column = 1, stick = 'nw', padx = 10, pady = 10)

count = count + 1




tk.Separator(ctrl_frame, bootstyle='secondary').grid(row=count, column = 0, columnspan=3, pady = 10, sticky = 'nsew')
count = count + 1
#---------------------------------------------------------

count = count + 1


# bt_draw = tk.Button(ctrl_frame,text="Draw",command=draw_figure)
# bt_draw.grid(row = 25, column = 0, stick = 'nw', padx = 10)
# count = count + 1

# print(path1)
# print(path2)

# ============================================================
# Top frame packing
# ============================================================
lbl_logoM.pack(side = 'left', pady= 2, padx = 10)
lbl_version.pack(side = 'left', pady= 0, padx = 0)
bt_quit.pack(side = 'left',  pady= 0, padx = 250)

# ============================================================



root.mainloop()
