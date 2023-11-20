from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

FORM_URL="https://docs.google.com/forms/d/e/1FAIpQLSfxEEGm78zyAy5SQR8VDGrLttvUFNOz4y1Etum3Vq2lIvKdQQ/viewform?usp=sf_link"
headers={
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Accept-Language":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
}

website=requests.get(url="https://appbrewery.github.io/Zillow-Clone/",headers=headers)
webpage=website.text
soup=BeautifulSoup(webpage,"html.parser")

properties=soup.select(".StyledPropertyCardDataWrapper a")
links=[i["href"] for i in properties]
print(links)

addresses=soup.select(".StyledPropertyCardDataWrapper address")
address=[i.text.strip() for i in addresses]
print(address)

all_price_elements = soup.select(".PropertyCardWrapper span")
all_prices = [price.get_text().replace("/mo", "").split("+")[0] for price in all_price_elements if "$" in price.text]
print(all_prices)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
driver.get(FORM_URL)

for i in range(len(all_prices)-1):
    sleep(1)
    first=driver.find_element(By.XPATH,value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    first.click()
    first.send_keys(f"{address[i]}")
    second=driver.find_element(By.XPATH,value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    second.click()
    second.send_keys(f"{all_prices[i]}")
    third=driver.find_element(By.XPATH,value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    third.click()
    third.send_keys(f"{links[i]}")
    submit=driver.find_element(By.XPATH,value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')
    submit.click()
    another=driver.find_element(By.LINK_TEXT,"Submit another response")
    if i!=(len(all_prices)-1):
        another.click()
