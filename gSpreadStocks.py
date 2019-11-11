import gspread
from oauth2client.service_account import ServiceAccountCredentials

# http://kw.wharton.upenn.edu/kwhs-invests-2019-2020/files/2019/09/2019-20-KWHS-Approved-Securities.pdf
# https://wrds-otis.wharton.upenn.edu/otis/security_detail.cfm?security_id=19531&PH=1&x=0

# HOW TO GET RSI
# http://www.stockta.com/cgi-bin/analysis.pl?symb=BBW&mode=table&table=rsi

#username = 'b0tm3in@gmail.com'
#password = 'b0tm45st3er'

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)

sheet = client.open("Approved Stock List").sheet1

data = sheet.get_all_records()

def getTop5inSector(sector):
    top5stocks = []
    for i in range(0, 5):
        top5stocks.append({'Ticker': "placeholder" + str(i), 'G-Index': -1000})
    for nextStock in data:
        if nextStock.get('Sector') == sector and nextStock.get('G-Index') != "#VALUE!":
            for i in range(0, len(top5stocks)):
                if nextStock.get('G-Index') > top5stocks[i].get('G-Index'):
                    top5stocks.insert(i, nextStock)
                    top5stocks.pop(len(top5stocks) - 1)
                    break
    return top5stocks

def getTop15():
    topStocks = []
    for i in range(0, 10):
        topStocks.append({'Ticker': "placeholder" + str(i), 'G-Index': -1000})
    for nextStock in data:
        if nextStock.get('G-Index') != "#VALUE!":
            for i in range(0, len(topStocks)):
                if nextStock.get('G-Index') > topStocks[i].get('G-Index'):
                    topStocks.insert(i, nextStock)
                    topStocks.pop(len(topStocks) - 1)
                    break
    return topStocks