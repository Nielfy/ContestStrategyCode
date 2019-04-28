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
    # strategies = {}
    # strategy1s = {}
    # strategy2s = {}
    # strategy3s = {}
    # pre_orders = {}
    # modes = {}
    last_price = {}
    center_price={}
    # for symbol in SYMBOLS:
    #     strategies[symbol] = Data_processing.Strategies()
    #     strategy1s[symbol] = Data_processing.DualThrust()
        #strategy1s[symbol] = R_Breaker.R_Breaker(symbol=symbol,Run_freq=20,data_freq=60)
        #strategy2s[symbol] = Data_processing.GFTD(symbol=symbol,Run_freq=20,data_freq=15)
        #strategy3s[symbol] = Data_processing.DualThrust()
    # strategy2s[symbol] = Data_processing.GFTD(symbol=symbol,Run_freq=20,data_freq=15)
    # strategy2s[SYMBOLS[0]] = Data_processing.GFTD(Run_freq=30, data_freq=30,n1=2,n2=3,n3=5)
    # strategy2s[SYMBOLS[1]] = Data_processing.GFTD(Run_freq=30, data_freq=30,n1=2,n2=5,n3=2)
    # strategy2s[SYMBOLS[2]] = Data_processing.GFTD(Run_freq=30, data_freq=30,n1=2,n2=6,n3=4)
    # strategy2s[SYMBOLS[3]] = Data_processing.GFTD(Run_freq=30, data_freq=30, n1=4, n2=4, n3=4)
    # # strategy2s[SYMBOLS[4]] = Data_processing.GFTD(Run_freq=30, data_freq=30, n1=3, n2=2, n3=4)
    # # strategy2s[SYMBOLS[5]] = Data_processing.GFTD(Run_freq=30, data_freq=30, n1=3, n2=4, n3=4)
    # modes[SYMBOLS[0]] = Data_processing.mode(rmean=0.0203994492797)
    # modes[SYMBOLS[1]] = Data_processing.mode(rmean=0.164587904643)
    # modes[SYMBOLS[2]] = Data_processing.mode(rmean=0.118585113226)
    # modes[SYMBOLS[3]] = Data_processing.mode(rmean=0.0203994492797)
    # modes[SYMBOLS[4]] = Data_processing.mode(rmean=0.164587904643)
    # modes[SYMBOLS[5]] = Data_processing.mode(rmean=0.118585113226)



    counter = 0
    lastp=dict()
    while 1:
        channel = grpc.insecure_channel(MARKET_CHANNEL)  # 57500
        stub = broker_pb2_grpc.MarketDataStub(channel)
        response = stub.subscribe(common_pb2.Empty())

        for market_data in response:
            #print(market_data)
            instruments = market_data.instruments
            for instrument in instruments:
                order.insert_closePosition(instrument.symbol)

            #order.execute()
                for orde in marketPosition.remaining_orders:

                    if orde.symbol==instrument.symbol and abs(orde.init_price - lastp[orde.symbol]) > 0.5:
                        order.insert_cancel_orders(orde.order_id)

            order.execute_with_multithread()
            for instrument in instruments:
                if counter==0:
                    pass
                else:
                    if(abs(instrument.last_price-lastp[instrument.symbol])>0.5):
                        Sli[instrument.symbol]=0.02
                    else:
                        Sli[instrument.symbol]=0.01
                if instrument.symbol in SYMBOLS:
                    center_price[instrument.symbol] = instrument.last_price

                    for i in range(len(posbias)):
                        # utils.new_order(common_pb2.NEW_ORDER, None, common_pb2.BID, instrument.symbol, posbias[i][1], instrument.last_price-SLIPPER*posbias[i][0], False, common_pb2.LONG)
                        order.insert_openLongPosition(symbol=instrument.symbol, volume=posbias[i][1],
                                                      price=center_price[instrument.symbol] - Sli[instrument.symbol]*posbias[i][0], is_market=False)
                    for j in range(len(negbias)):
                        # utils.new_order(common_pb2.NEW_ORDER, None, common_pb2.ASK, instrument.symbol, negbias[i][1],
                        #                 instrument.last_price - SLIPPER * negbias[i][0], False, common_pb2.SHORT)
                        order.insert_openShortPosition(symbol=instrument.symbol, volume=negbias[i][1],
                                                      price=center_price[instrument.symbol] - Sli[instrument.symbol] * negbias[i][0],
                                                      is_market=False)
                    lastp[instrument.symbol]=center_price[instrument.symbol]
                    continue
                if instrument.symbol in UNDERLYING:
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
            order.execute_with_multithread()
            # order.execute()
            print(marketPosition.renew_all_market_position())
            counter+=1
        break
            # print(counter)
                     #
                        # utils.new_order(common_pb2.NEW_ORDER, None, common_pb2.ASK, instrument.symbol, protectionbias[i][1],
                        #                 instrument.last_price - SLIPPER * negprotectbias[i][0], False, common_pb2.SHORT)



                    #print(instrument.symbol)
                    #last_price[instrument.symbol] = instrument.last_price

                    ## 调用策略对象
                    #print(instrument.last_price)
                    #print(strategies[instrument.symbol])
                    # FacName = instrument.symbol
                    # with open("C:\quant\Quantitative-Contest-master\Quantitative-Contest-master\data\\"+FacName+".csv",'a+') as fp:
                    #     a = csv.writer(fp);
                    #     price = [instrument.last_price]
                    #     a.writerow(price)

                    # strategies[instrument.symbol].add_Market_data(instrument.last_price)
                    # strategy1s[instrument.symbol].add_Market_data(instrument.last_price)
                    # strategy2s[instrument.symbol].add_Market_data(instrument.last_price)
                    # #strategy3s[instrument.symbol].add_Market_data(instrument.last_price)
                    # modes[instrument.symbol].add_Market_data(instrument.last_price)
                    # modes[instrument.symbol].judge()
                    # print('modes: %s'%(modes[instrument.symbol].flag))
                    # pre_orders[instrument.symbol] = strategies[instrument.symbol].run_timely(Marketjudge=modes[instrument.symbol].flag,strategy1=strategy1s[instrument.symbol],strategy2=strategy2s[instrument.symbol])
                    # #pre_orders[instrument.symbol] = strategies[instrument.symbol].run_timely(False,strategy1=strategy1s[instrument.symbol],strategy2=strategy2s[instrument.symbol])


                # trade_shares = int(TOTAL_TRADE_SHARES/len(SYMBOLS))
                # #print(pre_orders)


                # for symbol in pre_orders.keys():
                #     if pre_orders[symbol] == 1:
                #         if marketPosition.marketPosition[symbol] == 0:
                #             order.insert_openLongPosition(symbol=symbol, volume=trade_shares, price=None, is_market= True)
                #         if marketPosition.marketPosition[symbol] <= -1:
                #             order.insert_closePosition(symbol=symbol)
                #             order.insert_openLongPosition(symbol=symbol, volume=trade_shares, price=None, is_market=True)
                #     if pre_orders[symbol] == -1:
                #         if marketPosition.marketPosition[symbol] == 0:
                #             order.insert_openShortPosition(symbol=symbol, volume=trade_shares, price=None, is_market=True)
                #         if  marketPosition.marketPosition[symbol] >= 1:
                #             order.insert_closePosition(symbol=symbol)
                #             order.insert_openShortPosition(symbol=symbol, volume=trade_shares, price=None, is_market=True)
                #     if pre_orders[symbol] == 2: #平仓
                #         order.insert_closePosition(symbol)

                #----------------------------------------------

                # ----------------------------------------------


                # if counter >= 10:
                #     counter = 0
                    # 全局止盈止损
                    # for symbol in SYMBOLS:
                    #     isNeedClose = False
                    #     if marketPosition.marketPosition[symbol] > 0:
                    #         if last_price[symbol] - marketPosition.averageEntryPrice[symbol] > last_price[symbol] * STOP_PROFIT_PERCENT:
                    #             isNeedClose = True
                    #         if marketPosition.averageEntryPrice[symbol] - last_price[symbol] > last_price[symbol] * STOP_LOSS_PERCENT:
                    #             isNeedClose = True
                    #     if marketPosition.marketPosition[symbol] < 0:
                    #         if last_price[symbol] - marketPosition.averageEntryPrice[symbol] > last_price[symbol] * STOP_LOSS_PERCENT:
                    #             isNeedClose = True
                    #         if marketPosition.averageEntryPrice[symbol] - last_price[symbol] > last_price[symbol] * STOP_PROFIT_PERCENT:
                    #             isNeedClose = True
                    #     if isNeedClose:
                    #         order.insert_closePosition(symbol)
                    ## 更新仓位
                    # print("cur ",marketPosition.renew_all_market_position())






                ## 测试订单系统
                # """
                # OrderBuf.insert_openLongPosition(SYMBOLS[0], 2 ,None, True)
                # OrderBuf.insert_openShortPosition(SYMBOLS[1],2,None,True)
                # OrderBuf.execute()
                # print('insert')
                # print(marketPosition.renew_all_market_position())
                #
                # for symbol in SYMBOLS:
                #     OrderBuf.insert_closePosition(symbol)
                # OrderBuf.execute()
                # print('delete')
                # print(marketPosition.renew_all_market_position())
                # """

