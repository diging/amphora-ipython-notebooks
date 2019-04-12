import os
import excel_IO
import file_IO

metadata = "./5_Metadata"
folder = "./1_JournalCorpus_txt/"
parent = os.listdir(folder)[1:]

metaList = list()

for root, dirs, files in os.walk(metadata):
    
    for file in files:
        
        if file == '.DS_Store' or file == '_DS_Store':
            continue
        
        metaList += [os.path.join(root,file)]    

# print(metaList)

for i, exl in enumerate(metaList):
    
    listOfFiles = list()
    
    for dirpath, dirnames, filenames in os.walk(folder + parent[i]):
        
        for file in filenames:
            
            if file == '.DS_Store' or file == '_DS_Store':
                continue
            
            listOfFiles += [os.path.join(dirpath, file)]
    
    sizes = list()
    sizes += [int(os.stat(file).st_size / 3) for file in listOfFiles]
    
    # print(listOfFiles[0], sizes[0])
    # break

    checkFor = (excel_IO.readMeta(exl))

    title = [""] * len(checkFor)
    year = [""] * len(checkFor)
    volume = [""] * len(checkFor)
    DOI = [""] * len(checkFor)
    PII = [""] * len(checkFor)
    location = [""] * len(checkFor)
    accuracy = [""] * len(checkFor)
    
    for index,val in enumerate(checkFor):
        
        title[index] = val[0]
        year[index] = val[1]
        volume[index] = val[2]
        DOI[index] = val[3]
        PII[index] = val[4]
        maxAcc = 0
        loc = ''
        j = 0

        for target, size in zip(listOfFiles, sizes):

            if j != val[1]:
                j = val[1]
                print(j)

            if not str(val[1]) in target:
                continue
            
            else:
                link, acc, found = file_IO.readFile(target, size, val)
                
                if acc > maxAcc and found:
                    loc = link
                    maxAcc = acc
                    # if maxAcc > 64:
                    #     print(val, loc, maxAcc)
            
            if maxAcc > 44:
                
                if(loc):
                    relative_loc = os.path.relpath(loc)
                    location[index]=(relative_loc)

                    #remove the file
                    
                    # os.remove(target[0])

                    # listOfFiles.remove(i)
                    # sizes.remove(i)

                else:
                    location[index]=(loc)
                
                accuracy[index]=(maxAcc)
    
    # print(location,accuracy)
    excel_IO.writeMeta(exl,title,year,volume,DOI,location,accuracy)
    break