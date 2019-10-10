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
fileObject = open('index.json', 'w')

for i in my_index:
    # js_i = json.dumps(i)
    fileObject.write(i + '\n')
    for j in my_index[i]:
        fileObject.write('          ' + json.dumps(j) + ' ')
        fileObject.writelines(json.dumps(my_index[i][j]) + '\n')
    fileObject.write('\n')
fileObject.close()

fileObject = open('index.txt', 'w')
for i in my_index:
    fileObject.write(i + '\n')
    for j in my_index[i]:
        fileObject.write('          ' + str(j) + ' ')
        fileObject.write(str(my_index[i][j]) + '\n')
    fileObject.write('\n')
fileObject.close()

def one_term_search(my_index, one_term):
    # flag = 2
    results = 'No result'
    if my_index.get(one_term):
        return my_index[one_term]
    else:
        return results

def bool_term_search(my_index, bool_term_a, flag, bool_term_b):
    sear_type = 0 # AND = 1, OR = 2, NOT = 3
    if flag == 'AND': sear_type = 1
    elif flag == 'OR': sear_type = 2
    elif flag == 'AND NOT': sear_type = 3

    if sear_type == 1:
        if my_index.get(bool_term_a) and my_index.get(bool_term_b):
            # dict1 = defaultdict(list)
            # dict2 = defaultdict(list)
            dict1 = my_index[bool_term_a].copy()
            dict2 = my_index[bool_term_b].copy()
            d = []
            results = 0
            for docid in dict1:
                if docid in dict2.keys():
                    d.append(docid)
                    results = 1
            if results == 0:
                return 'No result'
            elif results == 1:
                d = sorted(list(set(d)))
                return d
        else:
            return  'No result'
    elif sear_type == 2:
        if my_index.get(bool_term_a) or my_index.get(bool_term_b):
            dict1 = my_index[bool_term_a].copy()
            dict2 = my_index[bool_term_b].copy()
            d = []
            for docid in dict1:
                d.append(docid)
            for docid in dict2:
                d.append(docid)
            d = sorted(list(set(d)))
            return d
        else:
            return 'No result'
    elif sear_type == 3:
        if my_index.get(bool_term_a) or my_index.get(bool_term_b):
            dict1 = my_index[bool_term_a].copy()
            dict2 = my_index[bool_term_b].copy()
            d = []
            results = 0
            for docid in dict1:
                if docid not in dict2.keys():
                    d.append(docid)
                    results = 1
            if results == 0:
                return 'No result'
            elif results == 1:
                d = sorted(list(set(d)))
                return d
        else:
            return 'No result'

def phrase_search(my_index, phrase_a, phrase_b):
    if my_index.get(phrase_a) and my_index.get(phrase_b):
        dict1 = my_index[phrase_a].copy()
        dict2 = my_index[phrase_b].copy()
        d = []
        results = 0
        for docid in dict1:
            if docid in dict2.keys():
                for position1 in dict1[docid]:
                    for position2 in dict2[docid]:
                        if (position2 - position1) == 1:
                            d.append(docid)
                            results = 1
        if results == 1:
            d = sorted(list(set(d)))
            return d
        elif results == 0:
            return 'No result'

def distence_search(my_index, dis_a, dis_b, dis):
    if my_index.get(dis_a) and my_index.get(dis_b):
        dict1 = my_index[dis_a].copy()
        dict2 = my_index[dis_b].copy()
        d = []
        results = 0
        for docid in dict1:
            if docid in dict2.keys():
                for position1 in dict1[docid]:
                    for position2 in dict2[docid]:
                        if abs(position1 - position2) <= dis:
                            d.append(docid)
                            results = 1
        if results == 1:
            d = sorted(list(set(d)))
            return d
        elif results == 0:
            return 'No result'

def comp_bool_search(my_index, term_a, term_b, flag):
    sear_type = 0 # AND = 1, OR = 2, NOT = 3
    if flag == 'AND': sear_type = 1
    elif flag == 'OR': sear_type = 2
    elif flag == 'AND NOT': sear_type = 3




