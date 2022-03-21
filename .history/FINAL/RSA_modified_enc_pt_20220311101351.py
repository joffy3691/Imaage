from PIL import Image
from matplotlib import image
import pandas as pd
import random
import RSA
import matplotlib.pyplot as plt
import os, binascii
from backports.pbkdf2 import pbkdf2_hmac
#image="C:/Users/vishn/PycharmProjects/imo/dtjdtg/FINAL/1628574184_sports-9.jpg"
image = "C:/Users/DELL/Downloads/Imaage/FINAL/lena.png"
imagelocation="output.jpg"
column=[]
my_img = Image.open(image)
pix = my_img.load()
size = my_img.size
row, col = my_img.size[0], my_img.size[1]
mod = min(size)

key = input()
enc_key = key
salt = binascii.unhexlify('aaef2d3f4d77ac66e9c5a6c3d8f921d1')
passwd = enc_key.encode("utf8")
key = pbkdf2_hmac("sha256", passwd, salt, 50, 2048)
print("Derived key:", binascii.hexlify(key))
key=binascii.hexlify(key)
key=str(key, 'UTF-8')
print(key);
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
print(key_array)

rsa_map={}
counter = 0
for i in range(len(key_array)):
    
    if counter >= 256:
        break
    
    special_key=key_array[i]*key_array[i+1]
    
    if special_key not in rsa_map:
        rsa_map[counter] = special_key
        counter += 1
    


E,D,N=RSA.gen_RSA_keys()
rsa_hashing = {}
rsa_keys = []
for i in range(256):
    C1 = pow(int(rsa_map[i]), E, N)
    rsa_hashing[i] = C1
    rsa_keys.append(C1)

random.shuffle(rsa_keys)

rsa_key_position = {}

for i in range(256):
    rsa_key_position[rsa_keys[i]] = i

# Step 5: Encryption
size = my_img.size
userdata = ""
for i in range(85):
    C1 = rsa_keys[i * 3]
    C2 = rsa_keys[i * 3 + 1]
    C3 = rsa_keys[i * 3 + 2]
    column.append((C1, C2, C3))
C1 = rsa_keys[255]
column.append((C1, 0, 0))
for i in range(row):
    for j in range(col):
        r, g, b = pix[i, j]
        C1 = rsa_key_position.get(rsa_hashing.get(r))
        C2 = rsa_key_position.get(rsa_hashing.get(g))
        C3 = rsa_key_position.get(rsa_hashing.get(b))
        # C1 = pow(r, E, N)
        # C2 = pow(g, E, N)
        # C3 = pow(b, E, N)
        column.append((C1, C2, C3))
        # userdata=userdata+str(C1)+","+str(C2)+","+str(C3)+","
        C1 = C1 % 256
        C2 = C2 % 256
        C3 = C3 % 256
        pix[i, j] = (C1, C2, C3)

plt.imshow(my_img)
plt.show()

df = pd.DataFrame(column, columns=['C1', 'C2', 'C3'])
df.to_parquet(f'{imagelocation}.parquet.gzip', compression='gzip')
my_img.save("output.jpg")