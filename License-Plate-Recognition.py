# -*- coding: utf-8 -*-
"""
Created on Wed May  2 22:23:23 2018

@author: Hoda Abdelbasit
"""
import pytesseract
pytesseract.pytesseract.tesseract_cmd=r"C:\Users\Lenovo\AppData\Local\Tesseract-OCR\tesseract"
import PIL.Image

from PIL import ImageTk
import numpy as np

import argparse
import cv2
import os.path


from tkinter import filedialog
from tkinter import *
import tkinter as tk


def pixel_intensity(x, y):
    if y >= yimage or x>=ximage:
        return 0
    pixel =image[y][x]
    return (0.3* pixel[2])+0.59*pixel[1] + 0.11*pixel[0]  ## r g b calculate inetnsity of the pixel


def cc(i, h, contour):
    if h[i][2] < 0:
        return 0
    else:
        count = 1
        if possible_char(contours[h[i][2]]):
            count = 1
        count += count_siblings(h[i][2], h, contour)
        return count

def is_c(i, h):
    return get_parent(i, h) > 0

def get_parent(i, hierarchy):
    pt = hierarchy[i][3]
    while possible_char(contours[pt]) and pt > 0:
        pt= hierarchy[pt][3]
    return pt

# Count the number of same level of a contour
def count_siblings(i, hierarchy, contour):
    count = 0
    p = hierarchy[i][0]
    while p > 0:
        if possible_char(contours[p]):
            count += cc(p, hierarchy, contour)
        p = hierarchy[p][0]
    return count

def possible_char(contour):
    x, y, width, height = cv2.boundingRect(contour)
    aspect_ratio = (width*1.0)/(height*1.0)
    area= (width*1.0)*(height*1.0)
    if aspect_ratio < 0.25 or aspect_ratio > 1 or (area <= 100):       # aspect ratio of min 0.1 and max 10 area greaterthan 100
        return False
    return True  and not cv2.isContourConvex(contour)

def include_box(i, hierarchy, contour):
    if is_c(i, hierarchy) and cc(get_parent(i, hierarchy), hierarchy, contour) <= 2:
        return False
    return True
def PhotoCallBack():
    global filename
   
    filename = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("PNG files",".png"),("all files",".")))

def clickcode():
    

    test()
    my_image=PhotoImage(file='out.png')
    canvas.create_image(0,0,anchor=NW,image=my_image)
    canvas.my_image=my_image
txt=""
OUT=[]
def test():
     
     global contours 
     global OUT
     txt=""
     global image, yimage, ximage
     image = cv2.imread(filename)
     yimage = len(image)
     ximage = len(image[0])
     edges=cv2.Canny(image,400, 1000)

     _,contours, hierarchy = cv2.findContours(edges.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
     hierarchy = hierarchy[0]

# find the bounding rect for each one in the contours
     for i, contourr in enumerate(contours):
         x, y, width, height = cv2.boundingRect(contourr)
         if possible_char(contourr) and include_box(i, hierarchy, contourr):
             OUT.append([contourr, [x, y, width, height]])

     final_image = edges.copy()
     final_image.fill(255)
 
     for i, (contourr, box) in enumerate(OUT):
         
         foreg_intensity = 0.0
         for p in contourr:
             foreg_intensity += pixel_intensity(p[0][0], p[0][1])

         foreg_intensity /= len(contourr)
        
         x, y, width, height = box

         for xx in range(x, x + width):
             for yy in range(y, y + height):
                 if pixel_intensity(xx, yy) > foreg_intensity:
                     final_image[yy][xx] = 255
                 else:
                     final_image[yy][xx] = 0

     final_image = cv2.blur(final_image, (3, 3))
     cv2.imwrite("out.png", final_image) 
     OUT=[]
     new_image='out.png'
     file=PIL.Image.open(new_image)
     txt = pytesseract.image_to_string(file)
     label1.configure(text=txt)
     label1.config(font=("Courier", 30))

     
     
     
     
     
     
     
     
window=tk.Tk()
label2 = Label(window, text="",font=("Courier", 30))
label2.pack()

window.title('License Plate Recognition')
canvas=Canvas(window,width=1000,height=500)
canvas.pack()
label1 = Label(window, text="please click (Show Output Image) after selecting the image  ",font=( 30))
label1.pack()


btn2=Button(window,text='Select Input Image',command=PhotoCallBack)
btn2.pack()

btn=Button(window,text='Show Output Image',command=clickcode)
btn.pack()


window.mainloop()