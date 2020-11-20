import os
from datetime import time as dt

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json")) as dataFile:
    data = eval(dataFile.read())

def getCRS(name):
    for station in data:
        if data[station]["name"] == name:
            return station
    raise Exception("No CRS code found.")
def getName(crs):
    if crs in data:
        return data[crs]["name"]
    else:
        raise Exception("CRS code invalid.")
def getLink(crs):
    if crs in data:
        return data[crs]["link"]
    else:
        raise Exception("CRS code invalid.")

def timeParse(time):
    split = [int(time[0:2]), int(time[2:4])]
    return dt(split[0], split[1])

def search(query):
    results = []
    if len(query) < 2:
        return results
    for station in data:
        if query.lower() in data[station]["name"].lower():
            results.append(data[station]["name"])
    return results