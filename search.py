import jieba
import jieba.posseg as pseg
import pymysql
import json
import math
import dict_cut
import time
import datetime
import es.es_config
import es.es_helper

class SearchFood(object):
    #输出菜品图片数
    _image_food_number = 10
    #输出菜品图片
    _image_food = []
    #数据库实例
    _es = None
    #结巴默认分词类型
    _jieba_type_list = ['n','nr','nz','a','m','c','PER','f','ns','v','ad','q','u','LOC','s','nt','vd','an','r','xc','ORG','t','nw','vn','d','p','w','TIME','per','loc','org']

    def __init__(self,es):
        
        self._es = es
        
        

    def analyse_food(self,name):
        sql_item_list = []
        #菜名分词结果
        food_list = self.__get_food_name(name)
        #风味分词结果
        taste_list = self.__get_taste_name(name)
        #烹饪分词结果
        technics_list = self.__get_technics_name(name)
        #原料分词结果
        material_list = self.__get_material_name(name)
        #默认分词结果
        default_list = self.__get_default_name(name)

        jieba_type_list = self._jieba_type_list
        
        print(food_list)
        print(taste_list)
        print(technics_list)
        print(material_list)
        print(default_list)
        words_list = []
        words_info_list = []
        for food in food_list:
            if food['word'] not in words_list and food['type'] not in jieba_type_list:
                words_list.append(food['word'])
                words_info_list.append({'word':food['word'],'boost':16})
        for taste in taste_list:
            if taste['word'] not in words_list and taste['type'] not in jieba_type_list:
                words_list.append(taste['word'])
                words_info_list.append({'word':taste['word'],'boost':8})
        for technics in technics_list:
            if technics['word'] not in words_list and technics['type'] not in jieba_type_list:
                words_list.append(technics['word'])
                words_info_list.append({'word':technics['word'],'boost':4})
        for material in material_list:
            if material['word'] not in words_list and material['type'] not in jieba_type_list:
                words_list.append(material['word'])
                words_info_list.append({'word':material['word'],'boost':2})
        for default in default_list:
            if default['word'] not in words_list:
                words_list.append(default['word'])
                words_info_list.append({'word':default['word'],'boost':1})
        # print(words_list)
        # print(words_info_list)

        for i in range(len(words_list)+1):
            must_list = []
            should_list = []
            for j,word1 in enumerate(words_info_list):
                # obj = {'term':{'title':word1}}
                if j<i or j == len(words_info_list):
                    must_list.append(word1)
                else:
                    should_list.append(word1)
            sql_item_list.append({'must_list':must_list,'should_list':should_list})
        # print(sql_item_list)
        data = self.__choose_sql(sql_item_list)
        # data = self.__getFoodList({'must_list':[],'should_list':words_info_list})
        # print(words_info_list)
        return data

    
    #二分法选取合适的sql
    def __choose_sql(self,sql_item_list,sql_item=''):
        print(sql_item_list)
        if len(sql_item_list)>2:
            index = math.ceil(len(sql_item_list)/2)-1
            sql_item = sql_item_list[index]
            count = self.__getFoodCount(sql_item)
            print(count)
            if count >= self._image_food_number:
                return self.__choose_sql(sql_item_list[index:],sql_item)
            else:
                return self.__choose_sql(sql_item_list[:index+1],sql_item)
        elif len(sql_item_list) == 2:
            count_one = self.__getFoodCount(sql_item_list[0])
            count_two = self.__getFoodCount(sql_item_list[1])
            
            if count_two >= count_one:
                print('结果：'+str(sql_item_list[1]))
                data_two = self.__getFoodList(sql_item_list[1])
                return data_two
            else:
                print('结果：'+str(sql_item_list[0]))
                data_one = self.__getFoodList(sql_item_list[0])
                return data_one
        else:
            return []
    

    #根据菜单字典获取主体菜品名称
    def __get_food_name(self,name):
        food_list = []
        food_name = dict_cut.foods_pseg.cut(name)
        for w in food_name:
            if w.flag == 'foods':
                # print('%s %s' % (w.word,w.flag))
                food_list.append({'word':w.word,'type':w.flag})
        return food_list

    #根据风味字典获取风味名称
    def __get_taste_name(self,name):
        taste_list = []
        taste_name = dict_cut.taste_pseg.cut(name)
        for w in taste_name:
            if w.flag == 'taste':
                # print('%s %s' % (w.word,w.flag))
                taste_list.append({'word':w.word,'type':w.flag})
        return taste_list

    #根据烹饪字典获取烹饪名称
    def __get_technics_name(self,name):
        technics_list = []
        technics_name = dict_cut.technics_pseg.cut(name)
        for w in technics_name:
            if w.flag == 'technics':
                # print('%s %s' % (w.word,w.flag))
                technics_list.append({'word':w.word,'type':w.flag})
        return technics_list

    #根据原料字典获取原料名称
    def __get_material_name(self,name):
        material_list = []
        material_name = dict_cut.material_pseg.cut(name)
        for w in material_name:
            material_list.append({'word':w.word,'type':w.flag})
        return material_list

    #根据默认字典进行分词
    def __get_default_name(self,name):
        default_list = []
        default_name = pseg.cut(name)
        for w in default_name:
            # print('%s %s' % (w.word,w.flag))
            default_list.append({'word':w.word,'type':w.flag})
        return default_list

    
    # 根据分词查询
    def __getFoodList(self,sql_item):
        
        musts = []
        for food_must in sql_item['must_list']:
            must = {'title':{'query':None,'boost':None}}
            must['title']['query'] = food_must['word']
            must['title']['boost'] = food_must['boost']
            musts.append(must)
        shoulds = []
        for food_should in sql_item['should_list']:
            should = {'title':{'query':None,'boost':None}}
            should['title']['query'] = food_should['word']
            should['title']['boost'] = food_should['boost']
            shoulds.append(should)

        data = self._es.search('food',musts=musts,shoulds=shoulds,size=self._image_food_number,sort=[{'_score':'desc'},{'star_level':'desc'},{'hot_count':'desc'}])

        # print(sql_item)
        # print('查询数量:'+str(len(data)))
        # print(json.dumps(data))
        return data

    def __getFoodCount(self,sql_item):
        musts = []
        for food_must in sql_item['must_list']:
            must = {'title':{'query':None,'boost':None}}
            must['title']['query'] = food_must['word']
            must['title']['boost'] = food_must['boost']
            musts.append(must)
        shoulds = []
        for food_should in sql_item['should_list']:
            should = {'title':{'query':None,'boost':None}}
            should['title']['query'] = food_should['word']
            should['title']['boost'] = food_should['boost']
            shoulds.append(should)
        
        count = self._es.count('food',musts=musts,shoulds=shoulds)

        return count['count']

    

if __name__ == '__main__':
    esObj = es.es_helper.EsHelper()
    search = SearchFood(esObj)
    search.analyse_food('番茄芝士土豆炖牛肉砂锅')
    app.run()
