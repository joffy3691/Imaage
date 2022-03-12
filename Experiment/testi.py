import binascii
from backports.pbkdf2 import pbkdf2_hmac
E=435
N=255
c=0
b=set()
enc_key = input()
salt = binascii.unhexlify('aaef2d3f4d77ac66e9c5a6c3d8f921d1')
passwd = enc_key.encode("utf8")
key = pbkdf2_hmac("sha256", passwd, salt, 50, 256)
# print("Derived key:", binascii.hexlify(key))
key = binascii.hexlify(key)
key = str(key, 'UTF-8')
# print(key);
key_length = len(key)
key_array = []
key_sum = sum(key_array)
key_arra = []
for key in key:
    key_arra.append(ord(key) % 256)
for j in range(1000):
    a=[]
    enc_key = str(j)
    salt = binascii.unhexlify('aaef2d3f4d77ac66e9c5a6c3d8f921d1')
    passwd = enc_key.encode("utf8")
    key = pbkdf2_hmac("sha256", passwd, salt, 50, 256)
    # print("Derived key:", binascii.hexlify(key))
    key = binascii.hexlify(key)
    key = str(key, 'UTF-8')
    # print(key);
    key_length = len(key)
    key_array = []
    key_sum = sum(key_array)
    key_arra1 = []
    for key in key:
        key_arra1.append(ord(key) % 256)
    for i in range(256):
        C1 = pow( key_arra[i],key_arra1[i], N)
        a.append(C1)
    if str(a) in b:
        print(j," ",a)
    b.add(str(a))

print(len(b))