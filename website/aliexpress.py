import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import *
import pandas as pd
from lxml import html
import csv
import os
import requests
driver = webdriver.Chrome(executable_path="E:\driver\chromedriver.exe")

headers = {
    "User=Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36"}


def write_csv(ads):
    with open('ali.csv', 'a+', encoding='utf-8') as f:
        fields = ['title', 'price', 'link', 'site']

        writer = csv.DictWriter(f, fieldnames=fields)

        for ad in ads:
            writer.writerow(ad)


def scrapeAliExpress(card):
    title = card.xpath('.//a[@class="item-title"]/@title')
    link = card.xpath('.//a[@class="item-title"]/@href')
    price = card.xpath('.//span[@class="price-current"]/text()')
    site = 'aliexpress'
    # data={}
    if title != []:
        data = {'title': title[0], 'price': price[0],
                'link': link[0], 'site': site}
        return data


def scraperAliExpress(item):
    ads_data = []
    _f = open('ali.csv', "w+", encoding='utf-8')
    _f.write("")
    _f.close()
    os.remove('ali.csv')
    _f = open('ali.csv', "x", encoding='utf-8')
    _f.close()
    for page in range(1, 10):
        url = f'https://www.aliexpress.com/wholesale?trafficChannel=main&d=y&CatId=0&SearchText={item}&ltype=wholesale&SortType=default&page={page}'
        driver.get(url)

        tree = html.fromstring(driver.page_source)
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")

        cards = tree.xpath('//li[@class="list-item"]')
        for card in cards:
            data = scrapeAliExpress(card)
            ads_data.append(data)

    with open('ali.csv', 'a+', encoding='utf-8') as f:
        f.write("title,price,link,site\n")
    f.close()
    write_csv(ads_data)


def main():
    scraperAliExpress('dress')


if __name__ == '__main__':
    main()
