from PIL import Image
from matplotlib import pyplot as plt
import imagehash

im = Image.open('abstact-thinking2.jpg')
hash = imagehash.phash(im)
print(hash)
pix = im.load()
size = im.size
mod = min(size)
print(mod)
enc_key = "CRYPTOGRAPHY"
key_length = len(enc_key)
key_array = []

for key in enc_key:
    key_array.append(ord(key)%mod)
print(key_array)

for q in range(size[0]):
    for r in range(size[1]):
        reds=pix[q,r][0]^(key_array[q*r%key_length]**2%255)
        greens=pix[q,r][1]^(key_array[q*r%key_length]**2%255)
        blues=pix[q,r][2]^(key_array[q*r%key_length]**2%255)
        pix[q,r] = (reds,greens,blues)

for k in range (2,int(mod)):
    for i in range (0,size[0],k):
        y1=i
        y2=(i+k*(key_array[k%(key_length)])**2)%size[0]
        for j in range(0,size[1]):
            x=j
            pixel1 = pix[y1,x]
            pixel2 = pix[y2,x]
            pix[y1,x] = pixel2
            pix[y2,x] = pixel1

    for i in range (0,size[0]):
        y=i
        for j in range(0,size[1],k):
            x1=j
            x2=(j+k*(key_array[k%(key_length)])**2)%size[1]
            pixel1 = pix[y,x1]
            pixel2 = pix[y,x2]
            pix[y,x1] = pixel2
            pix[y,x2] = pixel1

plt.imshow(im)
plt.show()
im.save('output.png') # Save the modified pixels as .png