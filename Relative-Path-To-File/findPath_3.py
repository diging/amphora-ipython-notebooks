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

    def setSheet(self, val, index):
        self.title[index] = val[0]
        self.year[index] = val[1]
        self.volume[index] = val[2]
        self.start[index] = val[3]
        self.end[index] = val[4]
        self.DOI[index] = val[5]
        self.PII[index] = val[6]

    def setLocation(self, location, accuracy, index):
        self.location[index] = location
        self.accuracy[index] = accuracy

    def getSheet(self):
        return (
            self.title,
            self.year,
            self.volume,
            self.start,
            self.end,
            self.DOI,
            self.location,
            self.accuracy,
        )

    def setExtra(self, value, location):
        self.extra[value] = location

    def getExtra(self):
        values = set(self.extra.keys())
        locations = set(self.extra.values())
        return (values, locations)


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
        self.extra_val = set([])

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
                print("SEARCHING FOR: {} (Deep)".format(exl))
                path = self.destination
            else:
                print("SEARCHING FOR: {}".format(exl))
                path = self.folder + self.parent[i]
            print("SEARCHING IN: {}".format(path))
            for dirpath, _, filenames in os.walk(path):
                for file in filenames:
                    if not (
                        file == ".DS_Store"
                        or file == "_DS_Store"
                        or file == "DEVONtech_storage"
                    ):
                        self.listOfFiles += [os.path.join(dirpath, file)]
            self.exl = exl
            try:
                self.checkFor = excel_IO.readMeta(exl)
                print("SUCCESS: Excel file read.")
            except:
                print("FAILED: Excel file read.")
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

    def searchFolder(self, title=False, year=True, deep=False):
        folder_year = 0
        if deep:
            directory = os.pardir
        else:
            directory = os.curdir
        for index, val in enumerate(self.checkFor):
            if val in self.extra_val:
                continue
            self.sheet.setSheet(val, index)
            maxAcc = 0
            loc = ""
            for target, size in zip(self.listOfFiles, self.sizes):
                if folder_year != val[1]:
                    folder_year = val[1]
                    print(folder_year)
                if not str(val[1]) in target and year:
                    continue
                else:
                    try:
                        link, acc, found = file_IO.readFile(target, size, val)
                        if acc > maxAcc and found:
                            loc = link
                            maxAcc = acc
                    except:
                        print("FAILED: {} read error.".format(target))
                if (maxAcc > 19 and not title) or (maxAcc < 19 and title):
                    self.sheet.setExtra(val, loc)
                    if len(loc) > 2:
                        self.sheet.setLocation(
                            os.path.relpath(loc, start=directory), maxAcc, index
                        )
                    else:
                        self.sheet.setLocation(loc, maxAcc, index)
                elif maxAcc > 19 and title:
                    self.sheet.setLocation(None, None, index)
            self.extra_val, self.extra_loc = self.sheet.getExtra()

    def notFound(self, title=False):
        if title:
            self.destination = "./Title"
        for srcfile in self.listOfFiles:
            if not title and not srcfile in self.extra_loc:
                assert not os.path.isabs(srcfile)
                dstdir = os.path.join(self.destination, os.path.dirname(srcfile))
                os.makedirs(dstdir, exist_ok=True)
                shutil.copy(srcfile, dstdir)
        print("SUCCESS: Create Not_Found folder.")

    def writeExcel(self):
        try:
            excel_IO.writeMeta(self.exl, *self.sheet.getSheet())
            print("SUCCESS: Excel file write.")
        except:
            print("FAILED: Excel file write.")

    def singleSearch(self, num, deep=False, title=False):
        self.findSizes(num, deep)
        self.searchFolder(title)
        if not deep:
            print("Pass 2:")
            self.searchFolder(title, year=False)
            self.notFound(title)
        self.writeExcel()

    def simpleSearch(self, deep=False, title=False):
        for num in range(10):
            self.singleSearch(num, deep, title)

    def deepSearch(self):
        self.simpleSearch()
        self.simpleSearch(deep=True)
        # self.simpleSearch(title=True)

    def titleSearch(self, num, deep=False, title=True):
        self.singleSearch(num, deep)
        self.searchFolder(title)
        self.notFound(title)
        self.writeExcel()


if __name__ == "__main__":
    journal = Journal()
    # journal.deepSearch()
    journal.singleSearch(num=3)
    journal.singleSearch(num=3, deep=True)
