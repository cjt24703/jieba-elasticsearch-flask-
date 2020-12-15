# encodeing=utf-8
import os,sys
base_dir=os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_dir)
from flask import Flask
from flask import _request_ctx_stack
from flask import request
from flask import make_response
from gevent import monkey
from gevent.pywsgi import WSGIServer
import json
import time
import datetime
from config import config
from exception.base_exception import APIException
from werkzeug.exceptions import HTTPException
from exception.success import Success
from exception.logger import build_logger
from db.mysqlhelper import MySqLHelper
from es.es_helper import EsHelper
import dict_cut
import search as se

app = Flask(__name__)



#载入配置文件
for conf in config:
    app.config.from_object(config[conf])

logger = build_logger(app.config.get('LOG_FILE'))

db = MySqLHelper()

es = EsHelper()

monkey.patch_all(thread=False)

def search_food(name):
    
    search_food = se.SearchFood(es)
    
    data = search_food.analyse_food(name)
    return data

@app.route('/',methods=['GET'])
def hello():
    # data = db.selectone('select * from foods')
    # print(data)

    must_list = [
        {'title':{'query':'香辣糍粑鱼','boost':3}}
    ]
    data = es.page(index='food',musts=must_list)
    print(data)
    success = Success(data=data)
    return success


@app.route('/search',methods=['POST'])
def search():
    res = []
    word = request.form['word']
    if word:
        print('start:' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
        food_list = search_food(word)
        json_str = json.dumps(food_list)
        print('end:' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
    # print('json:%s' % json_str)
    success = Success(data=food_list)
    print(success)
    return success

@app.errorhandler(Exception)
def framework_error(e):
    if app.config.get('DEBUG') == False:  
        if isinstance(e,APIException):
            return e
        try:
            currentTime = datetime.datetime.now()
            logger.info('Timestamp: %s'%(currentTime.strftime("%Y-%m-%d %H:%M:%S")))
            # logger.info("Uncaught exception: ")
            logger.exception(e)
            # for arg in e.args:
            #     logger.info(arg)
            logger.info('\n')
        except:
            pass
        if isinstance(e,HTTPException):
            code = e.code
            msg = e.description
            error_code = 1007
            return APIException(msg=msg,code=code,error_code=error_code)
        else:
            return APIException()
    else:
        
        raise logger.exception(e)



if __name__ == '__main__':
    http_server = WSGIServer(('127.0.0.1',5000),app)
    http_server.serve_forever()