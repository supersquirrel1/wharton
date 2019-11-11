from selenium import webdriver
import time
import gSpreadStocks

driver = webdriver.Chrome()
rsiURL = "http://www.stockta.com/cgi-bin/analysis.pl?symb=BBW&mode=table&table=rsi"
yahooFinanceURL = "https://finance.yahoo.com/quote/ABBV?p=ABBV"


def getRSI(ticker):
    driver.get("http://www.stockta.com/cgi-bin/analysis.pl?symb=" + ticker + "&mode=table&table=rsi")
    rsi = driver.find_element_by_xpath("/html/body/table[5]/tbody/tr/td[2]/table[2]/tbody/tr/td[2]/font").text
    return rsi


def getPE(ticker):
    driver.get("https://finance.yahoo.com/quote/" + ticker + "?p=" + ticker)
    pe = driver.find_element_by_xpath("//*[@id=\"quote-summary\"]/div[2]/table/tbody/tr[3]/td[2]/span").text
    return pe


def getEPS(ticker):
    driver.get("https://finance.yahoo.com/quote/" + ticker + "?p=" + ticker)
    eps = driver.find_element_by_xpath("//*[@id=\"quote-summary\"]/div[2]/table/tbody/tr[4]/td[2]/span").text
    return eps


# reloading the webpage every time is painfully slow so I am combining the two
def getPEandEPS(ticker):
    try:
        driver.get("https://finance.yahoo.com/quote/" + ticker + "?p=" + ticker)
        pe = driver.find_element_by_xpath("//*[@id=\"quote-summary\"]/div[2]/table/tbody/tr[3]/td[2]/span").text
        eps = driver.find_element_by_xpath("//*[@id=\"quote-summary\"]/div[2]/table/tbody/tr[4]/td[2]/span").text
        return [pe, eps]
    except:
        print("error with finding pe/eps for" + ticker)
        return [None, None]


def updateValues(index, rsi, pe, eps):
    # need rsi
    if rsi is not None:
        gSpreadStocks.sheet.update_cell(2 + index, 11, rsi)
    if pe is not None:
        gSpreadStocks.sheet.update_cell(2 + index, 12, pe)
    if eps is not None:
        gSpreadStocks.sheet.update_cell(2 + index, 13, eps)


def updateRanges(startIndex, endIndex):
    if endIndex is None:
        endIndex = len(gSpreadStocks.data)
    for index in range(startIndex, endIndex):
        ticker = gSpreadStocks.data[index].get('Ticker')
        if ticker is not None and ticker is not '':
            rsi = None
            a = [None, None]
            # if we need pe or eps
            if gSpreadStocks.data[index].get('P/E') == '' or gSpreadStocks.data[index].get('EPS') == '':
                a = getPEandEPS(ticker)
            # if we need rsi
            if gSpreadStocks.data[index].get('RSI') == '':
                rsi = getRSI(ticker)
            updateValues(index, rsi, a[0], a[1])
        else:
            updateValues(index, 'N/A', 'N/A', 'N/A')
    print("Stocks %s to %s have been updated." % (startIndex, endIndex))


"""driver.get(rsiURL)
rsi = driver.find_element_by_xpath("/html/body/table[5]/tbody/tr/td[2]/table[2]/tbody/tr/td[2]/font")
rsi = rsi.text
gSpreadStocks.data[0].get('')"""


import sys
while True:
    choice = input("Enter the number corresponding to the function you want to carry out:"
                   "\n1. Update Stocks"
                   "\n2. Find Top Stocks in a Sector"
                   "\n3. Find Top Stocks Overall"
                   "\n4. Exit"
                   "\n")
    if int(choice) == 4:
        sys.exit()
    if int(choice) == 1:
        # get the start and end index
        start = int(input("Enter the starting index: "))
        end = input("Enter the index you want to end at. If you want to do until the end of the list press enter: ")
        if end is not '':
            end = int(end)
        else:
            end = len(gSpreadStocks.data)
        # print("%s, %s" % (start, end))
        updateRanges(start, end)
    if int(choice) == 2:
        # get the sector needed
        sector = str(input("Enter the sector:"))
        top5stocks = gSpreadStocks.getTop5inSector(sector)
        for stock in top5stocks:
            print([stock.get('Ticker'), stock.get('G-Index')])
    if int(choice) == 3:
        topStocks = gSpreadStocks.getTop15()
        for stock in topStocks:
            print([stock.get('Ticker'), stock.get('G-Index')])
