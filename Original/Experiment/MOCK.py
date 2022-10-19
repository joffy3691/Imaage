import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import hashlib
my_img = Image.open('C:/Users/vishn/PycharmProjects/imo/dtjdtg/Image-Encryption-and-Authentication/lena.png')
# cv2_imshow(my_img)
plt.imshow(my_img)
pix = my_img.load()


key = input()
size = my_img.size
mod = min(size)
enc_key = key
key = hashlib.md5(key.encode()).hexdigest()
print(key)
key_length = len(key)
key_array = []


for key in key:
    key_array.append(ord(key) % mod)

key_sum = sum(key_array)
for q in range(size[0]):
    for r in range(size[1]):
        xoratts = []
        for atts in range(len(pix[q, r])):
            xoratts.append(pix[q, r][atts] ^ pix[(q - 1) % size[0], (r - 1) % size[1]][atts] ^ (
                        key_array[q * r % key_length] ** 2 % 255) ^ (key_length * key_sum % 255))
        pix[q, r] = tuple(xoratts)
plt.imshow(my_img)
plt.show()

key = input()
key = hashlib.md5(key.encode()).hexdigest()
print(key)
key_length = len(key)
key_array = []
key_sum = sum(key_array)
for key in key:
    key_array.append(ord(key) % mod)


for q in range(size[0] - 1, -1, -1):
    for r in range(size[1] - 1, -1, -1):
        xoratts = []
        for atts in range(len(pix[q, r])):
            xoratts.append(pix[q, r][atts] ^ pix[(q - 1) % size[0], (r - 1) % size[1]][atts] ^ (
                        key_array[q * r % key_length] ** 2 % 255) ^ (key_length * key_sum % 255))
        pix[q, r] = tuple(xoratts)

plt.imshow(my_img)
plt.show()