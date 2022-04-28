from base64 import b64encode, b64decode
import re
import numpy as np

# RFC6468 Section 4: Base 64 Alphabet
# Technically, "=":64 isn't present in the RFC4648 alphabet as the padding is a control character...
# ...but as we need this all to be numbers, and we don't have a genuine 64-character limit, we can
# get away with having range 65 characters (0-64) here.
dict_c2i = {
    "A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7, "I": 8, "J": 9,
    "K":10, "L":11, "M":12, "N":13, "O":14, "P":15, "Q":16, "R":17, "S":18, "T":19,
    "U":20, "V":21, "W":22, "X":23, "Y":24, "Z":25, "a":26, "b":27, "c":28, "d":29,
    "e":30, "f":31, "g":32, "h":33, "i":34, "j":35, "k":36, "l":37, "m":38, "n":39,
    "o":40, "p":41, "q":42, "r":43, "s":44, "t":45, "u":46, "v":47, "w":48, "x":49,
    "y":50, "z":51, "0":52, "1":53, "2":54, "3":55, "4":56, "5":57, "6":58, "7":59,
    "8":60, "9":61, "+":62, "/":63, "=":64
}
dict_i2c = {v: k for k, v in dict_c2i.items()}  # same but for the inverse process

def chars_to_ints(chars):
    if re.search("[^A-Za-z0-9\/\+=]", chars):  # TODO regex is not my strong suit, this needs to be unit tested
        raise ValueError("Invalid character not found in RFC4648 Base64 Alphabet")  # this *should* prevent any KeyErrors in the dict
    else:
        ints = []
        for c in chars:
            i = dict_c2i[c]
            ints.append(i)
        return ints

def ints_to_chars(ints):
    chars_list = []
    for i in ints:
        if type(i) != np.int64:
            raise TypeError("Invalid type, needs to be an int.", i, type(i))
        if i <0 or i > 65:
            raise ValueError("Invalid int, needs to be in range 0-65")
        else:
            c = dict_i2c[i]
            chars_list.append(c)
        chars_string = ''.join(chars_list)
    return chars_string

def file_to_matrix(path, m):
    """Converts binary file to matrix of Base64 byte's integer representations, dimensions (m,m)"""
    with open(path, "rb") as f:
        data1 = f.read()
    
    data2 = b64encode(data1)  # encode to b64 bytes
    
    l = len(data2)  # length of data
    r = l % m**2  # remainder in last m*m matrix
    p = m**2 - r  # amount of padding to fill last m*m matrix
    data3 = b''.join([data2, p*b'='])  # pad
    
    array1 = chars_to_ints(data3.decode('ascii'))
    # TODO checks for file size
    array2 = np.reshape(array1, (m,m)) # get array of integers into m*m matrix shape

    print(array2.shape)
    return array2


def matrix_to_file(matrix, path):
    """Convert matrix of Base64 byte's integer representations back to binary file"""

    ints = np.ravel(matrix)
    chars = ints_to_chars(ints)
    data = chars.encode('ascii')  # get B64 bytes
    data2 = b64decode(data)  # decode from B64 back to real binary
    with open(path, "wb") as f:
        f.write(data2)  # write binary back as a file
    print(path)