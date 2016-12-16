from __future__ import print_function

import time

import grpc

from pb import kv_pb2
from pb import search_pb2
from xrpc.resolver import ConsulResolver
from xrpc.client import new_lb_stub
from xrpc.breaker import CircuitBreakerError

def run():
    resolver = ConsulResolver('10.10.28.2')
    addrs = resolver.resolve('py-rpc-test')
    #addrs = resolver.resolve('py_rpc_test')
    print('addrs:', addrs)
    channels = [grpc.insecure_channel('{host}:{port}'.format(host=addr[0], port=addr[1])) for addr in addrs]
    kv_stub = new_lb_stub(kv_pb2.KeyValueStub, channels)
    try:
        response = kv_stub.SetValue(kv_pb2.SetValueRequest(key='foo', value='bar'), 1)
        assert response.result == kv_pb2.SetValueResponse.SUCC
        response = kv_stub.GetValue(kv_pb2.GetValueRequest(key='foo'), 1)
        assert response.value == 'bar'
        print(response)
    except Exception as e:
        print(e)

    search_stub = new_lb_stub(search_pb2.SearchServiceStub, channels)
    while True:
        try:
            response = search_stub.Search(search_pb2.SearchRequest(query='test', page_number=1, result_per_page=10), 1)
            print(response)
        except grpc.RpcError as e:
            print("----- rpc err")
            print(repr(e))
        except CircuitBreakerError as e1:
            print("----- break err")
            print(e1)
        print('')
        time.sleep(3)


if __name__ == '__main__':
    run()
