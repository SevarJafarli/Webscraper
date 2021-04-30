from bs4 import BeautifulSoup
from selenium import webdriver
from pathlib import Path
import csv
import os
from webscraper import *
from write_csv import *
class Amazon(Website):
    @staticmethod
    def do_scrape(card):
        try:
            h2 = card.h2

        except:
            title = ''
            link = ''

        else:
            title = h2.text.strip()
            link = h2.a.get('href')

        try:
            price = card.find(
                'span', class_='a-price-whole').text.strip('.').strip()
        except:
            price = ''
        else:
            price = ''.join(price.split(','))

        site = 'amazon'

        data = {'title': title, 'price': price, 'link': link, 'site': site}
        return data

    def scraper(self, item):
        ads_data = []

        for i in range(1, 5):
            url = f'https://www.amazon.com/s?k={item}&page={i}&qid=1617312099&ref=sr_pg_2'
            html = get_html(url)

            soup = BeautifulSoup(html, 'lxml')

            cards = soup.find_all(
                'div', {'data-asin': True, 'data-component-type': 's-search-result'})

            for card in cards:
                data = self.do_scrape(card)
                ads_data.append(data)

        with open('results.csv', 'a+', encoding='utf-8') as f:
            f.write("title,price,link,site\n")
        f.close()
        write_csv(ads_data)