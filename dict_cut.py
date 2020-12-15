import os
import jieba
import jieba.posseg as pseg
import model

class DictCut(object):
    _material_pseg = None
    _technics_pseg = None
    _foods_pseg = None
    _taste_pseg = None

    @property
    def material_pseg(self):
        if self._material_pseg == None:
            self._material_pseg = self.material_dict()
        return self._material_pseg

    @property
    def technics_pseg(self):
        if self._technics_pseg == None:
            self._technics_pseg = self.technics_dict()
        return self._technics_pseg

    @property
    def foods_pseg(self):
        if self._foods_pseg == None:
            self._foods_pseg = self.foods_dict()
        return self._foods_pseg

    @property
    def taste_pseg(self):
        if self._taste_pseg == None:
            self._taste_pseg = self.taste_dict()
        return self._taste_pseg

    def material_dict(self):
        data = model.Material.get_all()
        material_jieba = jieba.Tokenizer()
        for food in data:
            material_jieba.add_word(food['name'],2000,food['parent_code'])
        material_pseg = pseg.POSTokenizer(material_jieba)
        print('material_pseg:success init')
        return material_pseg

    def technics_dict(self):
        data = model.Technics.get_all()
        technics_jieba = jieba.Tokenizer()
        for food in data:
            technics_jieba.del_word(food['name'])
            # technics_jieba.add_word('是',2000,'ttt')
            technics_jieba.add_word(food['name'],2000,food['type'])
        technics_pseg = pseg.POSTokenizer(technics_jieba)
        print('technics_pseg:success init')
        return technics_pseg

    def foods_dict(self):
        data = model.Foods.get_all()
        foods_jieba = jieba.Tokenizer()
        for food in data:
            foods_jieba.add_word(food['name'],2000,food['type'])
        foods_pseg = pseg.POSTokenizer(foods_jieba)
        print('foods_pseg:success init')
        return foods_pseg

    def taste_dict(self):
        data = model.Taste.get_all()
        taste_jieba = jieba.Tokenizer()
        for food in data:
            taste_jieba.add_word(food['name'],2000,food['type'])
        taste_pseg = pseg.POSTokenizer(taste_jieba)
        print('taste_pseg:success init')
        return taste_pseg

dict_cut = DictCut()

foods_pseg = dict_cut.foods_pseg

material_pseg = dict_cut.material_pseg

technics_pseg = dict_cut.technics_pseg

taste_pseg = dict_cut.taste_pseg






