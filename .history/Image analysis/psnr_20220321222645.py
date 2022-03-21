from math import log10, sqrt
import cv2
import numpy as np

def PSNR(original, compressed):
    mse = np.mean((original - compressed) ** 2)
    if(mse == 0): # MSE is zero means no noise is present in the signal .
                # Therefore PSNR have no importance.
        return 100
    max_pixel = 255.0
    print(sqrt(mse))
    psnr = 20 * log10(max_pixel / sqrt(mse))
    return psnr

original = cv2.imread("C:/Users/DELL/Downloads/Imaage/Enc images/JPG_8bit/enc_image_jpg_8bit_1.jpg")
compressed = cv2.imread("C:/Users/DELL/Downloads/Imaage/Enc images/JPG_8bit/dec_image_jpg_8bit_1.jpg", 1)
value = PSNR(original, compressed)
print(f"PSNR value is {value} dB")
