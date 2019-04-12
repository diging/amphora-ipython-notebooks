import pandas as pd
from math import isnan
from pandas import ExcelWriter
from pandas import ExcelFile

def readMeta(fileName):
    df = pd.read_excel(fileName)
    titles = df["Title"]
    years = df["Year"]
    volumes = df["Volume"]
    dois = df["DOI"]
    values = []
    for val in zip(titles,years,volumes,dois):
        if isinstance(val[3],str):
            try:
                pii = tuple([(str(val[3]).split('/'))[1]])
            except:
                print(str(val[3]))
        elif isnan(val[3]):
            pii = tuple([str("")])
        val += pii
        # print(val + pii)
        if val[2] == '':
            val = (val[0], val[1], str(val[2]), val[3], val[4])
        elif not isnan(val[2]):
            val = (val[0], val[1], int(val[2]), val[3], val[4])
        # print(val)
        values.append(val)
    return values

def writeMeta(filename,title,year,volume,DOI,loc,acc):
    df = pd.DataFrame(
        {
            "Title"     : title,
            "Year"      : year,
            "Volume"    : volume,
            "DOI"       : DOI,
            "Location"  : loc,
            "Accuracy"  : acc
        }
    )
    with ExcelWriter(filename, mode="a") as writer:
        df.to_excel(writer)
        writer.save()