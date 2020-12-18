from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import csv

driver = webdriver.Chrome()
driver.implicitly_wait(30)
driver.maximize_window()

def write_csv(ads):
	with open('results.csv', 'a') as f_data:
		fields = ['title', 'price', 'url']

		writer = csv.DictWriter(f_data, fieldnames = fields)

		for ad in ads:
			writer.writerow(ad)



def get_html(url):
	driver.get(url)

	html = driver.page_source

	return driver.page_source

def scraped_data(card):
	try:
		h2 = card.h2
	except:
		title = ''
		url = ''
	else:
		title = card.find('h2').text.strip()
		url = h2.a.get('href')
	try:
		price = card.find('span', class_ = 'a-price-whole').text.strip()
	except:
		price = ''
	else:
		price = ''.join(price.split(','))
	
	data = {'title': title, 'url' : url, 'price': price}

	return data




def main():
	ads_data = []

	for i in range(1,164):
		url = f"https://www.amazon.in/s?i=electronics&bbn=1389401031&rh=n%3A976419031%2Cn%3A1389401031%2Cn%3A1389432031%2Cp_85%3A10440599031&dc&fs=true&page={i}&qid=1608278863&rnid=1389401031&ref=sr_pg_2"

		html = get_html(url)

		soup = BeautifulSoup(html, 'lxml')

		cards = soup.find_all('div', {'data-asin':True, 'data-component-type': 's-search-result'})


		for card in cards:
			data = scraped_data(card)
			ads_data.append(data)

	write_csv(ads_data)

if __name__ == '__main__':
	main()
