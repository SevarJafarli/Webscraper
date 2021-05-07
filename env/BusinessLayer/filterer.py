class Filterer:
    def __init__(self, ls_all__, filterOption, price_from, price_to, isAscending):
        self.__ls_all = ls_all__
        self.__filterOption = filterOption
        self.__isAscending = isAscending
        self.__price_from = price_from
        self.__price_to = price_to
        
    def filterBy(self, ls_all__, filterOption):
        ls_all = self.__ls_all[:]

        if self.__filterOption == "shipping":
            _nonShipable = []
            _shipable = []
            for elem in ls_all__:
                if elem[1] == "":
                    _nonShipable.append(elem)
                else:
                    _shipable.append(elem)
            ls_all__ = _nonShipable[:]
            ls_all__.extend(_shipable)

        if self.__filterOption == "price":
            ls_all__ = sorted(ls_all__, key=lambda row: float(row[1][:-1]))
            _ls_temp = []
            for elem in ls_all__:
                if elem[1] != "":
                    _ls_temp.append(elem)
                    ls_all__ = _ls_temp[:]
                    
        ls_all__= self.sort(ls_all__)
        return ls_all__
        # if isAscending == "ascending":
        #     Ascending = True
        # else:
        #     Ascending = False

        # if isAscending != None and not isAscending:
        #     ls_all__ = ls_all__[::-1]
        # return ls_all__

    def sort(self, ls_all__):
         ls_all__ = ls_all__[:]
         if self.__isAscending == "ascending":
                self.__isAscending = True
         else:
                self.__isAscending = False

         if self.__isAscending != None and not self.__isAscending:
                ls_all__ = ls_all__[::-1]
         return ls_all__
    

    def FilterPrices(self, ls_all__, price_from, price_to):
        
        if self.__price_from == None:
            self.__price_from = 0
        if self.__price_to == None:
            self.__price_to = 100000000

        _ls_temp = []
        for elem in ls_all__:
            if elem[1] != "" and elem[1].find('price') == -1 and elem[1].find(",") == -1 and float(elem[1][:-1]) >= int(price_from) and float(elem[1][:-1]) <= int(price_to):
                _ls_temp.append(elem)
        ls_all__ = _ls_temp[:]
        return ls_all__