import os, binascii
from backports.pbkdf2 import pbkdf2_hmac
import matplotlib.pyplot as plt
from PIL import Image
import json
import piexif
import piexif.helper
import hashlib
import pandas as pd
import numpy as np
def decrypt(image, key, rsa_key, public_key):
    my_img = Image.open(image)
    pix = my_img.load()
    size = my_img.size
    mod = min(size)
    row, col = my_img.size[0], my_img.size[1]
    data = pd.read_parquet(f'{image}.parquet.gzip')
    array = data.to_numpy()
    array = array.reshape(row, col, 3)
    """for i in range(len(array)):
        for j in range(col):
            print(array[i][j])"""

    D = rsa_key
    N = public_key
    print("D decryption = ", D)
    # Step 6: Decryption

    for i in range(row):
        for j in range(col):
            r, g, b = array[i][j]
            M1 = pow(int(r), D, N)
            M2 = pow(int(g), D, N)
            M3 = pow(int(b), D, N)
            pix[i, j] = (M1, M2, M3)

    plt.imshow(my_img)
    plt.show()

    enc_key = key
    salt = binascii.unhexlify('aaef2d3f4d77ac66e9c5a6c3d8f921d1')
    passwd = enc_key.encode("utf8")
    key = pbkdf2_hmac("sha256", passwd, salt, 50000, 2048)
    print("Derived key:", binascii.hexlify(key))
    key = binascii.hexlify(key)
    key = str(key, 'UTF-8')
    print(key)
    key_length = len(key)
    key_array = []
    key_arra = []
    for key in key:
        key_arra.append(ord(key) % mod)
    for i in range(len(key_arra) - 5):
        # adding the alternate numbers
        sum = key_arra[i] + key_arra[i + 1] + key_arra[i + 2] + key_arra[i + 3] + key_arra[i + 4] + key_arra[i + 5]
        key_array.append(sum % mod)
    res = []
    for i in key_array:
        if i not in res:
            res.append(i)
    print(key_array)
    i = size[0] * size[1]
    i = i - 1
    for q in range(size[0] - 1, -1, -1):
        for r in range(size[1] - 1, -1, -1):
            i = 1
            reds = pix[q, r][0] ^ pix[(q - i) % size[0], (r - i) % size[1]][0]
            greens = pix[q, r][1] ^ pix[(q - i) % size[0], (r - i) % size[1]][1]
            blues = pix[q, r][2] ^ pix[(q - i) % size[0], (r - i) % size[1]][2]
            pix[q, r] = (reds, greens, blues)
            reds = pix[q, r][0] ^ (key_array[q * r % len(key_array)] ** 2 % 255)
            greens = pix[q, r][1] ^ (key_array[q * r % len(key_array)] ** 2 % 255)
            blues = pix[q, r][2] ^ (key_array[q * r % len(key_array)] ** 2 % 255)
            pix[q, r] = (reds, greens, blues)

    plt.imshow(my_img)
    plt.show()

    my_img.save(image)