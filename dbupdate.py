import main as myMain
import parse as myParse
import datetime

def update(tickers, date):
    for ticker in tickers:
        T = myParse.Parser(ticker)
        for d in date: 
            options = T.toDict(d)
            update_db(options, ticker)

def update_db(options, ticker):
    maturity = options['maturity']
    for style in ["call","put"]:
        option = options[style]
        for target in option.iterkeys():
            attr = {}
            #attr["date"] = datetime.datetime.now().date()
            attr["ticker"] = ticker
            attr["target"] = target
            attr["price"]  = option[target]
            attr["maturity"] = maturity
            if style == "call":
                attr["style"]  = True
            else:
                attr["style"]  = False
            equity = myMain.Equity(**attr)
            equity.put()