from abc import ABC, abstractmethod

class MarketData(ABC):
    @abstractmethod
    def get_streaming_data(self,ticker):
        pass
    @abstractmethod
    def stop_streaming_data(self, ticker):
        pass