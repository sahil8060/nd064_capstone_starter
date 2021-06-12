#!/usr/bin/python

import sys
import grpc

import demo_pb2
import demo_pb2_grpc

from logger import getJSONLogger
logger = getJSONLogger('adservice-v2-server')

if __name__ == "__main__":

    # set up server stub
    # ensure the service is listening to port 9556
    adServiceV2_channel = grpc.insecure_channel('localhost:9556')
    stub = demo_pb2_grpc.AdServiceV2Stub(adServiceV2_channel)

    # form a request with the required input
    request = demo_pb2.AdRequest(context_keys=["1"])

    # make a call to server and return a response
    response = stub.GetAds(request)
    
    # Uncomment to log the resoinse from the Server
    logger.info(response)
