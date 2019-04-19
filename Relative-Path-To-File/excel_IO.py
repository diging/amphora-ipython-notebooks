import pandas as pd
from math import isnan
from pandas import ExcelWriter
from pandas import ExcelFile

def readMeta(fileName):
    df = pd.read_excel(fileName)
    titles = df["Title"]
    years = df["Year"]
    volumes = df["Volume"]
    start = df["Page start"]
    end = df["Page end"]
    dois = df["DOI"]
    values = []
    for val in zip(titles,years,volumes,start,end,dois):
        if isinstance(val[5],str):
            try:
                pii = tuple([(str(val[5]).split('/'))[1]])
            except:
                print(str(val[5]))
        elif isnan(val[5]):
            pii = tuple([str("")])
        val += pii
        # print(val + pii)
        if isinstance(val[2],str):
            val = (val[0], val[1], str(val[2]), val[3], val[4], val[5], val[6])
        elif not isnan(val[2]):
            val = (val[0], val[1], int(val[2]), val[3], val[4], val[5], val[6])
        # print(val)
        values.append(val)
    return values

def writeMeta(filename,title,year,volume,start,end,DOI,loc,acc):
    df = pd.DataFrame(
        {
            "Title"     : title,
            "Year"      : year,
            "Volume"    : volume,
            "Page Start": start,
            "Page End"  : end,
            "DOI"       : DOI,
            "Location"  : loc,
            "Accuracy"  : acc
        }
    )
    with ExcelWriter(filename, mode="a") as writer:
        df.to_excel(writer)
        writer.save()