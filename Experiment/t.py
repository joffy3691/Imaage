import os, binascii
from backports.pbkdf2 import pbkdf2_hmac
import matplotlib.pyplot as plt
from PIL import Image
import hashlib
my_img = Image.open('C:/Users/vishn/PycharmProjects/imo/dtjdtg/Image-Encryption-and-Authentication/Microsoft_Excel_2013_logo_with_background.png')
# cv2_imshow(my_img)
plt.imshow(my_img)
pix = my_img.load()
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


length = 20
P = generatePrimeNumber(length)
Q = generatePrimeNumber(length)
while(Q==P):
    Q = generatePrimeNumber(length)

print(P)
print(Q)

# Step 2: Calculate N=P*Q and Euler Totient Function = (P-1)*(Q-1)
N = P * Q
eulerTotient = (P - 1) * (Q - 1)
print(N)
print(eulerTotient)


# Step 3: Find E such that GCD(E,eulerTotient)=1(i.e., e should be co-prime) such that it satisfies this condition:-  1<E<eulerTotient

def GCD(a, b):
    if a == 0:
        return b;
    return GCD(b % a, a)


E = generatePrimeNumber(4)
while GCD(E, eulerTotient) != 1:
    E = generatePrimeNumber(4)
print(E)


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


D = gcdExtended(E, eulerTotient)
print("D ")
print(D)

row, col = my_img.size[0], my_img.size[1]
enc = [[0 for x in range(3000)] for y in range(3000)]

key = input()
size = my_img.size
mod = min(size)
print(mod)
enc_key = key
salt = binascii.unhexlify('aaef2d3f4d77ac66e9c5a6c3d8f921d1')
passwd = enc_key.encode("utf8")
key = pbkdf2_hmac("sha256", passwd, salt, 50, 2048)
print("Derived key:", binascii.hexlify(key))
key=binascii.hexlify(key)
key=str(key, 'UTF-8')
print(key);
key_length = len(key)
key_array = []
key_sum = sum(key_array)
key_arra = []
for key in key:
    key_arra.append(ord(key) % mod)
for i in range(len(key_arra) - 5):
    # adding the alternate numbers
    sum = key_arra[i] + key_arra[i + 1]+key_arra[i + 2]+key_arra[i + 3]+key_arra[i + 4]+key_arra[i + 5]
    key_array.append(sum % mod)
print(key_array)
res = []
#for i in key_array:
#    if i not in res:
#        res.append(i)

for q in range(size[0]):
    for r in range(size[1]):
        i =1
        reds = pix[q, r][0] ^ pix[(q - i) % size[0], (r - i) % size[1]][0]
        greens = pix[q, r][1] ^ pix[(q - i) % size[0], (r - i) % size[1]][1]
        blues = pix[q, r][2] ^ pix[(q - i) % size[0], (r - i) % size[1]][2]
        pix[q, r] = (reds, greens, blues)
        reds = pix[q, r][0] ^ (key_array[q*r%len(key_array)] ** 2 % 255)
        greens = pix[q, r][1] ^ (key_array[q*r%len(key_array)] ** 2 % 255)
        blues = pix[q, r][2] ^ (key_array[q*r%len(key_array)] ** 2 % 255)
        pix[q, r] = (reds, greens, blues)
plt.imshow(my_img)
plt.show()

key = input()
enc_key = key
salt = binascii.unhexlify('aaef2d3f4d77ac66e9c5a6c3d8f921d1')
passwd = enc_key.encode("utf8")
key = pbkdf2_hmac("sha256", passwd, salt, 50, 2048)
print("Derived key:", binascii.hexlify(key))
key=binascii.hexlify(key)
key=str(key, 'UTF-8')
print(key);
key_length = len(key)
key_array = []
key_arra = []
for key in key:
    key_arra.append(ord(key) % mod)
for i in range(len(key_arra) - 5):
    # adding the alternate numbers
    sum = key_arra[i] + key_arra[i + 1]+key_arra[i + 2]+key_arra[i + 3]+key_arra[i + 4]+key_arra[i + 5]
    key_array.append(sum % mod)
res = []
for i in key_array:
    if i not in res:
        res.append(i)
print(key_array)
i=size[0]*size[1]
i=i-1
for q in range(size[0] - 1, -1, -1):
    for r in range(size[1] - 1, -1, -1):
        i = 1
        reds = pix[q, r][0] ^pix[(q-i)%size[0],(r-i)%size[1]][0]
        greens = pix[q, r][1]^pix[(q-i)%size[0],(r-i)%size[1]][1]
        blues = pix[q, r][2] ^ pix[(q-i)%size[0],(r-i)%size[1]][2]
        pix[q, r] = (reds, greens, blues)
        reds = pix[q, r][0] ^ (key_array[q*r%len(key_array)] ** 2 % 255)
        greens = pix[q, r][1] ^ (key_array[q*r%len(key_array)] ** 2 % 255)
        blues = pix[q, r][2] ^ (key_array[q*r%len(key_array)] ** 2 % 255)
        pix[q, r] = (reds, greens, blues)


plt.imshow(my_img)
plt.show()