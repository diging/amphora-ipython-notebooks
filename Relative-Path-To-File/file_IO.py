# import os
# import os.path

# def readFile(filename,size, val):
#     acc = 0
#     found = False
#     fileObj = open(filename, "r")
#     data = fileObj.read(size)
#     fileObj.close()
#     data = data.replace(" ","")
#     doi = str(val[5])
#     pii = str(val[6])
#     if len(doi) > 6 and doi in data:
#         acc += 40
#         doi_found = True
#     elif len(pii) > 6 and pii in data:
#         acc += 40
#         found = True
#     if str(val[0]).replace(" ","") in data:
#         acc += 20
#         # found = True
#     first = str(val[3])
#     last = str(val[4])
#     if  last != "":
#         id1 = first + "-" + last
#         id2 = first + "?" + last
#     else:
#         id1 = id2 = first
#     if str(int(val[1])) in data:
#         acc += 5
#         if str(val[2]) in data:
#             acc += 15
#             if id1 in data or id2 in data:
#                 acc += 20
#                 found = True
#     return (filename, acc, found)

import os
import os.path

def readFile(filename,size, val):
    acc = 0
    found = False
    try:
        fileObj = open(filename, "r")
        data = fileObj.read(size)
    except UnicodeDecodeError:
        print(filename)
        fileObj = open(filename, "r", encoding = "ISO-8859-1")
        data = fileObj.read(size)
    fileObj.close()
    data = data.replace(" ","")
    doi = str(val[5])
    pii = str(val[6])
    first = str(val[3])
    last = str(val[4])
    if len(doi) > 6 and doi in data:
        acc += 40
        found = True
    elif len(pii) > 6 and pii in data:
        acc += 40
        found = True
    if str(val[0]).replace(" ","") in data:
        acc += 20
        # found = True

    if len(first) < 4:
        id1 = str(val[2])+ "(" + str(val[1]) + ")"
        id2 = ""
    if len(first) > 4 and len(last) < 4:
        id1 = str(val[2])+ "(" + str(val[1]) + ")" + first
        id2 = ""
    else:    
        id1 = str(val[2])+ "(" + str(val[1]) + ")" + first + "-" + last
        id2 = str(val[2])+ "(" + str(val[1]) + ")" + first + "?" + last
        
    if id1 in data or id2 in data:
        acc += 40
        found = True
    return (filename, acc, found)