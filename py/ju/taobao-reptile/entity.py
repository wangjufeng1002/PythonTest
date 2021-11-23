class Book:
    activeDesc = ''

    def __init__(self, tmId, name, isbn, auther, price, fixPrice, promotionPrice, activeDesc):
        self.tmId = tmId
        self.name = name
        self.auther = isbn
        self.auther = auther
        self.price = price
        self.fixPrice = fixPrice
        self.promotionPrice = promotionPrice
        self.activeDesc = activeDesc

    def setFixPrice(self, fixPrice):
        self.fixPrice = fixPrice

    def getFixPrice(self):
        if self.fixPrice is None:
            return "NULL"
        return self.fixPrice

    def setName(self, name):
        self.name = name

    def getName(self):
        if self.name is None:
            return "NULL"
        return self.name

    def setIsbn(self, isbn):
        self.isbn = isbn

    def getIsbn(self):
        if self.isbn is None:
            return "NULL"
        return self.isbn

    def setAuther(self, auther):
        self.auther = auther

    def getAuther(self):
        if self.auther is None:
            return "NULL"
        return self.auther

    def setPrice(self, price):
        self.price = price

    def getPrice(self):
        if self.price is None:
            return "NULL"
        return self.price

    def setPromotionPrice(self, promotionPrice):
        self.promotionPrice = promotionPrice

    def getPromotionPrice(self):
        if self.promotionPrice is None:
            return "NULL"
        return self.promotionPrice

    def setActiveDesc(self, activeDesc):
        self.activeDesc = activeDesc

    def getActiveDesc(self):
        if self.activeDesc is None:
            return []
        return self.activeDesc

    def getTmId(self):
        return self.tmId

    def toString(self):
        result = []
        result.append("[天猫ID:" + self.getTmId() + "]")
        result.append("[" + self.getName() + "]")
        result.append("[" + self.getIsbn() + "]")
        result.append("[" + self.getAuther() + "]")
        result.append("[" + self.getPrice() + "]")
        result.append("[促销价:" + self.getPromotionPrice() + "]")
        result.append("[活动:" + (",".join(self.getActiveDesc())) + "]")
        return ",".join(result)
    # return self.getName() + "," + self.getIsbn() + "," +self.getAuther()+ "," +self.getPrice() +"," +self.getPromotionPrice() + self.getActiveDesc()
class Data:
    date = ''
    desc = ''
    id = ''

    def __init__(self, date, desc, id):
        self.date = date
        self.desc = desc
        self.id = id

    @classmethod
    def getDesc(self):
        return self.desc

    @classmethod
    def getId(self):
        return self.id

    @classmethod
    def getDate(self):
        return self.date
