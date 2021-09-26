# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.12.0
#   kernelspec:
#     display_name: Python 3
#     name: python3
# ---

# + [markdown] id="Qx_23B0c98NW" colab_type="text"
# # Image Encryption using Chaos Maps

# + [markdown] id="NgB8Y-WJ6gK4" colab_type="text"
# <b> What are chaos maps? </b>
# <br>
# Chaotic systems are a simple sub-type of nonlinear dynamical systems. They may contain very few interacting parts and these may follow very simple rules, but these systems all have a very sensitive dependence on their **initial conditions**. Despite their deterministic simplicity, over time these systems can produce totally unpredictable and wildly divergent (aka, chaotic) behavior.
#
# <br>
#
# **Why Chaos Maps for encryption?**
# <br>
# Traditional encrypting mechanisms AES and RSA exhibit some drawbacks
# and weakness in the encryption of digital images 
#   and high computing
#
# *   Large computational time for large images
# *   High computing power for large images
# Consequently, there might be better techniques for image encryption.
#
# A few chaos based algorithms provide a good combination of speed, high security complexity, low computational overheads 
# Moreover, **certain** chaos-based and other dynamical systems based algorithms have many important properties such as 
#
# *   sensitive dependence on initial parameters
# *   pseudorandom properties
# *   ergodicity
# *   non periodicity

# + id="F5r94mNt-FcU" colab_type="code" colab={}
from PIL import Image
import numpy as np
import os
from matplotlib.pyplot import imshow
import matplotlib.pyplot as plt
import cv2 
import random
from math import log


# + [markdown] id="mDgy7aO731rC" colab_type="text"
# ###Downloading images 
# Downloading sample images "lena.png" and "lena.png"

# + id="_i4-LRoJ5wzM" colab_type="code" outputId="bea26d17-5a7a-412e-a2f6-2847e39aef07" colab={"base_uri": "https://localhost:8080/", "height": 603}
# Downloading lena.png
# !wget https://drive.google.com/uc?id=1Djfm4PqE7Su4WqEdZKiGL-8HtrbVBuMm
# !mv uc?id=1Djfm4PqE7Su4WqEdZKiGL-8HtrbVBuMm lena.png

# Downloading lena.png
# !wget https://drive.google.com/uc?id=19xZhsjs_r0tLwtu_Wl5DB5rG26dhw069
# !mv uc?id=19xZhsjs_r0tLwtu_Wl5DB5rG26dhw069 lena.png

# + [markdown] id="9Yi38yus-eP5" colab_type="text"
# Function to get Image matrix from Pixel Access object

# + id="OInkzPl3-dTP" colab_type="code" colab={}
def getImageMatrix(imageName):
    im = Image.open(imageName) 
    pix = im.load()
    color = 1
    if type(pix[0,0]) == int:
      color = 0
    image_size = im.size 
    image_matrix = []
    for width in range(int(image_size[0])):
        row = []
        for height in range(int(image_size[1])):
                row.append((pix[width,height]))
        image_matrix.append(row)
    return image_matrix, image_size[0], image_size[1],color


# + id="M4TVLiGpymBx" colab_type="code" colab={}
def getImageMatrix_gray(imageName):
    im = Image.open(imageName).convert('LA')
    pix = im.load()
    image_size = im.size 
    image_matrix = []
    for width in range(int(image_size[0])):
        row = []
        for height in range(int(image_size[1])):
                row.append((pix[width,height]))
        image_matrix.append(row)
    return image_matrix, image_size[0], image_size[1]


# # + [markdown] id="CJlC3VgW-B2H" colab_type="text"
# # # Arnold Cat Map
# #
# # + [markdown] id="FOspal9c9HAN" colab_type="text"
# # Arnold's cat map is a chaotic map often used for pixel manipulation. It applies a tranform on the image that essentially shuffles the pixels by stretching anf folding thethe image. When an optimal number of iterations of the transformation is applied on the image, the resulting image becomes incomprehensible and hence encrypted.
# #
# # For this implementation
# # The transform applied on the image is:
# # R([x,y]) = [(x + y) mod n, (x + 2y) mod n]
# # where n is the dimensions of the image
# #
# # <br>
# #
# # When the transformation is repeated enough times, the original image will reappear.
# # The number of iterations 'n' at which the original image will reappear is given by these rules of thumb:
# # Here 'd' is the dimension of the square image:
# #
# # 1.   if d =  2.(5^i) for i >=1, n = 3*d
# # 2.   if d = (5^i) for i >=1, n = 2*d
# # 3.   if d = 6.(5^i) for i>=1, n = 2*d
# # 4.   else n <= 12*d / 7
# #
# # This periodicity forms the crux of the encryption process. Here key is the number of iterations of transformations initially applied to get the encrypted image. n - key is the number of rounds of transformations applied to get the decrypted image.
#
# #+ id="mGbPRosB-Yv_" colab_type="code" colab={}
# def ArnoldCatTransform(img, num):
#     rows, cols, ch = img.shape
#     n = rows
#     img_arnold = np.zeros([rows, cols, ch])
#     for x in range(0, rows):
#         for y in range(0, cols):
#             img_arnold[x][y] = img[(x+y)%n][(x+2*y)%n]
#     return img_arnold
#
#
# # + [markdown] id="wYGBg8XAFyLC" colab_type="text"
# # Arnold Cat Encryption
#
# # + id="xj7_AyMB3STZ" colab_type="code" colab={}
# def ArnoldCatEncryption(imageName, key):
#     img = cv2.imread(imageName)
#     for i in range (0,key):
#         img = ArnoldCatTransform(img, i)
#     cv2.imwrite(imageName.split('.')[0] + "_ArnoldcatEnc.png", img)
#     return img
#
#
# # + [markdown] id="O_GFV63YF5YM" colab_type="text"
# # Arnold Cat Decryption
#
# # + id="sRJfx4jm32Z2" colab_type="code" colab={}
# def ArnoldCatDecryption(imageName, key):
#     img = cv2.imread(imageName)
#     rows, cols, ch = img.shape
#     dimension = rows
#     decrypt_it = dimension
#     if (dimension%2==0) and 5**int(round(log(dimension/2,5))) == int(dimension/2):
#         decrypt_it = 3*dimension
#     elif 5**int(round(log(dimension,5))) == int(dimension):
#         decrypt_it = 2*dimension
#     elif (dimension%6==0) and  5**int(round(log(dimension/6,5))) == int(dimension/6):
#         decrypt_it = 2*dimension
#     else:
#         decrypt_it = int(12*dimension/7)
#     for i in range(key,decrypt_it):
#         img = ArnoldCatTransform(img, i)
#     cv2.imwrite(imageName.split('_')[0] + "_ArnoldcatDec.png",img)
#     return img
#
#
# # + id="FacBvOj26MSf" colab_type="code" colab={}
# image = "lena"
# ext = ".png"
# key = 20
#
# # + id="AFOv1GEJ7H2n" colab_type="code" outputId="40b86a44-3e99-442d-9e7e-9d7e79df459f" colab={"base_uri": "https://localhost:8080/", "height": 267}
# img = cv2.imread(image + ext)
# imshow(img)
#
# # + id="dEEaCUCb4Ns4" colab_type="code" outputId="fb1af4ba-69be-4f7f-d80d-0a62dc8990f1" colab={"base_uri": "https://localhost:8080/", "height": 267}
# ArnoldCatEncryptionIm = ArnoldCatEncryption(image + ext, key)
# imshow(ArnoldCatEncryptionIm)
#
# # + id="a1jyAbjR3xOG" colab_type="code" outputId="02e9d474-c8cd-4ab9-cde8-ac444d4d2c11" colab={"base_uri": "https://localhost:8080/", "height": 267}
# ArnoldCatDecryptionIm = ArnoldCatDecryption(image + "_ArnoldcatEnc.png", key)
# imshow(ArnoldCatDecryptionIm)
#
# # + [markdown] id="FCoPmQDPCg4f" colab_type="text"
# # ## Histogram Analysis
# #
#
# # + [markdown] id="5WoVngyhINA-" colab_type="text"
# # The ciphertext image histogram analysis is one of the most straight-forward methods ofillustrating the image encryption quality. A good image encryption method tends to encrypt a plaintext image to a random incomprehensible form. Thus a good image encyption technique generates a cipher image that has a uniformly distributed intensity histogram.
#
# # + [markdown] id="pcdZRS4wncyD" colab_type="text"
# # ### Original Image
#
# # + id="zX0QcIdxCnBn" colab_type="code" outputId="9f386107-5e3c-42e2-a13d-1e5638362252" colab={"base_uri": "https://localhost:8080/", "height": 666}
# image = "lena"
# ext = ".png"
# img = cv2.imread(image + ext,1)
# pil_im = Image.open(image + ext, 'r')
# imshow(np.asarray(pil_im))
#
# plt.figure(figsize=(14,6))
# histogram_blue = cv2.calcHist([img],[0],None,[256],[0,256])
# plt.plot(histogram_blue, color='blue')
# histogram_green = cv2.calcHist([img],[1],None,[256],[0,256])
# plt.plot(histogram_green, color='green')
# histogram_red = cv2.calcHist([img],[2],None,[256],[0,256])
# plt.plot(histogram_red, color='red')
# plt.title('Intensity Histogram - Original Image', fontsize=20)
# plt.xlabel('pixel values', fontsize=16)
# plt.ylabel('pixel count', fontsize=16)
# plt.show()
#
# # + [markdown] id="D-4qtmj7nX8r" colab_type="text"
# # ### Encrypted Image
#
# # + id="K68n3FXBCuOW" colab_type="code" outputId="3a49d48d-8cbd-40de-f9bc-003e2ec53f91" colab={"base_uri": "https://localhost:8080/", "height": 666}
# image = "lena_ArnoldcatEnc"
# ext = ".png"
# img = cv2.imread(image + ext,1)
# pil_im = Image.open(image + ext, 'r')
# imshow(np.asarray(pil_im))
#
# plt.figure(figsize=(14,6))
# histogram_blue = cv2.calcHist([img],[0],None,[256],[0,256])
# plt.plot(histogram_blue, color='blue')
# histogram_green = cv2.calcHist([img],[1],None,[256],[0,256])
# plt.plot(histogram_green, color='green')
# histogram_red = cv2.calcHist([img],[2],None,[256],[0,256])
# plt.plot(histogram_red, color='red')
# plt.title('Intensity Histogram - Arnold Cat Encrypted', fontsize=20)
# plt.xlabel('pixel values', fontsize=16)
# plt.ylabel('pixel count', fontsize=16)
# plt.show()
#
# # + [markdown] id="xfQO_SN0Co_j" colab_type="text"
# # ## Adjacent Pixel Auto-Correlation
# # Since images exhibit high information redundancy, it is desirable to have an encryption algorithm that breaks this redundancy. Thus as a metric of encryption performance we find the correlation between adjacent pixels in a direction (Horizontal, Vertical or Diagonal). We have considered the Horizontal direction.
# #
# # 1024 random pixels are picked up from the image and its correlation between it's rightmost neighbour is found and plotted. For a good algorithm, the correlation plot should appear random with no discernable pattern
#
# # + id="Lm0D7NvxDNvL" colab_type="code" outputId="be558035-1b28-40d9-e2fa-76af34f026c7" colab={"base_uri": "https://localhost:8080/", "height": 286}
# image = "lena"
# ext = ".png"
# img = Image.open(image+ext).convert('LA')
# pil_im = Image.open(image + ext, 'r')
# imshow(np.asarray(pil_im))
#
# # + id="NyxUGGSwDPmr" colab_type="code" outputId="c3ae6d2a-6a1f-4222-cd30-66161a5556a1" colab={"base_uri": "https://localhost:8080/", "height": 504}
# image = "lena"
# ext = ".png"
# ImageMatrix,image_size = getImageMatrix_gray(image+ext)
# samples_x = []
# samples_y = []
# for i in range(1024):
#   x = random.randint(0,image_size-2)
#   y = random.randint(0,image_size-1)
#   samples_x.append(ImageMatrix[x][y])
#   samples_y.append(ImageMatrix[x+1][y])
# plt.figure(figsize=(10,8))
# plt.scatter(samples_x,samples_y,s=2)
# plt.title('Adjacent Pixel Autocorrelation - Original Image', fontsize=20)
# plt.show()
#
# # + id="DcPgutMWGXkV" colab_type="code" outputId="91d8f6cb-95f3-4ae6-dc14-7b4e1c4d7322" colab={"base_uri": "https://localhost:8080/", "height": 521}
# image = "lena_ArnoldcatEnc"
# ext = ".png"
# ImageMatrix,image_size = getImageMatrix_gray(image+ext)
# samples_x = []
# samples_y = []
# print(image_size)
# for i in range(1024):
#   x = random.randint(0,image_size-2)
#   y = random.randint(0,image_size-1)
#   samples_x.append(ImageMatrix[x][y])
#   samples_y.append(ImageMatrix[x+1][y])
# plt.figure(figsize=(10,8))
# plt.scatter(samples_x,samples_y,s=2)
# plt.title('Adjacent Pixel Autocorrelation - Arnold Cat Encryption on Image', fontsize=20)
# plt.show()


# # + [markdown] id="JoBDR3zhA0dA" colab_type="text"
# # # Henon Map
#
# # + [markdown] id="YOxTbe3mLMNn" colab_type="text"
# #
# # Given initial conditions (x0,y0), a henon map is given by the following equations:
# # <br>
# #
# # (Xn+1) = (Yn) + 1 − a.(Xn)
# #
# # (Yn+1) = b * (Xn)
# #
# # Classical Henon map have values of a = 1.4 and b = 0.3. For the classical values the Henon map is chaotic. For other values of a and b the map may be chaotic, intermittent, or converge to a periodic orbit.
#
# # + id="ugs89j-XG-pu" colab_type="code" colab={}
# def dec(bitSequence):
#     decimal = 0
#     for bit in bitSequence:
#         decimal = decimal * 2 + int(bit)
#     return decimal
#
#
# # + id="CtFIjQdzBX95" colab_type="code" colab={}
# def genHenonMap(dimension, key):
#     x = key[0]
#     y = key[1]
#     sequenceSize = dimension * dimension * 8 #Total Number of bitSequence produced
#     bitSequence = []    #Each bitSequence contains 8 bits
#     byteArray = []      #Each byteArray contains m( i.e 512 in this case) bitSequence
#     TImageMatrix = []   #Each TImageMatrix contains m*n byteArray( i.e 512 byteArray in this case)
#     for i in range(sequenceSize):
#         xN = y + 1 - 1.4 * x**2
#         yN = 0.3 * x
#
#         x = xN
#         y = yN
#
#         if xN <= 0.4:
#             bit = 0
#         else:
#             bit = 1
#
#         try:
#             bitSequence.append(bit)
#         except:
#             bitSequence = [bit]
#
#         if i % 8 == 7:
#             decimal = dec(bitSequence)
#             try:
#                 byteArray.append(decimal)
#             except:
#                 byteArray = [decimal]
#             bitSequence = []
#
#         byteArraySize = dimension*8
#         if i % byteArraySize == byteArraySize-1:
#             try:
#                 TImageMatrix.append(byteArray)
#             except:
#                 TImageMatrix = [byteArray]
#             byteArray = []
#     return TImageMatrix
#
#
# # + [markdown] id="GXqVyy7KCbKI" colab_type="text"
# # ## Henon Encryption
# #
#
# # + id="N6UNDcKnCGAD" colab_type="code" colab={}
# def HenonEncryption(imageName,key):
#     imageMatrix, dimensionX, dimensionY, color = getImageMatrix(imageName)
#     transformationMatrix = genHenonMap(dimension, key)
#     resultantMatrix = []
#     for i in range(dimensionX):
#         row = []
#         for j in range(dimensionY):
#             try:
#                 if color:
#                     row.append(tuple([transformationMatrix[i][j] ^ x for x in imageMatrix[i][j]]))
#                 else:
#                     row.append(transformationMatrix[i][j] ^ imageMatrix[i][j])
#             except:
#                 if color:
#                     row = [tuple([transformationMatrix[i][j] ^ x for x in imageMatrix[i][j]])]
#                 else :
#                     row = [transformationMatrix[i][j] ^ x for x in imageMatrix[i][j]]
#         try:
#             resultantMatrix.append(row)
#         except:
#             resultantMatrix = [row]
#     if color:
#       im = Image.new("RGB", (dimensionX, dimensionY))
#     else:
#       im = Image.new("L", (dimensionX, dimensionY)) # L is for Black and white pixels
#
#     pix = im.load()
#     for x in range(dimensionX):
#         for y in range(dimensionY):
#             pix[x, y] = resultantMatrix[x][y]
#     im.save(imageName.split('.')[0] + "_HenonEnc.png", "PNG")
#
#
# # + [markdown] id="HQZjz2UuE56r" colab_type="text"
# # ## Henon Decryption
#
# # + id="311mB_DOEtWZ" colab_type="code" colab={}
# def HenonDecryption(imageNameEnc, key):
#     imageMatrix, dimensionX, dimensionY, color = getImageMatrix(imageNameEnc)
#     transformationMatrix = genHenonMap(dimension, key)
#     pil_im = Image.open(imageNameEnc, 'r')
#     imshow(np.asarray(pil_im))
#     henonDecryptedImage = []
#     for i in range(dimensionX):
#         row = []
#         for j in range(dimensionY):
#             try:
#                 if color:
#                     row.append(tuple([transformationMatrix[i][j] ^ x for x in imageMatrix[i][j]]))
#                 else:
#                     row.append(transformationMatrix[i][j] ^ imageMatrix[i][j])
#             except:
#                 if color:
#                     row = [tuple([transformationMatrix[i][j] ^ x for x in imageMatrix[i][j]])]
#                 else :
#                     row = [transformationMatrix[i][j] ^ x for x in imageMatrix[i][j]]
#         try:
#             henonDecryptedImage.append(row)
#         except:
#             henonDecryptedImage = [row]
#     if color:
#         im = Image.new("RGB", (dimensionX, dimensionY))
#     else:
#         im = Image.new("L", (dimensionX, dimensionY)) # L is for Black and white pixels
#
#     pix = im.load()
#     for x in range(dimensionX):
#         for y in range(dimensionY):
#             pix[x, y] = henonDecryptedImage[x][y]
#     im.save(imageNameEnc.split('_')[0] + "_HenonDec.png", "PNG")
#
#
# # + [markdown] id="wmA42C8OGVNv" colab_type="text"
# # ## Comparision
#
# # + id="se-IL68rhrgW" colab_type="code" colab={}
# image = "lena"
# ext = ".png"
# key = (0.1,0.1)
#
# # + [markdown] id="h6AIWqkyNVQI" colab_type="text"
# # ### Original Image
#
# # + id="qWcGLH2LNU3W" colab_type="code" outputId="6ff9a8ed-7a4a-4d5e-9253-075f13a2382b" colab={"base_uri": "https://localhost:8080/", "height": 286}
# pil_im = Image.open(image + ext, 'r')
# imshow(np.asarray(pil_im))
#
# # + [markdown] id="_iPFf7CDNdfm" colab_type="text"
# # ### Encryption
#
# # + id="bLrEsECINO6R" colab_type="code" outputId="5539759f-3704-46a6-890c-1a5f908d2174" colab={"base_uri": "https://localhost:8080/", "height": 286}
# HenonEncryption(image + ext, key)
# im = Image.open(image + "_HenonEnc.png", 'r')
# imshow(np.asarray(im))
#
# # + [markdown] id="pZ8DB0q9NkOv" colab_type="text"
# # ### Decryption
#
# # + id="8-U_w-UANvB7" colab_type="code" outputId="9faf35c5-916f-47a3-dcdb-b94aa6adf608" colab={"base_uri": "https://localhost:8080/", "height": 286}
# HenonDecryption(image + "_HenonEnc.png", key)
# im = Image.open(image + "_HenonDec.png", 'r')
# imshow(np.asarray(im))
#
# # + id="OTrh4qeIjBvd" colab_type="code" colab={}
# image = "lena"
# ext = ".png"
# key = (0.1, 0.1)
#
# # + [markdown] colab_type="text" id="Q_JwnBejjJGi"
# # ### Original Image
#
# # + id="gDfcqZK-hVdi" colab_type="code" outputId="b4dd7490-a46c-4966-8a1c-f22766c8a749" colab={"base_uri": "https://localhost:8080/", "height": 286}
# pil_im = Image.open(image + ext, 'r')
# imshow(np.asarray(pil_im), cmap='gray')
#
# # + [markdown] id="HesnTGq5jQ2A" colab_type="text"
# # ### Encrypted Image
#
# # + id="-BXicXoQi3QD" colab_type="code" outputId="a6d50ba0-e060-4885-9da0-e6297f8340f4" colab={"base_uri": "https://localhost:8080/", "height": 286}
# HenonEncryption(image + ext, key)
# im = Image.open(image + "_HenonEnc.png", 'r')
# imshow(np.asarray(im), cmap='gray')
#
# # + [markdown] id="cZoaO09hjVyI" colab_type="text"
# # ### Decrypted Image
#
# # + id="PfOYPFjKi7T8" colab_type="code" outputId="3dcde1b4-aeeb-49d2-9794-612b683cd014" colab={"base_uri": "https://localhost:8080/", "height": 286}
# HenonDecryption(image + "_HenonEnc.png", key)
# im = Image.open(image + "_HenonDec.png", 'r')
# imshow(np.asarray(im), cmap='gray')
#
# # + [markdown] id="R3fbz7nvl6uh" colab_type="text"
# # ## Histogram
# #
#
# # + [markdown] id="fPNLFpp0nPUA" colab_type="text"
# # ### Original Image
#
# # + id="9iHsW2D_mD4V" colab_type="code" outputId="8f1b30e7-5865-43fc-9cd3-995055e9c3fa" colab={"base_uri": "https://localhost:8080/", "height": 666}
# image = "lena"
# ext = ".png"
# img = cv2.imread(image + ext,1)
# pil_im = Image.open(image + ext, 'r')
# imshow(np.asarray(pil_im))
# plt.figure(figsize=(14,6))
#
# histogram_blue = cv2.calcHist([img],[0],None,[256],[0,256])
# plt.plot(histogram_blue, color='blue')
# histogram_green = cv2.calcHist([img],[1],None,[256],[0,256])
# plt.plot(histogram_green, color='green')
# histogram_red = cv2.calcHist([img],[2],None,[256],[0,256])
# plt.plot(histogram_red, color='red')
# plt.title('Intensity Histogram - Original Image', fontsize=20)
# plt.xlabel('pixel values', fontsize=16)
# plt.ylabel('pixel count', fontsize=16)
# plt.show()
#
# # + [markdown] id="bFJ30Bl1nMFP" colab_type="text"
# # ### Encrypted Image
#
# # + id="i8axTPE9phNG" colab_type="code" outputId="c9f24dbd-bc18-4b16-a860-09dc4e78033d" colab={"base_uri": "https://localhost:8080/", "height": 666}
# image = "lena_HenonEnc"
# ext = ".png"
# img = cv2.imread(image + ext,1)
# pil_im = Image.open(image + ext, 'r')
# imshow(np.asarray(pil_im))
# plt.figure(figsize=(14,6))
#
# histogram_blue = cv2.calcHist([img],[0],None,[256],[0,256])
# plt.plot(histogram_blue, color='blue')
# histogram_green = cv2.calcHist([img],[1],None,[256],[0,256])
# plt.plot(histogram_green, color='green')
# histogram_red = cv2.calcHist([img],[2],None,[256],[0,256])
# plt.plot(histogram_red, color='red')
# plt.title('Intensity Histogram - Henon Map Encrypted Image', fontsize=20)
# plt.xlabel('pixel values', fontsize=16)
# plt.ylabel('pixel count', fontsize=16)
# plt.show()
#
# # + [markdown] id="_mjLNgRBp3iG" colab_type="text"
# # ## Adjacent Pixel AutoCorrelation
#
# # + id="hDCCJEjUyP5V" colab_type="code" outputId="f3308b46-c91a-4b2c-9fd0-f4f99796f755" colab={"base_uri": "https://localhost:8080/", "height": 286}
# image = "lena"
# ext = ".png"
# img = Image.open(image+ext).convert('LA')
# pil_im = Image.open(image + ext, 'r')
# imshow(np.asarray(pil_im))
#
# # + id="k578jDaoueIo" colab_type="code" outputId="5f74c4da-4f25-41f7-e67d-67d40d88ebb0" colab={"base_uri": "https://localhost:8080/", "height": 504}
# image = "lena"
# ext = ".png"
# ImageMatrix,image_size = getImageMatrix_gray(image+ext)
# samples_x = []
# samples_y = []
# for i in range(1024):
#   x = random.randint(0,image_size-2)
#   y = random.randint(0,image_size-1)
#   samples_x.append(ImageMatrix[x][y])
#   samples_y.append(ImageMatrix[x+1][y])
# plt.figure(figsize=(10,8))
# plt.scatter(samples_x,samples_y,s=2)
# plt.title('Adjacent Pixel Autocorrelation - Original Image', fontsize=20)
# plt.show()
#
# # + id="B-poQyxXxWiW" colab_type="code" outputId="49c054f4-f5ae-43f7-e36d-5037d3ff9402" colab={"base_uri": "https://localhost:8080/", "height": 521}
# image = "lena_HenonEnc"
# ext = ".png"
# ImageMatrix,image_size = getImageMatrix_gray(image+ext)
# samples_x = []
# samples_y = []
# print(image_size)
# for i in range(1024):
#   x = random.randint(0,image_size-2)
#   y = random.randint(0,image_size-1)
#   samples_x.append(ImageMatrix[x][y])
#   samples_y.append(ImageMatrix[x+1][y])
# plt.figure(figsize=(10,8))
# plt.scatter(samples_x,samples_y,s=2)
# plt.title('Adjacent Pixel Autocorrelation - Henon Encryption on Image', fontsize=20)
# plt.show()


# + [markdown] id="PY_imOTZg8oo" colab_type="text"
# # Logistic Chaos Maps with key mixing

# + [markdown] id="ZzdwV5gkSMbe" colab_type="text"
# The logistic map instead uses a nonlinear difference equation to look at discrete time steps. It’s called the logistic map because it maps the population value at any time step to its value at the next time step.
#
# The basic formula is:
# (X_t+1) = r.X_t.(1 - X_t)
#
# For this implementation we have included key mixing. The initial values of the chaos map is recalculated after every pixel encryption based on the previous encryption value as well as the key value.

# + id="8rVuVnWg8sMG" colab_type="code" colab={}
def LogisticEncryption(imageName, key):
    N = 256
    key_list = [ord(x) for x in key]
    G = [key_list[0:4] ,key_list[4:8], key_list[8:12]]
    g = []
    R = 1
    for i in range(1,4):
        s = 0
        for j in range(1,5):
            s += G[i-1][j-1] * (10**(-j))
        g.append(s)
        R = (R*s) % 1

    L = (R + key_list[12]/256) % 1
    S_x = round(((g[0]+g[1]+g[2])*(10**4) + L *(10**4)) % 256)
    V1 = sum(key_list)
    V2 = key_list[0]
    for i in range(1,13):
        V2 = V2 ^ key_list[i]
    V = V2/V1

    L_y = (V+key_list[12]/256) % 1
    S_y = round((V+V2+L_y*10**4) % 256)
    C1_0 = S_x
    C2_0 = S_y
    C = round((L*L_y*10**4) % 256)
    C_r = round((L*L_y*10**4) % 256)
    C_g = round((L*L_y*10**4) % 256)
    C_b = round((L*L_y*10**4) % 256)
    x = 4*(S_x)*(1-S_x)
    y = 4*(S_y)*(1-S_y)
    
    imageMatrix,dimensionX, dimensionY, color = getImageMatrix(imageName)
    LogisticEncryptionIm = []
    for i in range(dimensionX):
        row = []
        for j in range(dimensionY):
            while x <0.8 and x > 0.2 :
                x = 4*x*(1-x)
            while y <0.8 and y > 0.2 :
                y = 4*y*(1-y)
            x_round = round((x*(10**4))%256)
            y_round = round((y*(10**4))%256)
            C1 = x_round ^ ((key_list[0]+x_round) % N) ^ ((C1_0 + key_list[1])%N)
            C2 = x_round ^ ((key_list[2]+y_round) % N) ^ ((C2_0 + key_list[3])%N) 
            if color:
              C_r =((key_list[4]+C1) % N) ^ ((key_list[5]+C2) % N) ^ ((key_list[6]+imageMatrix[i][j][0]) % N) ^ ((C_r + key_list[7]) % N)
              C_g =((key_list[4]+C1) % N) ^ ((key_list[5]+C2) % N) ^ ((key_list[6]+imageMatrix[i][j][1]) % N) ^ ((C_g + key_list[7]) % N)
              C_b =((key_list[4]+C1) % N) ^ ((key_list[5]+C2) % N) ^ ((key_list[6]+imageMatrix[i][j][2]) % N) ^ ((C_b + key_list[7]) % N)
              row.append((C_r,C_g,C_b))
              C = C_r

            else:
              C = ((key_list[4]+C1) % N) ^ ((key_list[5]+C2) % N) ^ ((key_list[6]+imageMatrix[i][j]) % N) ^ ((C + key_list[7]) % N)
              row.append(C)

            x = (x + C/256 + key_list[8]/256 + key_list[9]/256) % 1
            y = (x + C/256 + key_list[8]/256 + key_list[9]/256) % 1
            for ki in range(12):
                key_list[ki] = (key_list[ki] + key_list[12]) % 256
                key_list[12] = key_list[12] ^ key_list[ki]
        LogisticEncryptionIm.append(row)

    im = Image.new("L", (dimensionX, dimensionY))
    if color:
        im = Image.new("RGB", (dimensionX, dimensionY))
    else: 
        im = Image.new("L", (dimensionX, dimensionY)) # L is for Black and white pixels
      
    pix = im.load()
    for x in range(dimensionX):
        for y in range(dimensionY):
            pix[x, y] = LogisticEncryptionIm[x][y]
    im.save(imageName.split('.')[0] + "_LogisticEnc.png", "PNG")


# + id="2t3ClAaAhCqe" colab_type="code" colab={}
def LogisticDecryption(imageName, key):
    N = 256
    key_list = [ord(x) for x in key]

    G = [key_list[0:4] ,key_list[4:8], key_list[8:12]]
    g = []
    R = 1
    for i in range(1,4):
        s = 0
        for j in range(1,5):
            s += G[i-1][j-1] * (10**(-j))
        g.append(s)
        R = (R*s) % 1
    
    L_x = (R + key_list[12]/256) % 1
    S_x = round(((g[0]+g[1]+g[2])*(10**4) + L_x *(10**4)) % 256)
    V1 = sum(key_list)
    V2 = key_list[0]
    for i in range(1,13):
        V2 = V2 ^ key_list[i]
    V = V2/V1

    L_y = (V+key_list[12]/256) % 1
    S_y = round((V+V2+L_y*10**4) % 256)
    C1_0 = S_x
    C2_0 = S_y
    
    C = round((L_x*L_y*10**4) % 256)
    I_prev = C
    I_prev_r = C
    I_prev_g = C
    I_prev_b = C
    I = C
    I_r = C
    I_g = C
    I_b = C
    x_prev = 4*(S_x)*(1-S_x)
    y_prev = 4*(L_x)*(1-S_y)
    x = x_prev
    y = y_prev
    imageMatrix,dimensionX, dimensionY, color = getImageMatrix(imageName)

    henonDecryptedImage = []
    for i in range(dimensionX):
        row = []
        for j in range(dimensionY):
            while x <0.8 and x > 0.2 :
                x = 4*x*(1-x)
            while y <0.8 and y > 0.2 :
                y = 4*y*(1-y)
            x_round = round((x*(10**4))%256)
            y_round = round((y*(10**4))%256)
            C1 = x_round ^ ((key_list[0]+x_round) % N) ^ ((C1_0 + key_list[1])%N)
            C2 = x_round ^ ((key_list[2]+y_round) % N) ^ ((C2_0 + key_list[3])%N) 
            if color:
                I_r = ((((key_list[4]+C1) % N) ^ ((key_list[5]+C2) % N) ^ ((I_prev_r + key_list[7]) % N) ^ imageMatrix[i][j][0]) + N-key_list[6])%N
                I_g = ((((key_list[4]+C1) % N) ^ ((key_list[5]+C2) % N) ^ ((I_prev_g + key_list[7]) % N) ^ imageMatrix[i][j][1]) + N-key_list[6])%N
                I_b = ((((key_list[4]+C1) % N) ^ ((key_list[5]+C2) % N) ^ ((I_prev_b + key_list[7]) % N) ^ imageMatrix[i][j][2]) + N-key_list[6])%N
                I_prev_r = imageMatrix[i][j][0]
                I_prev_g = imageMatrix[i][j][1]
                I_prev_b = imageMatrix[i][j][2]
                row.append((I_r,I_g,I_b))
                x = (x +  imageMatrix[i][j][0]/256 + key_list[8]/256 + key_list[9]/256) % 1
                y = (x +  imageMatrix[i][j][0]/256 + key_list[8]/256 + key_list[9]/256) % 1  
            else:
                I = ((((key_list[4]+C1) % N) ^ ((key_list[5]+C2) % N) ^ ((I_prev+key_list[7]) % N) ^ imageMatrix[i][j]) + N-key_list[6])%N
                I_prev = imageMatrix[i][j]
                row.append(I)
                x = (x +  imageMatrix[i][j]/256 + key_list[8]/256 + key_list[9]/256) % 1
                y = (x +  imageMatrix[i][j]/256 + key_list[8]/256 + key_list[9]/256) % 1
            for ki in range(12):
                key_list[ki] = (key_list[ki] + key_list[12]) % 256
                key_list[12] = key_list[12] ^ key_list[ki]
        henonDecryptedImage.append(row)
    if color:
        im = Image.new("RGB", (dimensionX, dimensionY))
    else: 
        im = Image.new("L", (dimensionX, dimensionY)) # L is for Black and white pixels
    pix = im.load()
    for x in range(dimensionX):
        for y in range(dimensionY):
            pix[x, y] = henonDecryptedImage[x][y]
    im.save(imageName.split('_')[0] + "_LogisticDec.png", "PNG")


# + [markdown] id="dqfg4Rx8mA7R" colab_type="text"
# ### Original Image

# + id="2WeULIaGmIiI" colab_type="code" colab={}
image = "lena"
ext = ".png"

# + id="WnCPbUJbl5WA" colab_type="code" outputId="570d9142-ea28-45e8-c517-1ec55f28c125" colab={"base_uri": "https://localhost:8080/", "height": 286}
pil_im = Image.open(image + ext, 'r')
imshow(np.asarray(pil_im), cmap='gray')

# + [markdown] id="gX09vAchmHB0" colab_type="text"
# ### Encryption

# + id="glpBumQBhMNY" colab_type="code" outputId="318af66b-697b-460d-9d8a-4c00ac8e6843" colab={"base_uri": "https://localhost:8080/", "height": 286}
# Note: As it is implemented, the funciton will assume a 13 character long encryption key.
#       One can tweak this limitation by changing the "key_list" structure at the Logistic functions.
LogisticEncryption("lena.png", "abcdefghijklm")
im = Image.open("lena_LogisticEnc.png", 'r')
imshow(np.asarray(im), cmap='gray')

# + [markdown] id="wu4LgZS2ma5x" colab_type="text"
# ### Decryption

# + id="bsBa0xtikO15" colab_type="code" outputId="04c4ecb5-44e3-4542-d123-5e8400652751" colab={"base_uri": "https://localhost:8080/", "height": 286}
LogisticDecryption("lena_LogisticEnc.png","abcdefghijklm")
im = Image.open("lena_LogisticDec.png", 'r')
imshow(np.asarray(im),cmap='gray')

# + [markdown] id="h4QRQeu6mWcO" colab_type="text"
# ### Original Image

# + id="VtAVT_DpjJx0" colab_type="code" colab={}
image = "lena"
ext = ".png"
key = "abcdefghijklm"

# + id="0pXvL8Rzme7R" colab_type="code" outputId="ea30dd24-ea1a-4049-f1ea-c3ffc7c0a8be" colab={"base_uri": "https://localhost:8080/", "height": 286}
pil_im = Image.open(image + ext, 'r')
imshow(np.asarray(pil_im), cmap='gray')

# + [markdown] id="nMJ3KZ3Ymj77" colab_type="text"
# ### Encryption

# + id="QL95IslTjP3y" colab_type="code" outputId="a1441ef5-36af-4f06-beea-dbb2d1a740f3" colab={"base_uri": "https://localhost:8080/", "height": 286}
LogisticEncryption(image + ext, key)
im = Image.open(image + "_LogisticEnc.png", 'r')
print("Encrypted")
imshow(np.asarray(im))
plt.show()
# + [markdown] id="c3sKrU0Kmm2c" colab_type="text"
# ### Decryption

# + id="5EXMdcJ9j4fj" colab_type="code" outputId="3dfa7c3a-983d-4641-c67f-402c321136bf" colab={"base_uri": "https://localhost:8080/", "height": 286}
LogisticDecryption(image + "_LogisticEnc.png", key)
im = Image.open(image + "_LogisticDec.png", 'r')
print("Dencrypted")
imshow(np.asarray(im))
plt.show()
# + [markdown] id="ls3zjCpbm1JX" colab_type="text"
# ## Histogram Analysis

# + [markdown] id="YWNxxgiim5ws" colab_type="text"
# ### Original Image

# + id="MXzFX4V9m357" colab_type="code" outputId="2ecec85e-2342-4bc7-9ae9-43ea20c6da3f" colab={"base_uri": "https://localhost:8080/", "height": 666}
image = "lena"
ext = ".png"
img = cv2.imread(image + ext,1)
pil_im = Image.open(image + ext, 'r')
imshow(np.asarray(pil_im))
plt.figure(figsize=(14,6))

histogram_blue = cv2.calcHist([img],[0],None,[256],[0,256])
plt.plot(histogram_blue, color='blue')
histogram_green = cv2.calcHist([img],[1],None,[256],[0,256])
plt.plot(histogram_green, color='green')
histogram_red = cv2.calcHist([img],[2],None,[256],[0,256])
plt.plot(histogram_red, color='red')
plt.title('Intensity Histogram - Original Image', fontsize=20)
plt.xlabel('pixel values', fontsize=16)
plt.ylabel('pixel count', fontsize=16)
plt.show()

# + [markdown] id="tVw_8jL6m8CD" colab_type="text"
# ### Encrypted Image

# + id="JuyhyffjnEvw" colab_type="code" outputId="d3694665-32a7-4f75-d2f2-92540f753bab" colab={"base_uri": "https://localhost:8080/", "height": 666}
image = "lena_LogisticEnc"
ext = ".png"
img = cv2.imread(image + ext,1)
pil_im = Image.open(image + ext, 'r')
imshow(np.asarray(pil_im))
plt.figure(figsize=(14,6))

histogram_blue = cv2.calcHist([img],[0],None,[256],[0,256])
plt.plot(histogram_blue, color='blue')
histogram_green = cv2.calcHist([img],[1],None,[256],[0,256])
plt.plot(histogram_green, color='green')
histogram_red = cv2.calcHist([img],[2],None,[256],[0,256])
plt.plot(histogram_red, color='red')
plt.title('Intensity Histogram - Logistic Encrypted Image', fontsize=20)
plt.xlabel('pixel values', fontsize=16)
plt.ylabel('pixel count', fontsize=16)
plt.show()

# + [markdown] id="XT5WHcn8nj29" colab_type="text"
# ## Adjacent Pixel Auto-Correlation

# + [markdown] id="tWTAiqIanqyL" colab_type="text"
# ### Original Image

# + id="ovowJ6lGnqQW" colab_type="code" outputId="3929caa8-d528-4bde-f1f3-fc4c3227630e" colab={"base_uri": "https://localhost:8080/", "height": 286}
# image = "lena"
# ext = ".png"
# img = Image.open(image+ext).convert('LA')
# pil_im = Image.open(image + ext, 'r')
# imshow(np.asarray(pil_im))
#
# # + id="c0Pv3au0nyR_" colab_type="code" outputId="65d37bd6-7591-4c54-872c-81f515ccaac6" colab={"base_uri": "https://localhost:8080/", "height": 504}
# image = "lena"
# ext = ".png"
# ImageMatrix,image_size = getImageMatrix_gray(image+ext)
# samples_x = []
# samples_y = []
# for i in range(1024):
#   x = random.randint(0,image_size-2)
#   y = random.randint(0,image_size-1)
#   samples_x.append(ImageMatrix[x][y])
#   samples_y.append(ImageMatrix[x+1][y])
# plt.figure(figsize=(10,8))
# plt.scatter(samples_x,samples_y,s=2)
# plt.title('Adjacent Pixel Autocorrelation - Original Image', fontsize=20)
# plt.show()
#
# # + [markdown] id="NH3YftcQnzM7" colab_type="text"
# # ### Encrypted Image
#
# # + id="DBdSpCrxn4yQ" colab_type="code" outputId="1666a8f8-ac9b-4460-d9b8-1d37a3435b5e" colab={"base_uri": "https://localhost:8080/", "height": 521}
# image = "lena_LogisticEnc"
# ext = ".png"
# ImageMatrix,image_size = getImageMatrix_gray(image+ext)
# samples_x = []
# samples_y = []
# print(image_size)
# for i in range(1024):
#   x = random.randint(0,image_size-2)
#   y = random.randint(0,image_size-1)
#   samples_x.append(ImageMatrix[x][y])
#   samples_y.append(ImageMatrix[x+1][y])
# plt.figure(figsize=(10,8))
# plt.scatter(samples_x,samples_y,s=2)
# plt.title('Adjacent Pixel Autocorrelation - Logistic Encryption on Image', fontsize=20)
# plt.show()
#
# # + [markdown] id="d0kKvIJixJ9_" colab_type="text"
# # # Key Sensitivity
#
# # + [markdown] id="j050xG2TxMdV" colab_type="text"
# # ### Original Image
#
# # + id="ebLOypBRxTTk" colab_type="code" outputId="88529ef6-20e6-4848-d1fd-ea7bd1a37513" colab={"base_uri": "https://localhost:8080/", "height": 286}
# image = "lena"
# ext = ".png"
# img = cv2.imread(image + ext,1)
# pil_im = Image.open(image + ext, 'r')
# imshow(np.asarray(pil_im))
#
# # + [markdown] id="zA2nVf1exUpq" colab_type="text"
# # ## Arnold Cat
#
# # + [markdown] id="LrvmLwuTxxnk" colab_type="text"
# # Encrypt with key = 20
#
# # + id="7n5AA0hDxW5a" colab_type="code" outputId="04c3f404-e2e2-4057-ed55-58a4b1e15cf7" colab={"base_uri": "https://localhost:8080/", "height": 267}
# ArnoldCatEncryptionIm = ArnoldCatEncryption(image + ext, 20)
# imshow(ArnoldCatEncryptionIm)
#
# # + [markdown] id="UbPO1GjUx7uh" colab_type="text"
# # Decrypt with key = 19
#
# # + id="zyB28pvcx5V9" colab_type="code" outputId="bc425865-7edc-4ad5-f375-8070ca3a8fca" colab={"base_uri": "https://localhost:8080/", "height": 267}
# ArnoldCatDecryptionIm = ArnoldCatDecryption(image + "_ArnoldcatEnc.png", 19)
# imshow(ArnoldCatDecryptionIm)
#
# # + [markdown] id="EdsbbrX8yOHx" colab_type="text"
# # ## Henon Maps
#
# # + [markdown] id="PQQPT9eJ2Bx_" colab_type="text"
# # Encrypt with key (0.1, 0.1)
#
# # + id="xfWK2XrdzcqH" colab_type="code" outputId="8d406a32-d0a8-4e49-baaf-c49001565970" colab={"base_uri": "https://localhost:8080/", "height": 286}
# HenonEncryption(image + ext, (0.1, 0.1))
# im = Image.open(image + "_HenonEnc.png", 'r')
# imshow(np.asarray(im))
#
# # + [markdown] id="Rhph8RtX0f6H" colab_type="text"
# # Decrypt with the key (0.1, 0.101)
#
# # + id="u9wPtl6G0gTp" colab_type="code" outputId="b7e67f3c-0cec-4dd5-9643-52613fe22c7f" colab={"base_uri": "https://localhost:8080/", "height": 286}
# HenonDecryption(image + "_HenonEnc.png", (0.1, 0.101))
# im = Image.open(image + "_HenonDec.png", 'r')
# imshow(np.asarray(im))
#
# # + [markdown] id="BlwnUazN1Dlq" colab_type="text"
# # ## Logistic Maps
#
# # + [markdown] id="_Op8EUga2NGJ" colab_type="text"
# # Decrypt with the key "supersecretke"
#
# # + id="QvNcJW__1NDP" colab_type="code" outputId="70897707-4011-4826-b601-3c4c0988116c" colab={"base_uri": "https://localhost:8080/", "height": 286}
# LogisticEncryption(image + ext, key = "supersecretke")
# im = Image.open(image + "_LogisticEnc.png", 'r')
# imshow(np.asarray(im))
#
# # + [markdown] id="08AQwals2UPr" colab_type="text"
# # Decrypt with the key "supersecretkd"
#
# # + id="7hiatxaI1Vel" colab_type="code" outputId="72e3387b-ef72-4c82-bf69-a643c043a4a3" colab={"base_uri": "https://localhost:8080/", "height": 286}
# LogisticDecryption(image + "_LogisticEnc.png", "supersecretkd")
# im = Image.open(image + "_LogisticDec.png", 'r')
# imshow(np.asarray(im))
