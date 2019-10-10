# import numpy as np
# import string
# import re
# import xml.etree.cElementTree as ET
#
# str_xml = open('sample.xml', 'r').read()
# root = ET.XML(str_xml)
# # 关于root的遍历方法
# for child in root:
#     for i in child:
#         print(i.text)
#
# for node in root.iter('DOCNO'):
#     print(node.text)
#
# for node in root.findall('DOC'):
#     rank = int(node.find('DOCNO').text)
#     # rank = int(rank)
#     print(rank)
#
# from collections import defaultdict
# # d = defaultdict(list) # 字典套List
# # d['a'].append(1)
# # d['a'].append(2)
# # d['b'].append(4)
# profile = defaultdict(dict)
# profile.setdefault('add',dict())
# profile['add'].setdefault(2,list())
# profile['add'][2].append(10)
# profile['add'][2].append(20)
# profile['add'].setdefault(55, list())
# profile['add'][55].append(555)
# t = 0
# tt = profile['add'][2][t]
# str_add = 'baby'
# docno = 1
# position = 1
# profile.setdefault(str_add, dict())
# profile[str_add].setdefault(docno, list())
# profile[str_add][docno].append(position)
# # 判断指定的string是否在字典的key中
# print(profile[str_add].keys())
# str_fake = 'babe'
# if profile.get(str_fake):
#     print(1)
# else:
#     print(11)


# apply in sample.xml
import string
from stemming.porter2 import stem
from collections import defaultdict
import xml.etree.cElementTree as ET
str_xml = open('trec.sample.xml', 'r').read()
root = ET.XML(str_xml)
trantab = str.maketrans(dict.fromkeys(string.punctuation, ''))
stopwords = open('englishST.txt')
stops = stopwords.read()
stops.split()
my_index = defaultdict(dict)
for node in root:
    docno = int(node.find('DOCNO').text)
    text_head = node.find('HEADLINE').text
    text_text = node.find('TEXT').text
    text = text_head + text_text
    text = text.translate(trantab)
    token_text = text.split()
    token_lower_text = []
    for term in token_text:
        token_lower_text.append(term.lower())
    token_lower_stop_text = []
    for term in token_lower_text:
        if term not in stops:
            token_lower_stop_text.append(term)
    token_lower_stop_stem_text = []
    for term in token_lower_stop_text:
        token_lower_stop_stem_text.append(stem(term))
    position = 1
    for term in token_lower_stop_stem_text:
        if term in my_index.keys():
            if docno in my_index[term].keys():
                my_index[term][docno].append(position)
                position += 1
            else:
                my_index[term].setdefault(docno, list()) # 1
                my_index[term][docno].append(position)
                position += 1
        else:
            my_index.setdefault(term, dict())
            my_index[term].setdefault(docno, list())
            my_index[term][docno].append(position)
            position += 1

import json
# js_my_index = json.dumps(my_index)

fileObject = open('index.json', 'w')
# fileObject.writelines(js_my_index)
# fileObject.close()

for i in my_index:
    # js_i = json.dumps(i)
    fileObject.write(i + ':\n')
    for j in my_index[i]:
        fileObject.write('          ' + json.dumps(j) + ': ')
        fileObject.writelines(json.dumps(my_index[i][j]) + '\n')
    fileObject.write('\n')
fileObject.close()

fileObject = open('index.txt', 'w')
for i in my_index:
    fileObject.write(i + ':\n')
    for j in my_index[i]:
        fileObject.write('          ' + str(j) + ': ')
        fileObject.write(str(my_index[i][j]) + '\n')
    fileObject.write('\n')
fileObject.close()





