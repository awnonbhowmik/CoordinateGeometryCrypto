import numpy as np
import math
from time import time

def sq_root_mod_n(n, p):
    n = n % p
    for x in range(2, p):
        if ((x * x) % p == n):
            return x
    return 0

def koblitz_encoder(plainText, elliptic_a, elliptic_b):
    ord_lst = [ord(ch) for ch in plainText]
    k = 20
    p = 751

    x_coords = []
    y_coords = []
    encoded_points = []

    for m in ord_lst:
        for j in range(1, k):
            x_m = m * k + j
            n = pow(x_m, 3) + elliptic_a * x_m + elliptic_b
            y_m = sq_root_mod_n(n, p)
            if (y_m != 0):
                x_coords.append(x_m)
                y_coords.append(y_m)
                encoded_points.append([x_m, y_m])
                break

    encoded = []
    for i in range(len(x_coords)):
        encoded.append([x_coords[i], y_coords[i]])
        #print('{},{}'.format(x_coords[i], y_coords[i]))
    return encoded


def koblitz_decoder(encoded_points):
    decoded_Msg = []
    k = 20
    for i in range(len(encoded_points)):
        d = math.floor((encoded_points[i][0] - 1) / k)
        #print(type(d))
        decoded_Msg.append(abs(d))

    # print(''.join(decoded_Msg))
    return ''.join(map(lambda x: chr(x),decoded_Msg))

def encrypt(lst_pts,h,k,n):
    for i in range(len(lst_pts)):
        lst_pts[i][0]+=h
        lst_pts[i][1]+=k
    
    theta = n * np.pi / 2
    R = [[int(np.cos(theta)), int(-np.sin(theta))],
         [int(np.sin(theta)), int(np.cos(theta))]]
    
    for i in range(len(lst_pts)):
        lst_pts[i] = np.matmul(lst_pts[i], R)
        lst_pts[i] = lst_pts[i].tolist()

    return lst_pts

def decrypt(enc_pts,h,k,n):
    theta = n * np.pi / 2
    R = [[int(np.cos(theta)), int(-np.sin(theta))],
         [int(np.sin(theta)), int(np.cos(theta))]]
    
    p=[]
    for i in range(len(enc_pts)):
        p.append(np.matmul(np.linalg.inv(R), enc_pts[i]).tolist())
    
    for i in range(len(p)):
        p[i][0] -= h
        p[i][1] -= k
        #p[i]=p[i].tolist()
        
    return p

#msg=input("Enter a message: ")
msg="abcdefghijklmnopqrstuvwxyz"*1000
a,b=map(int,input("\nEnter elliptic curve parameters (a,b): ").split())
h,k=map(int,input("\nEnter change of axes parameters (h,k): ").split())
n=int(input("\nEnter an integer to generate angle of rotation matrix: "))

t=time()
enc=koblitz_encoder(msg,a,b)
#t1=time()-t
#print("\nEncoded:\n{}".format(enc))
#print("\nTime elapsed: {}".format(t1))

#t=time()
encrypted_data=encrypt(enc,h,k,n)
#t1=time()-t
#print("\nEncrypted message:\n{}".format(encrypted_data))
#print("\nTime elapsed: {}".format(t1))

#t=time()
decrypted_data=decrypt(encrypted_data,h,k,n)
#t1=time()-t
#print("\nDecrypted message:\n{}".format(decrypted_data))
#print("\nTime elapsedL {}".format(t1))

#t=time()
dec=koblitz_decoder(decrypted_data)
t1=time()-t
#print("\nDecoded message:\n{}".format(dec))
print("\nTime elapsed: {}".format(t1))
