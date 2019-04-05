import os
import excel_IO
import file_IO

metadata = "./5_Metadata"
folder = "./1_JournalCorpus_txt/"
parent = os.listdir(folder)[1:]
print(parent)

for root, dirs, files in os.walk(metadata):
    for file in files:
        if file == '.DS_Store' or file == '_DS_Store':
            continue
        # print(file)
        i = 0
        exl = (os.path.join(root,file))
        checkFor = (excel_IO.readMeta(exl))
        location = []
        accuracy = []
        for root1, dirs1, files1 in os.walk(folder + parent[i]):
            for val in checkFor:
                maxAcc = 0
                loc = ''
                for file in files1:
                    if file == '.DS_Store' or file == '_DS_Store':
                        continue
                    target = os.path.join(root1, file)
                    size = int(os.stat(target).st_size / 3)
                    link, acc = file_IO.readFile(target, size, val)
                    if acc > maxAcc:
                        loc = link
                        maxAcc = acc
                        # print(val, link, acc)
            if(loc):
                relative_loc = os.path.relpath(loc)
                location.append(relative_loc)
            else:
                location.append(loc)
            accuracy.append(maxAcc)
        excel_IO.writeMeta(exl,location,accuracy)