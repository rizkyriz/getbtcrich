import time, json, requests

"""
API URLs
https://www.bitstamp.net/api/
https://www.bitfinex.com/pages/api
"""


# define the function which is requesting the API data in JSON
# return the bid and ask data from the API call as numbers 'float'
def bitstamp():
    stampv2 = requests.get('https://www.bitstamp.net/api/order_book/').json()
    return [float(stampv2['bids'][1][0]), float(stampv2['bids'][1][1])], [float(stampv2['asks'][1][0]), float(stampv2['asks'][1][1])]


def bitfinex():
    finexv2 = requests.get('https://api.bitfinex.com/v2/ticker/tBTCUSD').json()
    return [(finexv2[0]), (finexv2[1])], [(finexv2[2]), (finexv2[3])]

#initialize variables
stampBid = []
stampAsk = []
tradeSize = 0.00
spread = 0.00
pnl = 0.00
arbFlag = 0

interval = 5 #SECONDS BETWEEN EACH RUN

# While true will run the while statement forever until manually stopped
while True:

    tradeSize = 0.00
    spread = 0.00
    pnl = 0.00
    arbFlag = 1

    # Define variables and assign value for top of orderbook
    stampBid, stampAsk = bitstamp()
    finexBid, finexAsk = bitfinex()

    #print orderbook
    print ("Bitstamp market: ", stampBid[1], " ", stampBid[0], "/", stampAsk[0], " ", stampAsk[1])
    print ("Bitfinex market: ", finexBid[1], " ", finexBid[0], "/", finexAsk[0], " ", finexAsk[1])

    # Define variables that calculate the cash ask-bid arbitrage differences on each exchange
    if (stampBid[0]>finexAsk[0]):
        #buy finex sell stamp
        tradeSize = min(finexAsk[1],stampBid[1])
        spread = (stampBid[0]/finexAsk[0]-1)*100
        pnl = tradeSize * ((finexAsk[0]+stampBid[0])/2) * spread
    else:
        if (stampAsk[0]<finexBid[0]):
        #sell finex buy stamp
            tradeSize = min(finexBid[1], stampAsk[1])
            spread = (finexBid[0]/stampAsk[0] - 1)*100
            pnl = tradeSize * ((finexBid[0] + stampAsk[0]) / 2) * spread
        else:
        #nothing to do
            print("Nothing to do, better luck in %i seconds" % interval)
            arbFlag = 0

    if(arbFlag==1):
        print ("Money in the bank! Spread: %5.3f%%, P&L = $ %5.2f" % (spread, pnl))

    print ('\n')
    # Run every X seconds
    time.sleep(interval)  # time is in seconds
