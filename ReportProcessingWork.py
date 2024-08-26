import pandas as pd
from ReportFunctionalWork import *
import os
from pyexcelerate import Workbook


FILE_NAME_DIC = {
    1:'Staff Productivity'
   ,2:'RetailProductStock'
   ,3:'RetailSale'
   ,4:'AreaWiseSaleReport'
   ,5:'AreaWiseStockReport'
   ,6:'MerchantCatWiseSalePivot'
   ,7:'BatchWiseStock'
}
def getOutputFolder():
    OUTPUT_FOLDER = 'POSRetailOutputFiles/'
    return OUTPUT_FOLDER


def getStaffProductivityData(choice,SDate,EDate):
    StaffProductivity = getStaffProductivity(SDate,EDate)
    StaffProductivity.to_excel(getOutputFolder() + FILE_NAME_DIC.get(choice) + '.xlsx',index=False)


def getRetailStockData(choice):
    Zonedf = getZoneList()

    wb = Workbook()
    for zoneid, zonename in zip(Zonedf['ZoneId'],Zonedf['ZoneName']):
        print(zoneid,zonename)
        RetailStock = getRetailStock(zoneid)
        values = [RetailStock.columns] + list(RetailStock.values)
        wb.new_sheet(str(zonename), data=values)

    wb.save(getOutputFolder() + FILE_NAME_DIC.get(choice) + '.xlsx')



def getRetailSaleData(choice,SDate,EDate):
    DateRangeDf = getDateRangeForSale(SDate, EDate)

    wb = Workbook()
    for monthname, date_S, date_E in zip(DateRangeDf['MONTH NAME'],DateRangeDf['MIN_SALEDT'],DateRangeDf['MAX_SALEDT']):
        print(monthname)
        SaleDf = getSaleDataRetail(date_S, date_E)

        values = [SaleDf.columns] + list(SaleDf.values)
        wb.new_sheet(str(monthname), data=values)

    wb.save(getOutputFolder() + FILE_NAME_DIC.get(choice) + '.xlsx')

def getAreaListData():
    Areadf = getAreaList()
    Areadf['AreaId'] = Areadf['AreaId'].astype(int)
    for A_id, A_name in zip(Areadf['AreaId'], Areadf['AreaName']):
        print(A_name + ' -> ' + str(A_id))
    return Areadf


def getAreaWiseSaleData(choice,SDate,EDate,AreaId,AreaName):
    AreaSaledf = getAreaWiseRetailSale(SDate, EDate, AreaId)
    wb = Workbook()
    values = [AreaSaledf.columns] + list(AreaSaledf.values)
    wb.new_sheet(str(AreaName), data=values)
    wb.save(getOutputFolder() + FILE_NAME_DIC.get(choice) + '_' + AreaName + '.xlsx')

def getAreaWiseStockData(choice,AreaId,AreaName):
    AreaStockdf = getAreaWiseRetailStock(AreaId)
    wb = Workbook()
    values = [AreaStockdf.columns] + list(AreaStockdf.values)
    wb.new_sheet(str(AreaName), data=values)
    wb.save(getOutputFolder() + FILE_NAME_DIC.get(choice) + '_' + AreaName + '.xlsx')

def getMerchantCatWiseSalePivoteData(choice,SDate,EDate):
    MerchantCatWiseSalePivotedf = getMerchantCatWiseSalePivote(SDate, EDate)
    Pivotedf = pd.pivot_table(MerchantCatWiseSalePivotedf,
                              index=['AreaName', 'ShopId', 'ShopName'],
                              columns=['MERCHEN_CATEGORY'],
                              values=['Total Sale', 'Discount Amount'],
                              aggfunc='sum',
                              margins=True,
                              margins_name='Grand Total').fillna(0)
    Pivotedf.to_excel(getOutputFolder() + FILE_NAME_DIC.get(choice) + '.xlsx')

def  getBatchWiseStockData(choice):
    BatchWisePivotdf = getBatchWisePivotdf()
    Pivotdf = pd.pivot_table(BatchWisePivotdf,
                              index=['AreaName', 'Shop Id', 'Shop Name','MERCHEN_CATEGORY'],
                              columns=['Batch'],
                              values=[ 'Total Stock Qty','Stock value'],
                              aggfunc='sum',
                              margins=True,
                              margins_name='Grand Total').fillna(0)
    Pivotdf.to_excel(getOutputFolder() + FILE_NAME_DIC.get(choice)+ '.xlsx')



