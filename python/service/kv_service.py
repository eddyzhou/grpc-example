from pb import kv_pb2


values = {'hello': 'world'}

class KeyValueService(kv_pb2.KeyValueServicer):

    def SetValue(self, request, context):
        key = request.key
        value = request.value
        values[key] = value
        return kv_pb2.SetValueResponse(result=kv_pb2.SetValueResponse.SUCC)

    def GetValue(self, request, context):
        #raise RuntimeError('test')
        key = request.key
        value = values.get(key)
        if value is None:
            return kv_pb2.GetValueResponse(result=kv_pb2.GetValueResponse.NotFound)

        return kv_pb2.GetValueResponse(value=value)