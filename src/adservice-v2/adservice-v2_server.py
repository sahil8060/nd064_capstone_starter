#!/usr/bin/python

import os
import random
import time
import traceback
from concurrent import futures

import grpc

import demo_pb2
import demo_pb2_grpc

from grpc_health.v1 import health_pb2
from grpc_health.v1 import health_pb2_grpc

from logger import getJSONLogger
logger = getJSONLogger('adservice-v2-server')


class AdServiceV2(demo_pb2_grpc.AdServiceV2Servicer, health_pb2_grpc.HealthServicer):
    # Implemet the Ad service business logic
    
    def AdServiceV2Ads(self, request, context):
        product_channel = grpc.insecure_channel('PRODUCT_CATALOG_SERVICE_ADDR:3550')
        stub = demo_pb2_grpc.ProductCatalogServiceStub(product_channel)

        product_List = stub.ListProducts(request).products

        random_Product = random.choice(product_List).id

        return demo_pb2.AdResponse(random_Product, "AdV2 - Items with 25 discount!")

    # Uncomment to enable the HealthChecks for the Ad service
    # Note: These are needed for the liveness and readiness probes
    def Check(self, request, context):
        return health_pb2.HealthCheckResponse(
            status=health_pb2.HealthCheckResponse.SERVING)

    def Watch(self, request, context):
        return health_pb2.HealthCheckResponse(
            status=health_pb2.HealthCheckResponse.UNIMPLEMENTED)


if __name__ == "__main__":
    logger.info("initializing adservice-v2")

    # create gRPC server, add the Ad-v2 service and start it
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    service = AdServiceV2()
    demo_pb2_grpc.add_AdServiceV2Servicer_to_server(service, server)

    # Uncomment to add the HealthChecks to the gRPC server to the Ad-v2 service
    health_pb2_grpc.add_HealthServicer_to_server(service, server)
    
    print("Server starting on port 9556...")
    server.add_insecure_port("[::]:9556")
    server.start()
    server.wait_for_termination()
