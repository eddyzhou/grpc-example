from pb import search_pb2

class SearchService(search_pb2.SearchServiceServicer):
    
    def Search(self, request, context):
        #raise RuntimeError('test')
        #import time
        #time.sleep(5)
        print '------ Search(Python)'
        query = request.query
        page_number = request.page_number
        result_per_page = request.result_per_page

        response = search_pb2.SearchResponse()
        for _ in range(result_per_page):
            result = response.results.add()
            result.url='localhost:50051/search/%d' % page_number 
            result.title=query
            result.snippets.extend(['xxx' for _ in range(3)])

        return response
