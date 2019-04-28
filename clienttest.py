# -*- coding: utf-8 -*-

from __future__ import print_function
import logging

import grpc

import broker_pb2

import broker_pb2_grpc

import common_pb2

import common_pb2_grpc
# =============================================================================
# 
# def run():
# =============================================================================
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
# =============================================================================
# with grpc.insecure_channel('113.208.112.25:57600') as channel:
#     stub = broker_pb2_grpc.MarketDataStub(channel)
#     response = stub.list_instruments(common_pb2.Empty())
#     print("Instruments received: " )
#     print(response)
#     for data in stub.subscribe(common_pb2.Empty()):
# 
#         print("Subscription received: ")
#         print(data)
# 
# =============================================================================
with grpc.insecure_channel('113.208.112.25:57500') as channel:
    stub = broker_pb2_grpc.BrokerStub(channel)
    response = stub.get_trader(broker_pb2.TraderRequest(trader_id=42,trader_pin='NrojE4oZH',request_type = 'FULL_INFO'))
    print("Instruments received: " )
    print(response)
# =============================================================================
#     for data in stub.subscribe(common_pb2.Empty()):
# # =============================================================================
# #         response=stub.subscribe(common_pb2.Empty())
# # =============================================================================
#         print("Subscription received: ")
#         print(data)
#         
# =============================================================================
       
# =============================================================================
# trader_id=42,trader_pin='NrojE4oZH'
# 
# =============================================================================
# =============================================================================
# if __name__ == '__main__':  
#     logging.basicConfig()
#     run()
# =============================================================================
# =============================================================================
# 
# broker_pb2.list_instruments()
# broker_pb2.subscribe()
# =============================================================================

# =============================================================================
# trader_id=42,trader_pin='NrojE4oZH' )
# =============================================================================
