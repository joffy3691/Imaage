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


def LogisticEncryption(imageName, key):
    N = 256
    key_list = [ord(x) for x in key]
    G = [key_list[0:4], key_list[4:8], key_list[8:12]]
    g = []
    R = 1
    for i in range(1, 4):
        s = 0
        for j in range(1, 5):
            s += G[i - 1][j - 1] * (10 ** (-j))
        g.append(s)
        R = (R * s) % 1

    L = (R + key_list[12] / 256) % 1
    S_x = round(((g[0] + g[1] + g[2]) * (10 ** 4) + L * (10 ** 4)) % 256)
    V1 = sum(key_list)
    V2 = key_list[0]
    for i in range(1, 13):
        V2 = V2 ^ key_list[i]
    V = V2 / V1

    L_y = (V + key_list[12] / 256) % 1    y(i+1) = cos(key*(acosd(y(i))));

    S_y = round((V + V2 + L_y * 10 ** 4) % 256)
    C1_0 = S_x
    C2_0 = S_y
    C = round((L * L_y * 10 ** 4) % 256)
    C_r = round((L * L_y * 10 ** 4) % 256)
    C_g = round((L * L_y * 10 ** 4) % 256)
    C_b = round((L * L_y * 10 ** 4) % 256)
    x = 4 * (S_x) * (1 - S_x)
    y = 4 * (S_y) * (1 - S_y)

    imageMatrix, dimensionX, dimensionY, color = getImageMatrix(imageName)
    LogisticEncryptionIm = []
    for i in range(dimensionX):
        row = []
        for j in range(dimensionY):
            while x < 0.8 and x > 0.2:
                x = 4 * x * (1 - x)
            while y < 0.8 and y > 0.2:
                y = 4 * y * (1 - y)
            x_round = round((x * (10 ** 4)) % 256)
            y_round = round((y * (10 ** 4)) % 256)
            C1 = x_round ^ ((key_list[0] + x_round) % N) ^ ((C1_0 + key_list[1]) % N)
            C2 = x_round ^ ((key_list[2] + y_round) % N) ^ ((C2_0 + key_list[3]) % N)
            if color:
                C_r = ((key_list[4] + C1) % N) ^ ((key_list[5] + C2) % N) ^ (
                            (key_list[6] + imageMatrix[i][j][0]) % N) ^ ((C_r + key_list[7]) % N)
                C_g = ((key_list[4] + C1) % N) ^ ((key_list[5] + C2) % N) ^ (
                            (key_list[6] + imageMatrix[i][j][1]) % N) ^ ((C_g + key_list[7]) % N)
                C_b = ((key_list[4] + C1) % N) ^ ((key_list[5] + C2) % N) ^ (
                            (key_list[6] + imageMatrix[i][j][2]) % N) ^ ((C_b + key_list[7]) % N)
                row.append((C_r, C_g, C_b))
                C = C_r

            else:
                C = ((key_list[4] + C1) % N) ^ ((key_list[5] + C2) % N) ^ ((key_list[6] + imageMatrix[i][j]) % N) ^ (
                            (C + key_list[7]) % N)
                row.append(C)

            x = (x + C / 256 + key_list[8] / 256 + key_list[9] / 256) % 1
            y = (x + C / 256 + key_list[8] / 256 + key_list[9] / 256) % 1
            for ki in range(12):
                key_list[ki] = (key_list[ki] + key_list[12]) % 256
                key_list[12] = key_list[12] ^ key_list[ki]
        LogisticEncryptionIm.append(row)

    im = Image.new("L", (dimensionX, dimensionY))
    if color:
        im = Image.new("RGB", (dimensionX, dimensionY))
    else:
        im = Image.new("L", (dimensionX, dimensionY))  # L is for Black and white pixels

    pix = im.load()
    for x in range(dimensionX):
        for y in range(dimensionY):
            pix[x, y] = LogisticEncryptionIm[x][y]
    im.save(imageName.split('.')[0] + "_LogisticEnc.png", "PNG")


# + id="2t3ClAaAhCqe" colab_type="code" colab={}
def LogisticDecryption(imageName, key):
    N = 256
    key_list = [ord(x) for x in key]

    G = [key_list[0:4], key_list[4:8], key_list[8:12]]
    g = []
    R = 1
    for i in range(1, 4):
        s = 0
        for j in range(1, 5):
            s += G[i - 1][j - 1] * (10 ** (-j))
        g.append(s)
        R = (R * s) % 1

    L_x = (R + key_list[12] / 256) % 1
    S_x = round(((g[0] + g[1] + g[2]) * (10 ** 4) + L_x * (10 ** 4)) % 256)
    V1 = sum(key_list)
    V2 = key_list[0]
    for i in range(1, 13):
        V2 = V2 ^ key_list[i]
    V = V2 / V1

    L_y = (V + key_list[12] / 256) % 1
    S_y = round((V + V2 + L_y * 10 ** 4) % 256)
    C1_0 = S_x
    C2_0 = S_y

    C = round((L_x * L_y * 10 ** 4) % 256)
    I_prev = C
    I_prev_r = C
    I_prev_g = C
    I_prev_b = C
    I = C
    I_r = C
    I_g = C
    I_b = C
    x_prev = 4 * (S_x) * (1 - S_x)
    y_prev = 4 * (L_x) * (1 - S_y)
    x = x_prev
    y = y_prev
    imageMatrix, dimensionX, dimensionY, color = getImageMatrix(imageName)

    henonDecryptedImage = []
    for i in range(dimensionX):
        row = []
        for j in range(dimensionY):
            while x < 0.8 and x > 0.2:
                x = 4 * x * (1 - x)
            while y < 0.8 and y > 0.2:
                y = 4 * y * (1 - y)
            x_round = round((x * (10 ** 4)) % 256)
            y_round = round((y * (10 ** 4)) % 256)
            C1 = x_round ^ ((key_list[0] + x_round) % N) ^ ((C1_0 + key_list[1]) % N)
            C2 = x_round ^ ((key_list[2] + y_round) % N) ^ ((C2_0 + key_list[3]) % N)
            if color:
                I_r = ((((key_list[4] + C1) % N) ^ ((key_list[5] + C2) % N) ^ ((I_prev_r + key_list[7]) % N) ^
                        imageMatrix[i][j][0]) + N - key_list[6]) % N
                I_g = ((((key_list[4] + C1) % N) ^ ((key_list[5] + C2) % N) ^ ((I_prev_g + key_list[7]) % N) ^
                        imageMatrix[i][j][1]) + N - key_list[6]) % N
                I_b = ((((key_list[4] + C1) % N) ^ ((key_list[5] + C2) % N) ^ ((I_prev_b + key_list[7]) % N) ^
                        imageMatrix[i][j][2]) + N - key_list[6]) % N
                I_prev_r = imageMatrix[i][j][0]
                I_prev_g = imageMatrix[i][j][1]
                I_prev_b = imageMatrix[i][j][2]
                row.append((I_r, I_g, I_b))
                x = (x + imageMatrix[i][j][0] / 256 + key_list[8] / 256 + key_list[9] / 256) % 1
                y = (x + imageMatrix[i][j][0] / 256 + key_list[8] / 256 + key_list[9] / 256) % 1
            else:
                I = ((((key_list[4] + C1) % N) ^ ((key_list[5] + C2) % N) ^ ((I_prev + key_list[7]) % N) ^
                      imageMatrix[i][j]) + N - key_list[6]) % N
                I_prev = imageMatrix[i][j]
                row.append(I)
                x = (x + imageMatrix[i][j] / 256 + key_list[8] / 256 + key_list[9] / 256) % 1
                y = (x + imageMatrix[i][j] / 256 + key_list[8] / 256 + key_list[9] / 256) % 1
            for ki in range(12):
                key_list[ki] = (key_list[ki] + key_list[12]) % 256
                key_list[12] = key_list[12] ^ key_list[ki]
        henonDecryptedImage.append(row)
    if color:
        im = Image.new("RGB", (dimensionX, dimensionY))
    else:
        im = Image.new("L", (dimensionX, dimensionY))  # L is for Black and white pixels
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
LogisticDecryption("lena_LogisticEnc.png", "abcdefghijklm")
im = Image.open("lena_LogisticDec.png", 'r')
imshow(np.asarray(im), cmap='gray')

# + [markdown] id="h4QRQeu6mWcO" colab_type="text"
# ### Original Image

# + id="VtAVT_DpjJx0" colab_type="code" colab={}
image = "lena"
ext = ".png"
key = "Pratyush"

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
img = cv2.imread(image + ext, 1)
pil_im = Image.open(image + ext, 'r')
imshow(np.asarray(pil_im))
plt.figure(figsize=(14, 6))

histogram_blue = cv2.calcHist([img], [0], None, [256], [0, 256])
plt.plot(histogram_blue, color='blue')
histogram_green = cv2.calcHist([img], [1], None, [256], [0, 256])
plt.plot(histogram_green, color='green')
histogram_red = cv2.calcHist([img], [2], None, [256], [0, 256])
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
img = cv2.imread(image + ext, 1)
pil_im = Image.open(image + ext, 'r')
imshow(np.asarray(pil_im))
plt.figure(figsize=(14, 6))

histogram_blue = cv2.calcHist([img], [0], None, [256], [0, 256])
plt.plot(histogram_blue, color='blue')
histogram_green = cv2.calcHist([img], [1], None, [256], [0, 256])
plt.plot(histogram_green, color='green')
histogram_red = cv2.calcHist([img], [2], None, [256], [0, 256])
plt.plot(histogram_red, color='red')
plt.title('Intensity Histogram - Logistic Encrypted Image', fontsize=20)
plt.xlabel('pixel values', fontsize=16)
plt.ylabel('pixel count', fontsize=16)
plt.show()