import es.es_config as config
from elasticsearch import Elasticsearch

class EsHelper(object):
    
    # 分页最大条数
    _max_search_number = 500

    def __init__(self):
        self.es = Elasticsearch([{'host':config.ES_TEST_HOST,'port':config.ES_TEST_PORT}])

    @property
    def start(self):
        return (self.current_page - 1) * self.limit

    @property
    def end(self):
        return self.current_page * self.limit

    def page(self,index=None,musts=[],shoulds=[],size=10,current_page=1,sort=[]):
        current_page = int(current_page)
        start = self._max_search_number if (current_page - 1) * size > self._max_search_number else (current_page - 1) * size
        result = {}
        must_list = []
        for must in musts:
            must_item = {}
            must_item['match'] = must
            must_list.append(must_item)

        should_list = []
        for should in shoulds:
            should_item = {}
            should_item['match'] = should
            should_list.append(should_item)

        dsl = {
            'query':{
                'bool':{
                    'must':must_list,
                    'should':should_list
                }
            },
            'size':size,
            'from':start,
            'sort':sort,
            "highlight": {
    	        "fields": {
    		        "title": {}
    	        }
	        }
        }
        try:
            result = self.es.search(index=index,body=dsl,filter_path=['hits.hits.*'])
        except Exception as e:
            print("error_msg:",e.args)
        if not bool(result):
            result = []
        else:
            result = result['hits']['hits']
        return result



    
    def search(self,index=None,musts=[],shoulds=[],size=10,sort=[]):
        result = {}
        must_list = []
        for must in musts:
            must_item = {}
            must_item['match'] = must
            must_list.append(must_item)

        should_list = []
        for should in shoulds:
            should_item = {}
            should_item['match'] = should
            should_list.append(should_item)

        dsl = {
            'query':{
                'bool':{
                    'must':must_list,
                    'should':should_list
                }
            },
            'size':size,
            'sort':sort,
            "highlight": {
    	        "fields": {
    		        "title": {}
    	        }
	        }
        }
        # print(dsl)
        try:
            result = self.es.search(index=index,body=dsl,filter_path=['hits.hits.*'])
        except Exception as e:
            print("error_msg:",e.args)
        if not bool(result):
            result = []
        else:
            result = result['hits']['hits']
        return result

    
    def count(self,index=None,musts=[],shoulds=[]):
        result = 0
        must_list = []
        for must in musts:
            must_item = {}
            must_item['match'] = must
            must_list.append(must_item)

        should_list = []
        for should in shoulds:
            should_item = {}
            should_item['match'] = should
            should_list.append(should_item)

        dsl = {
            'query':{
                'bool':{
                    'must':must_list,
                    'should':should_list
                }
            }
        }
        
        try:
            result = self.es.count(index=index,body=dsl)
        except Exception as e:
            print("error_msg:",e.args)
        return result

    def insert(self,index,data):
        result = es.index(index=index,body=data)


    def delete(self,index,id):
        result = es.delete(index=index,id=id)

    def update(self,index,data):
        result = es.update(index=index,body=data)

    def result_transform(self,data):
        return




# musts = []
# foods = ['土豆炖牛肉','番茄','芝士','砂锅']
# for food in foods:
#     must = {}
#     must['title'] = food
#     musts.append(must)

# print( app.count(index='food1',musts=[],shoulds=musts) )

        