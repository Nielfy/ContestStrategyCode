from globalparameters import *
from global0 import *
import Data_processing
import utils
import csv
import RBreaker
from collections import deque
from collections import defaultdict
import marketposition2
import numpy as np
from scipy.stats import norm

# factors;
# window,
# the spread  0.05,
# protective order 10
# stop loss 500
# stop occupying 10000
# min tolong
# min sigma
# total volume 100

if __name__ == "__main__":
    defaultlong = 100
    defaultshort = 100
    sigma = dict()
    window = 50
    pastprices = dict()
    mktposition = marketposition2.MarketPosition()
    orders = dict()
    lastp = dict()
    meanp = dict()
    s="A001.PSE"
    totalvolume = dict()
    for symbol in [s]:
        orders[symbol] = Order.Order()
        sigma[symbol] = 0.02
        lastp[symbol] = 100
        pastprices[symbol] = deque(maxlen=window)
        meanp[symbol] = 100
        totalvolume[symbol] = 100
    channel = grpc.insecure_channel(MARKET_CHANNEL)  # 57500
    stub = broker_pb2_grpc.MarketDataStub(channel)
    while 1:
        mktposition.renew_market_positionandorder(s,orders[s])
        print(mktposition.marketLongPosition, mktposition.marketShortPosition)
        response = stub.subscribe(common_pb2.Empty())
        for market_data in response:
            instruments = market_data.instruments
            for instrument in instruments:
                if instrument.symbol==s:
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

                    if (sigma[instrument.symbol] < 0.1):
                        sigma[instrument.symbol] = 0.1
                    thisnorm = norm(meanp[instrument.symbol], sigma[instrument.symbol])
                    # print(thisnorm.cdf(lastp[instrument.symbol]))
                    p = thisnorm.cdf(lastp[instrument.symbol])
                    if p == np.nan:
                        p = 0.5
                    tolong = int(max(20, (1 - p) * totalvolume[instrument.symbol]))
                    toshort = int(max(20, p * totalvolume[instrument.symbol]))
                    longbias = max(min(0.05 * (1 - p), 0.1), 0.01)
                    shortbias = max(min(0.05 * p, 0.1), 0.01)
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
                    if mktposition.occupiedcashlong[instrument.symbol] > 10000:
                        utils.new_order(common_pb2.NEW_ORDER, None, common_pb2.ASK, instrument.symbol,
                                        mktposition.marketLongPosition[instrument.symbol], None,
                                        True, common_pb2.LONG)
                    if mktposition.unrealizedPnllong[instrument.symbol] < -500 or mktposition.unrealizedPnllong[
                        instrument.symbol] > 500:
                        utils.new_order(common_pb2.NEW_ORDER, None, common_pb2.ASK, instrument.symbol,
                                        mktposition.marketLongPosition[instrument.symbol], None,
                                        True, common_pb2.LONG)

                    if mktposition.occupiedcashshort[instrument.symbol] > 10000:
                        utils.new_order(common_pb2.NEW_ORDER, None, common_pb2.BID, instrument.symbol,
                                        mktposition.marketShortPosition[instrument.symbol], None,
                                        True, common_pb2.SHORT)
                    if mktposition.unrealizedPnlshort[instrument.symbol] < -500 or mktposition.unrealizedPnlshort[
                        instrument.symbol] > 500:
                        utils.new_order(common_pb2.NEW_ORDER, None, common_pb2.BID, instrument.symbol,
                                        mktposition.marketShortPosition[instrument.symbol], None,
                                        True, common_pb2.SHORT)

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

                    orders[instrument.symbol].execute()

            break