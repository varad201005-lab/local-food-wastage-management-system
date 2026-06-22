import pyodbc

def get_connection():

    conn = pyodbc.connect(
        r"DRIVER={SQL Server};"
        r"SERVER=localhost\SQLEXPRESS;"
        r"DATABASE=LocalFoodWastageDB;"
        r"Trusted_Connection=yes;"
    )

    return conn
