from concurrent import futures
import time

import grpc
import raven

from pb import kv_pb2
from pb import search_pb2
from service import kv_service
from service import search_service
from xrpc import monkey, monitor
from xrpc.server import register_signal_hanlder


SENTRY_DSN = 'http://6ac4e8e7a2de45579d5ee1df1899d4ed:92291760a07b46eaaccf24e46ffcfdcf@10.10.28.2:9000/2'
sentry = raven.Client(dsn=SENTRY_DSN)
monkey.patch_server('rpc_test', 50051, sentry)
monitor.start_metrics_server(40051)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=8))
    register_signal_hanlder(server)
    kv_pb2.add_KeyValueServicer_to_server(kv_service.KeyValueService(), server)
    search_pb2.add_SearchServiceServicer_to_server(search_service.SearchService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()

    try:
        while True:
            time.sleep(60 * 60 * 24)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
