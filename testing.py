"""import gSpreadStocks
ticker = gSpreadStocks.data[0].get('Ticker')
import main
a = main.getPEandEPS(ticker)
main.updateValues(0, main.getRSI(ticker), a[0], a[1])"""
import sheetsTesting
"""values=[]
values.append({'Ticker': 'a', 'Sector': 'A', 'p/e': 4, 'eps': 3, 'standardized p/e': 0.9921567416, 'standardized eps': -0.3197935972, 'G-Index': 0.6723631444})
#values.append({"4","ed",8})
#for i in sheetsTesting.data:
#    values.append(i)
values.insert(0, {'Ticker':'4', 'eps': 3})
print(values[0].get('Ticker'))"""
import sheetsTesting
top5stocks = sheetsTesting.getTop5inSector('A')
for stock in top5stocks:
    print([stock.get('Ticker'), stock.get('G-Index')])