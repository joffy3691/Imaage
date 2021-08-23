from PIL import Image
import hashlib
import cv2
from matplotlib import pyplot as plt

def encrypt(image,key,mode):
    im = Image.open(image)
    pix = im.load()
    size = im.size
    mod = min(size)
    enc_key = key
    key = hashlib.md5(key.encode()).hexdigest()
    print(key)
    key_length = len(key)
    key_array = []
    key_sum = sum(key_array)

    for key in key:
        key_array.append(ord(key)%mod)
    print(key_array)
    for q in range(size[0]):
        for r in range(size[1]):
            xoratts = []
            for atts in range(len(pix[q,r])):
                xoratts.append(pix[q,r][atts]^pix[(q-1)%size[0],(r-1)%size[1]][atts]^(key_array[q*r%key_length]**2%255)^(key_length*key_sum%255))
            pix[q,r] = tuple(xoratts)
            
    for k in range (2,key_length):
        for i in range (0,size[0],k):
            y1=i
            y2=(i+k*(key_array[k%(key_length)])**key_length)%size[0]
            for j in range(0,size[1]):
                x=j
                pixel1 = pix[y1,x]
                pixel2 = pix[y2,x]
                pix[y1,x] = pixel2
                pix[y2,x] = pixel1

        if mode == 'Secure':

            for i in range (0,size[0]):
                y=i
                for j in range(0,size[1],k):
                    x1=j
                    x2=(j+k*(key_array[k%(key_length)])**key_length)%size[1]
                    pixel1 = pix[y,x1]
                    pixel2 = pix[y,x2]
                    pix[y,x1] = pixel2
                    pix[y,x2] = pixel1
    im.save(image)
    img = cv2.imread(image)
    color = ('b','g','r')



    

