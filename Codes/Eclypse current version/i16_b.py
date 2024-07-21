# -*- coding: utf-8 -*-
"""
Created on Tue Dec 26 15:15:56 2023

@author: Mohammad Asif Zaman

Stackoverflow Help links:
=========================    
    Matplotlib in tkinter frame:
    - https://stackoverflow.com/questions/59001195/how-to-update-a-graph-created-by-matplotlib-in-tkinter

    Drag and drop implementation:
    - dnd2 feature: https://stackoverflow.com/questions/14267900/drag-and-drop-explorer-files-to-tkinter-entry-widget
    - implement within ttkbootstrap: https://stackoverflow.com/questions/76695493/how-do-i-add-drop-and-drag-functionality-to-different-tkinter-windows
    - delete previous entry: https://stackoverflow.com/questions/2260235/how-to-clear-the-entry-widget-after-a-button-is-pressed-in-tkinter

Version Notes:
==============

b03:
    - implemented rough figure enable/disable feature  
    
b04:
    - disabled the control knobs/buttons when figure is disabled     

b08:
    - used grid instead of pack in the output_frame. This helps with figure resizing a little.
    
b10:
    - Saved zoom state. Now, when a figure is adjusted, it does not go back to the default view anymore.
    
b11-14:
    - Added analysis backend for detecting fluorescent objects in image 2
    - On screen annotation of mean value and bounding boxes
    - Added version and date variables
        
"""

#===================================
# Version and date text
#===================================
vr_txt = 'Version b0.16'
dt_txt = 'July, 2024'
#===================================

# import tkinter as tk
# from tkinter import *
import ttkbootstrap as tk

# https://stackoverflow.com/questions/76717279/ttkbootstrap-meter-widget-doc-example-not-working
from PIL import Image
Image.CUBIC = Image.BICUBIC  # this is for the meter widget in ttkbootstrap. Check the stackoverflow link above


from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

from tkinter.filedialog import askopenfile 
from ttkbootstrap.dialogs import Messagebox

from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinterdnd2.TkinterDnD import _require


import numpy as np
import cv2


# import custom functions
# from func_fl_single_img_v1_5 import *
from func_fl_single_img import *
import os


import matplotlib.pyplot as py

   
def runB_analysis():
    global Bx_store
    global By_store
    global Bo_mean
    global BiB_store
    
    Bo_mean, Bo_size, Bb_mean, Bx_store, By_store, BiB_store = single_img_analysis(path1, os.path.dirname(path1), 41, -0.1)
    showB_label()
    

def showB_label():
    # b0.14 update. This will show all annotation instead of just showing the label from now.
    
    global ax
    global Bx_store
    global By_store
    global BiB_store
    
    try:  # check if x_store has values (which it will have when run_analysis() function has been run at least once
        Nobj = len(Bx_store)  # number of object detected by the analysis program
    except: # in case of error, exit function using return command
        print('Can not show labels. Analysis have not been performed or returned errors.')
        return 0
    
    for m in range(Nobj):
        BiB = BiB_store[m]
        
        # display label text
        ax.text(Bx_store[m], By_store[m], str(m) + ':', fontsize = 6, color = '#ff55ff')
        
        # display bounding box
        yt = [BiB[0], BiB[1], BiB[1], BiB[0], BiB[0]]
        xt = [BiB[2], BiB[2], BiB[3], BiB[3], BiB[2]]
        ax.plot(xt,yt,'#00aaaa', linewidth = 0.5)    # plot boxes
        
        # display mean value
        # ax.text(BiB[3], BiB[0], str(Bo_mean[m]), fontsize = 6, color = '#66ff66')
        # ax.text(BiB[3], BiB[0], str(Bo_mean[m]), fontsize = 6, color = '#66ff66')
    
    canvas.draw_idle() 


def run_analysis():
    # block_size = 81
    # th_factor = 0.1
    
    global x_store
    global y_store
    global o_mean
    global iB_store
    try:
        block_size = int(ent_block_size.get())
    except ValueError:
        Messagebox.show_error('Failed to run. Block size must be an integer', 'Input error', parent = output_frame)
        return 0
    try:
        th_factor = float(ent_threshold.get())
    except ValueError:
        Messagebox.show_error('Failed to run. Threshold must be a number', 'Input error', parent = output_frame)
        return 0
    
     
    
    o_mean, o_size, b_mean, x_store, y_store, iB_store = single_img_analysis(path2, os.path.dirname(path2), block_size, th_factor)
    show_label()
    # show_box()
    # show_mean()
    
    
def show_label():
    # b0.14 update. This will show all annotation instead of just showing the label from now.
    
    global ax
    global x_store
    global y_store
    global iB_store
    
    try:  # check if x_store has values (which it will have when run_analysis() function has been run at least once
        Nobj = len(x_store)  # number of object detected by the analysis program
    except: # in case of error, exit function using return command
        print('Can not show labels. Analysis have not been performed or returned errors.')
        return 0
    
    for m in range(Nobj):
        iB = iB_store[m]
        
        # display label text
        ax.text(x_store[m], y_store[m], str(m) + ':', fontsize = 6, color = 'w')
        
        # display bounding box
        yt = [iB[0], iB[1], iB[1], iB[0], iB[0]]
        xt = [iB[2], iB[2], iB[3], iB[3], iB[2]]
        ax.plot(xt,yt,'#ff5555', linewidth = 0.5)    # plot boxes
        
        # display mean value
        ax.text(iB[3], iB[0], str(o_mean[m]), fontsize = 6, color = '#66ff66')
        ax.text(iB[3], iB[0], str(o_mean[m]), fontsize = 6, color = '#66ff66')
    
    canvas.draw_idle() 


def show_box():
    global ax
   
    global iB_store
    
    try:  # check if iB_store has values (which it will have when run_analysis() function has been run at least once
        Nobj = len(iB_store)  # number of object detected by the analysis program
    except: # in case of error, exit function using return command
        print('Can not show boxes. Analysis have not been performed or returned errors.')
        return 0
    
    for m in range(Nobj):
        iB = iB_store[m]
        yt = [iB[0], iB[1], iB[1], iB[0], iB[0]]
        xt = [iB[2], iB[2], iB[3], iB[3], iB[2]]
        ax.plot(xt,yt,'#ff5555', linewidth = 0.5)    # plot boxes
        
    canvas.draw_idle() 

def show_mean():
    global ax
    global x_store
    global y_store
    global o_mean
    
    global iB_store
    
    
    
    try:  # check if x_store has values (which it will have when run_analysis() function has been run at least once
        Nobj = len(x_store)  # number of object detected by the analysis program
    except: # in case of error, exit function using return command
        print('Can not show mean intensity. Analysis have not been performed or returned errors.')
        return 0
    
    for m in range(Nobj):
        iB = iB_store[m]
        ax.text(iB[3], iB[0], str(o_mean[m]), fontsize = 6, color = '#66ff66')
        ax.text(iB[3], iB[0], str(o_mean[m]), fontsize = 6, color = '#66ff66')
    canvas.draw_idle() 
        
    
    
# Function to update slider labels when sliders are updated
def scale_update(evnt):
    # Function to update slider labels when sliders are updated

    # update the text near the sliders
    lbl_min1.config(text = 'Min: ' + str(int(float(sld_min1.get()))))
    lbl_max1.config(text = 'Max: ' + str(int(float(sld_max1.get()))))
    lbl_min2.config(text = 'Min: ' + str(int(float(sld_min2.get()))))
    lbl_max2.config(text = 'Max: ' + str(int(float(sld_max2.get()))))
 
    ent_min1.delete(0, tk.END)
    ent_min1.insert(0, int(float(sld_min1.get())))
    ent_max1.delete(0, tk.END)
    ent_max1.insert(0, int(float(sld_max1.get())))
    
    ent_min2.delete(0, tk.END)
    ent_min2.insert(0, int(float(sld_min2.get())))
    ent_max2.delete(0, tk.END)
    ent_max2.insert(0, int(float(sld_max2.get())))
    
    # ent_min1.get(sld_min1.get())
    # Call function to draw the figures
    draw_figure()

# ==========================================================
# Update and draw/display figure
# ==========================================================
def draw_figure():
    # Update and draw/display figure    
    # clear figure
    
    # recall global fig and ax variables/handles 
    global fig
    global ax
    global xlim_org
    global ylim_org
    # print('In draw figure')    
    
    
    # ==========================================================
    # Try to save the current axis limits (zoom settings)   
    # ==========================================================
    try:
        xlim_save = ax.get_xlim()
        ylim_save = ax.get_ylim()
        # print(xlim_save)
        # print(ylim_save)
        
       
        # save the default original view    
        if xlim_save != [0,1]:
            if 'xlim_org' not in globals():
                print('Saved original default view.')
                xlim_org = xlim_save
                ylim_org = ylim_save
                # print(xlim_org)
        
        
    except:
        # print('pass')
        pass
    # ==========================================================
    
    # fig.clear()   # it seems that this clear command and the output_frame update are not needed. The one clear command after these is enough
    # output_frame.update()
    
    fig.clear()
    
    ax = fig.add_subplot(111)
    
    # display image 1 with appropriate color scale and transparency
    img = img1
    if enable1.get() == True:
        im_obj = ax.imshow(img,cmap = spn_cmp1.get(), alpha = float(mtr_alp1.amountusedvar.get()/100))
        im_obj.set_clim([sld_min1.get(), sld_max1.get()])

    
    # display image 2 with appropriate color scale and transparency
    img = img2
    if enable2.get() == True:
        im_obj = ax.imshow(img,cmap = spn_cmp2.get(), alpha = float(mtr_alp2.amountusedvar.get()/100))
        im_obj.set_clim([sld_min2.get(), sld_max2.get()])
        # ax.text(500, 500, 'test', fontsize = 6, color = 'w')
    # Turn axis labels off
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    
    # ==========================================================
    # Set current axis limits (zoom) to previously saved one
    # ==========================================================
    if abs(np.sum(xlim_save)) + abs(np.sum(ylim_save)) > 3:   # this is a sum check to see if a valid zoom state was saved. Sometimes the limits are (0,1) which is not valid
        ax.set_xlim(xlim_save)
        ax.set_ylim(ylim_save)
    # ==========================================================
 
    # print('sld_min1 = %i' % sld_min1.get())
    
    # Draw canvas
    canvas.draw_idle()
# ==========================================================



# ==========================================================
# Function to reset view
# ==========================================================

def reset_view():
    global xlim_org
    global ylim_org
    global ax
    try:
        # print(xlim_org)
        # print(ylim_org)
        ax.set_xlim(xlim_org)
        ax.set_ylim(ylim_org)
        draw_figure()
        print('View reset')
    except:
        pass
            
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
    # ! the temp store is important. The first call of sld.set sets both
    # min2 and max2 from the slider state. The entry box value
    # for the second call (max in this case), gets lost. Hence,
    # store it in a temporary variable.
    
    # Reset sliders to full range first. If we try to set slider value that is outside its range, it fails. Hence, reset it to full range before attempting to set it to a new range.
    try:
        sld_min1.configure(from_=0, to = 2**16-1)
    except:
        pass
            
    try:
        sld_max1.configure(from_=0, to = 2**16-1)
    except:
        pass
    
    
    # Set slider values based on the entry box value
    temp = ent_max1.get()
    sld_min1.set(ent_min1.get())
    sld_max1.set(temp)
    
    # Change slider limits to fit/center the new set value
    try:
        sld_min1.configure(from_=sld_min1.get()*sld_fct, to = sld_min1.get()*(1+sld_fct))
    except:
        pass
            
    try:
        sld_max1.configure(from_=sld_max1.get()*sld_fct, to = sld_max1.get()*(1+sld_fct))
    except:
        pass
    

    

def man_set2():
    # ! the temp store is important. The first call of sld.set sets both
    # min2 and max2 from the slider state. The entry box value
    # for the second call (max in this case), gets lost. Hence,
    # store it in a temporary variable.
    
    
    global sld_fct
    
    # Reset sliders to full range first. If we try to set slider value that is outside its range, it fails. Hence, reset it to full range before attempting to set it to a new range.
    try:
        sld_min2.configure(from_=0, to = 2**16-1)
    except:
        pass
            
    try:
        sld_max2.configure(from_=0, to = 2**16-1)
    except:
        pass
    
    # Set slider values based on the entry box value
    temp = ent_max2.get()  
    sld_min2.set(ent_min2.get())
    sld_max2.set(temp)
    
    # Change slider limits to fit/center the new set value
    try:
        sld_min2.configure(from_=sld_min2.get()*sld_fct, to = sld_min2.get()*(1+sld_fct))
    except:
        pass
            
    try:
        sld_max2.configure(from_=sld_max2.get()*sld_fct, to = sld_max2.get()*(1+sld_fct))
    except:
        pass
# ==========================================================


# ==========================================================
# Keyboard/mouse binding functions of manual set. They take 
# event argument, where as the button press functions for the
# same action don't. For this reason, these extra set of
# functions were necessary. 
# ==========================================================
def key_set1(ev):
    man_set1()

def key_set2(ev):
    man_set2()
# ==========================================================


# ==========================================================
# This function will bind mouse key to the opacity meters later
# ==========================================================
def mtr_mouse(ev):
    print('in mtr_mouse function')
    draw_figure()
# ==========================================================

    
def load_img():
    global img1
    global img2
    
    global bmn1
    global bmx1
    global bmn2
    global bmx2
    

    
    global org_xlim
    global org_ylim
    
    
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
      
        print('\nThank you for using the program. Focus on the big picture!\n')
        root.quit()     # Sometimes, the terminal gets stuck when quitting the program. This might help.
        root.destroy()
    else:
        pass
# =============================================================================    

def show_info():
    freadme = open('readme.txt').read()  
    Messagebox.show_info(freadme, 'Information', parent = ctrl_frame) 
# =============================================================================    



# =============================================================================    
# Drag and drop functions for the two DND boxes
# =============================================================================    

def drag_drp1(e):
    global path1   # global variable that contains the path of file 1
    
    st = str(e.data) # get drag n drop event data and assign it to a string        
    
    # replace curly brackets (if any). These braces seem to show up on when the file path has space character.
    st = st.replace('{','')
    st = st.replace('}','')
    
    path1 = st  # feed the cleaned string data in path1 global variable

    ent_dnd1.delete(0,'end')  # remove old text from the DND box
    ent_dnd1.insert(tk.END, st)  # insert new text in the DND box
    
    lbl_path1.config(text = 'File 1 = ' + path1)  # update path label in the output frame

    # Load and draw image based on the new path
    load_img()
    draw_figure()
    
def drag_drp2(e):
    global path2   # global variable that contains the path of file 1
    
    st = str(e.data) # get drag n drop event data and assign it to a string        
    
    # replace curly brackets (if any). These braces seem to show up on when the file path has space character.
    st = st.replace('{','')
    st = st.replace('}','')
    
    path2 = st  # feed the cleaned string data in path1 global variable

    ent_dnd2.delete(0,'end')  # remove old text from the DND box
    ent_dnd2.insert(tk.END, st)  # insert new text in the DND box
    
    lbl_path2.config(text = 'File 2 = ' + path2)  # update path label in the output frame

    # Load and draw image based on the new path
    load_img()
    draw_figure()
# =============================================================================    
    
# =============================================================================    
# Enable/disable figure with check button
# =============================================================================    
def en_dis():
    # Enable/disable figure with check button
    
    # Figure disable procedure:set opacity to zero and draw figure. 
    # store current opacity value, then set opacity to zero, then draw
    # and then restore opacity values without drawing (for future)    
    
    
    # status variable for all the control sliders/buttons
    sts1 = 'enabled'
    sts2 = 'enabled'
    
    # Get value of the opacity/alpha meters and store in temp variables
    m1 = mtr_alp1.amountusedvar.get()
    m2 = mtr_alp2.amountusedvar.get()
    
    if enable1.get() == False:
        sts1 = 'disabled'  # set the status of controls to disable later in the function
        mtr_alp1.configure(amountused = 0,interactive = False, bootstyle = 'secondary', subtextstyle = 'secondary')   # set meter alpha to zero if checkbox is false
    else:
        mtr_alp1.configure(interactive = True, bootstyle = im1_style, subtextstyle = im1_style) 
    
    
    if enable2.get() == False:
        sts2 = 'disabled'     # set the status of the controles to disable later in the function
        mtr_alp2.configure(amountused = 0,interactive = False, bootstyle = 'secondary', subtextstyle = 'secondary')   # set meter alpha to zero if checkbox is false
    else:
        mtr_alp2.configure(interactive = True, bootstyle = im2_style, subtextstyle = im2_style) 
    
    
    draw_figure()   # update figure
    
    # reset alpha meters to old values
    mtr_alp1.configure(amountused = m1)
    mtr_alp2.configure(amountused = m2)
    
    
    # set all the controls to disable/enable based on the checkbutton state
    # for image 1
    sld_min1.configure(state = sts1)
    sld_max1.configure(state = sts1)
    btn_auto_set1.configure(state = sts1)
    btn_man_set1.configure(state = sts1)
    btn_set_mtr1.configure(state = sts1)
    btn_browse1.configure(state = sts1)
    spn_cmp1.configure(state = sts1)
    
    # for image 2
    sld_min2.configure(state = sts2)
    sld_max2.configure(state = sts2)
    btn_auto_set2.configure(state = sts2)    
    btn_man_set2.configure(state = sts2) 
    btn_set_mtr2.configure(state = sts2)
    btn_browse2.configure(state = sts2)
    spn_cmp2.configure(state = sts2)
# =============================================================================    



    
# ==========================================================
# Main Program
# ==========================================================
    
print('Starting Eclipse ' + vr_txt + ', ' + dt_txt + '\n\n')
    
# =============================================================================
# Window and frame parameters
# =============================================================================
window_width = 1400
window_height = 910    
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
sld_fct = 0.5

# =============================================================================

# =============================================================================
# Default values of parameters
# =============================================================================

bmn1, bmx1 = 400, 4000



bmn2, bmx2 = bmn1, bmx1

path1 = 'Test images/s1.tif'
path2 = 'Test images/s2.tif'

im1_style = 'info'
im2_style = 'success'

# =============================================================================

# =============================================================================
# root window
# =============================================================================

root = tk.Window(themename="journal")    # set root windows and theme
_require(root)  # for drag and drop support
root.title('Eclipse: View and Superimpose 16 bit Images')    # Set title of the root frame
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

img_logoM = tk.PhotoImage(file = 'ec_logo_90px.png')
lbl_logoM = tk.Label(top_frame,  image = img_logoM)
lbl_version = tk.Label(top_frame, text = 'Mohammad Asif Zaman \n' + vr_txt + '\n' + dt_txt, bootstyle = 'secondary')
btn_quit = tk.Button(top_frame, text = 'Quit', bootstyle = 'primary', command = quit_program)
btn_info = tk.Button(top_frame, text = 'Info', bootstyle = 'dark', command = show_info)

lbl_path1 = tk.Label(output_frame,text = 'File 1 = ' + path1, bootstyle = im1_style)
lbl_path2 = tk.Label(output_frame,text = 'File 2 = ' + path2, bootstyle = im2_style)








btn_browse1 = tk.Button(ctrl_frame, text = '   Browse    ', bootstyle = im1_style, command = open_file1)
btn_browse2 = tk.Button(ctrl_frame, text = '   Browse    ', bootstyle = im2_style, command = open_file2)

ent_dnd1 = tk.Entry(ctrl_frame, bootstyle = im1_style)
ent_dnd1.drop_target_register(DND_FILES)
ent_dnd1.dnd_bind('<<Drop>>', drag_drp1)
lb_dnd1 = tk.Label(ctrl_frame, text = 'Drag and drop here', bootstyle = im1_style)

ent_dnd2 = tk.Entry(ctrl_frame, bootstyle = im2_style)
ent_dnd2.drop_target_register(DND_FILES)
ent_dnd2.dnd_bind('<<Drop>>', drag_drp2)
lb_dnd2 = tk.Label(ctrl_frame, text = 'Drag and drop here', bootstyle = im2_style)



fig = Figure(figsize=(4, 3), dpi=150)
# fig = Figure()
ax = fig.add_subplot(111)

fig.tight_layout()


# ==========================================================
# Display figure and toolbar
# ==========================================================
canvas = FigureCanvasTkAgg(fig, master=output_frame)  # A tk.DrawingArea.

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
                    subtextfont='-size 7 -weight normal',
                    )



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

# mtr_alp1.bind("<Button>", mtr_mouse)
# mtr_alp2.bind("<Button-1>", mtr_mouse)


lbl_cmp1 = tk.Label(ctrl_frame,text = 'Colormap 1', bootstyle = im1_style)
spn_cmp1  = tk.Spinbox(ctrl_frame, 
                       bootstyle= im1_style,
                       values = ['viridis', 'jet', 'Greys', 'Greys_r', 'cividis', 'Blues', 'Blues_r'], state= 'readonly',
                       wrap = True,
                       command = draw_figure,
                       )
spn_cmp1.set('Greys_r')

enable1 = tk.BooleanVar(value = True)
chk_enable1 = tk.Checkbutton(ctrl_frame, bootstyle = im1_style + '-round-toggle', text = 'Enable', variable = enable1, command = en_dis)
enable2 = tk.BooleanVar(value = False)
chk_enable2 = tk.Checkbutton(ctrl_frame, bootstyle = im2_style + '-round-toggle', text = 'Enable', variable = enable2, command = en_dis)


lbl_cmp2 = tk.Label(ctrl_frame,text = 'Colormap 2', bootstyle = im2_style)
spn_cmp2  = tk.Spinbox(ctrl_frame, 
                       bootstyle= im2_style,
                       values = ['hot', 'Reds', 'PuRd','Greens', 'plasma', 'magma', 'jet'], state= 'readonly',
                       wrap = True,
                       command = draw_figure,
                       )
spn_cmp2.set('magma')


# Load image
load_img()


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

ent_min1.insert(0, bmn1)
ent_max1.insert(0, bmx1)
ent_min2.insert(0, bmn2)
ent_max2.insert(0, bmx2)

ent_min1.bind("<Return>", key_set1)
ent_min1.bind("<Tab>", key_set1)
ent_max1.bind("<Return>", key_set1)
ent_max1.bind("<Tab>", key_set1)

# ent_min1.bind("<Button>", mtr_mouse)

ent_min2.bind("<Return>", key_set2)
ent_min2.bind("<Tab>", key_set2)
ent_max2.bind("<Return>", key_set2)
ent_max2.bind("<Tab>", key_set2)


sld_min1 = tk.Scale(ctrl_frame, 
                    bootstyle = im1_style, 
                    from_ = 0, #np.round(mn1L,2),
                    to = 2**16 - 1, #np.round(mn1H,2),
                    command = scale_update,
                    )

sld_max1 = tk.Scale(ctrl_frame, 
                    from_ = 0, #np.round(mx1L,2),
                    to = 2**16 - 1, #np.round(mx1H,2),
                    bootstyle = im1_style,
                    command = scale_update,
                    )

sld_min2 = tk.Scale(ctrl_frame, 
                    bootstyle = im2_style,
                    from_ = 0, #np.round(mn2L,2),
                    to = 2**16 - 1, #np.round(mn2H,2),
                    command = scale_update,
                    )

sld_max2 = tk.Scale(ctrl_frame, 
                    bootstyle = im2_style,
                    from_ = 0, #np.round(mx2L,2),
                    to = 2**16 - 1, #np.round(mx2H,2),
                    command = scale_update,
                    )

# set slider values
sld_min1.set(bmn1)
sld_max1.set(bmx1)
sld_min2.set(bmn2)
sld_max2.set(bmx2)

# display slider text
lbl_min1 = tk.Label(ctrl_frame, text = 'Min: ' + str(int(float(sld_min1.get()))), bootstyle = im1_style)
lbl_max1 = tk.Label(ctrl_frame, text = 'Max: ' + str(int(float(sld_max1.get()))), bootstyle = im1_style)
lbl_min2 = tk.Label(ctrl_frame, text = 'Min: ' + str(int(float(sld_min2.get()))), bootstyle = im2_style)
lbl_max2 = tk.Label(ctrl_frame, text = 'Max: ' + str(int(float(sld_max2.get()))), bootstyle = im2_style)



# Button for setting slider to auto range
btn_auto_set1 = tk.Button(ctrl_frame, text = 'Auto Set', bootstyle = im1_style, command = auto_set1)
btn_auto_set2 = tk.Button(ctrl_frame, text = 'Auto Set', bootstyle = im2_style, command = auto_set2)

# Button for setting slider to manual range
btn_man_set1 = tk.Button(ctrl_frame, text = 'Set', bootstyle = im1_style, command = man_set1)
btn_man_set2 = tk.Button(ctrl_frame, text = 'Set', bootstyle = im2_style, command = man_set2)

# Buttons for setting opacity
btn_set_mtr1 = tk.Button(ctrl_frame, bootstyle = im1_style, text = 'Set Opacity', command = draw_figure)
btn_set_mtr2 = tk.Button(ctrl_frame, bootstyle = im2_style, text = 'Set Opacity', command = draw_figure)



# btn_reset_v = tk.Button(ctrl_frame, bootstyle = im1_style, text = 'Reset View', command = reset_view)
btn_reset_v = tk.Button(output_frame, bootstyle = im1_style, text = 'Reset View', command = reset_view)

en_dis()   # call the function to make sure the figures correspond to checkbutton states







# =============================================================================
# Layout (mostly grid)
# =============================================================================

# =============================================================================
# Ctrl_frame fill
# =============================================================================
ctrl_frame.columnconfigure(0, weight = 1)
ctrl_frame.columnconfigure(1, weight = 1)
ctrl_frame.columnconfigure(2, weight = 1)

ctrl_frame.rowconfigure((0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16, 17, 18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34), weight = 1)
ctrl_frame.rowconfigure(35, weight = 1000)   # this will stay an empty row. The large height will pack the other rows tight..


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

lb_dnd1.grid(row = count, column = 0, stick = 'nw', padx = 10)
ent_dnd1.grid(row = count, column = 0, rowspan = 2, columnspan = 2, stick = 'nw', padx = 10,pady = 2, ipady = 20, ipadx = 50)
btn_browse1.grid(row = count, column = 1, stick = 'ne', padx = 10, pady = 2)
count = count + 1

btn_set_mtr1.grid(row = count, column = 1, stick ='ne', padx = 10, pady = 2)
count = count + 1
mtr_alp1.grid(row = count, column = 0, columnspan = 2, rowspan = 4, stick = 'ne', padx = 10)

count = count + 1


lbl_cmp1.grid(row = count, column = 0, stick = 'nw', padx = 10)

count = count + 1
spn_cmp1.grid(row = count, column = 0,  stick = 'nw', padx = 10)
chk_enable1.grid(row = count, column = 1, stick = 'w', padx = 10)
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


# July 20, 2024: Brightfield running command
# Additional button to analyze the bright-field image (image 1)

btn_runB_analysis = tk.Button(ctrl_frame, text = 'Run Analysis', bootstyle = 'danger', command = runB_analysis)
btn_runB_analysis.grid(row = count, rowspan = 1, column = 1, stick = 'nw', padx = 10, pady = 5, ipady = 2)

btn_showB_label = tk.Button(ctrl_frame, text = 'Show labels', bootstyle = im1_style, command = showB_label)
btn_showB_label.grid(row = count, rowspan = 1, column = 0, stick = 'nw', padx = 10, pady = 5, ipady = 2)


count = count + 1

btn_clearB_annotation = tk.Button(ctrl_frame, text = 'Clear Annot.', bootstyle = im1_style, command = draw_figure)
btn_clearB_annotation.grid(row = count, rowspan = 1, column = 1, stick = 'nw', padx = 10, pady = 5, ipady = 2)

count = count + 1

tk.Separator(ctrl_frame, bootstyle='secondary').grid(row=count, column = 0, columnspan=3, pady = 10, sticky = 'nsew')
count = count + 1


#------------------------------------------
# Image 2 controls
#------------------------------------------

lbl_header2.grid(row = count, column = 0, columnspan = 2,  stick = 'nw', padx = 10)
count = count + 1
lb_dnd2.grid(row = count, column = 0, stick = 'nw', padx = 10)
ent_dnd2.grid(row = count, column = 0, rowspan = 2, columnspan = 2, stick = 'nw', padx = 10,pady = 2, ipady = 20, ipadx = 50)
btn_browse2.grid(row = count, column = 1, stick = 'ne', padx = 10, pady = 2)
count = count + 1

btn_set_mtr2.grid(row = count, column = 1, stick ='ne',pady = 2, padx = 10)
count = count + 1
mtr_alp2.grid(row = count, column = 0, columnspan = 2, rowspan = 4, stick = 'ne', padx = 10)

count = count + 1

lbl_cmp2.grid(row = count, column = 0, stick = 'nw', padx = 10)

count = count + 1
spn_cmp2.grid(row = count, column = 0,  stick = 'nw', padx = 10)
chk_enable2.grid(row = count, column = 1, stick = 'w', padx = 10)

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



# tk.Separator(ctrl_frame, bootstyle='secondary').grid(row=count, column = 0, columnspan=3, pady = 10, sticky = 'nsew')
# count = count + 1
#---------------------------------------------------------
tk.Separator(ctrl_frame, bootstyle='secondary').grid(row=count, column = 0, columnspan=3, pady = 10, sticky = 'new')
# count = count + 1

# btn_reset_v.grid(row = count, column = 1, stick = 'nw', padx = 10, pady = 10)
# count = count + 1


# count = count + 1


# bt_draw = tk.Button(ctrl_frame,text="Draw",command=draw_figure)
# bt_draw.grid(row = 25, column = 0, stick = 'nw', padx = 10)
# count = count + 1

# print(path1)
# print(path2)

# ============================================================
# Top frame packing
# ============================================================
lbl_logoM.pack(side = 'left', pady= 2, padx = 30)
lbl_version.pack(side = 'left', pady= 0, padx = 0)
btn_info.pack(side = 'left',  pady= 0, padx = 50, ipadx = 30, ipady = 10)
btn_quit.pack(side = 'left',  pady= 0, padx = 10,ipadx = 30, ipady = 10)

# ============================================================



# ============================================================
# Output frame packing
# ============================================================
output_frame.rowconfigure((0,1,3), weight=1)
output_frame.rowconfigure(2, weight=60)


output_frame.columnconfigure(0, weight=1)
output_frame.columnconfigure(1, weight=2)



lbl_path1.grid(row = 0, column = 0,  sticky = 'nw')
lbl_path2.grid(row = 1, column = 0,  sticky = 'nw')
# lbl_path2.grid(row = 0, column = 1,  sticky = 'nw')
btn_reset_v.grid(row = 1, column = 0, stick = 'ne', ipady = 6, padx = 70)

canvas.get_tk_widget().grid(row = 2, column = 0, sticky = 'news')
# btn_reset_v.grid(row = 3, column = 0, stick = 'nw', ipady = 10, padx = 10)


# lbl_space = tk.Label(output_frame, text = '!')
# lbl_space.grid(row = 2, column = 1)

# # Pack output frame texts immediately so that they appear on the top (above the figure)
# lbl_path1.pack(side = 'top', anchor = 'nw', padx = 10)
# lbl_path2.pack(side =  'top', anchor = 'nw', padx = 10)

# canvas.get_tk_widget().pack(anchor = 'nw')





# canvas.get_tk_widget().pack(side = 'top', fill = 'both', expand = True)
# canvas.get_tk_widget().pack(anchor= 'e', fill = 'both', expand = True)

# ============================================================









# =============================================================================


# Analysis backend implementation (May 2, 2024)
# both the UI definition and packinga are done here together. Rather than separating define and pack, it is better
# to separate the image viewing commands to the analysis commands for debugging purposes. The code can be rearranged later
# if need arises.


  
    
    
  

    # print('test')
    # print(os.path.dirname(path2))
lbl_header3 =tk.Label(ctrl_frame,text = 'Image 2 Analysis', font = ('bold', 12))

lbl_block_size= tk.Label(ctrl_frame,text = 'Block size', bootstyle = 'info')
ent_block_size = tk.Entry(ctrl_frame, bootstyle = im2_style)
ent_block_size.insert(0,81) # default value set


lbl_threshold= tk.Label(ctrl_frame,text = 'Threshold', bootstyle = 'info')
ent_threshold = tk.Entry(ctrl_frame, bootstyle = im2_style)
ent_threshold.insert(0,0.2) # default value set


btn_run_analysis = tk.Button(ctrl_frame, text = 'Run Analysis', bootstyle = 'danger', command = run_analysis)
btn_show_label = tk.Button(ctrl_frame, text = 'Show labels', bootstyle = im2_style, command = show_label)
btn_show_mean = tk.Button(ctrl_frame, text =  'Show mean  ', bootstyle = im2_style, command = show_mean)

btn_show_box = tk.Button(ctrl_frame, text = 'Show box   ', bootstyle = im2_style, command = show_box)
btn_clear_annotation = tk.Button(ctrl_frame, text = 'Clear Annot.', bootstyle = im2_style, command = draw_figure)



count = count + 1
lbl_header3.grid(row = count, column = 0, columnspan = 2,  stick = 'nw', padx = 10)


count = count + 1
lbl_threshold.grid(row=count, column = 0, sticky = 'nw', padx = 10)
lbl_block_size.grid(row=count, column = 1, sticky = 'nw', padx = 10)

count = count + 1
ent_threshold.grid(row=count, column = 0, sticky = 'nw', padx = 10)
ent_block_size.grid(row=count, column = 1, sticky = 'nw', padx = 10)


count = count + 1
btn_show_label.grid(row = count, column = 0, stick = 'nw', padx = 10, pady = 10)
btn_run_analysis.grid(row = count, rowspan = 2, column = 1, stick = 'nw', padx = 10, pady = 10, ipady = 20)


count = count + 1
btn_show_mean.grid(row = count, column = 0, stick = 'nw', padx = 10, pady = 10)


count = count + 1
btn_show_box.grid(row = count, column = 0, stick = 'nw', padx = 10, pady = 10)
btn_clear_annotation.grid(row = count, column = 1, stick = 'nw', padx = 10, pady = 10)


count = count + 1


tk.Separator(ctrl_frame, bootstyle='secondary').grid(row=count, column = 0, columnspan=3, pady = 10, sticky = 'new')

root.mainloop()
