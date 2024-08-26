import pandas as pd
import numpy as np
import pyodbc
import datetime

from ReportProcessingWork import *
from ConnectionDir.ConnectionFile import *


SERVER_CHECK_QUERY = '''

        SELECT [FLAG] FROM [POS_MASTER_DB].[dbo].[REPORT_LOGIN]
		  WHERE [DepartmentId] = 3

'''

def SERVER_CHECK():
    POSConnection = getPOSConnection()
    df = pd.read_sql(SERVER_CHECK_QUERY, POSConnection)
    return df.iloc[0][0]


def dateRangeValidation(SDate, EDate):
    SDate = datetime.datetime.strptime(SDate, '%Y-%m-%d').date()
    EDate = datetime.datetime.strptime(EDate, '%Y-%m-%d').date()
    return EDate >= SDate


def DateChecker(SDate, EDate):
    RangeFlag = False
    if dateRangeValidation(SDate, EDate):
        RangeFlag = True
    return RangeFlag


def main():
    Flag = 1
    while True:
        print('Enter 1: Staff Productivity Report.')
        print('Enter 2: Retail Stock Report.')
        print('Enter 3: Retail Sale Report.')
        print('Enter 4: Sale Report for Particular Area.')
        print('Enter 5: Stock Report for Particular Area.')
        print('Enter 6: Merchant Category Wise Sale & Discount Data (Pivot).')
        print('Enter 7: Batch wise stock(Pivot)')
        print('Enter 0: Exit the Programme.')

        if SERVER_CHECK() == 1:
            choice = int(input())
            if choice == 1:
                print('Enter Start Date(YYYY-MM-DD):')
                SDate = input()

                print('Enter End Date(YYYY-MM-DD):')
                EDate = input()

                if DateChecker(SDate, EDate):
                    getStaffProductivityData(choice, SDate, EDate)
                else:
                    print('Start Date Grater Than End Date!!!!!')

            elif choice == 2:
                getRetailStockData(choice)

            elif choice == 3:
                print('Enter Start Date(YYYY-MM-DD):')
                SDate = input()

                print('Enter End Date(YYYY-MM-DD):')
                EDate = input()

                if DateChecker(SDate, EDate):
                    getRetailSaleData(choice, SDate, EDate)
                else:
                    print('Start Date Grater Than End Date!!!!!')
            elif choice == 4:
                Area_FLAG = 1
                Date_FLAG = 1

                Areadf = getAreaListData()
                Areadf['AreaId'] = Areadf['AreaId'].astype(str)

                print('Choose your Selected Area Id:')
                AreaId = input()

                print('Enter Start Date(YYYY-MM-DD):')
                SDate = input()

                print('Enter End Date(YYYY-MM-DD):')
                EDate = input()


                if Areadf[Areadf['AreaId'] == AreaId].shape[0] == 0:
                    Area_FLAG = 0
                    print('No Area Id in System!!!!!')
                if DateChecker(SDate, EDate) == False:
                    Date_FLAG = 0
                    print('Start Date Grater Than End Date!!!!!')

                if (Area_FLAG == 1) & (Date_FLAG == 1):
                    AreaName = Areadf[Areadf['AreaId'] == AreaId]['AreaName'].iloc[0]
                    getAreaWiseSaleData(choice, SDate, EDate, AreaId, AreaName)
                else:
                    print('Wrong Input!!!')

            elif choice == 5:
                Area_FLAG = 1

                Areadf = getAreaListData()
                Areadf['AreaId'] = Areadf['AreaId'].astype(str)

                print('Choose your Selected Area Id:')
                AreaId = input()


                if Areadf[Areadf['AreaId'] == AreaId].shape[0] == 0:
                    Area_FLAG = 0
                    print('No Area Id in System!!!!!')

                if (Area_FLAG == 1):
                    AreaName = Areadf[Areadf['AreaId'] == AreaId]['AreaName'].iloc[0]
                    getAreaWiseStockData(choice,AreaId,AreaName)
                else:
                    print('Wrong Input!!!')



            elif choice == 6:
                print('Enter Start Date(YYYY-MM-DD):')
                SDate = input()

                print('Enter End Date(YYYY-MM-DD):')
                EDate = input()

                if DateChecker(SDate, EDate):
                    getMerchantCatWiseSalePivoteData(choice,SDate,EDate)
                else:
                    print('Start Date Grater Than End Date!!!!!')


            elif choice == 7:
               getBatchWiseStockData(choice)


            elif choice == 0:
                Flag = 0
                break


        else:
            print('Server Is Busy. Try Later.')
            print('Press any Key to Continue.........')
            input()
        if Flag == 0:
            break


if __name__ == '__main__':
    main()
    SERVER_CHECK()