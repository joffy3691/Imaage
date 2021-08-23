from PIL import Image
from matplotlib import pyplot as plt
import cv2
import imagehash
import numpy as np

def mse(imageA, imageB):
	# the 'Mean Squared Error' between the two images is the
	# sum of the squared difference between the two images;
	# NOTE: the two images must have the same dimension
	err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
	err /= float(imageA.shape[0] * imageA.shape[1])
	
	# return the MSE, the lower the error, the more "similar"
	# the two images are
	return err


im = Image.open('output.png')
original = im
hash = imagehash.phash(im)
print(hash)
pix = im.load()
size = im.size
mod = min(size)
enc_key = "mena"
key_length = len(enc_key)
key_array = []

key_xor = 0
for key in enc_key:
    key_array.append(ord(key)%mod)
    key_xor = key_xor^ord(key)

key_xor = key_xor**key_xor%256
print(key_xor)
key_sum = sum(key_array)**7%256

for k in range (key_length,0,-1):
    for i in range (size[0]-1-(size[0]-1)%k,-1,-k):
        y1=i
        y2=(i+1*(key_array[k%(key_length)])**7+key_sum)%size[0]
        for j in range(size[1]-1,-1,-1):
            x=j
            pixel1 = pix[y1,x]
            pixel2 = pix[y2,x]
            pix[y1,x] = pixel2
            pix[y2,x] = pixel1

plt.imshow(im)
plt.show()

for q in range(size[0]-1,-1,-1):
    for r in range(size[1]-1,-1,-1):
        reds=(pix[q,r][0]^q^(key_array[q*r%key_length]**2%256)^pix[(q-1)%size[0],(r-1)%size[1]][0]^key_xor)%256
        greens=(pix[q,r][1]^r^(key_array[q*r%key_length]**2%256)^pix[(q-1)%size[0],(r-1)%size[1]][1]^key_xor)%256
        blues=(pix[q,r][2]^q^r^(key_array[q*r%key_length]**2%256)^pix[(q-1)%size[0],(r-1)%size[1]][2]^key_xor)%256
        pix[q,r] = (reds,greens,blues)

plt.imshow(im)

im.save('decrypted.png')  # Save the modified pixels as .png

cor = mse(im,original)

print("Correlation: ",cor)
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
