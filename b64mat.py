from base64 import b64encode, b64decode
import numpy as np

def intreps_to_bytes(s):
    """Converts integer representations [0-255] back to bytes."""
    
    # TODO: check signed vs unsigned/encoding
    v = int(s, 2)
    b = bytearray()
    while v:
        b.append(v & 0xff)
        v >>= 8
    return bytes(b[::-1])

def ftm(path, m):
    """Converts binary file to matrix of Base64 byte's integer representations, dimensions m*m*-1"""
    with open(path, "rb") as f:
        data1 = f.read()
    
    data2 = b64encode(data1)
    
    l = len(data2)  # length of data
    r = l % m**2  # remainder in last m*m matrix
    p = m**2 - r  # amount of padding to fill last m*m matrix
    data3 = b''.join([data2, p*b'='])  # pad
    
    array1 = np.fromiter(data3, dtype=int)  # get integer from bytes literal (by iterating)
    array2 = np.reshape(array1, (m,m,-1)) # get array of integers into m*m matrix shape

    return array2


def mtf(matrix, path):
    """Convert matrix of Base64 byte's integer representations back to binary file"""

    data = b''  # create blank byte
    for i in np.ravel(matrix):
        byte = intreps_to_bytes(bin(i))
        data = b''.join([data,byte])

    print(data)
    data2 = b64decode(data)
    with open(path, "wb") as f:
        f.write(data2)





    