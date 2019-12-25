# -*- coding: utf-8 -*-
"摘自https://www.biendata.com/forum/view_post_category/718/"
import pandas as pd
import random
import jieba
import os
from pyltp import Segmentor
from random import shuffle
from xml.dom.minidom import parse
class NearFormReplacer:
#错别字
    def __init__(self, NearForm_file_path):
        self.NearForm = self.load_NearForm(NearForm_file_path)

    def segment(self, sentence):
        """将一句话拆成字符并以list形式返回"""
        list = []
        for x in sentence:
            list.append(x)
        return list

    def load_NearForm(self, file_path):
        """
        加载形近字表
        :param file_path: 形近字表路径
        :return: 形近字表[[xx,xx],[xx,xx]...]
        """
        NearForm = []
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                NearForm.append(line.strip().split(' '))
        return NearForm

    def get_nearform_sents_list(self, input_sentence):
        """
        产生错别字
        :param input_sentence: 需要制造错别字的原始句子
        :return:
        """
        assert len(input_sentence) > 0, "Length of sentence must greater than 0."
        seged_sentence = self.segment(input_sentence)
        
        #随机变化一个错别字
        change = random.randrange(0, len(seged_sentence),1)
        word = seged_sentence[change]
        seged_sentence1 = seged_sentence
        nearform_sent_list = []
        for nf in self.NearForm:  # 遍历形近字表，为其中的一条
            if word in nf:  # 如果句子中的词在形近字表某一条目中，将该条目中它的形近字添加到该词的形近字列表中
                nf.remove(word)
                if(nf):
                    word1 = random.choice(nf)
                    seged_sentence1[change] = word1
                nearform_sent_list.append(''.join(seged_sentence1))
                break    #一个字可能在好几个行，只要进行一次处理即可
        return nearform_sent_list
        
class SynonymsReplacer:
#同义词替换
    def __init__(self, synonyms_file_path, cws_model_path):
        self.synonyms = self.load_synonyms(synonyms_file_path)
        self.segmentor = self.load_segmentor(cws_model_path)

    def __del__(self):
        """对象销毁时要释放pyltp分词模型"""
        self.segmentor.release()

    def load_segmentor(self, cws_model_path):
        """
        加载ltp分词模型
        :param cws_model_path: 分词模型路径
        :return: 分词器对象
        """
        segmentor = Segmentor()
        segmentor.load(cws_model_path)
        return segmentor

    def segment(self, sentence):
        """调用pyltp的分词方法将str类型的句子分词并以list形式返回"""
        return list(self.segmentor.segment(sentence))

    def load_synonyms(self, file_path):
        """
        加载同义词表
        :param file_path: 同义词表路径
        :return: 同义词列表[[xx,xx],[xx,xx]...]
        """
        synonyms = []
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                synonyms.append(line.strip().split(' '))
        return synonyms

    def get_syno_sents_list(self, input_sentence):
        """
        产生同义句，并返回同义句列表，返回的同义句列表没有包含该句本身
        :param input_sentence: 需要制造同义句的原始句子
        :return:
        """
        assert len(input_sentence) > 0, "Length of sentence must greater than 0."
        seged_sentence = self.segment(input_sentence)
        #随机变化一个同义词
        change = random.randrange(0, len(seged_sentence),1)
        word = seged_sentence[change]
        word_synonyms = [word]  # 初始化一个词的同义词列表
        for syn in self.synonyms:  # 遍历同义词表，syn为其中的一条
            if word in syn:  # 如果句子中的词在同义词表某一条目中，将该条目中它的同义词添加到该词的同义词列表中
                syn.remove(word)
                if(syn):
                    word1 = random.choice(syn)
                    seged_sentence[change] = word1
                    break
        return ''.join(seged_sentence)
#数据增强
class NlpEda:
    def __init__(self):
        pass
    def synonyms(self, segment):
        LTP_DATA_DIR = './pyltp-master/ltp_data_v3.4.0/'  # ltp模型目录的路径
        cws_model_path1 = os.path.join(LTP_DATA_DIR, 'cws.model')  # 分词模型路径，模型名称为`cws.model`
        synonyms_file_path1 = os.path.join(LTP_DATA_DIR, 'cilin_ex_nonum') #同义词集路径
        replacer = SynonymsReplacer(synonyms_file_path=synonyms_file_path1, cws_model_path=cws_model_path1)
        test_sentence = segment
        _syn = replacer.get_syno_sents_list(test_sentence)
        return _syn
    def nearform(self, segment):
        LTP_DATA_DIR = './pyltp-master/ltp_data_v3.4.0/'  # ltp模型目录的路径
        NearForm_file_path1 = os.path.join(LTP_DATA_DIR, 'newShape.txt') #形近字集路径
        replacer = NearFormReplacer(NearForm_file_path=NearForm_file_path1)
        test_sentence = segment
        _syn = replacer.get_nearform_sents_list(test_sentence)
        return _syn
    # 数据增强
    def synonyms_eda_list(self, seg_list):
        ret_list = []
        for seg in seg_list:
            new_seg = self.synonyms(seg)
            ret_list.append(new_seg)
        return ret_list
    def nearform_eda_list(self, seg_list):
        ret_list = []
        for seg in seg_list:
            new_seg = self.nearform(seg)
            ret_list.extend(new_seg)
        return ret_list

def generate_train_data_pair(equ_questions,synonyms_equ_questions,nearform_equ_questions, not_equ_questions,synonyms_not_equ_questions,nearform_not_equ_questions):
    #增加A+B'搭配对
    #B'包括替换同义词和形近字的
    a = [x+"\t"+y+"\t"+"0" for x in equ_questions for y in synonyms_not_equ_questions]
    b = [x+"\t"+y+"\t"+"0" for x in equ_questions for y in nearform_not_equ_questions]
    c = [x+"\t"+y+"\t"+"1" for x in equ_questions for y in synonyms_equ_questions]
    d = [x+"\t"+y+"\t"+"1" for x in equ_questions for y in nearform_equ_questions]
    return a+b+c+d
def parse_train_data(xml_data):
    eda = NlpEda()
    pair_list = []
    doc = parse(xml_data)
    collection = doc.documentElement
    flag = 0
    for i in collection.getElementsByTagName("Questions"):
        flag = flag + 1
        print(flag)
        # if i.hasAttribute("number"):
        #     print ("Questions number=", i.getAttribute("number"))
        EquivalenceQuestions = i.getElementsByTagName("EquivalenceQuestions")
        NotEquivalenceQuestions = i.getElementsByTagName("NotEquivalenceQuestions")
        equ_questions = EquivalenceQuestions[0].getElementsByTagName("question")
        not_equ_questions = NotEquivalenceQuestions[0].getElementsByTagName("question")
        equ_questions_list, not_equ_questions_list = [], []
        for q in equ_questions:
            try:
                equ_questions_list.append(q.childNodes[0].data.strip())
            except:
                continue
        for q in not_equ_questions:
            try:
                not_equ_questions_list.append(q.childNodes[0].data.strip())
            except:
                continue
        synonyms_equ_questions_list = eda.synonyms_eda_list(equ_questions_list)
        nearform_equ_questions_list = eda.nearform_eda_list(equ_questions_list)
        synonyms_not_equ_questions_list = eda.synonyms_eda_list(not_equ_questions_list)
        nearform_not_equ_questions_list = eda.nearform_eda_list(not_equ_questions_list)
        pair = generate_train_data_pair(equ_questions_list,synonyms_equ_questions_list,nearform_equ_questions_list, not_equ_questions_list,synonyms_not_equ_questions_list,nearform_not_equ_questions_list)
        pair_list.extend(pair)
    print("All pair count=", len(pair_list))
    return pair_list
def write_train_data(file, pairs):
    with open(file, "w") as f:
        for pair in pairs:                     
            f.write(pair+"\n")
if __name__ == "__main__":
    DATA_DIR1 = "./data_origin/"
    DATA_DIR2 = "./data_gitignore/"
    pair_list = parse_train_data(DATA_DIR1+"train_set.xml")
    question1=[]
    question2=[]
    label=[]
    for pair in pair_list:
        pair=pair.split('\t')
        question1.append(pair[0])
        question2.append(pair[1])
        label.append(pair[2])
    df=pd.DataFrame()
    df['question1']=question1
    df['question2']=question2
    df['label']=label
    df.to_csv(DATA_DIR2+'train_augment.csv',index=False,encoding='utf-8')

