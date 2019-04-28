from globalparameters import *
from global0 import *
import  Data_processing
import utils
import csv
import RBreaker
from collections import deque
from collections import defaultdict
import marketposition2
import numpy as np
from scipy.stats import norm
if __name__=="__main__":
    flag=dict()
    for s in SYMBOLS:
        flag[s]=0
    channel = grpc.insecure_channel(MARKET_CHANNEL)  # 57500
    stub = broker_pb2_grpc.MarketDataStub(channel)
    while 1:
        response = stub.subscribe(common_pb2.Empty())
        for market_data in response:
            if int(market_data.instruments[0].timestamp)%900==899:
                for instrument in market_data.instruments:
                    if instrument.symbol in SYMBOLS:
                        if instrument.last_price-instrument.deliver_price>0.1:
                            utils.new_order(common_pb2.NEW_ORDER,None,common_pb2.ASK,instrument.symbol,50,None,True,common_pb2.SHORT)
                            flag[s]=-1
                            print("233")
                        if instrument.last_price - instrument.deliver_price < -0.1:
                            utils.new_order(common_pb2.NEW_ORDER, None, common_pb2.BID, instrument.symbol, 50, None,
                                            True, common_pb2.LONG)
                            flag[s]=1
                            print("233")
            else:
                if int(market_data.instruments[0].timestamp) % 900 == 1:
                    for s in SYMBOLS:
                        if flag[s]==-1:
                            utils.new_order(common_pb2.NEW_ORDER, None, common_pb2.BID, instrument.symbol, 50, None,
                                            True, common_pb2.SHORT)
                        if flag[s]==1:
                            utils.new_order(common_pb2.NEW_ORDER, None, common_pb2.ASK, instrument.symbol, 50, None,
                                            True, common_pb2.LONG)
            break


