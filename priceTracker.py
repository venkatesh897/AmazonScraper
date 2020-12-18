import csv
import smtplib
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


csvfile=open('results.csv','r', newline='')
obj=csv.reader(csvfile)

driver = webdriver.Chrome()
driver.implicitly_wait(30)
driver.maximize_window()


products = []
for row in obj:
	products.append(row)
csvfile.close()



def get_price():
	for product in products:
		try:
			url = "https://www.amazon.in" + product[2]
			driver.get(url)
		except IndexError:
			continue
		try:
			price = driver.find_element_by_id("priceblock_dealprice").text 
		except:
			price = driver.find_element_by_id("priceblock_ourprice").text
		print(price)
		final_price = ''.join(price)[2:12]
		final_price = float(final_price.replace(',', '').replace("₹", '').replace(" ", ''))
		print(final_price)
		if final_price < float(product[1]):
		   send_email(product)


def send_email(product):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('venkatesh.b.8.97@gmail.com', 'aqwsderf3')

    subject = "Price fell down"
    body = "https://www.amazon.in" + product[2] + " " + product[0]
    msg = f"Subject:{subject}\n\n{body}"

    server.sendmail('venkatesh.b.8.97@gmail.com', 'venkatesh.b.8.97@gmail.com', msg)

    print("Hey, email has been sent!")
    server.quit()


while True:
    get_price()
    time.sleep(60)



