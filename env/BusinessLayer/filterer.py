class Filterer:
    def filterBy(self, ls_all__, filterOption, isAscending):
        if filterOption == "shipping":
            _nonShipable = []
            _shipable = []
            for elem in ls_all__:
                if elem[1] == "":
                    _nonShipable.append(elem)
                else:
                    _shipable.append(elem)
            ls_all__ = _nonShipable[:]
            ls_all__.extend(_shipable)

        if filterOption == "price":
            ls_all__ = sorted(ls_all__, key=lambda row: float(row[1][:-1]))
            _ls_temp = []
            for elem in ls_all__:
                if elem[1] != "":
                    _ls_temp.append(elem)
                    ls_all__ = _ls_temp[:]

        if isAscending == "ascending":
            isAscsending = True
        else:
            isAscending = False

        if isAscending != None and not isAscending:
            ls_all__ = ls_all__[::-1]
        return ls_all__

class Sorter:
    def sortPrices(self, ls_all__, price_from, price_to):
        if price_from == None:
            price_from = 0
        if price_to == None:
            price_to = 100000000

        _ls_temp = []
        for elem in ls_all__:
            if elem[1] != "" and elem[1].find('price') == -1 and elem[1].find(",") == -1 and float(elem[1][:-1]) >= int(price_from) and float(elem[1][:-1]) <= int(price_to):
                _ls_temp.append(elem)
        ls_all__ = _ls_temp[:]
        return ls_all__