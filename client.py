"""FIX GATEWAY"""
import connector.bitstamp_connector as connector
import time

def callback (book):
    print(book)

if __name__=='__main__':

    callback = callback
    connector = connector.BitStamp_Connector(callback)
    # connector.get_streaming_data("BTC/USD")
    connector.send_limit_order("BTC/USD","BUY",0,100)
    while 1:
        time.sleep(1)
    # connector.stop_streaming_data("BTC/USD")


