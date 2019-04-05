import os
import os.path

def readFile(filename,size, val):
    acc = 0
    fileObj = open(filename, "r")
    data = fileObj.read(size)
    if str(val[0]) in data:
        acc += 35
    if str(val[1]) in data:
        acc += 5
    if str(val[2]) in data:
        acc += 15
    if str(val[3]) in data:
        acc += 45
    return (filename, acc)