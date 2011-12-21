from google.appengine.api import urlfetch
from BeautifulSoup import BeautifulSoup
import re
from datetime import datetime

# input : ticker (AAPL)
# output : structured data
class Parser:
    def __init__(self, ticker):
        self.ticker = ticker
        self.link = "http://finance.yahoo.com/q/op?s="
    
    def toLink(self, year, month):
        post = "%s&m=%s-%s"%(self.ticker, year, month)
        return self.link + post
        
    def fetch(self, url):
        result = urlfetch.fetch(url)
        if result.status_code == 200:
          return result.content
        else:
          return None
          
    def debug(self):
        data = self.fetch(self.toLink('2012', '02'))
        return self.process(data)
    
    def toDict(self, date):
        year = date.year
        month = date.month
        data = self.process( self.fetch(self.toLink(year, month)))
        return data
    
    def process(self, data):
        option = {}
        soup = BeautifulSoup(data)
        pdate = soup.find(text = re.compile("Expire at close*") ).split(',')
        ddate = datetime.strptime(pdate[1] + pdate[2], " %B %d %Y")
        option['maturity'] = ddate.date()
        
        tables = soup.findAll("table", {"class":"yfnc_datamodoutline1"})
        
        
        # parsing call options price
        table = tables[0]
        pairs = {}
        trs = table.findAll("tr")
        for tr in trs:
            tds = tr.findAll("td", {"class":lambda x: x in ["yfnc_h","yfnc_tabledata1"]})
            if len(tds) > 7:
                strike = float(tds[0].find("strong").string)
                last   = float(tds[2].find("span").string)
                pairs[strike] = last
        option['call'] = pairs
        
        # parsing put options price
        table = tables[1]
        pairs = {}
        trs = table.findAll("tr")
        for tr in trs:
            tds = tr.findAll("td", {"class":lambda x: x in ["yfnc_h","yfnc_tabledata1"]})
            if len(tds) > 7:
                strike = float(tds[0].find("strong").string)
                last   = float(tds[2].find("span").string)
                pairs[strike] = last
        option['put'] = pairs
        
        return option

