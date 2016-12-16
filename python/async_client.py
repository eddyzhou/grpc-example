from __future__ import print_function

import grpc
from tornado import ioloop
from tornado.gen import coroutine

from pb import kv_pb2
from pb import search_pb2
from tornado_patch import fwrap

@coroutine
def run():
    channel = grpc.insecure_channel('localhost:50052')
    kv_stub = kv_pb2.KeyValueStub(channel)
    response = yield fwrap(kv_stub.SetValue.future(kv_pb2.SetValueRequest(key='foo', value='bar'), timeout=3))
    assert response.result == kv_pb2.SetValueResponse.SUCC
    response = yield fwrap(kv_stub.GetValue.future(kv_pb2.GetValueRequest(key='foo'), timeout=3))
    assert response.value == 'bar'

    search_stub = search_pb2.SearchServiceStub(channel)
    response = yield fwrap(search_stub.Search.future(search_pb2.SearchRequest(query='test', page_number=1, result_per_page=10), timeout=3))
    print(response)

if __name__ == '__main__':
    ioloop.IOLoop.current().run_sync(run)
