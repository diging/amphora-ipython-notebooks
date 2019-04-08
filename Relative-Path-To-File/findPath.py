import os
import excel_IO
import file_IO

metadata = "./5_Metadata"
folder = "./1_JournalCorpus_txt/"
parent = os.listdir(folder)[1:]
# print(parent)

for root, dirs, files in os.walk(metadata):
    for file in files:
        if file == '.DS_Store' or file == '_DS_Store':
            continue
        print(file)
        i = 0
        exl = (os.path.join(root,file))
        checkFor = (excel_IO.readMeta(exl))
        title = [""] * len(checkFor)
        year = [""] * len(checkFor)
        volume = [""] * len(checkFor)
        DOI = [""] * len(checkFor)
        location = [""] * len(checkFor)
        accuracy = [""] * len(checkFor)
        for root1, dirs1, files1 in os.walk(folder + parent[i]):
            for index,val in enumerate(checkFor):
                title[index]=val[0]
                year[index]=val[1]
                volume[index]=val[2]
                DOI[index]=val[3]
                maxAcc = 0
                loc = ''
                for file in files1:
                    if file == '.DS_Store' or file == '_DS_Store':
                        continue
                    target = os.path.join(root1, file)
                    size = int(os.stat(target).st_size / 3)
                    link, acc, found = file_IO.readFile(target, size, val)
                    if acc > maxAcc and found:
                        loc = link
                        maxAcc = acc
                        # if maxAcc > 64:
                            # print(val, loc, maxAcc)
                if maxAcc > 50:
                    if(loc):
                        relative_loc = os.path.relpath(loc)
                        location[index]=(relative_loc)
                    else:
                        location[index]=(loc)
                    accuracy[index]=(maxAcc)
        print(location,accuracy)
        excel_IO.writeMeta(exl,location,accuracy)
        # i += 1
        break