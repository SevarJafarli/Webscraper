from bs4 import BeautifulSoup
from selenium import webdriver
from pathlib import Path
import csv
import os
from webscraper import *
from write_csv import *
from browser import *

class TapAz(WebScraper):
    @staticmethod
    def do_scrape(card):
        link = card.find('a', class_='products-link').get('href')
        title = card.find('div', class_='products-top').img.get('alt')
        price = card.find('div', class_='products-price-container')

        if price is None:
            print("")
        else:
            Price = price.div.span.text.replace(' ', '')
        Price = ''.join(Price.split(','))

        site = 'tapaz'
        data = {'title': title, 'price': Price, 'link': link, 'site': site}
        return data

    def scraper(self, item):
        ads_data = []
        url = f"https://tap.az/elanlar?utf8=%E2%9C%93&log=true&keywords={item}&q%5Bregion_id%5D="
        html = get_html(url)
        soup = BeautifulSoup(html, 'lxml')

        cards = soup.find_all('div', class_='products-i rounded')
        for card in cards:
            data = self.do_scrape(card)
            ads_data.append(data)

        with open('results.csv', 'a+', encoding='utf-8') as f:
            f.write("title,price,link,site\n")
        f.close()
        write_csv(ads_data)