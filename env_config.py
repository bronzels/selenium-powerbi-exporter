from urllib import parse

dlpath = 'C:/Users/xbli06/Downloads/'
drvpath = r'E:\powerbi_exporter\chromedriver\windows\chromedriver.exe'
passowrd = parse.quote_plus('Dev@#0907Dba')
mssql_url = 'mssql+pymssql://DevDBA:{}@192.168.74.42/'.format(passowrd)
url_suffix = ''#'?autocommit=1'
