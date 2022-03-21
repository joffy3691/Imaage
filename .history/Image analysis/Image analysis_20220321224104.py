"""
This is a standalone application to analyze the image .It uses a tkinter library of python to make gui for windows.
It consist of allanalysis(),rmse(),uac() , npcr() , askopenfile(), doegraphplot().All the modules defined in this file
is for analyzing image

"""
import os
from tkinter import *
from tkinter import filedialog

from PIL import ImageTk, Image
from coplot import coplot_horizontal,coplot_vertical
from correlationcofficient import corr_of_rgb
from histogram import rgbhistogram,rgbhistogram2
from npcr import npcrv
from uaci import rootmeansquareerror,uaci

Dec_image="C:/Users/DELL/Downloads/Imaage/Enc images/JPG_8bit/dec_image_jpg_8bit_1.jpg"
Enc_image="C:/Users/DELL/Downloads/Imaage/output1.png"
print("RMSE :" + str(rootmeansquareerror(Dec_image,Enc_image)))
print("NPCR :"+str(npcrv(Dec_image,Enc_image)))
print("UCAI :" + str(uaci(Dec_image,Enc_image)))

print("Encrypted Image :")
print("Correlation coefficient :"+str(corr_of_rgb(Enc_image)))
coplot_horizontal(Enc_image,"EncCorelationh1")
coplot_vertical(Enc_image,"EncCorelationv1")
# rgbhistogram(Enc_image,"Encrgb1")

print("Decrypted Image :")
print("Correlation coefficient :"+str(corr_of_rgb(Dec_image)))
coplot_horizontal(Dec_image,"DecCorelationh1")
coplot_vertical(Dec_image,"DecCorelationv1")
# rgbhistogram2(Dec_image,"Decrgb1")
