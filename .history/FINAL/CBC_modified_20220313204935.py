pratyparty
#3583

joffy — 03/10/2022
lo
l
pratyparty — 03/10/2022
Is it okay or any changes required?
ytrain is not defined
Image
joffy — 03/10/2022
that is just pratyush drunk things
from sklearn.neural_network import MLPClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
import pandas as pd

data = pd.read_csv('car_evaluation.csv')
#Converting categorical data to numeriacal
data.buying_price = data.buying_price.astype("category").cat.codes
data.maintenance_cost = data.maintenance_cost.astype("category").cat.codes
data.number_of_doors = data.number_of_doors.astype("category").cat.codes
data.number_of_persons = data.number_of_persons.astype("category").cat.codes
data.lug_boot = data.lug_boot.astype("category").cat.codes
data.safety = data.safety.astype("category").cat.codes
data.decision = data.decision.astype("category").cat.codes

X = data.iloc[:,:-1].values #get a copy of dataset exclude last column
y = data.iloc[:, -1].values #get array of dataset in column 1st
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y,random_state=1,test_size=0.01)
clf = MLPClassifier(random_state=1, max_iter=300)
clf.fit(X_train, ytrain)
for i in range(len(clf.coefs)):
    number_neurons_inlayer = clf.coefs[i].shape[1]
    for j in range(number_neurons_inlayer):
        weights = clf.coefs[i][:,j]
        print(i, j, weights, end=", ")
        print()
    print()

y_pred = clf.predict(X_test)
print("Actual Set of Y values : ",y_test[:].tolist())
print("Predicted Y values: ",y_pred[:].tolist())
print()
from sklearn.metrics import precision_score,recall_score,confusion_matrix,accuracy_score
print('Test Data Metrics:')
print('Precision: %.3f' % precision_score(y_test, y_pred,average='micro'))
print('Recall: %.3f' % recall_score(y_test, y_pred,average='micro'))
print('Confusion Matrix \n',confusion_matrix(y_test, y_pred))
print('Accuracy: %.3f' % accuracy_score(y_test, y_pred))
print("\n")
Idk how it changes
changed
pratyparty — 03/10/2022
Oh okay
Bro, it is Discord problem
underscore changes the further letters into italics
joffy — 03/10/2022
lol
pratyparty — 03/10/2022
Bro, how big is the output
pratyparty
 started a call that lasted 2 minutes.
 — 03/10/2022
joffy — 03/10/2022
https://python-course.eu/machine-learning/neural-networks-with-scikit.php
Neural Networks with Scikit | Machine Learning | python-course.eu
Tutorial on Neural Networks with Python and Scikit
pratyparty — 03/10/2022
Is your attendance over?
joffy — 03/10/2022
no
wbu?
pratyparty — 03/10/2022
Okay
Nope
Is Ayush there?
joffy — 03/10/2022
no
pratyparty — 03/10/2022
What!!
I told him to go to your room and I'll give his kettle in ur room
maybe his attendance is also not over yet
joffy
 started a call that lasted 4 minutes.
 — 03/10/2022
pratyparty — 03/10/2022
Can you hear me?
joffy — 03/10/2022
hellllllllllllllllllllo
nooooooooooooooooooooo
pratyparty — 03/10/2022
I can't hear you
VIT wifi
Call me on my phone
pratyparty — 03/10/2022
Tell me if you want me to change anything
Attachment file type: acrobat
19BCE0506_Assessment3.pdf
296.77 KB
joffy — 03/10/2022
Change the size
i have also taken same
test size 0.02 or something
u take
pratyparty — 03/10/2022
I have taken 0.03
joffy — 03/10/2022
k
pratyparty — 03/10/2022
Done and uploaded
joffy — 03/10/2022
y bro
u were supposed to test the limits
to try at 11 59
joffy
 started a call that lasted 29 minutes.
 — 03/11/2022
pratyparty — 03/11/2022
from PIL import Image
from matplotlib import image
import pandas as pd
import random
import RSA
import matplotlib.pyplot as plt
Expand
message.txt
3 KB
Encryption
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt
import os, binascii
from backports.pbkdf2 import pbkdf2_hmac
Expand
message.txt
3 KB
Decryption
pratyparty — 03/11/2022
Image
joffy — Today at 8:46 PM
import binascii
from backports.pbkdf2 import pbkdf2_hmac
import matplotlib.pyplot as plt
from PIL import Image
import pandas as pd
import numpy
import random
import cv2
import cvlib as cv

import time
# my_img = Image.open('/home/pratyush/Downloads/Imaage-main/Experiment/PROFILE.jpeg')
# cv2_imshow(my_img)
# plt.imshow(my_img)
# pix = my_img.load()
def rotateRowRight(arr, d, n, i):
    arr[i][:] = arr[i][d:n] + arr[i][0:d]


def rotateRowLeft(arr, d, n, i):
    arr[i][:] = arr[i][n - d:n] + arr[i][0:n - d]


def rotateColDown(arr, d, n, j):
    arr[:, j] = numpy.concatenate((arr[d:n, j], arr[0:d, j]))


def rotateColUp(arr, d, n, j):
    arr[:, j] = numpy.concatenate((arr[n - d:n, j], arr[0:n - d, j]))


def partialencrypt(image, key, column,imagelocation):
    my_img = Image.open(image)
    pix = my_img.load()
    size = my_img.size
    row, col = my_img.size[0], my_img.size[1]
    print(row," ",col)
    mod = min(size)

    #PBKDF2
    enc_key = key
    salt = binascii.unhexlify('aaef2d3f4d77ac66e9c5a6c3d8f921d1')
    passwd = enc_key.encode("utf8")
    key = pbkdf2_hmac("sha256", passwd, salt, 50, 2048)
    #print("Derived key:", binascii.hexlify(key))
    key = binascii.hexlify(key)
    key = str(key, 'UTF-8')
    #print(key)
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
    #print(key_array)
    res = []
    # for i in key_array:
    #    if i not in res:
    #        res.append(i)


    #CBC
    total_size=col*row
    all_pixels=[]
    random_ordering=[]
    for i in range(0,total_size):
        all_pixels.append(i)

    for i in range(0, total_size):
        pos=key_array[i%len(key_array)] ** 3 %(len(all_pixels))
        random_ordering.append(all_pixels[pos])
        # print(random_ordering[i])
        all_pixels.pop(pos)

    print(len(random_ordering)," ",total_size)
    print(random_ordering)
    for i in range(0,total_size):
        if(i==0):
            pos = random_ordering[0]
            q = int(pos / size[0])
            r = pos % size[1]
            reds = pix[q, r][0] ^ (key_array[0] ** 2 % 255)
            greens = pix[q, r][1] ^ (key_array[0] ** 2 % 255)
            blues = pix[q, r][2] ^ (key_array[0] ** 2 % 255)
            pix[q, r] = (reds, greens, blues)
        # elif i>=total_size/100:
        #     break
        else:
            pos=random_ordering[i]
            prev_pos=random_ordering[i-1]
            q=int(pos/row)
            r=pos%col
            randomrow=int(prev_pos/size[0])
            randomcol=prev_pos%size[1]
            # print(str(q)+" "+str(r)+" "+str(randomcol)+" "+str(randomcol))
            reds = pix[q, r][0] ^ pix[randomrow, randomcol][0]
... (183 lines left)
Collapse
message.txt
11 KB
﻿
import binascii
from backports.pbkdf2 import pbkdf2_hmac
import matplotlib.pyplot as plt
from PIL import Image
import pandas as pd
import numpy
import random
import cv2
import cvlib as cv

import time
# my_img = Image.open('/home/pratyush/Downloads/Imaage-main/Experiment/PROFILE.jpeg')
# cv2_imshow(my_img)
# plt.imshow(my_img)
# pix = my_img.load()
def rotateRowRight(arr, d, n, i):
    arr[i][:] = arr[i][d:n] + arr[i][0:d]


def rotateRowLeft(arr, d, n, i):
    arr[i][:] = arr[i][n - d:n] + arr[i][0:n - d]


def rotateColDown(arr, d, n, j):
    arr[:, j] = numpy.concatenate((arr[d:n, j], arr[0:d, j]))


def rotateColUp(arr, d, n, j):
    arr[:, j] = numpy.concatenate((arr[n - d:n, j], arr[0:n - d, j]))


def partialencrypt(image, key, column,imagelocation):
    my_img = Image.open(image)
    pix = my_img.load()
    size = my_img.size
    row, col = my_img.size[0], my_img.size[1]
    print(row," ",col)
    mod = min(size)

    #PBKDF2
    enc_key = key
    salt = binascii.unhexlify('aaef2d3f4d77ac66e9c5a6c3d8f921d1')
    passwd = enc_key.encode("utf8")
    key = pbkdf2_hmac("sha256", passwd, salt, 50, 2048)
    #print("Derived key:", binascii.hexlify(key))
    key = binascii.hexlify(key)
    key = str(key, 'UTF-8')
    #print(key)
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
    #print(key_array)
    res = []
    # for i in key_array:
    #    if i not in res:
    #        res.append(i)


    #CBC
    total_size=col*row
    all_pixels=[]
    random_ordering=[]
    for i in range(0,total_size):
        all_pixels.append(i)

    for i in range(0, total_size):
        pos=key_array[i%len(key_array)] ** 3 %(len(all_pixels))
        random_ordering.append(all_pixels[pos])
        # print(random_ordering[i])
        all_pixels.pop(pos)

    print(len(random_ordering)," ",total_size)
    print(random_ordering)
    for i in range(0,total_size):
        if(i==0):
            pos = random_ordering[0]
            q = int(pos / size[0])
            r = pos % size[1]
            reds = pix[q, r][0] ^ (key_array[0] ** 2 % 255)
            greens = pix[q, r][1] ^ (key_array[0] ** 2 % 255)
            blues = pix[q, r][2] ^ (key_array[0] ** 2 % 255)
            pix[q, r] = (reds, greens, blues)
        # elif i>=total_size/100:
        #     break
        else:
            pos=random_ordering[i]
            prev_pos=random_ordering[i-1]
            q=int(pos/row)
            r=pos%col
            randomrow=int(prev_pos/size[0])
            randomcol=prev_pos%size[1]
            # print(str(q)+" "+str(r)+" "+str(randomcol)+" "+str(randomcol))
            reds = pix[q, r][0] ^ pix[randomrow, randomcol][0]
            greens = pix[q, r][1] ^ pix[randomrow, randomcol][1]
            blues = pix[q, r][2] ^ pix[randomrow, randomcol][2]
            pix[q, r] = (reds, greens, blues)
            reds = pix[q, r][0] ^ (key_array[q * r % len(key_array)] ** 2 % 255)
            greens = pix[q, r][1] ^ (key_array[q * r % len(key_array)] ** 2 % 255)
            blues = pix[q, r][2] ^ (key_array[q * r % len(key_array)] ** 2 % 255)
            pix[q, r] = (reds, greens, blues)
    plt.imshow(my_img)
    plt.show()
    for i in range(total_size-1,-1,-1):
        if(i==0):
            pos = random_ordering[0]
            q = int(pos / size[0])
            r = pos % size[1]
            reds = pix[q, r][0] ^ (key_array[0] ** 2 % 255)
            greens = pix[q, r][1] ^ (key_array[0] ** 2 % 255)
            blues = pix[q, r][2] ^ (key_array[0] ** 2 % 255)
            pix[q, r] = (reds, greens, blues)

        else:
            pos=random_ordering[i]
            prev_pos=random_ordering[i-1]
            q=int(pos/row)
            r=pos%col
            randomrow=int(prev_pos/size[0])
            randomcol=prev_pos%size[1]
            # print(str(q)+" "+str(r)+" "+str(randomcol)+" "+str(randomcol))
            reds = pix[q, r][0] ^ pix[randomrow, randomcol][0]
            greens = pix[q, r][1] ^ pix[randomrow, randomcol][1]
            blues = pix[q, r][2] ^ pix[randomrow, randomcol][2]
            pix[q, r] = (reds, greens, blues)
            reds = pix[q, r][0] ^ (key_array[q * r % len(key_array)] ** 2 % 255)
            greens = pix[q, r][1] ^ (key_array[q * r % len(key_array)] ** 2 % 255)
            blues = pix[q, r][2] ^ (key_array[q * r % len(key_array)] ** 2 % 255)
            pix[q, r] = (reds, greens, blues)
    plt.imshow(my_img)
    plt.show()
    # for q in range(size[0]):
    #     for r in range(size[1]):
    #         i = 1
    #         if(q==0 and r==0):
    #
    #             continue
    #         else:
    #
    #             randomchoice=key_array[q * r % len(key_array)] ** 2 % ((q*511)+r)
    #             if q!=0:
    #                 randomrow=randomchoice%q
    #             else:
    #                 randomrow=0
    #             randomcol=randomchoice%col
    #             #print(q," ",r," Random ",randomrow, " ", randomcol)
    #             reds = pix[q, r][0] ^ pix[randomrow, randomcol][0]
    #             greens = pix[q, r][1] ^ pix[randomrow, randomcol][1]
    #             blues = pix[q, r][2] ^ pix[randomrow, randomcol][2]
    #             pix[q, r] = (reds, greens, blues)
    #             reds = pix[q, r][0] ^ (key_array[q * r % len(key_array)] ** 2 % 255)
    #             greens = pix[q, r][1] ^ (key_array[q * r % len(key_array)] ** 2 % 255)
    #             blues = pix[q, r][2] ^ (key_array[q * r % len(key_array)] ** 2 % 255)
    #             pix[q, r] = (reds, greens, blues)
    # plt.imshow(my_img)
    # plt.show()
    #
    # for q in range(size[0] - 1, -1, -1):
    #     for r in range(size[1] - 1, -1, -1):
    #         i = 1
    #         if (q == 0 and r == 0):
    #             reds = pix[0, 0][0] ^ (key_array[0] ** 2 % 255)
    #             greens = pix[0, 0][1] ^ (key_array[0] ** 2 % 255)
    #             blues = pix[0, 0][2] ^ (key_array[0] ** 2 % 255)
    #             pix[0, 0] = (reds, greens, blues)
    #             continue
    #         else:
    #             print(q, " ", r)
    #             randomchoice = key_array[q * r % len(key_array)] ** 2 % ((q * 511) + r)
    #             if q != 0:
    #                 randomrow = randomchoice % q
    #             else:
    #                 randomrow = 0
    #             randomcol = randomchoice % col
    #             print(randomrow, " ", randomcol)
    #             reds = pix[q, r][0] ^ pix[randomrow, randomcol][0]
    #             greens = pix[q, r][1] ^ pix[randomrow, randomcol][1]
    #             blues = pix[q, r][2] ^ pix[randomrow, randomcol][2]
    #             pix[q, r] = (reds, greens, blues)
    #             reds = pix[q, r][0] ^ (key_array[q * r % len(key_array)] ** 2 % 255)
    #             greens = pix[q, r][1] ^ (key_array[q * r % len(key_array)] ** 2 % 255)
    #             blues = pix[q, r][2] ^ (key_array[q * r % len(key_array)] ** 2 % 255)
    #             pix[q, r] = (reds, greens, blues)
    #
    # plt.imshow(my_img)
    # plt.show()
    #
    # #SCRAMBLING
    # enc = [[0 for x in range(col)] for y in range(row)]
    # for i in range(row):
    #     for j in range(col):
    #         enc[i][j] = [pix[i, j][0], pix[i, j][1], pix[i, j][2]]
    # for i in range(2):
    #     if (i >= 1):
    #         enc = enc.tolist()
    #     for q in range(size[0]):
    #         var = key_array[q] % 2
    #         if var:
    #             rotateRowLeft(enc, (key_array[q % len(key_array)] ** 2) % size[1], size[1], q)
    #         else:
    #             rotateRowRight(enc, (key_array[q % len(key_array)] ** 2) % size[1], size[1], q)
    #
    #     enc = numpy.array(enc)
    #
    #     for q in range(size[1]):
    #         var = key_array[q] % 2
    #         if var:
    #             rotateColUp(enc, (key_array[q % len(key_array)] ** 2) % size[0], size[0], q)
    #         else:
    #             rotateColDown(enc, (key_array[q % len(key_array)] ** 2) % size[0], size[0], q)
    # for i in range(size[0]):
    #     for j in range(size[1]):
    #         pix[i, j] = (enc[i][j][0], enc[i][j][1], enc[i][j][2])
    #
    # #plt.imshow(my_img)
    # #plt.show()
    #
    # #RSA
    # E,D,N=RSA.gen_RSA_keys()
    # rsa_hashing = {}
    # rsa_keys = []
    # for i in range(256):
    #     C1 = pow(i, E, N)
    #     rsa_hashing[i] = C1
    #     rsa_keys.append(C1)
    #
    # random.shuffle(rsa_keys)
    #
    # rsa_key_position = {}
    #
    # for i in range(256):
    #     rsa_key_position[rsa_keys[i]] = i
    #
    # # Step 5: Encryption
    # size = my_img.size
    # userdata = ""
    # for i in range(85):
    #     C1 = rsa_keys[i * 3]
    #     C2 = rsa_keys[i * 3 + 1]
    #     C3 = rsa_keys[i * 3 + 2]
    #     column.append((C1, C2, C3))
    # C1 = rsa_keys[255]
    # column.append((C1, 0, 0))
    # for i in range(row):
    #     for j in range(col):
    #         r, g, b = pix[i, j]
    #         C1 = rsa_key_position.get(rsa_hashing.get(r))
    #         C2 = rsa_key_position.get(rsa_hashing.get(g))
    #         C3 = rsa_key_position.get(rsa_hashing.get(b))
    #         # C1 = pow(r, E, N)
    #         # C2 = pow(g, E, N)
    #         # C3 = pow(b, E, N)
    #         column.append((C1, C2, C3))
    #         # userdata=userdata+str(C1)+","+str(C2)+","+str(C3)+","
    #         C1 = C1 % 256
    #         C2 = C2 % 256
    #         C3 = C3 % 256
    #         pix[i, j] = (C1, C2, C3)
    #
    # #plt.imshow(my_img)
    # #plt.show()
    #
    # df = pd.DataFrame(column, columns=['C1', 'C2', 'C3'])
    # df.to_parquet(f'{imagelocation}.jpg.parquet.gzip', compression='gzip')

    my_img.save(f'{imagelocation}.jpg')

    #print("Encryption completed")


column = []
column.append((0, 0, 0))
column.append((0, 0, 0))
tic = time.perf_counter()
partialencrypt("C:/Users/vishn/PycharmProjects/imo/dtjdtg/Images/PNG/png 8-bit/4.1.04.png","ABCD",column,"enc_image")
toc = time.perf_counter()
print(f"Finished encryption in {toc - tic:0.4f} seconds")
message.txt
11 KB