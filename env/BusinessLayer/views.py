from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
import csv
from webscraper import *
from tapaz import *
from amazon import *
from .filterer import *
from browser import *


views = Blueprint('views', __name__)
ls_all = []


@views.route('/')
@login_required
def home():
    ls_all.clear()
    return render_template("home.html", user=current_user, isSearching=False)


def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier


@views.route("/find/<itemToFind>/stores/<store_list>/filterBy/<filterOption>/<isAscending>/priceRange/from/<price_from>/to/<price_to>/currency/<currency>", methods=['GET', 'POST'])
def findPage(itemToFind, store_list, filterOption, isAscending, price_from, price_to, currency):
    ls_all = []
    _store_list = str(store_list)
    obj1 = Amazon()
    obj2 = TapAz()
    if "tapaz" in _store_list:
        obj2.scraper(itemToFind)
    if "amazon" in _store_list:
        obj1.scraper(itemToFind)

    with open('results.csv', mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count != 0:
                if row["price"] != "" and row["price"].find('price') == -1 and row["price"].find(",") == -1:
                    if currency == "azn":
                        if row["site"] == "tapaz":
                            row["price"] = row["price"] + "₼"  # ₼
                        if row["site"] == "amazon":
                            row["price"] = str(
                                truncate(int(row["price"]) * 1.7, 2)) + "₼"
                    elif currency == "usd":  # us dollars
                        if row["site"] == "tapaz":
                            row["price"] = str(
                                truncate(int(row["price"]) / 1.7, 2)) + "$"
                        if row["site"] == "amazon":
                            row["price"] = row["price"] + "$"
                else:
                    row["price"] = ""

                if row["site"] == "amazon":
                    row["link"] = "https://amazon.com" + row["link"]
                    row["title"] += " -Amazon"
                if row["site"] == "tapaz":
                    row["link"] = "https://tap.az" + row["link"]
                    row["title"] += " -TapAz"

                ls_temp = [row["title"], row["price"],
                           row["link"], row["site"]]
                ls_all.append(ls_temp)
            line_count = line_count + 1

    _f = open('results.csv', "w+", encoding='utf-8')
    filterer = Filterer()
    pricefilter = Price()
    if filterOption.find('shipping') == -1:
        ls_all = pricefilter.FilterPrices(ls_all, price_from, price_to)[:]

    if filterOption != None:
        ls_all = filterer.filterBy(ls_all, filterOption, isAscending)[:]

    ls_amazon = []
    ls_tapaz = []
    for elem in ls_all:
        if elem[3] == 'amazon':
            ls_amazon.append(elem)
        if elem[3] == 'tapaz':
            ls_tapaz.append(elem)

    return render_template("base.html", user=current_user, isSearching=True, itemsAmazon=ls_amazon, itemsTapaz=ls_tapaz)


@views.route("/process", methods=['GET', 'POST'])
def process():
    ls_all.clear()
    if request.method == "POST":
        if request.form['search_button'] == 'Search':
            itemToFind = request.form['search_text']
            store_list = request.form.getlist('store')
            filterOption = request.form.get('filteroption')
            Ascending = request.form.getlist('ascending')[0]
            price_from = request.form.get('from')
            price_to = request.form.get('to')
            currency = request.form.getlist('currency')[0]

            return redirect(url_for("views.findPage", itemToFind=itemToFind, store_list=store_list, filterOption=filterOption, isAscending=Ascending, price_from=price_from, price_to=price_to, currency=currency))

    return redirect(url_for("views.home"))
