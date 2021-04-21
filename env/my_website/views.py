from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
import csv
from webscraper import *


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


# data = []
# @views.route('/find/<item>')
# @login_required
# def find(item):
#     data.clear()
#     scraperAmazon(item)
#     # scraperTapAz(item)
#     with open("results.csv", mode="r", encoding='utf-8') as csv_file:
#         csv_reader = csv.DictReader(csv_file)
#         line_count = 0
#         for row in csv_reader:
#             if line_count != 0:
#                 if row["price"] != "":
#                     row["price"] = row["price"] + "$"
#                 else:
#                     row["price"] = "Price is not defined"

#                 ls_temp = [row["title"], "https://amazon.com" +
#                            row["link"], row["price"]]
#                 data.append(ls_temp)
#                 # if row["site"] == "Amazon":
#                 #     row["link"] = "https://amazon.com" + row["link"]
#                 #     row["title"] += "(Amazon)"
#                 # else:
#                 #     row["link"] = "https://tap.az" + row["link"]
#                 #     row["title"] += "(TapAz)"

#                 # ls_temp = [row["title"], row["link"], row["price"], row["site"]]
#                 data.append(ls_temp)
#             line_count = line_count + 1
#     return render_template("home.html", user=current_user, isSearching=True, items=data)


# @views.route("/find/<itemToFind>/stores/<store_list>/filterBy/<filterOption>/<isAcsending>/priceRange/from/<price_from>/to/<price_to>/currency/<currency>", methods=['GET', 'POST'])
# def findPage(itemToFind, store_list, filterOption, isAcsending, price_from, price_to, currency):
@views.route("/find/<itemToFind>/stores/<store_list>/currency/<currency>", methods=['GET', 'POST'])
def findPage(itemToFind, store_list, currency):
    ls_all = []
    _store_list = store_list.lower().split("_")
    print(_store_list)
    
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
                            row["price"] = row["price"] + "₼"  # ₼
                        else:
                            row["price"] = str(
                                truncate(int(row["price"]) * 1.7, 2)) + "₼"
                    else:  # us dollars
                        if row["site"] == "tapaz":
                            row["price"] = str(
                                truncate(int(row["price"]) / 1.7, 2)) + "$"
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

    # if filterOption.find('shipping') == -1:
    #     ls_all = filterPrices(ls_all, price_from, price_to)[:]

    # if filterOption != None:
    #     ls_all = filterBy(ls_all, filterOption, isAcsending)[:]
    ls_amazon = []
    ls_tapaz = []
    for elem in ls_all:
        if elem[3] == 'amazon':
            ls_amazon.append(elem)
        elif elem[3]=='tapaz':
            ls_tapaz.append(elem)
            
    return render_template("base.html", user=current_user, isSearching=True, itemsAmazon=ls_amazon, itemsTapaz=ls_tapaz)


# def filterBy(ls_all__, filterOption, isAcsending):
#     if filterOption == "shipping":
#         _nonShipable = []
#         _shipable = []
#         for elem in ls_all__:
#             if elem[1] == "---":
#                 _nonShipable.append(elem)
#             else:
#                 _shipable.append(elem)
#         ls_all__ = _nonShipable[:]
#         ls_all__.extend(_shipable)

#     elif filterOption == "price":
#         ls_all__ = sorted(ls_all__, key=lambda row: row[1])
#         _ls_temp = []
#         for elem in ls_all__:
#             if elem[1] != "---":
#                 _ls_temp.append(elem)
#         ls_all__ = _ls_temp[:]

#     if isAcsending == "true":
#         isAcsending = True
#     else:
#         isAcsending = False

#     if isAcsending != None and not isAcsending:
#         ls_all__ = ls_all__[::-1]
#     return ls_all__


# def filterPrices(ls_all__, price_from, price_to):
#     if price_from == None:
#         price_from = 0
#     if price_to == None:
#         price_to = 100000000

#     _ls_temp = []
#     for elem in ls_all__:
#         if elem[1] != "---" and elem[1].find('price') == -1 and elem[1].find(",") == -1 and float(elem[1][:-1]) >= int(price_from) and float(elem[1][:-1]) <= int(price_to):
#             _ls_temp.append(elem)
#     ls_all__ = _ls_temp[:]
#     return ls_all__


@views.route("/process", methods=['GET', 'POST'])
def process():
    ls_all.clear()
    if request.method == "POST":
        if request.form['search_button'] == 'Search':
            return redirect(url_for("findPage", itemToFind = request.form['search_text'], store_list=request.form['store'], currency=request.form['Currency']))
    
    return redirect(url_for("views.home"))



# @views.route('/results', methods=['GET', 'POST'])
# def results():
#     form=SearchForm()
    