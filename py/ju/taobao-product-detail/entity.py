from typing import Any
import threading, time
import logging
from logging import handlers


class Book:
    activeDesc = ''

    def __init__(self, tmId, name, isbn, auther, price, fixPrice, promotionPrice, promotionPriceDesc, promotionType,
                 activeDesc,
                 activeStartTime,
                 activeEndTime,
                 shopName, category):
        self.tmId = tmId
        self.name = name
        self.isbn = isbn
        self.auther = auther
        self.price = price
        self.fixPrice = fixPrice
        self.promotionPrice = promotionPrice
        self.promotionPriceDesc = promotionPriceDesc
        self.promotionType = promotionType
        self.activeDesc = activeDesc
        self.activeStartTime = activeStartTime
        self.activeEndTime = activeEndTime
        self.shopName = shopName
        self.category = category

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

    def setPromotionType(self, promotionPriceType):
        self.promotionType = promotionPriceType

    def getPromotionType(self):
        if self.promotionType is None:
            return "NULL"
        return self.promotionType

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

    def getActiveDescStr(self):
        if self.activeDesc is None:
            return ''
        return ",".join(self.getActiveDesc())

    def getTmId(self):
        return self.tmId

    def getPromotionPriceDesc(self):
        return self.promotionPriceDesc

    def setPromotionPriceDesc(self, promotionPriceDesc):
        self.promotionPriceDesc = promotionPriceDesc

    def setShopName(self, shopName):
        self.shopName = shopName

    def getShopName(self):
        return self.shopName

    def setActiveStartTime(self, activeStartTime):
        self.activeStartTime = activeStartTime

    def getActiveStartTime(self):
        if self.activeStartTime is None:
            return "1996-10-02"
        activeStartTime = self.activeStartTime / 1000.0
        timearr = time.localtime(activeStartTime)
        return time.strftime("%Y-%m-%d %H:%M:%S", timearr)

    def setActiveEndTime(self, activeEndTime):
        self.activeEndTime = activeEndTime

    def getActiveEndTime(self):
        if self.activeEndTime is None:
            return "1996-10-02"
        activeEndTime = self.activeEndTime / 1000.0
        timearr = time.localtime(activeEndTime)
        return time.strftime("%Y-%m-%d %H:%M:%S", timearr)

    def getCategory(self):
        return self.category
    def setCategory(self,category):
        self.category  =category

    def toString(self):
        result = []
        result.append("[天猫ID:" + self.getTmId() + "]")
        result.append("[书名:" + self.getName() + "]")
        result.append("[ISBN编码:" + self.getIsbn() + "]")
        result.append("[作者:" + self.getAuther() + "]")
        result.append("[默认价格:" + self.getPrice() + "]")
        result.append("[促销价:" + self.getPromotionPrice() + "]")
        result.append("[促销价描述:" + self.getPromotionPriceDesc() + "]")
        result.append("[活动:" + (",".join(self.getActiveDesc())) + "]")
        return ",".join(result)
    # return self.getName() + "," + self.getIsbn() + "," +self.getAuther()+ "," +self.getPrice() +"," +self.getPromotionPrice() + self.getActiveDesc()


class ItemUrl:
    def __init__(self, itemId, itemUrl, shopName, category):
        self.itemId = itemId
        self.itemUrl = itemUrl
        self.shopName = shopName
        self.category = category

    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)

    def __getattribute__(self, name: str) -> Any:
        return super().__getattribute__(name)

    # def getItemId(self):
    #     return self.itemId
    #
    # def getItemUrl(self):
    #     return self.itemUrl
    #
    # def getShopName(self):
    #     return self.shopName
    #
    # def setItemId(self, itemId):
    #     self.itemId = itemId
    #
    # def setItemUrl(self, itemUrl):
    #     self.itemUrl = itemUrl
    #
    # def setShopName(self, shopName):
    #     self.shopName = shopName


class Logger(object):
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }  # 日志级别关系映射

    def __init__(self, filename, level='info', when='D', backCount=3,
                 fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'):
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)  # 设置日志格式
        self.logger.setLevel(self.level_relations.get(level))  # 设置日志级别
        sh = logging.StreamHandler()  # 往屏幕上输出
        sh.setFormatter(format_str)  # 设置屏幕上显示的格式
        th = handlers.TimedRotatingFileHandler(filename=filename, when=when, backupCount=backCount,
                                               encoding="utf-8")  # 往文件里写入#指定间隔时间自动生成文件的处理器
        # 实例化TimedRotatingFileHandler
        # interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一）
        # midnight 每天凌晨
        th.setFormatter(format_str)  # 设置文件里写入的格式
        self.logger.addHandler(sh)  # 把对象加到logger里
        self.logger.addHandler(th)


if __name__ == '__main__':
    log = Logger('all.log', level='debug')
    log.logger.debug('debug')
    log.logger.info('info')
    log.logger.warning('警告')
    log.logger.error('报错')
    log.logger.critical('严重')
    Logger('error.log', level='error').logger.error('error')
