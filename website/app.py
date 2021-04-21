from flask import Flask, redirect, url_for, render_template , request
from webscraper import scraperAmazon, scraperTapAz
import csv
import math

app = Flask(__name__)

def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier

@app.route("/", methods=['GET', 'POST'])
def home():
    # ls_all.clear()
    return render_template("./public/base.html", isSearching = False)

@app.route("/find/<itemToFind>/stores/<store_list>/filterBy/<filterOption>/<isAcsending>/priceRange/from/<price_from>/to/<price_to>/currency/<currency>", methods=['GET', 'POST'])
def findPage(itemToFind, store_list, filterOption, isAcsending, price_from, price_to, currency):
    ls_all = []
    _store_list = store_list.lower().split("_")
    print(_store_list)
    # ls_all.clear()
    # scraper(itemToFind)
    if "amazon" in _store_list:
        scraperAmazon(itemToFind)
    if "tapaz" in _store_list:
        scraperTapAz(itemToFind)
    
    with open('results.csv', mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count != 0:
                if row["price"] != "" and row["price"].find('price') == -1 and row["price"].find(",") == -1:
                    if currency == "azn":     
                        if row["site"] == "tapaz":
                            row["price"] = row["price"] + "₼" # ₼
                        else:
                            row["price"] = str(truncate(int(row["price"]) * 1.7, 2)) + "₼"
                    else: # us dollars
                        if row["site"] == "tapaz":
                            row["price"] = str(truncate(int(row["price"]) / 1.7, 2)) + "$"
                        else:
                            row["price"] = row["price"] + "$"
                else:
                    row["price"] = "---"
                    
                if row["site"] == "amazon":
                    row["link"] = "https://amazon.com" + row["link"]
                    row["title"] += "(Amazon)"
                else:
                    row["link"] = "https://tap.az" + row["link"]
                    row["title"] += "(TapAz)"

                ls_temp = [row["title"], row["price"], row["link"], row["site"]]
                ls_all.append(ls_temp)
            line_count = line_count + 1

    if filterOption.find('shipping') == -1:
        ls_all = filterPrices(ls_all, price_from, price_to)[:]

    if filterOption != None:
        ls_all = filterBy(ls_all, filterOption, isAcsending)[:]
    


    return render_template("./public/base.html", isSearching = True, items = ls_all)


def filterBy(ls_all__, filterOption, isAcsending):
    if filterOption == "shipping":
        _nonShipable = []
        _shipable = []
        for elem in ls_all__:
            if elem[1] == "---":
                _nonShipable.append(elem)
            else:
                _shipable.append(elem)
        ls_all__ = _nonShipable[:]
        ls_all__.extend(_shipable)

    elif filterOption == "price":
        ls_all__ = sorted(ls_all__, key = lambda row: row[1])
        _ls_temp = []
        for elem in ls_all__:
            if elem[1] != "---":
               _ls_temp.append(elem)  
        ls_all__ = _ls_temp[:]

    if isAcsending == "true":
        isAcsending = True
    else:
        isAcsending = False

    if isAcsending != None and not isAcsending:
        ls_all__ = ls_all__[::-1]
    return ls_all__

def filterPrices(ls_all__, price_from, price_to):
    if price_from == None:
        price_from = 0
    if price_to == None:
        price_to = 100000000
    
    _ls_temp = []
    for elem in ls_all__:
        if elem[1] != "---" and elem[1].find('price') == -1 and elem[1].find(",") == -1 and float(elem[1][:-1]) >= int(price_from) and float(elem[1][:-1]) <= int(price_to):
            _ls_temp.append(elem)  
    ls_all__ = _ls_temp[:]
    return ls_all__


@app.route("/process", methods=['GET', 'POST'])
def process():
    ls_all.clear()
    if request.method == "POST":
        if request.form['submit_button'] == 'Search':
            return redirect(url_for("findPage", itemToFind = request.form['search_text']))
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)