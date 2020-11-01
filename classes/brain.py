import connector.bitstamp_connector as connector
import time
from classes.book import LAST_TRADE,BOOK
import collections
import bitstamp.client

class Brain():
    connector = 0
    book = BOOK()
    lt = LAST_TRADE()
    handlers = None

    btc_balance = 0
    btc_available = 0
    trading_client = 0

    def __init__(self):
        self.handlers = collections.defaultdict(set)
        self.register("OnBookUpdated", self.OnBookUpdated)
        self.register("OnTradeUpdated", self.OnTradeUpdated)
        self.connector = connector.BitStamp_Connector(self.handlers)
        self.trading_client = bitstamp.client.Trading(
        username = 'YOUR USERNAME ID', key = 'YOUT API KEY', secret = 'YOUR API SECRET')


    def register(self, event, callback):
        self.handlers[event].add(callback)

    def run(self):
        self.GetBalance()
        self.connector.get_streaming_data("BTC/USD")
        # self.connector.send_limit_order("BTC/USD", "BUY", 0, 100)
        while 1:
            time.sleep(1)
        # connector.stop_streaming_data("BTC/USD")

    def OnBookUpdated(self,book):

        """
        YOUR CODE TO RUN ON BOOK UPDATED
        """

        print(book)

    def OnTradeUpdated(self,trade):

        """
        YOUR CODE TO RUN ON BOOK UPDATED
        """

        print(trade)

    def GetBalance(self):
        self.btc_available = self.trading_client.account_balance()['btc_available']
        self.btc_balance = self.trading_client.account_balance()['btc_balance']
        print(self.trading_client.account_balance())
        print("Available BTC: " + str(self.btc_available) + "\tBalance BTC: " + str(self.btc_balance))