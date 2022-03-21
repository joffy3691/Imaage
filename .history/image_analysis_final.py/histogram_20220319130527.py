from skimage import io
import matplotlib.pyplot as plt

image = io.imread('C:/Users/DELL/Downloads/Imaage/Images/JPEG/Jpeg 8-bit/4.1.04.jpg')
# image = io.imread('C:/Users/DELL/Downloads/Imaage/Image-Encryption-and-Authentication/Pratyush.png')
_ = plt.hist(image.ravel(), bins = 256, color = 'orange', )
_ = plt.hist(image[:, :, 0].ravel(), bins = 256, color = 'red', alpha = 0.5)
_ = plt.hist(image[:, :, 1].ravel(), bins = 256, color = 'Green', alpha = 0.5)
_ = plt.hist(image[:, :, 2].ravel(), bins = 256, color = 'Blue', alpha = 0.5)
_ = plt.xlabel('Intensity Value')
_ = plt.ylabel('Count')
_ = plt.legend(['Total', 'Red_Channel', 'Green_Channel', 'Blue_Channel'])
plt.show()

import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('C:/Users/DELL/Downloads/Imaage/Image-Encryption-and-Authentication/Pratyush.png', -1)
cv2.imshow('Lena',img)

color = ('b','g','r')
for channel,col in enumerate(color):
    histr = cv2.calcHist([img],[channel],None,[256],[0,256])
    plt.plot(histr,color = col)
    plt.xlim([0,256])
plt.title('Histogram for color scale picture')
plt.show()

while True:
    k = cv2.waitKey(0) & 0xFF     
    if k == 27: break             # ESC key to exit 
cv2.destroyAllWindows()