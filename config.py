import json
import urllib

# open config.json file
with open("config.json") as config_file:
    config = json.load(config_file)

# Create a class for configuration
params = urllib.parse.quote_plus('DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;PORT=;DATABASE=flaskdb;Trusted_Connection=yes;')

class Config:
    SECRET_KEY = config.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = "mssql+pyodbc:///?odbc_connect=%s" % params
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = config.get('EMAIL_USER')
    MAIL_PASSWORD = config.get('EMAIL_PASS')