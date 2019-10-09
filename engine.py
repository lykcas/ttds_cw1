import numpy as np
import string
import re
import xml.etree.cElementTree as ET

str_xml = open('sample.xml', 'r').read()
root = ET.XML(str_xml)

for child in root:
    for i in child:
        print(i.text)

for node in root.iter('DOCNO'):
    print(node.text)

for node in root.findall('DOC'):
    rank = int(node.find('DOCNO').text)
    print(rank)

from collections import defaultdict
# d = defaultdict(list) # 字典套List
# d['a'].append(1)
# d['a'].append(2)
# d['b'].append(4)
# d = defaultdict(set) #不推荐，set是无序的
# d['a'].add(1)
# d['a'].add(2)
# d['b'].add(4)
###############################################################################
# d = {} # A regular dictionary 字典套list
# d.setdefault('a', []).append(1)
# d.setdefault('a', []).append(2)
# d.setdefault('b', []).append(4)
###############################################################################
profile = defaultdict(dict)
profile.setdefault('add',dict())
profile['add'].setdefault(2,list())
profile['add'][2].append(10)
profile['add'][2].append(20)
profile['add'].setdefault(55, list())
profile['add'][55].append(555)
t = 0
tt = profile['add'][2][t]

# import string
# # token
# trantab = str.maketrans(dict.fromkeys(string.punctuation, ' '))
# text = "He likes to wink, he likes to drink"
# text.translate(trantab)
# token_text = text.split()
# token_lower_text = []
# for term in token_text:
#     token_lower_text.append(term.lower())
#
# # stopwords
# token_lower_stop_text = []
# stopwords = open('englishST.txt')
# stops = stopwords.read()
# stops.split()
# for term in token_lower_text:
#     if term not in stops:
#         token_lower_stop_text.append(term)

# apply in sample.xml
import string
from stemming.porter2 import stem
trantab = str.maketrans(dict.fromkeys(string.punctuation, ' '))
stopwords = open('englishST.txt')
stops = stopwords.read()
stops.split()
for node in root.findall('DOC'):
    docno = int(node.find('DOCNO').text)
    text = node.find('Text').text
    text.translate(trantab)
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



