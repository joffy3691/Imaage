import time

import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import pandas as pd


# RSA

# STEP 1: Generate Two Large Prime Numbers (p,q) randomly
from random import randrange, getrandbits


def power(a, d, n):
    ans = 1;
    while d != 0:
        if d % 2 == 1:
            ans = ((ans % n) * (a % n)) % n
        a = ((a % n) * (a % n)) % n
        d >>= 1
    return ans;

def poer(a, d, n):
    abc=pow(a,d)
    ans = abc%n;
    return ans;

def MillerRabin(N, d):
    a = randrange(2, N - 1)
    x = power(a, d, N);
    if x == 1 or x == N - 1:
        return True;
    else:
        while (d != N - 1):
            x = ((x % N) * (x % N)) % N;
            if x == 1:
                return False;
            if x == N - 1:
                return True;
            d <<= 1;
    return False;


def is_prime(N, K):
    if N == 3 or N == 2:
        return True;
    if N <= 1 or N % 2 == 0:
        return False;

    # Find d such that d*(2^r)=X-1
    d = N - 1
    while d % 2 != 0:
        d /= 2;

    for _ in range(K):
        if not MillerRabin(N, d):
            return False;
    return True;


def generate_prime_candidate(length):
    # generate random bits
    p = getrandbits(length)
    # apply a mask to set MSB and LSB to 1
    # Set MSB to 1 to make sure we have a Number of 1024 bits.
    # Set LSB to 1 to make sure we get a Odd Number.
    p |= (1 << length - 1) | 1
    return p


def generatePrimeNumber(length):
    A = 4
    while not is_prime(A, 128):
        A = generate_prime_candidate(length)
    return A




# Step 3: Find E such that GCD(E,eulerTotient)=1(i.e., e should be co-prime) such that it satisfies this condition:-  1<E<eulerTotient

def GCD(a, b):
    if a == 0:
        return b;
    return GCD(b % a, a)


# Step 4: Find D.
# For Finding D: It must satisfies this property:-  (D*E)Mod(eulerTotient)=1;
# Now we have two Choices
# 1. That we randomly choose D and check which condition is satisfying above condition.
# 2. For Finding D we can Use Extended Euclidean Algorithm: ax+by=1 i.e., eulerTotient(x)+E(y)=GCD(eulerTotient,e)
# Here, Best approach is to go for option 2.( Extended Euclidean Algorithm.)

def gcdExtended(E, eulerTotient):
    a1, a2, b1, b2, d1, d2 = 1, 0, 0, 1, eulerTotient, E

    while d2 != 1:
        # k
        k = (d1 // d2)

        # a
        temp = a2
        a2 = a1 - (a2 * k)
        a1 = temp

        # b
        temp = b2
        b2 = b1 - (b2 * k)
        b1 = temp

        # d
        temp = d2
        d2 = d1 - (d2 * k)
        d1 = temp

        D = b2

    if D > eulerTotient:
        D = D % eulerTotient
    elif D < 0:
        D = D + eulerTotient

    return D


def Rsa_testing(image_loc,D,N,outputloc):
    my_img = Image.open(image_loc)
    # cv2_imshow(my_img)
    # plt.imshow(my_img)
    pix = my_img.load()
    length = 20
    row, col = my_img.size[0], my_img.size[1]
    data = pd.read_parquet(f'{image_loc}.parquet.gzip')
    array = data.to_numpy()
    array = array[2:]
    array = array.reshape(row, col, 3)

    # Step 6: Decryption
    for i in range(row):
        for j in range(col):
            r, g, b = array[i][j]
            M1 = pow(int(r), D, N)
            M2 = pow(int(g), D, N)
            M3 = pow(int(b), D, N)
            pix[i, j] = (M1, M2, M3)
            #print(pix[i,j])

    my_img.save(f'{outputloc}.tiff')
    # plt.imshow(my_img)
    # plt.show()


loc="RSA-tiff-Enc-4.2.06.tiff"
outputloc="RSA-tiff-Dec-4.2.06.tiff"
N=994788998783
D=271305545891
column = []
column.append((0, 0, 0))
column.append((0, 0, 0))
tic = time.perf_counter()
Rsa_testing(loc,D,N,outputloc)
toc = time.perf_counter()
print(f"Finished Decryption in {toc - tic:0.4f} seconds")