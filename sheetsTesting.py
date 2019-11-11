import gspread
from oauth2client.service_account import ServiceAccountCredentials

# username = 'b0tm3in@gmail.com'
# password = 'b0tm45st3er'

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)

sheet = client.open("testing data spreadsheet").sheet1

data = sheet.get_all_records()


def getTop5inSector(sector):
    top5stocks = []
    for i in range(0, 5):
        top5stocks.append({'Ticker': "placeholder" + str(i), 'G-Index': -100})
    for nextStock in data:
        if nextStock.get('Sector') == sector and nextStock.get('G-Index') != "#VALUE!":
            for i in range(0, len(top5stocks)):
                if nextStock.get('G-Index') > top5stocks[i].get('G-Index'):
                    top5stocks.insert(i, nextStock)
                    top5stocks.pop(len(top5stocks) - 1)
                    break
    return top5stocks
