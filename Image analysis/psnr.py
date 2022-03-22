from math import log10, sqrt
import cv2
import numpy as np

def RMSE(loc1, loc2):
    original = cv2.imread(loc1)
    compressed = cv2.imread(loc2, 1)
    mse = np.mean((original - compressed) ** 2)
    # if(mse == 0): # MSE is zero means no noise is present in the signal .
    #             # Therefore PSNR have no importance.
    #     return 100
    # max_pixel = 255.0
    print("RMSE :",mse)
    # psnr = 20 * log10(max_pixel / sqrt(mse))
    # print(f"PSNR value is {psnr} dB")
    # return psnr

#
# value = PSNR(original, compressed)
# print(f"PSNR value is {value} dB")
