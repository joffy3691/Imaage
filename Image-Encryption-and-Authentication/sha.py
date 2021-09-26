import sys
import hashlib
from PIL import Image
from matplotlib import pyplot as plt
import imagehash

im = Image.open('C:/Users/vishn/PycharmProjects/imo/dtjdtg/Image-Encryption-and-Authentication/Microsoft_Excel_2013_logo_with_background.png')


if sys.version_info < (3, 6):
    import sha3

# initialize a string
str = "GeeksforGeeks"

# encode the string
encoded_str = str.encode()

# create sha3-384 hash objects
obj_sha3_384 = hashlib.sha3_384(im)

# print in hexadecimal
print("\nSHA3-384 Hash: ", obj_sha3_384.hexdigest())