import os
import excel_IO
import file_IO
import shutil

metadata = "./5_Metadata"
folder = "./1_JournalCorpus_txt/"
dest = "./Not_Found"
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
    for file in listOfFiles:
        size = int(os.stat(file).st_size)
        if size < 3000:
            sizes.append(size)
        else:
            sizes.append(int(size/3))
        # sizes.append(int(size/3))
    
    # print(listOfFiles[0], sizes[0])
    # break

    checkFor = (excel_IO.readMeta(exl))

    title       = [""] * len(checkFor)
    year        = [""] * len(checkFor)
    volume      = [""] * len(checkFor)
    start       = [""] * len(checkFor)
    end         = [""] * len(checkFor)
    DOI         = [""] * len(checkFor)
    PII         = [""] * len(checkFor)
    location    = [""] * len(checkFor)
    accuracy    = [""] * len(checkFor)
    extra       = {}
    
    for index,val in enumerate(checkFor):
        
        title[index]    = val[0]
        year[index]     = val[1]
        volume[index]   = val[2]
        start[index]    = val[3]
        end[index]      = val[4]
        DOI[index]      = val[5]
        PII[index]      = val[6]
        maxAcc          = 0
        loc             = ''
        j               = 0

        # if val[1] != 2012:
        #     continue

        for i, (target, size) in enumerate(zip(listOfFiles, sizes)):

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
            
            if maxAcc > 39:

                extra[val] = loc
                
                if(len(loc) > 2):
                    relative_loc = os.path.relpath(loc)
                    location[index]=(relative_loc)

                    # Remove the file
                    # os.remove(target[0])

                    # Remove from the list
                    # listOfFiles.remove(i)
                    # del listOfFiles[i]
                    # sizes.remove(i)
                    # del sizes[i]

                else:
                    location[index]=(loc)
                
                accuracy[index]=(maxAcc)
        
        # Remove val from List
        # del checkFor[index]

    extra_loc = set(extra.values())
    extra_val = set(extra.keys())

    for index,val in enumerate(checkFor):

        if val in extra_val:
            continue

        # if val[1] != 2012:
        #     continue

        title[index]    = val[0]
        year[index]     = val[1]
        volume[index]   = val[2]
        start[index]    = val[3]
        end[index]      = val[4]
        DOI[index]      = val[5]
        PII[index]      = val[6]
        maxAcc          = 0
        loc             = ''
        j               = 0

        for i, (target, size) in enumerate(zip(listOfFiles, sizes)):

            if target in extra_loc:
                continue

            if j != val[1]:
                j = val[1]
                print(j)
            
            link, acc, found = file_IO.readFile(target, size, val)
            
            if acc > maxAcc and found:
                loc = link
                maxAcc = acc
                # if maxAcc > 64:
                #     print(val, loc, maxAcc)
            
            if maxAcc > 39:

                extra[val] = loc
                
                if(loc):
                    relative_loc = os.path.relpath(loc)
                    location[index]=(relative_loc)

                    # Remove the file
                    # os.remove(target[0])

                    # Remove from the list
                    # listOfFiles.remove(i)
                    # del listOfFiles[i]
                    # sizes.remove(i)
                    # del sizes[i]

                else:
                    location[index]=(loc)
                
                accuracy[index]=(maxAcc)

    extra_loc = set(extra.values())

    for srcfile in listOfFiles:
        if not srcfile in extra_loc:
            assert not os.path.isabs(srcfile)
            dstdir =  os.path.join(dest, os.path.dirname(srcfile))
            os.makedirs(dstdir, exist_ok=True)
            shutil.copy(srcfile, dstdir)

    # print(location,accuracy)
    excel_IO.writeMeta(exl,title,year,volume,start,end,DOI,location,accuracy)
    break