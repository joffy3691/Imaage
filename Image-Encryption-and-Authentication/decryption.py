from PIL import Image
from matplotlib import pyplot as plt
import cv2
import imagehash
import os, binascii
from backports.pbkdf2 import pbkdf2_hmac

im = Image.open('output.png')
hash = imagehash.phash(im)
print(hash)
pix = im.load()
size = im.size
mod = min(size)
print(mod)
enc_key = "A"

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

for k in range (int(mod)-1,1,-1):
    for i in range (size[0]-1,-1,-1):
        y=i
        for j in range(size[1]-1-(size[1]-1)%k,-1,-k):
            x1=j
            x2=(j+k*(key_array[k%(key_length)])**2)%size[1]
            pixel1 = pix[y,x1]
            pixel2 = pix[y,x2]
            pix[y,x1] = pixel2
            pix[y,x2] = pixel1

    for i in range (size[0]-1-(size[0]-1)%k,-1,-k):
        y1=i
        y2=(i+k*(key_array[k%(key_length)])**2)%size[0]
        for j in range(size[1]-1,-1,-1):
            x=j
            pixel1 = pix[y1,x]
            pixel2 = pix[y2,x]
            pix[y1,x] = pixel2
            pix[y2,x] = pixel1

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

im.save('decrypted.png')  # Save the modified pixels as .png
hash = imagehash.phash(im)
print(hash)
plt.imshow(im)
plt.show()
img = cv2.imread('decrypted.png')
color = ('b','g','r')

for i,col in enumerate(color):
    histr = cv2.calcHist([img],[i],None,[256],[0,256])
    plt.plot(histr,color = col)
    plt.xlim([0,256])
plt.show()