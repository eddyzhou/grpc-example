from tornado.ioloop import IOLoop
from tornado.gen import Future

def _fwrap(f, gf):
    try:
        f.set_result(gf.result())
    except Exception as e:
        f.set_exception(e)

def fwrap(gf, ioloop=None):
    '''
        Wraps a GRPC result in a future that can be yielded by tornado

        Usage::

            @coroutine
            def my_fn(param):
                result = yield fwrap(stub.function_name.future(param, timeout))

    '''
    f = Future()

    if ioloop is None:
        ioloop = IOLoop.current()

    gf.add_done_callback(lambda _: ioloop.add_callback(_fwrap, f, gf))
    return f
