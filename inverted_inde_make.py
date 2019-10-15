import string
import json
import re
from stemming.porter2 import stem
from collections import defaultdict
import xml.etree.cElementTree as ET

str_xml = open('trec.sample.xml', 'r').read()
root = ET.XML(str_xml)
trantab = str.maketrans(dict.fromkeys(string.punctuation, ' '))
stopwords = open('englishST.txt')
stops = stopwords.read()
stops = stops.split()
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


with open('index.json', 'w') as fw:
    # json.dump(my_index, fw)
    json.dump(my_index, fw, indent=4, separators=(',', ': '))
fw.close()

fileObject = open('index.txt', 'w')
for i in my_index:
    fileObject.write(i + '\n')
    for j in my_index[i]:
        fileObject.write('          ' + str(j) + ' ')
        fileObject.write(str(my_index[i][j]) + '\n')
    fileObject.write('\n')
fileObject.close()