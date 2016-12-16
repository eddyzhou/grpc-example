from __future__ import print_function

import time

import grpc

from pb import kv_pb2
from pb import search_pb2
from xrpc.resolver import ConsulResolver
from xrpc.client import new_stub
from xrpc.breaker import CircuitBreakerError

def run():
    #channel = grpc.insecure_channel('localhost:33210')
    #channel = grpc.insecure_channel('localhost:50051')
    resolver = ConsulResolver('10.10.28.2')
    addr = resolver.resolve('py_rpc_test')[0]
    print('addr:', addr)
    channel = grpc.insecure_channel('{host}:{port}'.format(host=addr[0], port=addr[1]))
    #channel.subscribe(lambda x: print("cb: ", x), True)
    kv_stub = new_stub(kv_pb2.KeyValueStub, channel)
    response = kv_stub.SetValue(kv_pb2.SetValueRequest(key='foo', value='bar'), 1)
    assert response.result == kv_pb2.SetValueResponse.SUCC
    response = kv_stub.GetValue(kv_pb2.GetValueRequest(key='foo'), 1)
    assert response.value == 'bar'
    print(response)

    search_stub = new_stub(search_pb2.SearchServiceStub, channel)
    while True:
        try:
            response = search_stub.Search(search_pb2.SearchRequest(query='test', page_number=1, result_per_page=10), 1)
            print(response)
        except grpc.RpcError as e:
            print(e)
            print('-----------')
            #previous_connectivity_state = channel._channel.check_connectivity_state(True)
            #print('check_connectivity_state returned with %s.' % previous_connectivity_state)
        except CircuitBreakerError as e1:
            print(e1)
        time.sleep(3)


if __name__ == '__main__':
    run()
