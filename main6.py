from globalparameters import *
from global0 import *
import Data_processing
import utils
import csv
import RBreaker

un_PNL = None

#print(new_order(common_pb2.NEW_ORDER,2,common_pb2.BID,"A001.PSE",1,0,True,common_pb2.LONG))
#print(new_order(common_pb2.NEW_ORDER,2,common_pb2.ASK,"A001.PSE",1,123,False,common_pb2.LONG))


if __name__ == '__main__':
    channel = grpc.insecure_channel(MARKET_CHANNEL)  # 57500
    stub = broker_pb2_grpc.MarketDataStub(channel)
    response = stub.subscribe(common_pb2.Empty())
    symbol="B000.PSE"
    last_price = {}
    center_price={}

    counter = 0
    lastp=dict()

    for market_data in response:
        #print(market_data)
        instruments = market_data.instruments
        order.close_allpositions()
        #order.execute()
        for orde in marketPosition.remaining_orders:

            if orde.symbol==symbol and abs(orde.init_price - lastp[orde.symbol]) > 0.05:
                order.insert_cancel_orders(orde.order_id)

        for instrument in instruments:



            # if instrument.symbol==symbol:
            #     if counter == 0:
            #         pass
            #     else:
            #         if (abs(instrument.last_price - lastp[instrument.symbol]) > 0.5):
            #             Sli[instrument.symbol] = 0.02
            #         else:
            #             Sli[instrument.symbol] = 0.01
            #     center_price[instrument.symbol] = instrument.last_price

                # for i in range(len(posbias)):
                #     # utils.new_order(common_pb2.NEW_ORDER, None, common_pb2.BID, instrument.symbol, posbias[i][1], instrument.last_price-SLIPPER*posbias[i][0], False, common_pb2.LONG)
                #     order.insert_openLongPosition(symbol=instrument.symbol, volume=posbias[i][1],
                #                                   price=center_price[instrument.symbol] - Sli[instrument.symbol]*posbias[i][0], is_market=False)
                # for j in range(len(negbias)):
                #     # utils.new_order(common_pb2.NEW_ORDER, None, common_pb2.ASK, instrument.symbol, negbias[i][1],
                #     #                 instrument.last_price - SLIPPER * negbias[i][0], False, common_pb2.SHORT)
                #     order.insert_openShortPosition(symbol=instrument.symbol, volume=negbias[i][1],
                #                                   price=center_price[instrument.symbol] - Sli[instrument.symbol] * negbias[i][0],
                #                                   is_market=False)
                # lastp[instrument.symbol]=center_price[instrument.symbol]
                # continue
            if instrument.symbol ==symbol:
                if counter == 0:
                    pass
                else:
                    if (abs(instrument.last_price - lastp[instrument.symbol]) > 0.5):
                        Sli[instrument.symbol] = 0.02
                    else:
                        Sli[instrument.symbol] = 0.01
                center_price[instrument.symbol] = instrument.last_price

                center_price[instrument.symbol] = instrument.last_price
                for i in range(len(protectionbias)):
                    order.insert_openLongPosition(symbol=instrument.symbol, volume=protectionbias[i][1],
                                                  price=instrument.last_price - SLIPPER * protectionbias[i][0],
                                                  is_market=False)
                for j in range(len(negprotectbias)):
                    order.insert_openShortPosition(symbol=instrument.symbol, volume=protectionbias[i][1],
                                                   price=instrument.last_price - SLIPPER * negprotectbias[i][0],
                                                   is_market=False)
                lastp[instrument.symbol] = center_price[instrument.symbol]
            #
            #
            #
            #         # utils.new_order(common_pb2.NEW_ORDER, None, common_pb2.BID, instrument.symbol, protectionbias[i][1],
            #         #                 instrument.last_price - SLIPPER * protectionbias[i][0], False, common_pb2.LONG)
            #

        order.execute()
        marketPosition.renew_all_market_position()
        counter+=1
        print(counter)