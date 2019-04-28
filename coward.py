from globalparameters import *
from global0 import *
# import  Data_processing
import utils
# import csv
# import RBreaker
from collections import deque
# from collections import defaultdict
import marketposition2
import numpy as np
from scipy.stats import norm
import threading
#factors;
#window,
riskyspread=0.1,
miniumbidinterval=0.04
miniumaskinterval=0.04

mintolong=10
mintoshort=10

protectiveorder=10
# stoploss=1000
# stopprofit=1000
# stopoccupying=10000
# min tolong
minsigma=0.2
# total volume 100
def run(s):
    for instrument in instruments:
        if instrument.symbol == s:
            # todo long short
            for orde in mktposition.orderdict[instrument.symbol]:
                orders[instrument.symbol].insert_cancel_orders(orde.order_id)
            lastp[instrument.symbol] = instrument.last_price
            pastprices[instrument.symbol].append(instrument.last_price)
            sigma[instrument.symbol] = np.std(pastprices[instrument.symbol])
            meanp[instrument.symbol] = np.mean(pastprices[instrument.symbol])
            # print(sigma[instrument.symbol])
            # print(np.mean(pastprices[instrument.symbol]))

            tocloseshort = 0
            tocloselong = 0
            if mktposition.marketLongPosition[instrument.symbol] > 0:
                tocloselong = mktposition.marketLongPosition[instrument.symbol]
            if mktposition.marketShortPosition[instrument.symbol] > 0:
                tocloseshort = mktposition.marketShortPosition[instrument.symbol]
                # todo check occupied cash!


            sigma[instrument.symbol] = max(minsigma,sigma[instrument.symbol])
            thisnorm = norm(meanp[instrument.symbol], sigma[instrument.symbol])
            # print(thisnorm.cdf(lastp[instrument.symbol]))
            p = thisnorm.cdf(lastp[instrument.symbol])
            if p == np.nan:
                p = 0.5

            tolong = int(max(mintolong, (1.0 - p) * totalvolume[instrument.symbol]))
            toshort = int(max(mintoshort, p * totalvolume[instrument.symbol]))
            longbias = max(min(0.15 * (1.0 - p), 0.1), miniumbidinterval)
            shortbias = max(min(0.15 * p, 0.1), miniumaskinterval)
            flag1=0
            flag2=0
            # if mktposition.occupiedcashlong[instrument.symbol] > 10000:
            #     # utils.new_order(common_pb2.NEW_ORDER, None, common_pb2.ASK, instrument.symbol,
            #     #                 mktposition.marketLongPosition[instrument.symbol], None,
            #     #                 True, common_pb2.LONG)
            #     orders[instrument.symbol].insert_order(common_pb2.ASK, instrument.symbol,
            #                                            mktposition.marketShortPosition[instrument.symbol],
            #                                            meanp[instrument.symbol] + shortbias,True,
            #                                            common_pb2.LONG)
            if mktposition.unrealizedPnllong[instrument.symbol] < -500 or mktposition.unrealizedPnllong[
                instrument.symbol] > 1000 or mktposition.occupiedcashlong[instrument.symbol] > 5000 or mktposition.marketLongPosition[instrument.symbol]>120:
                # utils.new_order(common_pb2.NEW_ORDER, None, common_pb2.ASK, instrument.symbol,
                #                 mktposition.marketLongPosition[instrument.symbol], None,
                #                 True, common_pb2.LONG)
                orders[instrument.symbol].insert_order(common_pb2.ASK, instrument.symbol,
                                                       mktposition.marketShortPosition[instrument.symbol],
                                                       meanp[instrument.symbol] + shortbias, True,
                                                       common_pb2.LONG)
                flag1=1

            # if mktposition.occupiedcashshort[instrument.symbol] > 10000:
            #     # utils.new_order(common_pb2.NEW_ORDER, None, common_pb2.BID, instrument.symbol,
            #     #                 mktposition.marketShortPosition[instrument.symbol], None,
            #     #                 True, common_pb2.SHORT)
            #     orders[instrument.symbol].insert_order(common_pb2.BID, instrument.symbol,
            #                                            mktposition.marketShortPosition[instrument.symbol],
            #                                            meanp[instrument.symbol] + shortbias, True,
            #                                            common_pb2.SHORT)
            if mktposition.unrealizedPnlshort[instrument.symbol] < -500 or mktposition.unrealizedPnlshort[
                instrument.symbol] > 1000 or mktposition.occupiedcashshort[instrument.symbol] > 5000 or mktposition.marketShortPosition[instrument.symbol]>120:
                # utils.new_order(common_pb2.NEW_ORDER, None, common_pb2.BID, instrument.symbol,
                #                 mktposition.marketShortPosition[instrument.symbol], None,
                #                 True, common_pb2.SHORT)
                orders[instrument.symbol].insert_order(common_pb2.BID, instrument.symbol,
                                                       mktposition.marketShortPosition[instrument.symbol],
                                                       meanp[instrument.symbol] + shortbias, True,
                                                       common_pb2.SHORT)
                flag2=1

            if flag1==0:
                if tocloseshort >= tolong:
                    orders[instrument.symbol].insert_order(common_pb2.BID, instrument.symbol,
                                                           mktposition.marketShortPosition[instrument.symbol],
                                                           meanp[instrument.symbol] - longbias, False,
                                                           common_pb2.SHORT)
                    tolong = 0
                else:
                    tolong -= tocloseshort
                    orders[instrument.symbol].insert_order(common_pb2.BID, instrument.symbol,
                                                           mktposition.marketShortPosition[instrument.symbol],
                                                           meanp[instrument.symbol] - longbias, False,
                                                           common_pb2.SHORT)
            if flag2==0:
                if tocloselong >= toshort:
                    orders[instrument.symbol].insert_order(common_pb2.ASK, instrument.symbol,
                                                           mktposition.marketShortPosition[instrument.symbol],
                                                           meanp[instrument.symbol] + shortbias, False,
                                                           common_pb2.LONG)
                    tolong = 0
                else:
                    toshort -= tocloselong
                    orders[instrument.symbol].insert_order(common_pb2.ASK, instrument.symbol,
                                                           mktposition.marketShortPosition[instrument.symbol],
                                                           meanp[instrument.symbol] + shortbias, False,
                                                           common_pb2.LONG)

            orders[instrument.symbol].insert_openLongPosition(instrument.symbol, tolong,
                                                              meanp[instrument.symbol] - longbias, False)

            orders[instrument.symbol].insert_openLongPosition(instrument.symbol, 10,
                                                              instrument.last_price - 0.1, False)

            orders[instrument.symbol].insert_openShortPosition(instrument.symbol, toshort,
                                                               meanp[instrument.symbol] + shortbias, False)

            orders[instrument.symbol].insert_openShortPosition(instrument.symbol, 10,
                                                               instrument.last_price + 0.1, False)


if __name__=="__main__":
    defaultlong=100
    defaultshort=100
    sigma=dict()
    window=50
    pastprices=dict()
    mktposition=marketposition2.MarketPosition()
    orders=dict()
    lastp = dict()
    meanp=dict()
    totalvolume=dict()
    for symbol in ALLSYMBOL:
        orders[symbol]=Order.Order()
        sigma[symbol]=0.2
        lastp[symbol]=100
        pastprices[symbol]=deque(maxlen=window)
        meanp[symbol]=100
        totalvolume[symbol]=30
    channel = grpc.insecure_channel(MARKET_CHANNEL)  # 57500
    stub = broker_pb2_grpc.MarketDataStub(channel)
    while 1:
        mktposition.renew_allfast(orders)
        #print(mktposition.marketLongPosition,mktposition.marketShortPosition)
        response = stub.subscribe(common_pb2.Empty())
        for market_data in response:
            instruments = market_data.instruments
            threads=[]
            for instrument in instruments:
                if instrument.symbol in SYMBOLS:
                #todo long short
                    t=threading.Thread(target=run,args=(instrument.symbol,))
                    threads.append(t)
            for t in threads:
                t.start()
            for t in threads:
                t.join()
            for instrument in instruments:
                if instrument.symbol in SYMBOLS:
                    orders[instrument.symbol].execute()
            break
