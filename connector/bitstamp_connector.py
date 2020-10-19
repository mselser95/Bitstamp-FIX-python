from connector.fixconnector import FixConnector
from classes.marketdata import MarketData
import quickfix


class BitStamp_Connector(MarketData):

    initiator = 0
    settings = 0
    fix_connector = 0

    def __init__(self,Brain):
        self.fix_connector = FixConnector(Brain)

        self.settings = quickfix.SessionSettings("./config/config.cfg")
        storefactory = quickfix.FileStoreFactory(self.settings)
        logfactory = quickfix.FileLogFactory(self.settings)
        self.initiator = quickfix.SocketInitiator(self.fix_connector, storefactory, self.settings, logfactory)
        self.initiator.start()
        while not self.initiator.isLoggedOn():
            a = 1

    def get_streaming_data(self, ticker):
        self.fix_connector.marketDataRequest(ticker,
                                             quickfix.SubscriptionRequestType_SNAPSHOT_PLUS_UPDATES)

    def stop_streaming_data(self, ticker):
        self.fix_connector.marketDataRequest(ticker,
                                             quickfix.SubscriptionRequestType_DISABLE_PREVIOUS_SNAPSHOT_PLUS_UPDATE_REQUEST)

    def send_market_order(self,ticker,side,qty):
        self.fix_connector.sendOrder(ticker, side, "MARKET", 0, qty)

    def send_limit_order(self, ticker, side, px, qty):
        self.fix_connector.sendOrder(ticker,side,"MARKET",0,qty)
