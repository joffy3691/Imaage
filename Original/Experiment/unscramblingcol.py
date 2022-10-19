from ctypes import sizeof
import os, binascii
from backports.pbkdf2 import pbkdf2_hmac
import matplotlib.pyplot as plt
from PIL import Image
import numpy
import json
import piexif
import piexif.helper
import hashlib
import pandas as pd
import numpy as np


def rotateRowRight(arr, d, n, i):
    arr[i][:] = arr[i][d:n] + arr[i][0:d]


def rotateRowLeft(arr, d, n, i):
    arr[i][:] = arr[i][n - d:n] + arr[i][0:n - d]


def rotateColDown(arr, d, n, j):
    arr[:, j] = numpy.concatenate((arr[d:n, j], arr[0:d, j]))


def rotateColUp(arr, d, n, j):
    arr[:, j] = numpy.concatenate((arr[n - d:n, j], arr[0:n - d, j]))


my_img = Image.open(
    'output.png')
key = input()
pix = my_img.load()
plt.imshow(my_img)
plt.show()
size = my_img.size
row, col = my_img.size[0], my_img.size[1]
enc = [[0 for x in range(col)] for y in range(row)]
print(row, " ", col)
mod = min(size)
enc_key = key
salt = binascii.unhexlify('aaef2d3f4d77ac66e9c5a6c3d8f921d1')
passwd = enc_key.encode("utf8")
key = pbkdf2_hmac("sha256", passwd, salt, 50, 2048)
print("Derived key:", binascii.hexlify(key))
key = binascii.hexlify(key)
key = str(key, 'UTF-8')
print(key)
key_length = len(key)
key_array = []
# key_sum = sum(key_array)
key_arra = []
for key in key:
    key_arra.append(ord(key) % mod)
for i in range(len(key_arra) - 5):
    # adding the alternate numbers
    sum = key_arra[i] + key_arra[i + 1] + key_arra[i + 2] + key_arra[i + 3] + key_arra[i + 4] + key_arra[i + 5]
    key_array.append(sum % mod)
print(key_array)
for i in range(size[0]):
    for j in range(size[1]):
        enc[i][j] = [pix[i, j][0], pix[i, j][1], pix[i, j][2]]
for i in range(2):
    enc = numpy.array(enc)
    for q in range(size[1] - 1, -1, -1):
        var = key_array[q] % 2
        if var:
            rotateColDown(enc, (key_array[q % len(key_array)] ** 2) % size[0], size[0], q)
        else:
            rotateColUp(enc, (key_array[q % len(key_array)] ** 2) % size[0], size[0], q)

    enc=enc.tolist()
    for q in range(size[0] - 1, -1, -1):
        var = key_array[q] % 2
        if var:
            rotateRowRight(enc, (key_array[q % len(key_array)] ** 2) % size[1], size[1], q)
        else:
            rotateRowLeft(enc, (key_array[q % len(key_array)] ** 2) % size[1], size[1], q)


for i in range(size[0]):
    for j in range(size[1]):
        pix[i, j] = (enc[i][j][0], enc[i][j][1], enc[i][j][2])

plt.imshow(my_img)
plt.show()
my_img.save('decrypted.png')   # Save the modified pixels as .png