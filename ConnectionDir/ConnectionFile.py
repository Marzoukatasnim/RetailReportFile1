import pyodbc

def getPOSConnection():
    connectionString = 'Driver={SQL Server};Server=x.x.x.x;Database=POS;uid=qaa;pwd=q1a'
    connection = pyodbc.connect(connectionString)
    return connection
