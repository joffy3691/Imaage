from PIL import Image
import numpy as np
import os
from matplotlib.pyplot import imshow
import matplotlib.pyplot as plt
import cv2
import random
from math import log



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


# + [markdown] id="CJlC3VgW-B2H" colab_type="text"
# # Arnold Cat Map
#
# + [markdown] id="FOspal9c9HAN" colab_type="text"
# Arnold's cat map is a chaotic map often used for pixel manipulation. It applies a tranform on the image that essentially shuffles the pixels by stretching anf folding thethe image. When an optimal number of iterations of the transformation is applied on the image, the resulting image becomes incomprehensible and hence encrypted.
#
# For this implementation
# The transform applied on the image is:
# R([x,y]) = [(x + y) mod n, (x + 2y) mod n]
# where n is the dimensions of the image
#
# <br>
#
# When the transformation is repeated enough times, the original image will reappear.
# The number of iterations 'n' at which the original image will reappear is given by these rules of thumb:
# Here 'd' is the dimension of the square image:
#
# 1.   if d =  2.(5^i) for i >=1, n = 3*d
# 2.   if d = (5^i) for i >=1, n = 2*d
# 3.   if d = 6.(5^i) for i>=1, n = 2*d
# 4.   else n <= 12*d / 7
#
# This periodicity forms the crux of the encryption process. Here key is the number of iterations of transformations initially applied to get the encrypted image. n - key is the number of rounds of transformations applied to get the decrypted image.

#+ id="mGbPRosB-Yv_" colab_type="code" colab={}
def ArnoldCatTransform(img, num):
    rows, cols, ch = img.shape
    n = rows
    img_arnold = np.zeros([rows, cols, ch])
    for x in range(0, rows):
        for y in range(0, cols):
            img_arnold[x][y] = img[(x+y)%n][(x+2*y)%n]
    return img_arnold


# + [markdown] id="wYGBg8XAFyLC" colab_type="text"
# Arnold Cat Encryption

# + id="xj7_AyMB3STZ" colab_type="code" colab={}
def ArnoldCatEncryption(imageName, key):
    img = cv2.imread(imageName)
    for i in range (0,key):
        img = ArnoldCatTransform(img, i)
    cv2.imwrite(imageName.split('.')[0] + "_ArnoldcatEnc.png", img)
    return img


# + [markdown] id="O_GFV63YF5YM" colab_type="text"
# Arnold Cat Decryption

# + id="sRJfx4jm32Z2" colab_type="code" colab={}
def ArnoldCatDecryption(imageName, key):
    img = cv2.imread(imageName)
    rows, cols, ch = img.shape
    dimension = rows
    decrypt_it = dimension
    if (dimension%2==0) and 5**int(round(log(dimension/2,5))) == int(dimension/2):
        decrypt_it = 3*dimension
    elif 5**int(round(log(dimension,5))) == int(dimension):
        decrypt_it = 2*dimension
    elif (dimension%6==0) and  5**int(round(log(dimension/6,5))) == int(dimension/6):
        decrypt_it = 2*dimension
    else:
        decrypt_it = int(12*dimension/7)
    for i in range(key,decrypt_it):
        img = ArnoldCatTransform(img, i)
    cv2.imwrite(imageName.split('_')[0] + "_ArnoldcatDec.png",img)
    return img


# + id="FacBvOj26MSf" colab_type="code" colab={}
image = "lena"
ext = ".png"
key = 20

# + id="AFOv1GEJ7H2n" colab_type="code" outputId="40b86a44-3e99-442d-9e7e-9d7e79df459f" colab={"base_uri": "https://localhost:8080/", "height": 267}
img = cv2.imread(image + ext)
imshow(img)
plt.show()
# + id="dEEaCUCb4Ns4" colab_type="code" outputId="fb1af4ba-69be-4f7f-d80d-0a62dc8990f1" colab={"base_uri": "https://localhost:8080/", "height": 267}
ArnoldCatEncryptionIm = ArnoldCatEncryption(image + ext, key)
imshow(ArnoldCatEncryptionIm)
plt.show()
key=21
# + id="a1jyAbjR3xOG" colab_type="code" outputId="02e9d474-c8cd-4ab9-cde8-ac444d4d2c11" colab={"base_uri": "https://localhost:8080/", "height": 267}
ArnoldCatDecryptionIm = ArnoldCatDecryption(image + "_ArnoldcatEnc.png", key)
imshow(ArnoldCatDecryptionIm)
plt.show()