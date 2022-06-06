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
from histogram import histo_ski,histo_normal
from correlationcofficient import corr_of_rgb
from npcr import npcrv
from uaci import rootmeansquareerror,uaci
from uaci2 import uaci2
from psnr import RMSE

Dec_image="C:/Users/DELL/Downloads/Imaage/TESTING/RSA BMP/Dec/RSA-BMP-Dec-4.1.04.bmp.bmp" #change 1
Enc_image="C:/Users/DELL/Downloads/Imaage/TESTING/RSA BMP/ENC/RSA-BMP-Enc-4.1.04.bmp" #change 2

dec_store_loc="RSA-BMP-Dec-4.1.04" #change 3
enc_store_loc="RSA-BMP-Enc-4.1.04" #change 4

#no more changes

print("RMSE 1:" + str(rootmeansquareerror(Dec_image,Enc_image)))
print("RMSE 2:"+str(RMSE(Dec_image,Enc_image)))
print("NPCR :"+str(npcrv(Dec_image,Enc_image)))
# print("UCAI :" + str(uaci(Dec_image,Enc_image)))

print("UCAI :" + str(uaci2(Dec_image,Enc_image)))



print("Encrypted Image :")
print("Encrypted Correlation coefficient :"+str(corr_of_rgb(Enc_image)))
# coplot_horizontal(Enc_image,"")
# coplot_vertical(Enc_image,"")
histo_ski(Enc_image,enc_store_loc+"ski")
histo_normal(Enc_image,enc_store_loc+"normal")
# rgbhistogram(Enc_image,"Encrgb1")

print("Decrypted Image :")
print("Decrypted Correlation coefficient :"+str(corr_of_rgb(Dec_image)))
# coplot_horizontal(Dec_image,"")
# coplot_vertical(Dec_image,"")
histo_ski(Dec_image,dec_store_loc+"ski")
histo_normal(Dec_image,dec_store_loc+"normal")
# rgbhistogram2(Dec_image,"Decrgb1")
