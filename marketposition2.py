from globalparameters import *
from global0 import *
import collections
import utils


class MarketPosition:
    def __init__(self):
        self.marketPosition = collections.defaultdict(int)
        self.averageEntryPrice = collections.defaultdict(int)
        self.unrealizedPnl = collections.defaultdict(float)
        self.remaining_orders=[]
        self.orderdict = collections.defaultdict(list)
        self.marketLongPosition=collections.defaultdict(int)
        self.marketShortPosition=collections.defaultdict(int)
        self.occupiedcashlong=collections.defaultdict(float)
        self.occupiedcashshort=collections.defaultdict(float)
        self.unrealizedPnllong=collections.defaultdict(float)
        self.unrealizedPnlshort=collections.defaultdict(float)
        for symbol in SYMBOLS:
            self.marketPosition[symbol] = 0
            self.averageEntryPrice[symbol] = 0
            self.unrealizedPnl[symbol] = 0
            self.orderdict[symbol]=[]
            self.occupiedcashlong[symbol]=0


    def renew_market_position(self,symbol):
        ress=utils.get_trader(common_pb2.FULL_INFO)
        market_position = 0
        avg_entry_price = 0
        unrealized_pnl = 0
        positions=ress.positions
        if hasattr(positions, 'long_positions') and positions.long_positions[symbol] is not None:
            if hasattr(positions.long_positions[symbol], 'volume'):
                if positions.long_positions[symbol].volume > 0:
                    market_position = positions.long_positions[symbol].volume
                    avg_entry_price = positions.long_positions[symbol].avg_price
                    self.unrealizedPnllong[symbol] = positions.long_positions[symbol].unrealized_pnl
                    self.occupiedcashlong[symbol]=positions.long_positions[symbol].occupied_cash
        if hasattr(positions, 'short_positions') and positions.short_positions[symbol] is not None:
            if hasattr(positions.short_positions[symbol], 'volume'):
                if positions.short_positions[symbol].volume > 0:
                    market_position = - positions.short_positions[symbol].volume
                    avg_entry_price = positions.short_positions[symbol].avg_price
                    self.unrealizedPnlshort[symbol] = positions.short_positions[symbol].unrealized_pnl
                    self.occupiedcashshort[symbol]=positions.short_positions[symbol].occupied_cash
        self.marketPosition[symbol] = market_position
        self.averageEntryPrice[symbol] = avg_entry_price
        #self.unrealizedPnl[symbol] = unrealized_pnl
    def renew_all_longshort(self):
        ress = utils.get_trader(common_pb2.FULL_INFO)
        positions = ress.positions
        for symbol in SYMBOLS:
            market_position = 0
            avg_entry_price = 0
            unrealized_pnl = 0

            if hasattr(positions, 'long_positions') and positions.long_positions[symbol] is not None:
                if hasattr(positions.long_positions[symbol], 'volume'):
                    if positions.long_positions[symbol].volume > 0:
                        market_position = positions.long_positions[symbol].volume
                        avg_entry_price = positions.long_positions[symbol].avg_price
                        unrealized_pnl = positions.long_positions[symbol].unrealized_pnl
                        self.marketLongPosition[symbol]=positions.long_positions[symbol].volume
            if hasattr(positions, 'short_positions') and positions.short_positions[symbol] is not None:
                if hasattr(positions.short_positions[symbol], 'volume'):
                    if positions.short_positions[symbol].volume > 0:
                        market_position = - positions.short_positions[symbol].volume
                        avg_entry_price = positions.short_positions[symbol].avg_price
                        unrealized_pnl = positions.short_positions[symbol].unrealized_pnl
                        self.marketShortPosition[symbol]=positions.short_positions[symbol].volume
            self.marketPosition[symbol] = market_position
            self.averageEntryPrice[symbol] = avg_entry_price
            self.unrealizedPnl[symbol] = unrealized_pnl
        for symbol in UNDERLYING:
            market_position = 0
            avg_entry_price = 0
            unrealized_pnl = 0

            if hasattr(positions, 'long_positions') and positions.long_positions[symbol] is not None:
                if hasattr(positions.long_positions[symbol], 'volume'):
                    if positions.long_positions[symbol].volume > 0:
                        market_position = positions.long_positions[symbol].volume
                        avg_entry_price = positions.long_positions[symbol].avg_price
                        unrealized_pnl = positions.long_positions[symbol].unrealized_pnl
                        self.marketLongPosition[symbol] = positions.long_positions[symbol].volume
            if hasattr(positions, 'short_positions') and positions.short_positions[symbol] is not None:
                if hasattr(positions.short_positions[symbol], 'volume'):
                    if positions.short_positions[symbol].volume > 0:
                        market_position = - positions.short_positions[symbol].volume
                        avg_entry_price = positions.short_positions[symbol].avg_price
                        unrealized_pnl = positions.short_positions[symbol].unrealized_pnl
                        self.marketShortPosition[symbol] = positions.short_positions[symbol].volume
            self.marketPosition[symbol] = market_position
            self.averageEntryPrice[symbol] = avg_entry_price
            self.unrealizedPnl[symbol] = unrealized_pnl
        return self.marketPosition
    def renew_all_market_position(self):
        # positions = utils.get_trader(common_pb2.FULL_INFO).positions
        ress = utils.get_trader(common_pb2.FULL_INFO)
        positions=ress.positions
        rorders=[]
        # if hasattr(utils.get_trader(common_pb2.FULL_INFO),"orders"):
        #     orderrr=utils.get_trader(common_pb2.FULL_INFO).orders
        #
        #     rorders=list(orderrr.orders.values())
        if hasattr(ress,"orders"):
            orderrr=ress.orders

            rorders=list(orderrr.orders.values())
            #todo
        self.remaining_orders=rorders
        for symbol in SYMBOLS:
            market_position = 0
            avg_entry_price = 0
            unrealized_pnl = 0

            if hasattr(positions, 'long_positions') and positions.long_positions[symbol] is not None:
                if hasattr(positions.long_positions[symbol], 'volume'):
                    if positions.long_positions[symbol].volume > 0:
                        market_position = positions.long_positions[symbol].volume
                        avg_entry_price = positions.long_positions[symbol].avg_price
                        unrealized_pnl = positions.long_positions[symbol].unrealized_pnl

            if hasattr(positions, 'short_positions') and positions.short_positions[symbol] is not None:
                if hasattr(positions.short_positions[symbol], 'volume'):
                    if positions.short_positions[symbol].volume > 0:
                        market_position = - positions.short_positions[symbol].volume
                        avg_entry_price = positions.short_positions[symbol].avg_price
                        unrealized_pnl = positions.short_positions[symbol].unrealized_pnl

            self.marketPosition[symbol] = market_position
            self.averageEntryPrice[symbol] = avg_entry_price
            self.unrealizedPnl[symbol] = unrealized_pnl
        for symbol in UNDERLYING:
            market_position = 0
            avg_entry_price = 0
            unrealized_pnl = 0

            if hasattr(positions, 'long_positions') and positions.long_positions[symbol] is not None:
                if hasattr(positions.long_positions[symbol], 'volume'):
                    if positions.long_positions[symbol].volume > 0:
                        market_position = positions.long_positions[symbol].volume
                        avg_entry_price = positions.long_positions[symbol].avg_price
                        unrealized_pnl = positions.long_positions[symbol].unrealized_pnl

            if hasattr(positions, 'short_positions') and positions.short_positions[symbol] is not None:
                if hasattr(positions.short_positions[symbol], 'volume'):
                    if positions.short_positions[symbol].volume > 0:
                        market_position = - positions.short_positions[symbol].volume
                        avg_entry_price = positions.short_positions[symbol].avg_price
                        unrealized_pnl = positions.short_positions[symbol].unrealized_pnl

            self.marketPosition[symbol] = market_position
            self.averageEntryPrice[symbol] = avg_entry_price
            self.unrealizedPnl[symbol] = unrealized_pnl
        return self.marketPosition

    def renew_all(self,orders):
        for symbol in ALLSYMBOL:
            self.renew_market_positionandorder(symbol,orders[symbol])

    def renew_allfast(self,orders):
        ress = utils.get_trader(common_pb2.FULL_INFO)

        # print(ress.positions)
        # 正式比赛时考虑注释这一行
        # print(ress.market_records[2])
        # print(ress.pnl)
        # print(ress.market_records)
        rorders = []
        for symbol in SYMBOLS:
            if hasattr(ress, "orders"):
                orderrr = ress.orders.orders
                for id in orders[symbol].outgoingorder:
                    if not id is None:
                        if not orderrr[id].symbol == '':
                            rorders.append(orderrr[id])
            self.orderdict[symbol] = rorders
            market_position = 0
            avg_entry_price = 0
            unrealized_pnl = 0
            positions = ress.positions
            if hasattr(positions, 'long_positions') and positions.long_positions[symbol] is not None:
                if hasattr(positions.long_positions[symbol], 'volume'):
                    if positions.long_positions[symbol].volume > 0:
                        self.marketLongPosition[symbol] = positions.long_positions[symbol].volume
                        market_position = positions.long_positions[symbol].volume
                        avg_entry_price = positions.long_positions[symbol].avg_price
                        # unrealized_pnl = positions.long_positions[symbol].unrealized_pnl
                        self.unrealizedPnllong[symbol] = positions.long_positions[symbol].unrealized_pnl
                        self.occupiedcashlong[symbol] = positions.long_positions[symbol].occupied_cash
            if hasattr(positions, 'short_positions') and positions.short_positions[symbol] is not None:
                if hasattr(positions.short_positions[symbol], 'volume'):
                    if positions.short_positions[symbol].volume > 0:
                        self.marketShortPosition[symbol] = positions.short_positions[symbol].volume
                        market_position = - positions.short_positions[symbol].volume
                        avg_entry_price = positions.short_positions[symbol].avg_price
                        # unrealized_pnl = positions.short_positions[symbol].unrealized_pnl
                        self.unrealizedPnlshort[symbol] = positions.short_positions[symbol].unrealized_pnl
                        self.occupiedcashshort[symbol] = positions.short_positions[symbol].occupied_cash
            self.marketPosition[symbol] = market_position
            self.averageEntryPrice[symbol] = avg_entry_price
            # self.unrealizedPnl[symbol] = unrealized_pnl
    #todo renewall marketposition Longshort
    def renew_market_positionandorder(self,symbol,thisorder):
        ress=utils.get_trader(common_pb2.FULL_INFO)

        # print(ress.positions)
        # 正式比赛时考虑注释这一行
        #print(ress.market_records[1])
        print(ress.pnl)
        # print(ress.market_records)
        rorders = []
        if hasattr(ress, "orders"):
            orderrr = ress.orders.orders
            for id in thisorder.outgoingorder:
                if not id is None:
                    if not orderrr[id].symbol=='':
                        rorders.append(orderrr[id])
        self.orderdict[symbol] = rorders
        market_position = 0
        avg_entry_price = 0
        unrealized_pnl = 0
        positions=ress.positions
        if hasattr(positions, 'long_positions') and positions.long_positions[symbol] is not None:
            if hasattr(positions.long_positions[symbol], 'volume'):
                if positions.long_positions[symbol].volume > 0:
                    self.marketLongPosition[symbol]=positions.long_positions[symbol].volume
                    market_position = positions.long_positions[symbol].volume
                    avg_entry_price = positions.long_positions[symbol].avg_price
                    #unrealized_pnl = positions.long_positions[symbol].unrealized_pnl
                    self.unrealizedPnllong[symbol] = positions.long_positions[symbol].unrealized_pnl
                    self.occupiedcashlong[symbol] = positions.long_positions[symbol].occupied_cash
        if hasattr(positions, 'short_positions') and positions.short_positions[symbol] is not None:
            if hasattr(positions.short_positions[symbol], 'volume'):
                if positions.short_positions[symbol].volume > 0:
                    self.marketShortPosition[symbol]=positions.short_positions[symbol].volume
                    market_position = - positions.short_positions[symbol].volume
                    avg_entry_price = positions.short_positions[symbol].avg_price
                    #unrealized_pnl = positions.short_positions[symbol].unrealized_pnl
                    self.unrealizedPnlshort[symbol] = positions.short_positions[symbol].unrealized_pnl
                    self.occupiedcashshort[symbol] = positions.short_positions[symbol].occupied_cash
        self.marketPosition[symbol] = market_position
        self.averageEntryPrice[symbol] = avg_entry_price
        #self.unrealizedPnl[symbol] = unrealized_pnl
