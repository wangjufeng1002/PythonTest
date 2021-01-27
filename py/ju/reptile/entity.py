class Data:
    date = ''
    desc = ''
    url = ''

    def __init__(self, date, desc, url):
        self.date = date
        self.desc = desc
        self.url = url

    @classmethod
    def getDesc(self):
        return self.desc

    @classmethod
    def getUrl(self):
        return self.url
