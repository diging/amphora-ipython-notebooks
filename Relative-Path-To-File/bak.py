import os
import os.path

def readFile(filename,size, val):
    acc = 0
    found = False
    fileObj = open(filename, "r")
    data = fileObj.read(size)
    fileObj.close()
    data = data.replace(" ","")    
    if len(str(val[5])) > 6 and str(val[5]) in data:
        acc += 40
        doi_found = True
    elif len(str(val[6])) > 6 and str(val[6]) in data:
        acc += 40
        found = True
    if str(val[0]).replace(" ","") in data:
        acc += 20
        # found = True

    if len(str(val[3])) < 4:
        id1 = str(val[2])+ "(" + str(val[1]) + ")"
        id2 = ""
    if len(str(val[3])) > 4 and len(str(val[4])) < 4:
        id1 = str(val[2])+ "(" + str(val[1]) + ")" + str(val[3])
        id2 = ""
    else:    
        id1 = str(val[2])+ "(" + str(val[1]) + ")" + str(val[3]) + "-" + str(val[4])
        id2 = str(val[2])+ "(" + str(val[1]) + ")" + str(val[3]) + "?" + str(val[4])
        
    if id1 in data or id2 in data:
        acc += 40
        found = True
    return (filename, acc, found)

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