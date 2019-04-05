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
        if isinstance(val[3], str):
            if not isnan(val[2]):
                val = (val[0], val[1], int(val[2]), val[3])
            values.append(val)
    return values

def writeMeta(filename, loc, acc):
    df = pd.DataFrame(
        {
        "Location" : loc,
        "Accuracy" : acc
        }
    )
    with ExcelWriter(filename, mode="a") as writer:
        df.to_excel(writer)
        writer.save()