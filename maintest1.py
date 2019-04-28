from globalparameters import *
from global0 import *
import Data_processing
import utils
import csv
import RBreaker
# import Status
import time
import Levels

un_PNL = None

# print(new_order(common_pb2.NEW_ORDER,2,common_pb2.BID,"A001.PSE",1,0,True,common_pb2.LONG))
# print(new_order(common_pb2.NEW_ORDER,2,common_pb2.ASK,"A001.PSE",1,123,False,common_pb2.LONG))


if __name__ == '__main__':
    channel = grpc.insecure_channel(MARKET_CHANNEL)  # 57500

    # symbol="A001.PSE"
    # cur=Status.status(symbol)
    last_price = {}
    center_price = {}
    symbol = "A001.PSE"
    counter = 0
    A1Level = Levels.Levels()

    lastp = dict()
    while 1:
        stub = broker_pb2_grpc.MarketDataStub(channel)
        response = stub.subscribe(common_pb2.Empty())
        for market_data in response:
            # print(market_data)
            for i in market_data.instruments:
                if i.symbol == symbol:
                    instrument = i
            print(instrument.last_price)
            bidlevels=list(instrument.bid_levels) # price;volume;order_count
            for i in range(1,len(bidlevels)):
                if instrument.last_price-0.1<bidlevels[i].price<instrument.last_price and bidlevels[i].volume>=50:
                    # todo if position then dump position here
                    #todo else order 30 here

                #todo order remaining 50 at -0.1
            for i in range(1,len(asklevels)):
                if instrument.last_price+0.1>asklevels[i].price>instrument.last_price and asklevels[i].volume>=50:
                    #todo if position then dump position here
                    #todo else order 30 here

                #todo order remaining 50 at +0.1
            
            #
            asklevels=list(instrument.ask_levels) #sorted by price ask:low--high bid high--low


            marketPosition1.renew_market_positionandorder(instrument.symbol, order1)
            # print(marketPosition1.marketPosition)
            print(marketPosition1.marketShortPosition, marketPosition1.marketLongPosition)
            # print(marketPosition1.remaining_orders)
            A1Level = Levels.Levels()

            # if counter == 0:
            #     pass
            # else:
            #     if (abs(instrument.last_price - lastp[instrument.symbol]) > 0.5):
            #         Sli[instrument.symbol] = 0.02
            #     else:
            #         Sli[instrument.symbol] = 0.01
            center_price[instrument.symbol] = instrument.last_price
            # order.close_allpositions()
            # todo consider current positions
            # #order.execute()
            for orde in marketPosition1.remaining_orders:
                # todo consider remaining positions
                if orde.symbol == instrument.symbol:
                    order.insert_cancel_orders(orde.order_id)
                # elif orde.symbol==instrument.symbol and orde.init_price-lastp[orde.symbol]>0:
                #     A1Level.Level1[1]=max(A1Level.Level1[1]-orde.volume,0)
                #
                # elif orde.symbol==instrument.symbol and orde.init_price-lastp[orde.symbol]<0:
                #     A1Level.Level1[1] = max(A1Level.Level_1[1] - orde.volume, 0)

            if marketPosition1.marketLongPosition.get(instrument.symbol, 0) > 0:
                temp1 = A1Level.Level_1[1]
                A1Level.Level_1[1] = max(A1Level.Level_1[1] - marketPosition1.marketLongPosition[instrument.symbol], 0)
                if A1Level.Level_1[1] == 0:
                    temp2 = A1Level.Level_1[1]
                    A1Level.Level_2[1] = max(
                        A1Level.Level_2[1] - (marketPosition1.marketLongPosition[instrument.symbol] - temp1), 0)
                if A1Level.Level_2[1] == 0:
                    # temp2 = A1Level.Level1[1]
                    A1Level.Level_3[1] = max(
                        A1Level.Level_3[1] - (marketPosition1.marketLongPosition[instrument.symbol] - temp2 - temp1), 0)

                # order1.insert_order(common_pb2.ASK,instrument.symbol,marketPosition1.marketLongPosition[instrument.symbol],center_price[instrument.symbol]+A1Level.Level1[0]//4*Sli[instrument.symbol],False,common_pb2.LONG)
                order1.insert_order(common_pb2.ASK, instrument.symbol,
                                    marketPosition1.marketLongPosition[instrument.symbol],
                                    center_price[instrument.symbol] + A1Level.Level1[0] // 4 * Sli[instrument.symbol],
                                    True, common_pb2.LONG)
            if marketPosition1.marketShortPosition.get(instrument.symbol, 0) > 0:
                temp1 = A1Level.Level1[1]
                A1Level.Level1[1] = max(A1Level.Level1[1] - marketPosition1.marketShortPosition[instrument.symbol], 0)
                if A1Level.Level1[1] == 0:
                    temp2 = A1Level.Level1[1]
                    A1Level.Level2[1] = max(
                        A1Level.Level2[1] - (marketPosition1.marketShortPosition[instrument.symbol] - temp1), 0)
                if A1Level.Level2[1] == 0:
                    # temp2 = A1Level.Level1[1]
                    A1Level.Level3[1] = max(
                        A1Level.Level3[1] - (marketPosition1.marketShortPosition[instrument.symbol] - temp2 - temp1), 0)
                # order1.insert_order(common_pb2.BID, instrument.symbol,
                #                    marketPosition1.marketShortPosition[instrument.symbol],
                #                    center_price[instrument.symbol] + A1Level.Level_1[0]//4 * Sli[instrument.symbol], False,
                #                    common_pb2.SHORT)
                order1.insert_order(common_pb2.BID, instrument.symbol,
                                    marketPosition1.marketShortPosition[instrument.symbol],
                                    center_price[instrument.symbol] + A1Level.Level_1[0] // 4 * Sli[instrument.symbol],
                                    True,
                                    common_pb2.SHORT)
            # todo consider hedging
            # for instrument in instruments:
            # if instrument.symbol==symbol:1
            if A1Level.Level1[1] > 0:
                order1.insert_openLongPosition(symbol=instrument.symbol, volume=A1Level.Level1[1],
                                               price=center_price[instrument.symbol] - Sli[instrument.symbol] *
                                                     A1Level.Level1[0],
                                               is_market=False)
            if A1Level.Level2[1] > 0:
                order1.insert_openLongPosition(symbol=instrument.symbol, volume=A1Level.Level2[1],
                                               price=center_price[instrument.symbol] - Sli[instrument.symbol] *
                                                     A1Level.Level2[0],
                                               is_market=False)

            if A1Level.Level3[1] > 0:
                order1.insert_openLongPosition(symbol=instrument.symbol, volume=A1Level.Level3[1],
                                               price=center_price[instrument.symbol] - Sli[instrument.symbol] *
                                                     A1Level.Level3[0],
                                               is_market=False)
            if A1Level.Level_1[1] > 0:
                order1.insert_openShortPosition(symbol=instrument.symbol, volume=A1Level.Level_1[1],
                                                price=center_price[instrument.symbol] - Sli[instrument.symbol] *
                                                      A1Level.Level_1[0],
                                                is_market=False)

            if A1Level.Level_2[1] > 0:
                order1.insert_openShortPosition(symbol=instrument.symbol, volume=A1Level.Level_2[1],
                                                price=center_price[instrument.symbol] - Sli[instrument.symbol] *
                                                      A1Level.Level_2[0],
                                                is_market=False)

            if A1Level.Level_3[1] > 0:
                order1.insert_openShortPosition(symbol=instrument.symbol, volume=A1Level.Level_3[1],
                                                price=center_price[instrument.symbol] - Sli[instrument.symbol] *
                                                      A1Level.Level_3[0],
                                                is_market=False)
            # for i in range(len(posbias)):
            #     # utils.new_order(common_pb2.NEW_ORDER, None, common_pb2.BID, instrument.symbol, posbias[i][1], instrument.last_price-SLIPPER*posbias[i][0], False, common_pb2.LONG)
            #     order1.insert_openLongPosition(symbol=instrument.symbol, volume=posbias[i][1],
            #                                   price=center_price[instrument.symbol] - Sli[instrument.symbol]*posbias[i][0], is_market=False)
            # for j in range(len(negbias)):
            #     # utils.new_order(common_pb2.NEW_ORDER, None, common_pb2.ASK, instrument.symbol, negbias[i][1],
            #     #                 instrument.last_price - SLIPPER * negbias[i][0], False, common_pb2.SHORT)
            #     order1.insert_openShortPosition(symbol=instrument.symbol, volume=negbias[i][1],
            #                                   price=center_price[instrument.symbol] - Sli[instrument.symbol] * negbias[i][0],
            #                                   is_market=False)
            lastp[instrument.symbol] = instrument.last_price
            # order1.execute_with_multithread()
            order1.execute()
            # print(instrument.timestamp)
            counter = 1
            break

            # if instrument.symbol ==symbol:
            #     center_price[instrument.symbol] = instrument.last_price
            #     for i in range(len(protectionbias)):
            #         order.insert_openLongPosition(symbol=instrument.symbol, volume=protectionbias[i][1],
            #                                       price=instrument.last_price - SLIPPER * protectionbias[i][0],
            #                                       is_market=False)
            #     for j in range(len(negprotectbias)):
            #         order.insert_openShortPosition(symbol=instrument.symbol, volume=protectionbias[i][1],
            #                                        price=instrument.last_price - SLIPPER * negprotectbias[i][0],
            #                                        is_market=False)
            #     lastp[instrument.symbol] = center_price[instrument.symbol]
            #
            #
            #
            #         # utils.new_order(common_pb2.NEW_ORDER, None, common_pb2.BID, instrument.symbol, protectionbias[i][1],
            #         #                 instrument.last_price - SLIPPER * protectionbias[i][0], False, common_pb2.LONG)
            #
        #
        # order.execute()
        # marketPosition.renew_all_market_position()
        # counter+=1
        # print(counter)