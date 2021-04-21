from bs4 import BeautifulSoup
from selenium import webdriver
from pathlib import Path
import csv
import os

browser = webdriver.Chrome(executable_path="E:\driver\chromedriver.exe")
def get_html(url):
    browser.get(url)
    return browser.page_source

class Website:
    def write_csv(self, ads, filename):
        with open(filename, 'a+', encoding='utf-8') as f:
            fields = ['title', 'link', 'price']

            writer = csv.DictWriter(f, fieldnames=fields)

            for ad in ads:
                writer.writerow(ad)

    def scraper(self, item):
        pass

    def scrape_data(self, card):
        pass


class Amazon(Website):

    def scrape_data(self, card):
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

        data = {'title': title, 'link': link, 'price': price}
        return data

    def scraper(self, item, filename):
        ads_data = []
        _f = open(filename, "w+", encoding='utf-8')
        _f.write("")
        _f.close()
        os.remove(filename)
        _f = open(filename, "x", encoding='utf-8')
        _f.close()
        for i in range(1, 5):
            url = f'https://www.amazon.com/s?k={item}&page={i}&qid=1617312099&ref=sr_pg_2'
            html = get_html(url)

            soup = BeautifulSoup(html, 'lxml')

            cards = soup.find_all(
                'div', {'data-asin': True, 'data-component-type': 's-search-result'})

            for card in cards:
                data = self.scrape_data(card)
                ads_data.append(data)

        with open(filename, 'a+', encoding='utf-8') as f:
            f.write("title,link,price\n")
        f.close()
        self.write_csv(ads_data)


# class AliExpress(Website):
#     def scrape_data(self, card):
#         pass

#     def scraper(self, item):
#         ads_data = []
#         _f = open("results.csv", "w+", encoding='utf-8')
#         _f.write("")
#         _f.close()
#         os.remove("results.csv")
#         _f = open("results.csv", "x", encoding='utf-8')
#         _f.close()
#         for i in range(1, 5):
#             url = f'https://www.aliexpress.com/wholesale?trafficChannel=main&d=y&CatId=0&SearchText={item}&ltype=wholesale&SortType=default&page={i}'
#             html = get_html(url)
#             soup = BeautifulSoup(html, 'lxml')
#             cards=soup.find_all('li', class_='list-item')


class TapAz(Website):

    def scraper(self, item, filename):
        ads_data = []
        _f = open(filename, "w+", encoding='utf-8')
        _f.write("")
        _f.close()
        os.remove(filename)
        _f = open(filename, "x", encoding='utf-8')
        _f.close()
        url = f'https://tap.az/elanlar?utf8=%E2%9C%93&log=true&keywords={item}&q%5Bregion_id%5D='
        html = get_html(url)
        soup = BeautifulSoup(html, 'lxml')

        cards = soup.find_all('div', class_='products-i rounded')
        for card in cards:
            data = self.scrape_data(card)
            ads_data.append(data)

        with open(filename, 'a+', encoding='utf-8') as f:
            f.write("title,link,price\n")
        f.close()
        self.write_csv(ads_data, filename)

    def scrape_data(self, card):

        link = card.find('a', class_='products-link').get('href')
        title = card.find('div', class_='products-top').img.get('alt')
        price = card.find('div', class_='products-price-container')

        if price is None:
            print('')
        else:
            Price = price.div.span.text

        Link = 'https://tap.az' + link
        site='TapAz'
        data = {'title': title, 'link': Link, 'price': Price, 'site':site}
        return data


def main():
    ads = []
    tapaz = TapAz()
    tapaz.scraper('telefon', 'resul2.csv')


if __name__ == "__main__":
    main()
