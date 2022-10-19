from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt
import os, binascii
from backports.pbkdf2 import pbkdf2_hmac

image="output.jpg"
imagelocation="output.jpg"
my_img = Image.open(image)
pix = my_img.load()
size = my_img.size
mod = min(size)
row, col = my_img.size[0], my_img.size[1]

image2 = "C:/Users/DELL/Downloads/Imaage/FINAL/lena.png"
column=[]
my_img2 = Image.open(image2)
pix2 = my_img2.load()
size2 = my_img2.size


key = input()
enc_key = key
salt = binascii.unhexlify('aaef2d3f4d77ac66e9c5a6c3d8f921d1')
passwd = enc_key.encode("utf8")
key = pbkdf2_hmac("sha256", passwd, salt, 50, 2048)
# print("Derived key:", binascii.hexlify(key))
key=binascii.hexlify(key)
key=str(key, 'UTF-8')
# print(key)
key_length = len(key)
key_array = []
key_arra = []
for key in key:
    key_arra.append(ord(key) % mod)
for i in range(len(key_arra) - 5):
    # adding the alternate numbers
    sum = key_arra[i] + key_arra[i + 1]+key_arra[i + 2]+key_arra[i + 3]+key_arra[i + 4]+key_arra[i + 5]
    key_array.append(sum % mod)
res = []
for i in key_array:
    if i not in res:
        res.append(i)
# print(key_array)
rsa_map={}
counter = 0
for i in range(len(key_array)):
    
    if counter >= 256:
        break
    
    special_key=key_array[i]*key_array[i+1]
    
    if special_key not in rsa_map:
        rsa_map[special_key] = counter
        counter += 1
# print("rsa map length = ",len(rsa_map))
# print(rsa_map)
data = pd.read_parquet(f'{imagelocation}.parquet.gzip')
array = data.to_numpy()
array1=array[0:86]
array1=array1.flatten()
array1=array1[:-2].tolist()
array=array[86:]
array = array.reshape(row, col, 3)
D = int(input("Enter RSA key"))
N = int(input("Enter Public key"))
# print("D decryption = ", D)
rsa_keys1 =array1
rsa_key_position1 = {}

for i in range(256):
    rsa_key_position1[i] = rsa_keys1[i]

rsa_hashing1 = {}
for i in range(256):
    C1 = pow(rsa_keys1[i], D, N)
    rsa_hashing1[rsa_keys1[i]] = int(rsa_map[C1])

counter=0
rgb = set()
for i in range(row):
    for j in range(col):
        r, g, b = array[i][j]
        M1 = rsa_hashing1.get(rsa_key_position1.get(r))
        M2 = rsa_hashing1.get(rsa_key_position1.get(g))
        M3 = rsa_hashing1.get(rsa_key_position1.get(b))
        pix[i, j] = (M1 % 256, M2 % 256, M3 % 256)
        # if(pix[i,j][0] != pix2[i,j][0] and  r not in rgb):
        #     rgb.add(r)
        # if(pix[i,j][1] != pix2[i,j][1] and  g not in rgb):
        #     rgb.add(g)
        # if(pix[i,j][2] != pix2[i,j][2] and  b not in rgb):
        #     rgb.add(b)
           
# print("length = ", len(rgb))
# print(rgb)

plt.imshow(my_img)
plt.show()
my_img.save("output.jpg")