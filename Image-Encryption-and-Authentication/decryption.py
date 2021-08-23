from PIL import Image
from matplotlib import pyplot as plt
import cv2
import imagehash

im = Image.open('output.png')
hash = imagehash.phash(im)
print(hash)
pix = im.load()
size = im.size
mod = min(size)
enc_key = "CRYPTOGRAPHY"
key_length = len(enc_key)
key_array = []

for key in enc_key:
    key_array.append(ord(key)%mod)
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

for q in range(size[0]):
    for r in range(size[1]):
        reds=pix[q,r][0]^(key_array[q*r%key_length]**2%255)
        greens=pix[q,r][1]^(key_array[q*r%key_length]**2%255)
        blues=pix[q,r][2]^(key_array[q*r%key_length]**2%255)
        pix[q,r] = (reds,greens,blues)
plt.imshow(im)

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
