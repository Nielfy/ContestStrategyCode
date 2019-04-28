from globalparameters import*
from global0 import *
import utils

class status:
    def __init__(self,symbol):
        self.symbol=symbol
        self.pricelist=[]
        self.longpositions=0
        self.avgentry_long=0
        self.longpnl=0
        self.shortpositons=0
        self.avgentry_short=0
        self.shortpnl=0
        self.pendingorders=[] #store pending orderid


    def renew_market_position(self):
        positions=utils.get_trader(common_pb2.FULL_INFO)
        if hasattr(positions, 'long_positions') and positions.long_positions[self.symbol] is not None:
            if hasattr(positions.long_positions[self.symbol],'volume'):
                if positions.long_positions[self.symbol].volume>0:
                    self.longpositions = positions.long_positions[self.symbol].volume
                    self.avgentry_long = positions.long_positions[self.symbol].avg_price
                    self.longpnl= positions.long_positions[self.symbol].unrealized_pnl
        if hasattr(positions, 'short_positions') and positions.short_positions[self.symbol] is not None:
            if hasattr(positions.short_positions[self.symbol], 'volume'):
                if positions.short_positions[self.symbol].volume > 0:
                    self.shortpositions = - positions.short_positions[self.symbol].volume
                    self.avgentry_long = positions.short_positions[self.symbol].avg_price
                    self.shortpnl = positions.short_positions[self.symbol].unrealized_pnl
    def add_to_price(self,p):
        self.pricelist.append(p)
    def open_long(self):
        #todo should return orderid

    def open_short(self):
        #todo should return orderid

    def close_long(self):
        #todo try close by market order

    def close_short(self):
        #todo same as above



