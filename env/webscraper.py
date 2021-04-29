from bs4 import BeautifulSoup
from selenium import webdriver
from pathlib import Path
import csv
import os
# from my_website.views import *

browser = webdriver.Chrome(executable_path="E:\driver\chromedriver.exe")


def get_html(url):
    browser.get(url)
    return browser.page_source


def write_csv(ads):
    with open('results.csv', 'a+', encoding='utf-8') as f:
        fields = ['title', 'price', 'link', 'site']

        writer = csv.DictWriter(f, fieldnames=fields)

        for ad in ads:
            writer.writerow(ad)


class Website:
    @staticmethod
    def scrapeAmazon(card):
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

    def scraperAmazon(self, item):
        ads_data = []

        for i in range(1, 5):
            url = f'https://www.amazon.com/s?k={item}&page={i}&qid=1617312099&ref=sr_pg_2'
            html = get_html(url)

            soup = BeautifulSoup(html, 'lxml')

            cards = soup.find_all(
                'div', {'data-asin': True, 'data-component-type': 's-search-result'})

            for card in cards:
                data = self.scrapeAmazon(card)
                ads_data.append(data)

        with open('results.csv', 'a+', encoding='utf-8') as f:
            f.write("title,price,link,site\n")
        f.close()
        write_csv(ads_data)

    def scraperTapAz(self, item):
        ads_data = []
        url = f"https://tap.az/elanlar?utf8=%E2%9C%93&log=true&keywords={item}&q%5Bregion_id%5D="
        html = get_html(url)
        soup = BeautifulSoup(html, 'lxml')

        cards = soup.find_all('div', class_='products-i rounded')
        for card in cards:
            data = self.scrapeTapAz(card)
            ads_data.append(data)

        with open('results.csv', 'a+', encoding='utf-8') as f:
            f.write("title,price,link,site\n")
        f.close()
        write_csv(ads_data)

    @staticmethod
    def scrapeTapAz(card):
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


def main():
    obj = Website()
    obj.scraperAmazon("PC")


if __name__ == "__main__":
    if __name__ == '__main__':
        main()


# from bs4 import BeautifulSoup
# from selenium import webdriver
# from pathlib import Path
# import csv
# import os
# from my_website.views import *

# browser = webdriver.Chrome(executable_path="E:\driver\chromedriver.exe")

# def write_csv(ads):
#     with open('results.csv', 'a+', encoding='utf-8') as f:
#         fields = ['title', 'price', 'link', 'site']

#         writer = csv.DictWriter(f, fieldnames=fields)

#         for ad in ads:
#             writer.writerow(ad)


# def get_html(url):

#     browser.get(url)
#     return browser.page_source


# def scrapeAmazon(card):
#     try:
#         h2 = card.h2

#     except:
#         title = ''
#         link = ''

#     else:
#         title = h2.text.strip()
#         link = h2.a.get('href')

#     try:
#         price = card.find(
#             'span', class_='a-price-whole').text.strip('.').strip()
#     except:
#         price = ''
#     else:
#         price = ''.join(price.split(','))

#     site = 'amazon'

#     data = {'title': title, 'price': price, 'link': link, 'site': site}
#     return data


# def scraperAmazon(item):
#     ads_data = []
#     for i in range(1, 5):
#         url = f'https://www.amazon.com/s?k={item}&page={i}&qid=1617312099&ref=sr_pg_2'
#         html = get_html(url)

#         soup = BeautifulSoup(html, 'lxml')

#         cards = soup.find_all(
#             'div', {'data-asin': True, 'data-component-type': 's-search-result'})

#         for card in cards:
#             data = scrapeAmazon(card)
#             ads_data.append(data)

#     with open('results.csv', 'a+', encoding='utf-8') as f:
#         f.write("title,price,link,site\n")
#     f.close()
#     write_csv(ads_data)


# def scraperTapAz(item):
#     ads_data=[]
#     url = f"https://tap.az/elanlar?utf8=%E2%9C%93&log=true&keywords={item}&q%5Bregion_id%5D="
#     html = get_html(url)
#     soup = BeautifulSoup(html, 'lxml')

#     cards = soup.find_all('div', class_='products-i rounded')
#     for card in cards:
#         data = scrapeTapAz(card)
#         ads_data.append(data)

#     with open('results.csv', 'a+', encoding='utf-8') as f:
#         f.write("title,price,link,site\n")
#     f.close()
#     write_csv(ads_data)


# def scrapeTapAz(card):
#     link = card.find('a', class_='products-link').get('href')
#     title = card.find('div', class_='products-top').img.get('alt')
#     price = card.find('div', class_='products-price-container')

#     if price is None:
#         print("")
#     else:
#         Price = price.div.span.text.replace(' ', '')
#     Price = ''.join(Price.split(','))

#     site = 'tapaz'
#     data = {'title': title, 'price': Price, 'link': link, 'site': site}
#     return data
