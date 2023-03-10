import pyodbc as db

server = 'localhost'
database = 'flaskdb'
username = 'sa'
password = 'hjs07311'
port = 1433
driver = '{ODBC Driver 17 for SQL Server}'

# connectionstring = f'DRIVER={driver};SERVER={server};PORT={port};DATABASE={database};UID={username};PWD={password}'
connectionstring = f'DRIVER={driver};SERVER={server};PORT={port};DATABASE={database};Trusted_Connection=yes;'

connection = db.connect(connectionstring)
cursor = connection.cursor()
