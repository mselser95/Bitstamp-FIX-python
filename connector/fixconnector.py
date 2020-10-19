#!/usr/bin/python
# -*- coding: utf8 -*-
"""FIX Application"""
import sys

# from datetime import datetime
import quickfix as fix
import quickfix44 as fix44

# configured
__SOH__ = chr(1)



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

class FixConnector(fix.Application):
    """FIX Application"""

    callback = 0
    sessionID = 0

    orderID = 0
    execID = 0

    def __init__(self,callback=0):
        fix.Application.__init__(self)
        self.callback = callback

    def onCreate(self, sessionID):
        self.sessionID = sessionID
        return
    def onLogon(self, sessionID):
        self.sessionID = sessionID
        print("logged on!")
        return
    def onLogout(self, sessionID): 
        return

    def toAdmin(self, message, sessionID):
        username = fix.Username("w8poYpKKww6gHqclxdzxYYcVnHODFnAz")
        mypass = fix.Password("eSEMPHiajtPWk3ZvYXFx4MhziuzqIyRc")
        message.setField(username)
        message.setField(mypass)
        msg = message.toString().replace(__SOH__, "|")
        return
    def fromAdmin(self, message, sessionID):
        msg = message.toString().replace(__SOH__, "|")
        return
    def toApp(self, message, sessionID):
        msg = message.toString().replace(__SOH__, "|")
        return
    def fromApp(self, message, sessionID):
        msg = message.toString().replace(__SOH__, "|")
        self.onMessage(message, sessionID)
        return

    def onMessage(self, message, sessionID):
        # print("OnMessage %s" % message)
        msgType = fix.MsgType()
        message.getHeader().getField(msgType)
        if msgType.getValue() == "X":
            # print("MarketDataIncrementalRefresh %s" % message)
            noMDEntries = fix.NoMDEntries()
            message.getField(noMDEntries)
            if (noMDEntries.getValue() != 1):
                # print("NoMDEntries in MarketDataIncrementalRefresh is not 1!")
                return
            group = fix44.MarketDataIncrementalRefresh.NoMDEntries()
            message.getGroup(1, group);

            entryID = fix.MDEntryID()
            group.getField(entryID)
            action = fix.MDUpdateAction()
            group.getField(action);
            security = LAST_TRADE()
            security.MDEntryID = entryID.getValue()
            security.MDUpdateAction = action.getValue()
            symbol = fix.Symbol()
            if (group.isSetField(symbol)):
                group.getField(symbol)
                security.Symbol = symbol.getValue()
            entryType = fix.MDEntryType()
            if (group.isSetField(entryType)):
                group.getField(entryType)
                security.MDEntryType = entryType.getValue()
            price = fix.MDEntryPx()
            if (group.isSetField(price)):
                group.getField(price)
                security.MDEntryPx = price.getValue()
            size = fix.MDEntrySize()
            if (group.isSetField(size)):
                group.getField(size)
                security.MDEntrySize = size.getValue()
            qty = fix.MinQty()
            if (group.isSetField(qty)):
                group.getField(qty)
                security.MinQty = qty.getValue()

            self.callback(security)

        book = BOOK()
        if msgType.getValue() == 'W':


            Symbol = fix.Symbol()
            message.getField(Symbol)
            book.symbol = Symbol.getValue()

            noMDEntries = fix.NoMDEntries()
            message.getField(noMDEntries)

            group = fix44.MarketDataSnapshotFullRefresh.NoMDEntries()
            MDEntryType = fix.MDEntryType()
            MDEntryPx = fix.MDEntryPx()
            MDEntrySize = fix.MDEntrySize()

            for i in range(1,noMDEntries.getValue()):
                message.getGroup(i, group)
                group.getField(MDEntryType)
                group.getField(MDEntryPx)
                group.getField(MDEntrySize)
                if MDEntryType.getValue() == '0':
                    book.bid.append(MDEntryPx.getValue())
                    book.bid_size.append(MDEntrySize.getValue())
                if MDEntryType.getValue() == '1':
                    book.ask.append(MDEntryPx.getValue())
                    book.ask_size.append(MDEntrySize.getValue())

            print("TOB:\t" + book.symbol + "\tAsk_Px: " + str(book.ask[0]) + "\tAsk_size: " + str(book.ask_size[0]) + "\tBid_px: " + str(book.bid[0]) + "\tBid_size: " + str(book.bid_size[0]))
    pass


    def genOrderID(self):
        self.orderID = self.orderID+1
        return str(self.orderID)
    def genExecID(self):
        self.execID = self.execID+1
        return str(self.execID)


    def marketDataRequest(self,ticker,subscription_type):
        mdr = fix.Message()
        mdr.getHeader().setField(fix.BeginString(fix.BeginString_FIX44))
        mdr.getHeader().setField(fix.MsgType(fix.MsgType_MarketDataRequest))

        group = fix44.MarketDataRequest().NoRelatedSym()
        group.setField(fix.Symbol(ticker))
        mdr.addGroup(group)

        mdr.setField(fix.MDReqID('1'))
        mdr.setField(fix.SubscriptionRequestType(subscription_type))
        mdr.setField(fix.MarketDepth(0))
        mdr.setField(fix.NoMDEntryTypes(3))

        group = fix44.MarketDataRequest().NoMDEntryTypes()
        group.setField(fix.MDEntryType(fix.MDEntryType_BID))
        mdr.addGroup(group)
        group.setField(fix.MDEntryType(fix.MDEntryType_OFFER))
        mdr.addGroup(group)
        group.setField(fix.MDEntryType(fix.MDEntryType_TRADE))
        mdr.addGroup(group)
        fix.Session.sendToTarget(mdr, self.sessionID)
        return

    def sendOrder(self,ticker,side,type,px,qty):
        nos = fix.Message()
        nos.getHeader().setField(fix.BeginString(fix.BeginString_FIX44))
        nos.getHeader().setField(fix.MsgType(fix.MsgType_NewOrderSingle))

        symbol = fix.Symbol(ticker)
        nos.setField(symbol)
        if side == "BUY":
            side = fix.Side(fix.Side_BUY)
        if side == "SELL":
            side = fix.Side(fix.Side_SELL)
        nos.setField(side)

        if type == "MARKET":
            ordType = fix.OrdType(fix.OrdType_MARKET)
            px = fix.Price(0)
        if type == "LIMIT":
            ordType = fix.OrdType(fix.OrdType_MARKET)
            px = fix.Price(px)
        nos.setField(ordType)
        nos.setField(px)

        orderQty = fix.OrderQty(qty)
        clOrdID = fix.ClOrdID(self.genOrderID())
        nos.setField(orderQty)
        nos.setField(clOrdID)

        TimeInForce = fix.TimeInForce(fix.TimeInForce_GOOD_TILL_CANCEL)
        TransactTime = fix.TransactTime()
        nos.setField(TimeInForce)
        nos.setField(TransactTime)

        fix.Session.sendToTarget(nos, self.sessionID)

