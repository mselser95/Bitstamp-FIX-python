
class LAST_TRADE():
    def __init__(self):
        self.Symbol=""
        self.MDEntryID=""
        self.MDUpdateAction=""
        self.MDEntryType=""
        self.MDEntryPx=0
        self.MDEntrySize=0
    def __str__(self):
        return ('LT: \t%s\tPrice: %f\tSize: %f'
                % (self.Symbol,self.MDEntryPx, self.MDEntrySize))

class BOOK():
    symbol = ""
    bid = list()
    ask = list()
    bid_size = list()
    ask_size = list()

    def __str__(self):
        return ("TOB:\t" + self.symbol + "\tAsk_Px: " + str(self.ask[0]) +
                "\tAsk_size: " + str(self.ask_size[0]) + "\tBid_px: " +
                str(self.bid[0]) + "\tBid_size: " + str(self.bid_size[0]))