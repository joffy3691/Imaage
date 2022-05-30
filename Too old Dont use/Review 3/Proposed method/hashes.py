import imagehash
from PIL import Image

def ahash(image,hash_size=8):
    im = Image.open(image)
    hashd = imagehash.average_hash(im)
    return hashd

def phash(image,hash_size=8):
    im = Image.open(image)
    hashd = imagehash.phash(im)
    return hashd

def dhash(image,hash_size=8):
    im = Image.open(image)
    hashd = imagehash.dhash(im)
    return hashd

def whash(image,hash_size=8):
    im = Image.open(image)
    hashd = imagehash.whash(im)
    return hashd

def chash(image):
    im = Image.open(image)
    hashd = imagehash.colorhash(im)
    return hashd

