from db.mysqlhelper import MySqLHelper
db = MySqLHelper()

class Taste(object):
    __tablename__ = 'taste'
    @staticmethod
    def get_all():
        data = db.selectall(sql='select id,name,type from taste')
        return data

class Material(object):
    # 定义表名
    __tablename__ = 'material'
    @staticmethod
    def get_all():
        data = db.selectall(sql='select id,name,type,category,parent,category_name,parent_name,parent_code,category_code from material')
        return data
    
class Technics(object):
    __tablename__ = 'technics'
    @staticmethod
    def get_all():
        data = db.selectall(sql='select id,name,type from technics')
        return data
 
class Foods(object):
    __tablename__ = 'foods'
    @staticmethod
    def get_all():
        data = db.selectall(sql='select id,name,type,category,parent from foods')
        return data

class WordType(object):
    __tablename__ = 'type'
    @staticmethod
    def get_all():
        data = db.selectall(sql='select id,name,status,create_time,update_time from type')
        return data