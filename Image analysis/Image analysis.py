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

Dec_image="C:/Users/vishn/PycharmProjects/imo/dtjdtg/Review 3/dec_image.png"
Enc_image="C:/Users/vishn/PycharmProjects/imo/dtjdtg/Review 3/enc_image.png"
print("RMSE :" + str(rootmeansquareerror(Dec_image,Enc_image)))
print("NPCR :"+str(npcrv(Dec_image,Enc_image)))
# print("UCAI :" + str(uaci(Dec_image,Enc_image)))

print("UCAI :" + str(uaci2(Dec_image,Enc_image)))
RMSE(Dec_image,Enc_image)


print("Encrypted Image :")
print("Correlation coefficient :"+str(corr_of_rgb(Enc_image)))
coplot_horizontal(Enc_image,"EncCorelationh1")
coplot_vertical(Enc_image,"EncCorelationv1")
histo_ski(Enc_image)
histo_normal(Enc_image)
# rgbhistogram(Enc_image,"Encrgb1")

print("Decrypted Image :")
print("Correlation coefficient :"+str(corr_of_rgb(Dec_image)))
coplot_horizontal(Dec_image,"DecCorelationh1")
coplot_vertical(Dec_image,"DecCorelationv1")
histo_ski(Dec_image)
histo_normal(Dec_image)
# rgbhistogram2(Dec_image,"Decrgb1")
