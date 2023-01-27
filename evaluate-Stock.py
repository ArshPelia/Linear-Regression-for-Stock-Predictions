# https://www.scraperapi.com/blog/how-to-scrape-stock-market-data-with-python/

#dependencies
import requests, re, csv, joblib
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from sklearn.linear_model import LinearRegression
# from sklearn.metrics import mean_squared_error, r2_score
 
#list of URLs
urls = [
'https://www.investing.com/equities/nike',
# 'https://www.investing.com/equities/coca-cola-co',
# 'https://www.investing.com/equities/microsoft-corp',
]
 
#starting our CSV file
# file = open('stockprices.csv', 'w')
# writer = csv.writer(file)
# writer.writerow(['Company', 'Price', 'Change'])
 
#looping through our list
for url in urls:
    #sending our request through ScraperAPI
    params = {'api_key': '51e43be283e4db2a5afb62660fc6ee44', 'url': url}
    page = requests.get('http://api.scraperapi.com/', params=urlencode(params))
    
    #our parser
    soup = BeautifulSoup(page.text, 'html.parser')
    company = soup.find('h1', {'class': 'text-2xl font-semibold instrument-header_title__gCaMF mobile:mb-2'}).text
    price = soup.find('div', {'class': 'instrument-price_instrument-price__xfgbB flex items-end flex-wrap font-bold'}).find_all('span')[0].text
    percentchange = soup.find('div', {'class': 'instrument-price_instrument-price__xfgbB flex items-end flex-wrap font-bold'}).find_all('span')[2].text
    yest_close = soup.find('div', {'class': 'flex justify-between border-b py-2 desktop:py-0.5'}).find_all('dd')[0].text

    div_element = soup.find_all('div', {'class': 'flex justify-between border-b py-2 desktop:py-0.5'})[3]
    # Find the element containing the "Open" value
    open_price = div_element.find('dd').text

    div_element = soup.find_all('div', {'class': 'flex justify-between border-b py-2 desktop:py-0.5'})[6]
    # Find the element containing the "Open" value
    volume = div_element.find('dd').text

    if(price < open_price):
        low = price
        high = open_price
    else:
        low = open_price
        high = price

    #calculate open price based on price and percent change since close oo previous day
    # openprice = float(price) / (1 + float(percentchange.strip('()').strip('%'))/100)
    
    #printing to have some visual feedback
    print('-----------------------------')
    print('Loading :', url)
    print(company, 'Current Price: ' + price, percentchange)
    print('-----------------------------')
    print('Open price:', open_price)
    print('Yesterday close price:', yest_close)
    print('Volume:', volume)
    print('Low:', low)
    print('High:', high)
    print('-----------------------------')

    
    #writing the data into our CSV file
#     writer.writerow([company.encode('utf-8'), price.encode('utf-8'), percentchange.encode('utf-8')])

# file.close()
volume = volume.replace(',', '')

# load the model
model = joblib.load('model.joblib')
stock_prediction = model.predict([[float(open_price), float(high), float(low), float(volume)]])
print("Predicted stock price: ", stock_prediction)

if stock_prediction[0] > float(price):
    print("It is a good idea to invest in this stock")
else:
    print("It might be a good idea to wait before investing in this stock")

print('')
print('---------------------------------------')
print('finished')