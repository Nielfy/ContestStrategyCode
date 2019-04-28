from globalparameters import *
from global0 import *
import Data_processing
import utils
import csv
import RBreaker
#import Status
import time
import Levels


if __name__=="__main__":
    channel = grpc.insecure_channel(MARKET_CHANNEL)  # 57500

    # symbol="A001.PSE"
    # cur=Status.status(symbol)

    last_price = {}
    center_price = {}
    symbol1 = "A000.PSE"
    symbol2="B000.PSE"
    counter = 0
    A1Level = Levels.Levels()
    lastp = dict()
    while 1:
        stub = broker_pb2_grpc.MarketDataStub(channel)
        response = stub.subscribe(common_pb2.Empty())
        for market_data in response:
            # print(market_data)
            marketPosition.renew_all_longshort()
            print(marketPosition.marketPosition)
            instruments = market_data.instruments
            for instrument in instruments:
                if 'A' in instrument.symbol and marketPosition.marketLongPosition[instrument.symbol]>marketPosition.marketShortPosition[symbol1]:
                    order.insert_openShortPosition(symbol1,marketPosition.marketLongPosition[instrument.symbol]-marketPosition.marketShortPosition[symbol1],None,True)
                elif 'A' in instrument.symbol and marketPosition.marketLongPosition[instrument.symbol]<marketPosition.marketShortPosition[symbol1]:
                    order.insert_order(common_pb2.ASK,symbol1,marketPosition.marketShortPosition[symbol1]-marketPosition.marketLongPosition[instrument.symbol],None,True,common_pb2.LONG)
                if 'A' in instrument.symbol and marketPosition.marketShortPosition[instrument.symbol] > marketPosition.marketLongPosition[symbol1]:
                    order.insert_openLongPosition(symbol1, marketPosition.marketShortPosition[instrument.symbol]-marketPosition.marketLongPosition[symbol1],
                                                  None, True)
                elif 'A' in instrument.symbol and marketPosition.marketShortPosition[instrument.symbol] < \
                        marketPosition.marketLongPosition[symbol1]:
                    order.insert_order(common_pb2.BID, symbol1, marketPosition.marketLongPosition[symbol1] -
                                       marketPosition.marketShortPosition[instrument.symbol], None, True,
                                       common_pb2.SHORT)
                if 'B' in instrument.symbol and marketPosition.marketLongPosition[instrument.symbol]>marketPosition.marketShortPosition[symbol2]:
                    order.insert_openShortPosition(symbol2,marketPosition.marketLongPosition[instrument.symbol]-marketPosition.marketShortPosition[symbol2],None,True)
                elif 'B' in instrument.symbol and marketPosition.marketLongPosition[instrument.symbol]<marketPosition.marketShortPosition[symbol2]:
                    order.insert_order(common_pb2.ASK,symbol2,marketPosition.marketShortPosition[symbol2]-marketPosition.marketLongPosition[instrument.symbol],None,True,common_pb2.LONG)
                if 'B' in instrument.symbol and marketPosition.marketShortPosition[instrument.symbol] > marketPosition.marketLongPosition[symbol2]:
                    order.insert_openLongPosition(symbol2, marketPosition.marketShortPosition[instrument.symbol]-marketPosition.marketLongPosition[symbol2],
                                                  None, True)
                elif 'B' in instrument.symbol and marketPosition.marketShortPosition[instrument.symbol] < \
                        marketPosition.marketLongPosition[symbol2]:
                    order.insert_order(common_pb2.BID, symbol2, marketPosition.marketLongPosition[symbol2] -
                                       marketPosition.marketShortPosition[instrument.symbol], None, True,
                                       common_pb2.SHORT)
            order.execute()
        break



