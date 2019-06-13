import os
import excel_IO
import file_IO
import shutil


class Sheet:
    def __init__(self, checkFor):
        self.length = len(checkFor)
        self.title = [""] * self.length
        self.year = [""] * self.length
        self.volume = [""] * self.length
        self.start = [""] * self.length
        self.end = [""] * self.length
        self.DOI = [""] * self.length
        self.PII = [""] * self.length
        self.location = [""] * self.length
        self.accuracy = [""] * self.length
        self.extra = {}


class Journal:
    def __init__(self):
        self.metadata = "./5_Metadata"
        self.folder = "./1_JournalCorpus_txt/"
        self.destination = "./Not_Found"
        self.parent = os.listdir(self.folder)[1:]
        self.metaList = list()
        self.listOfFiles = list()
        self.sizes = list()
        self.extra_loc = None
        self.checkFor = None
        self.sheet = None
        self.extra_val = []

    def fillJournalList(self):
        for root, _, files in os.walk(self.metadata):
            for file in files:
                if not (file == ".DS_Store" or file == "_DS_Store"):
                    self.metaList += [os.path.join(root, file)]

    def fillFolderList(self, fileNum, deep=False):
        self.fillJournalList()
        for i, exl in enumerate(self.metaList):
            if i != fileNum:
                continue
            elif deep == True:
                path = self.folder
            else:
                path = self.folder + self.parent[i]
            for dirpath, _, filenames in os.walk(path):
                for file in filenames:
                    if not (
                        file == ".DS_Store"
                        or file == "_DS_Store"
                        or file == "DEVONtech_storage"
                    ):
                        self.listOfFiles += [os.path.join(dirpath, file)]
            self.exl = exl
            self.checkFor = excel_IO.readMeta(exl)
            self.sheet = Sheet(self.checkFor)

    def findSizes(self, fileNum, deep=False):
        self.fillFolderList(fileNum, deep)
        for file in self.listOfFiles:
            size = int(os.stat(file).st_size)
            if size < 3000:
                self.sizes.append(size)
            elif size > 3000 and size < 6000:
                self.sizes.append(int(size * 2 / 3))
            else:
                self.sizes.append(int(size / 3))

    def searchFolder(self, title=False, year=True):
        for index, val in enumerate(self.checkFor):
            if val in self.extra_val:
                continue
            self.sheet.title[index] = val[0]
            self.sheet.year[index] = val[1]
            self.sheet.volume[index] = val[2]
            self.sheet.start[index] = val[3]
            self.sheet.end[index] = val[4]
            self.sheet.DOI[index] = val[5]
            self.sheet.PII[index] = val[6]
            maxAcc = 0
            loc = ""
            j = 0
            for target, size in zip(self.listOfFiles, self.sizes):
                if j != val[1]:
                    j = val[1]
                    print(j)
                if not str(val[1]) in target and year:
                    continue
                else:
                    link, acc, found = file_IO.readFile(target, size, val)
                    if acc > maxAcc and found:
                        loc = link
                        maxAcc = acc
                if (maxAcc > 19 and not title) or (maxAcc < 19 and title):
                    self.sheet.extra[val] = loc
                    if len(loc) > 2:
                        self.sheet.location[index] = os.path.relpath(loc)
                    else:
                        self.sheet.location[index] = loc
                    self.sheet.accuracy[index] = maxAcc
                elif maxAcc > 19 and title:
                    self.sheet.location[index] = None
                    self.sheet.accuracy[index] = None
            self.extra_val = set(self.sheet.extra.keys())
            self.extra_loc = set(self.sheet.extra.values())

    def notFound(self, title=False):
        if title:
            self.destination = "./Title"
        for srcfile in self.listOfFiles:
            if not title and not srcfile in self.extra_loc:
                assert not os.path.isabs(srcfile)
                dstdir = os.path.join(self.destination, os.path.dirname(srcfile))
                os.makedirs(dstdir, exist_ok=True)
                shutil.copy(srcfile, dstdir)

    def writeExcel(self):
        excel_IO.writeMeta(
            self.exl,
            self.sheet.title,
            self.sheet.year,
            self.sheet.volume,
            self.sheet.start,
            self.sheet.end,
            self.sheet.DOI,
            self.sheet.location,
            self.sheet.accuracy,
        )

    def singleNoTitle(self, num, deep=False, title=False):
        self.findSizes(num, deep)
        self.searchFolder(title)
        self.searchFolder(title,year=False)
        self.notFound(title)
        self.writeExcel()

    def simpleSearch(self, deep=False, title=False):
        for num in range(10):
            self.singleNoTitle(num, deep, title)

    def deepSearch(self):
        self.simpleSearch()
        self.folder = self.destination
        self.simpleSearch(deep=True)
        # self.simpleSearch(title=True)
    
    def titleSearch(self, num, deep=False, title=True):
        self.singleNoTitle(num,deep)
        self.searchFolder(title)
        self.notFound(title)
        self.writeExcel()

if __name__ == "__main__":
    journal = Journal()
    journal.deepSearch()
