import binascii
from backports.pbkdf2 import pbkdf2_hmac
import matplotlib.pyplot as plt
from PIL import Image
import pandas as pd
import numpy
import random
import cv2
import cvlib as cv
import RSA
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
    total_size = col * row
    all_pixels = []
    random_ordering = []
    for i in range(0, total_size):
        all_pixels.append(i)

    for i in range(0, total_size):
        pos = key_array[i % len(key_array)] ** 3 % (len(all_pixels))
        random_ordering.append(all_pixels[pos])
        # print(random_ordering[i])
        all_pixels.pop(pos)

    print(len(random_ordering), " ", total_size)
    print(random_ordering)
    for i in range(0, total_size):
        if (i == 0):
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
            pos = random_ordering[i]
            prev_pos = random_ordering[i - 1]
            q = int(pos / row)
            r = pos % col
            randomrow = int(prev_pos / size[0])
            randomcol = prev_pos % size[1]
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
    #plt.imshow(my_img)
    #plt.show()

    #SCRAMBLING
    enc = [[0 for x in range(col)] for y in range(row)]
    for i in range(row):
        for j in range(col):
            enc[i][j] = [pix[i, j][0], pix[i, j][1], pix[i, j][2]]
    for i in range(2):
        if (i >= 1):
            enc = enc.tolist()
        for q in range(size[0]):
            var = key_array[q] % 2
            if var:
                rotateRowLeft(enc, (key_array[q % len(key_array)] ** 2) % size[1], size[1], q)
            else:
                rotateRowRight(enc, (key_array[q % len(key_array)] ** 2) % size[1], size[1], q)

        enc = numpy.array(enc)

        for q in range(size[1]):
            var = key_array[q] % 2
            if var:
                rotateColUp(enc, (key_array[q % len(key_array)] ** 2) % size[0], size[0], q)
            else:
                rotateColDown(enc, (key_array[q % len(key_array)] ** 2) % size[0], size[0], q)
    for i in range(size[0]):
        for j in range(size[1]):
            pix[i, j] = (enc[i][j][0], enc[i][j][1], enc[i][j][2])

    #plt.imshow(my_img)
    #plt.show()

    #RSA
    rsa_map = {}
    test_rsa_map = {}
    counter = 0
    for i in range(len(key_array)):

        if counter >= 256:
            break

        special_key = key_array[i] * key_array[i + 1]

        if special_key not in rsa_map.values():
            rsa_map[counter] = special_key
            test_rsa_map[special_key] = counter
            counter += 1
    # print("length of rsa map = ", len(rsa_map), "rsa_map = ", rsa_map)
    # print("length of test rsa map = ", len(test_rsa_map), "test_rsa_map = ", test_rsa_map)

    E, D, N = RSA.gen_RSA_keys()
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

    df = pd.DataFrame(column, columns=['C1', 'C2', 'C3'])
    df.to_parquet(f'{imagelocation}.jpg.parquet.gzip', compression='gzip')

    my_img.save(f'{imagelocation}.jpg')

    #print("Encryption completed")


def encryption(imagelocation, key):
    im = cv2.imread(imagelocation)
    faces, confidences = cv.detect_face(im)
    # loop through detected faces and add bounding box
    userdata = ""
    for face in faces:
        (startX, startY) = face[0], face[1]
        (endX, endY) = face[2], face[3]
        userdata = str(face[0]) + " " + str(face[1]) + " " + str(face[2]) + " " + str(face[3])
        column = []
        column.append((face[0], face[1], face[2]))
        column.append((face[3], 0, 0))
        crop = im[startY:endY, startX:endX]
        cv2.imwrite("crop_{0}.png", crop)
        partialencrypt("crop_{0}.png", key, column,imagelocation)
        temp = cv2.imread("crop_{0}.png")
        im[startY:endY, startX:endX] = temp
        cv2.imwrite(imagelocation, im)

column = []
column.append((0, 0, 0))
column.append((0, 0, 0))
tic = time.perf_counter()
partialencrypt("C:/Users/vishn/PycharmProjects/imo/dtjdtg/Images/JPEG/Jpeg 8-bit/4.2.01.jpg","ABCD",column,"enc_image")
toc = time.perf_counter()
print(f"Finished encryption in {toc - tic:0.4f} seconds")