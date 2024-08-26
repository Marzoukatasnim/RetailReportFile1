def getStaffProductivityQuery(SDate,EDate):
    return '''
    
        SELECT S.[SalesManID]
                ,E.FirstName + ' ' + E.LastName AS [Emp Name]
                ,E.Designation
                ,CASE 
                    WHEN E.Inactive = 'N'
                        THEN 'Active'
                    ELSE 'Inactive'
                    END AS [Employee Status]
                ,S.[ShopId] AS [Sales Shop Id]
                ,SL.ShopName AS [ Sale Shop Name]
                ,E.ShopId AS [Emp at Shop Name]
                ,SL1.ShopName AS [Emp at Shop Name]
                ,YEAR(S.[SaleDT]) * 100 + MONTH([SaleDT]) AS [MONTH NAME]
                ,CAST(S.[SaleDT] AS DATE) AS [SaleDT]
                ,SUM(S.Qty - S.rQty) AS [Total sale Quantity]
                ,SUM(S.NetAmt - S.rAmt) NetSale
                ,COUNT(DISTINCT Invoice) AS [Cash Memo]
            FROM [POS_MASTER_DB].[dbo].[Sale] S
            LEFT JOIN [POS_MASTER_DB].[dbo].[Employee] E ON S.SalesManID = E.EmpID
            LEFT JOIN [POS_MASTER_DB].[dbo].[ShopList] SL ON S.ShopId = SL.ShopId
            LEFT JOIN [POS_MASTER_DB].[dbo].[ShopList] SL1 ON E.ShopId = SL1.ShopId
            WHERE CAST(S.[SaleDT] AS DATE) BETWEEN '{}' AND '{}'
                AND 
                (
                        SUBSTRING([BarCode],1,10) <> '09020A0241' 
                    AND SUBSTRING([BarCode],6,1) != 'S'
                )
                AND S.ShopId NOT IN ('G300','G400')
            GROUP BY S.[SalesManID]
                ,E.FirstName + ' ' + E.LastName
                ,E.Designation
                ,CASE 
                    WHEN E.Inactive = 'N'
                        THEN 'Active'
                    ELSE 'Inactive'
                    END
                ,S.[ShopId]
                ,SL.ShopName
                ,E.ShopId
                ,SL1.ShopName
                ,YEAR(S.[SaleDT]) * 100 + MONTH([SaleDT]) 
                ,CAST(S.[SaleDT] AS DATE) 
            HAVING SUM(S.NetAmt - S.rAmt) != 0 
    
    
    '''.format(SDate,EDate)


def getAreaListQuery():
    return '''
    
    SELECT [AreaId]
          ,[AreaName]
          ,[AreaManagerId]
          ,[ZoneId]
          ,[EventName]
      FROM [POS_MASTER_DB].[dbo].[AreaList]
      WHERE [AreaId] != 35
    
    '''
def getZoneListQuery():
    return '''
    
        SELECT [ZoneId]
              ,[ZoneName]
          FROM [ZoneList] WHERE ZoneId IN(
            SELECT ZoneId FROM AreaList
  )
    
    '''


def getRetailStockQuery(zoneid):
    return '''
    
    SELECT 
             AL.AreaName
            ,S.ShopId
            ,SL.ShopName
            ,MG.GROUP_DESC
            ,MC.MERCHEN_CATEGORY
            ,SUBSTRING(S.BarCode,1,8) AS [ARTICLE]
            ,SUBSTRING(S.BarCode,9,2) AS [SIZE]
            ,SUBSTRING(S.BarCode,13,2) AS [YEAR LOT]
            ,MT.RPU AS MRP
            ,SUM(BalQty) AS [TOTAL STOCK]
            ,MT.RPU * SUM(BalQty) AS [STOCK VALUE]
            FROM ProductStock S 
            LEFT JOIN PART_WISE_MERCHEN_CATEGORY_TAB PWMC ON SUBSTRING(S.BarCode,1,10) = PWMC.PART_NO
            LEFT JOIN MERCHAN_CATEGORY_TAB MC ON PWMC.MERCHEN_CAT_ID = MC.MER_CAT_ID
            LEFT JOIN MERCHEN_GROUP MG ON MC.MER_GROUP_ID = MG.GROUP_ID
            LEFT JOIN ShopList SL ON S.ShopId = SL.ShopId
            LEFT JOIN AreaWiseShopList AWSL ON SL.ShopId = AWSL.ShopId
            LEFT JOIN AreaList AL ON AWSL.AreaId = AL.AreaId
            LEFT JOIN MRP_TABLE MT ON SUBSTRING(S.BarCode,1,10) = MT.PART_NO
			LEFT JOIN ZoneList ZL ON AL.ZoneId = ZL.ZoneId

            WHERE S.ShopId NOT IN ('G300','G400')
            AND 
            (
                SUBSTRING(S.[BarCode], 1, 10) <> '09020A0241'
                AND SUBSTRING(S.[BarCode], 6, 1) != 'S'
            )
            AND S.BalQty != 0
            AND ZL.ZoneId = {}
            GROUP BY 
             AL.AreaId
            ,AL.AreaName
            ,S.ShopId
            ,SL.ShopName
            ,MG.GROUP_ID
            ,MG.GROUP_DESC
            ,MC.MER_CAT_ID
            ,MC.MERCHEN_CATEGORY
            ,SUBSTRING(S.BarCode,1,8)  
            ,SUBSTRING(S.BarCode,9,2)  
            ,SUBSTRING(S.BarCode,13,2)  
            ,MT.RPU  
    
    '''.format(zoneid)


def getDateRangeForSaleQuery(SDate, EDate):
    return '''
        
        	SELECT 
            DISTINCT 
                    YEAR(S.SaleDT) * 100 + MONTH(S.SaleDT) AS [MONTH NAME]
                   ,CAST(MIN(S.SaleDT) AS DATE) AS [MIN_SALEDT]
                   ,CAST(MAX(S.SaleDT) AS DATE) AS [MAX_SALEDT]
            FROM Sale S
                WHERE CAST(S.SaleDT AS DATE) BETWEEN '{}' AND '{}' 
                GROUP BY YEAR(S.SaleDT) * 100 + MONTH(S.SaleDT)
                ORDER BY 1
    
    '''.format(SDate, EDate)

def getSaleDataRetailQuery(SDate, EDate):
    return '''
    
    SELECT 
            AL.AreaName
            ,S.ShopId
            ,SL.ShopName
            ,MG.GROUP_DESC
            ,MC.MERCHEN_CATEGORY
            ,SUBSTRING(S.BarCode,1,8) AS [ARTICLE]
            ,SUBSTRING(S.BarCode,9,2) AS [SIZE]
            ,SUBSTRING(S.BarCode,13,2) AS [BATCH]
			,S.DiscRef
            ,CAST(S.SaleDT AS DATE) AS SaleDT
            ,MT.RPU AS MRP
            ,SUM(S.NetAmt - S.rAmt) AS [Total Sale]
            ,SUM(S.Qty - S.rQty) AS [Total Quantity]
			,SUM(S.CDiscAmt + S.SDiscAmt) AS [Discount Amount]
            FROM Sale S
            LEFT JOIN PART_WISE_MERCHEN_CATEGORY_TAB PWMC ON SUBSTRING(S.BarCode,1,10) = PWMC.PART_NO
            LEFT JOIN MERCHAN_CATEGORY_TAB MC ON PWMC.MERCHEN_CAT_ID = MC.MER_CAT_ID
            LEFT JOIN MERCHEN_GROUP MG ON MC.MER_GROUP_ID = MG.GROUP_ID
            LEFT JOIN ShopList SL ON S.ShopId = SL.ShopId
            LEFT JOIN AreaWiseShopList AWSL ON SL.ShopId = AWSL.ShopId
            LEFT JOIN AreaList AL ON AWSL.AreaId = AL.AreaId
            LEFT JOIN MRP_TABLE MT ON SUBSTRING(S.BarCode,1,10) = MT.PART_NO
        
            WHERE S.ShopId NOT IN ('G300','G400')
            AND 
            (
                SUBSTRING(S.[BarCode], 1, 10) <> '09020A0241'
                AND SUBSTRING(S.[BarCode], 6, 1) != 'S'
            )
            AND CAST(S.SaleDT AS DATE) BETWEEN '{}' AND '{}'
            GROUP BY
             AL.AreaId
            ,AL.AreaName
            ,S.ShopId
            ,SL.ShopName
            ,MG.GROUP_ID
            ,MG.GROUP_DESC
            ,MC.MER_CAT_ID
            ,MC.MERCHEN_CATEGORY
            ,SUBSTRING(S.BarCode,1,8)  
            ,SUBSTRING(S.BarCode,9,2)  
            ,SUBSTRING(S.BarCode,13,2)  
			,S.DiscRef
            ,CAST(S.SaleDT AS DATE)  
            ,MT.RPU
    
    
    '''.format(SDate, EDate)


def getAreaWiseSaleQuery(SDate,EDate,AreaId):
    return '''
    
        SELECT 
            S.ShopId
            ,SL.ShopName
            ,MG.GROUP_DESC
            ,MC.MERCHEN_CATEGORY
            ,SUBSTRING(S.BarCode,1,8) AS [ARTICLE]
            ,SUBSTRING(S.BarCode,9,2) AS [SIZE]
            ,SUBSTRING(S.BarCode,13,2) AS [BATCH]
			,S.DiscRef
            ,CAST(S.SaleDT AS DATE) AS SaleDT
            ,MT.RPU AS MRP
            ,SUM(S.NetAmt - S.rAmt) AS [Total Sale]
            ,SUM(S.Qty - S.rQty) AS [Total Quantity]
			,SUM(S.CDiscAmt + S.SDiscAmt) AS [Discount Amount]
            FROM Sale S
            LEFT JOIN PART_WISE_MERCHEN_CATEGORY_TAB PWMC ON SUBSTRING(S.BarCode,1,10) = PWMC.PART_NO
            LEFT JOIN MERCHAN_CATEGORY_TAB MC ON PWMC.MERCHEN_CAT_ID = MC.MER_CAT_ID
            LEFT JOIN MERCHEN_GROUP MG ON MC.MER_GROUP_ID = MG.GROUP_ID
            LEFT JOIN ShopList SL ON S.ShopId = SL.ShopId
            LEFT JOIN AreaWiseShopList AWSL ON SL.ShopId = AWSL.ShopId
            LEFT JOIN AreaList AL ON AWSL.AreaId = AL.AreaId
            LEFT JOIN MRP_TABLE MT ON SUBSTRING(S.BarCode,1,10) = MT.PART_NO
        
            WHERE S.ShopId NOT IN ('G300','G400')
            AND 
            (
                SUBSTRING(S.[BarCode], 1, 10) <> '09020A0241'
                AND SUBSTRING(S.[BarCode], 6, 1) != 'S'
            )
            AND CAST(S.SaleDT AS DATE) BETWEEN '{}' AND '{}'
			AND AL.AreaId = {}
            GROUP BY
			S.ShopId
            ,SL.ShopName
            ,MG.GROUP_ID
            ,MG.GROUP_DESC
            ,MC.MER_CAT_ID
            ,MC.MERCHEN_CATEGORY
            ,SUBSTRING(S.BarCode,1,8)  
            ,SUBSTRING(S.BarCode,9,2)  
            ,SUBSTRING(S.BarCode,13,2)  
			,S.DiscRef
            ,CAST(S.SaleDT AS DATE)  
            ,MT.RPU
    
    '''.format(SDate,EDate,AreaId)

def getAreaWiseStockQuery(AreaId):
    return '''
    
        SELECT 
              S.ShopId
            ,SL.ShopName
            ,MG.GROUP_DESC
            ,MC.MERCHEN_CATEGORY
            ,SUBSTRING(S.BarCode,1,8) AS [ARTICLE]
            ,SUBSTRING(S.BarCode,9,2) AS [SIZE]
            ,SUBSTRING(S.BarCode,13,2) AS [YEAR LOT]
            ,MT.RPU AS MRP
            ,SUM(BalQty) AS [TOTAL STOCK]
            ,MT.RPU * SUM(BalQty) AS [STOCK VALUE]
            FROM ProductStock S 
            LEFT JOIN PART_WISE_MERCHEN_CATEGORY_TAB PWMC ON SUBSTRING(S.BarCode,1,10) = PWMC.PART_NO
            LEFT JOIN MERCHAN_CATEGORY_TAB MC ON PWMC.MERCHEN_CAT_ID = MC.MER_CAT_ID
            LEFT JOIN MERCHEN_GROUP MG ON MC.MER_GROUP_ID = MG.GROUP_ID
            LEFT JOIN ShopList SL ON S.ShopId = SL.ShopId
            LEFT JOIN AreaWiseShopList AWSL ON SL.ShopId = AWSL.ShopId
            LEFT JOIN AreaList AL ON AWSL.AreaId = AL.AreaId
            LEFT JOIN MRP_TABLE MT ON SUBSTRING(S.BarCode,1,10) = MT.PART_NO 

            WHERE S.ShopId NOT IN ('G300','G400')
            AND 
            (
                SUBSTRING(S.[BarCode], 1, 10) <> '09020A0241'
                AND SUBSTRING(S.[BarCode], 6, 1) != 'S'
            )
            AND S.BalQty != 0
            AND AL.AreaId = {}
            GROUP BY  
			  S.ShopId
            ,SL.ShopName
            ,MG.GROUP_ID
            ,MG.GROUP_DESC
            ,MC.MER_CAT_ID
            ,MC.MERCHEN_CATEGORY
            ,SUBSTRING(S.BarCode,1,8)  
            ,SUBSTRING(S.BarCode,9,2)  
            ,SUBSTRING(S.BarCode,13,2)  
            ,MT.RPU  
    
    '''.format(AreaId)

def getMerchantCatWiseSalePivoteQuery(SDate,EDate):
    return '''
    
        SELECT 
             AL.AreaName
			,S.ShopId
            ,SL.ShopName
            ,MC.MERCHEN_CATEGORY
            ,SUM(S.NetAmt - S.rAmt) AS [Total Sale]
			,SUM(S.CDiscAmt + S.SDiscAmt) AS [Discount Amount]
            FROM Sale S
            LEFT JOIN PART_WISE_MERCHEN_CATEGORY_TAB PWMC ON SUBSTRING(S.BarCode,1,10) = PWMC.PART_NO
            LEFT JOIN MERCHAN_CATEGORY_TAB MC ON PWMC.MERCHEN_CAT_ID = MC.MER_CAT_ID
            LEFT JOIN ShopList SL ON S.ShopId = SL.ShopId
            LEFT JOIN AreaWiseShopList AWSL ON SL.ShopId = AWSL.ShopId
            LEFT JOIN AreaList AL ON AWSL.AreaId = AL.AreaId
            LEFT JOIN MRP_TABLE MT ON SUBSTRING(S.BarCode,1,10) = MT.PART_NO
        
            WHERE S.ShopId NOT IN ('G300','G400')
            AND 
            (
                SUBSTRING(S.[BarCode], 1, 10) <> '09020A0241'
                AND SUBSTRING(S.[BarCode], 6, 1) != 'S'
            )
            AND CAST(S.SaleDT AS DATE) BETWEEN '{}' AND '{}'
            GROUP BY
			 AL.AreaId
			,AL.AreaName
			,S.ShopId
            ,SL.ShopName
            ,MC.MER_CAT_ID
            ,MC.MERCHEN_CATEGORY 
    
    
    '''.format(SDate,EDate)

def getBatchWisePivotQuery():
    return '''

    SELECT p.ShopId AS [Shop Id]
    	,sl.ShopName AS [Shop Name]
    	,AreaName
    	,mc.MERCHEN_CATEGORY
    	,'Batch ' + SUBSTRING(p.BarCode, 13, 2) + ' Stock' AS Batch
    	,SUM(p.RPU * BalQty) AS [Stock value]
    	,SUM(BalQty) AS [Total Stock Qty]
    	
    FROM ProductStock p
    LEFT JOIN ShopList sl ON p.ShopId = sl.ShopId
    LEFT JOIN AreaWiseShopList aws ON p.ShopId = aws.ShopId
    LEFT JOIN AreaList a ON aws.AreaId = a.AreaId
    LEFT JOIN PART_WISE_MERCHEN_CATEGORY_TAB pwm ON SUBSTRING(p.Barcode, 1, 10) = pwm.PART_NO
    LEFT JOIN MERCHAN_CATEGORY_TAB mc ON pwm.MERCHEN_CAT_ID = mc.MER_CAT_ID
    WHERE (
    		SUBSTRING([BarCode], 1, 10) <> '09020A0241'
    		AND SUBSTRING([BarCode], 6, 1) != 'S'
    		)
    	AND p.ShopId NOT IN (
    		'G300'
    		,'G400'
    		)
    	AND P.BalQty != 0
    GROUP BY p.ShopId
    	,sl.ShopName
    	,AreaName
    	,mc.MERCHEN_CATEGORY
    	,SUBSTRING(p.BarCode, 13, 2)
    	
    '''.format()

