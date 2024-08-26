import pandas as pd
from tqdm import tqdm

from ConnectionDir.ConnectionFile import *
from QueryDir.ApexPOSRetailQuery import *


def getStaffProductivity(SDate,EDate):
    Query = getStaffProductivityQuery(SDate,EDate)
    POSConnection = getPOSConnection()

    chunks = pd.read_sql(Query, con=POSConnection, chunksize=30000)

    df = pd.DataFrame()
    for chunk in tqdm(chunks):
        df = pd.concat([df, chunk])
    return df

def getZoneList():
    Query = getZoneListQuery()
    POSConnection = getPOSConnection()
    df = pd.read_sql(Query, con=POSConnection)
    return df


def getAreaList():
    Query = getAreaListQuery()
    POSConnection = getPOSConnection()
    df = pd.read_sql(Query, con=POSConnection)
    return df


def getRetailStock(zoneid):
    Query = getRetailStockQuery(zoneid)
    POSConnection = getPOSConnection()

    chunks = pd.read_sql(Query, con=POSConnection, chunksize=30000)

    df = pd.DataFrame()
    for chunk in tqdm(chunks):
        df = pd.concat([df, chunk])
    return df

def getDateRangeForSale(SDate, EDate):
    Query = getDateRangeForSaleQuery(SDate, EDate)
    POSConnection = getPOSConnection()

    chunks = pd.read_sql(Query, con=POSConnection, chunksize=30000)

    df = pd.DataFrame()
    for chunk in tqdm(chunks):
        df = pd.concat([df, chunk])
    return df

def getSaleDataRetail(SDate, EDate):
    Query = getSaleDataRetailQuery(SDate, EDate)
    POSConnection = getPOSConnection()

    chunks = pd.read_sql(Query, con=POSConnection, chunksize=30000)

    df = pd.DataFrame()
    for chunk in tqdm(chunks):
        df = pd.concat([df, chunk])
    return df


def getAreaWiseRetailSale(SDate, EDate, AreaId):
    Query = getAreaWiseSaleQuery(SDate, EDate, AreaId)
    POSConnection = getPOSConnection()

    chunks = pd.read_sql(Query, con=POSConnection, chunksize=30000)

    df = pd.DataFrame()
    for chunk in tqdm(chunks):
        df = pd.concat([df, chunk])
    return df

def getAreaWiseRetailStock(AreaId):
    Query = getAreaWiseStockQuery(AreaId)
    POSConnection = getPOSConnection()

    chunks = pd.read_sql(Query, con=POSConnection, chunksize=30000)

    df = pd.DataFrame()
    for chunk in tqdm(chunks):
        df = pd.concat([df, chunk])
    return df

def getMerchantCatWiseSalePivote(SDate,EDate):
    Query = getMerchantCatWiseSalePivoteQuery(SDate,EDate)
    POSConnection = getPOSConnection()

    chunks = pd.read_sql(Query, con=POSConnection, chunksize=30000)

    df = pd.DataFrame()
    for chunk in tqdm(chunks):
        df = pd.concat([df, chunk])
    return df

def getBatchWisePivotdf():
    Query=getBatchWisePivotQuery()
    POSConnection = getPOSConnection()

    chunks = pd.read_sql(Query, con=POSConnection, chunksize=30000)

    df = pd.DataFrame()
    for chunk in tqdm(chunks):
        df = pd.concat([df, chunk])
    return df

