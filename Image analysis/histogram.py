# """
# This module consist of three module redhistogram,bluehistogram,greenhitogram.All these modules does the histogram analysis of the
# red , blue and green color present in the images.For calculating the histogram of different color ,pillow image library
# is used .And to plot the data on graph matplotlib library has been used.
# """
#
# from PIL import Image
# from pylab import *
# import matplotlib.pylab as plt
# import matplotlib.pylab as plt2
#
#
# def rgbhistogram(loc,output):
#
#     im = array(Image.open(loc).convert('RGB'))
#
#     im2 = 255 - im  # invert image green
#     im3 = (100.0 / 255) * im + 100  # clamp to interval 100...200 red
#     im4 = 255.0 * (im / 255.0) ** 2  # squared blue
#     plt2.axis('equal')
#     plt2.axis('off')
#     plt2.figure()
#     plt2.hist(im2.flatten(), 128)
#     plt2.hist(im3.flatten(), 128)
#     plt2.hist(im4.flatten(), 128)
#     plt2.show()
#     plt2.savefig(output+".png")
#
#
# def rgbhistogram2(loc,output):
#     im = array(Image.open(loc).convert('RGB'))
#
#     im2 = 255 - im  # invert image green
#     im3 = (100.0 / 255) * im + 100  # clamp to interval 100...200 red
#     im4 = 255.0 * (im / 255.0) ** 2  # squared blue
#     plt2.axis('equal')
#     plt2.axis('on')
#     plt2.figure()
#     plt2.hist(im2.flatten(), 128)
#     plt2.hist(im3.flatten(), 128)
#     plt2.hist(im4.flatten(), 128)
#     plt2.show()
#     plt2.savefig(output+".png")
#
#
# def redhistogram(loc):
#     im = array(Image.open(loc).convert('RGB')) #Opening the image
#     im = (100.0 / 255) * im + 100  # clamp to interval 100...200 red
#     #Fecthing red pixels
#     axis('equal')
#     axis('off')
#     figure()
#     hist(im.flatten(), 128) #Designing the histogram
#
#     show()
#
#
# def greenhistogram(loc):
#     im = array(Image.open(loc).convert('RGB')) #Opening the image
#     im = 255 - im  # invert image green #Fecthing green pixels
#     axis('equal')
#     axis('off')
#     figure()
#     hist(im.flatten(), 128)#Designing the histogram
#     show()
#
#
# def bluehistogram(loc):
#     im = array(Image.open(loc).convert('RGB')) #Opening the image
#     im = 255.0 * (im / 255.0) ** 2  # squared blue #Fecthing blue pixels
#     axis('equal')
#     axis('off')
#     figure()
#     hist(im.flatten(), 128)#Designing the histogram
#     show()
#
#
# # im = array(Image.open('abc.png').convert('RGB'))
# #
# # im2 = 255 - im # invert image green
# #
# # im3 = (100.0/255) * im + 100 # clamp to interval 100...200 red
# #
# # im4 = 255.0 * (im/255.0)**2 # squared blue
# # # create a new figure
# # figure()
# # # don't use colors
# # #gray()
# # # show contours with origin upper left corner
# # #contour(im2, origin='image')
# #
# # axis('equal')
# # axis('off')
# # figure()
# # hist(im2.flatten(),128)
# # # hist(im3.flatten(),128)
# # # hist(im.flatten(),128)
# # # hist(im4.flatten(),128)
# # # #
# # show()
# rgbhistogram('C:/Users/DELL/Downloads/Imaage/Image-Encryption-and-Authentication/Pratyush.png','ab')
from skimage import io
import matplotlib.pyplot as plt
def histo_ski(loc):
    image = io.imread(loc)
    # image = io.imread('C:/Users/DELL/Downloads/Imaage/Image-Encryption-and-Authentication/Pratyush.png')
    _ = plt.hist(image.ravel(), bins = 256, color = 'yellow', )
    _ = plt.hist(image[:, :, 0].ravel(), bins = 256, color = 'red', alpha = 0.5)
    _ = plt.hist(image[:, :, 1].ravel(), bins = 256, color = 'Green', alpha = 0.5)
    _ = plt.hist(image[:, :, 2].ravel(), bins = 256, color = 'Blue', alpha = 0.5)
    _ = plt.xlabel('Intensity Value')
    _ = plt.ylabel('Count')
    _ = plt.legend(['Total', 'Red_Channel', 'Green_Channel', 'Blue_Channel'])
    plt.show()

import cv2
import numpy as np
from matplotlib import pyplot as plt

def histo_normal(loc):
    img = cv2.imread(loc, -1)
    # cv2.imshow('Lena',img)

    color = ('b','g','r')
    for channel,col in enumerate(color):
        histr = cv2.calcHist([img],[channel],None,[256],[0,256])
        plt.plot(histr,color = col)
        plt.xlim([0,256])
    plt.title('Histogram for color scale picture')
    plt.show()

# while True:
#     k = cv2.waitKey(0) & 0xFF
#     if k == 27: break             # ESC key to exit
# cv2.destroyAllWindows()
