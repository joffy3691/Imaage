from PIL import Image
from matplotlib import pyplot as plt
import imagehash

im = Image.open('lena.png')
hash = imagehash.phash(im)
print(hash)

pix = im.load()
size = im.size
mod = min(size)
print(mod)

enc_key = "lena"
key_length = len(enc_key)
key_array = []

key_xor = 0
for key in enc_key:
    key_array.append(ord(key)%mod)
    key_xor = key_xor^ord(key)

key_xor = key_xor**key_xor%256
print(key_xor)

key_sum = sum(key_array)**7%256

for q in range(size[0]):
    for r in range(size[1]):
        reds=(pix[q,r][0]^q^(key_array[q*r%key_length]**2%256)^pix[(q-1)%size[0],(r-1)%size[1]][0]^key_xor)%256
        greens=(pix[q,r][1]^r^(key_array[q*r%key_length]**2%256)^pix[(q-1)%size[0],(r-1)%size[1]][1]^key_xor)%256
        blues=(pix[q,r][2]^q^r^(key_array[q*r%key_length]**2%256)^pix[(q-1)%size[0],(r-1)%size[1]][2]^key_xor)%256
        pix[q,r] = (reds,greens,blues)
plt.imshow(im)
plt.show()

for k in range (1,key_length+1):
    for i in range (0,size[0],k):
        y1=i
        y2=(i+1*(key_array[k%(key_length)])**7+key_sum)%size[0]
        for j in range(0,size[1]):
            x=j
            pixel1 = pix[y1,x]
            pixel2 = pix[y2,x]
            pix[y1,x] = pixel2
            pix[y2,x] = pixel1

plt.imshow(im)
plt.show()
im.save('output.png')