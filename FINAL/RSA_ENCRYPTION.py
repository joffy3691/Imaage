from PIL import Image
import pandas as pd
import random
import RSA
import matplotlib.pyplot as plt
image="C:/Users/vishn/PycharmProjects/imo/dtjdtg/Image-Encryption-and-Authentication/tom.bmp"
imagelocation="output.jpg"
column=[]
my_img = Image.open(image)
pix = my_img.load()
size = my_img.size
row, col = my_img.size[0], my_img.size[1]
mod = min(size)
E,D,N=RSA.gen_RSA_keys()
rsa_hashing = {}
rsa_keys = []
for i in range(256):
    C1 = pow(i, E, N)
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