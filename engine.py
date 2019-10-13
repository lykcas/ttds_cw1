# apply in sample.xml
import string
import json
import re
from stemming.porter2 import stem
from collections import defaultdict
import xml.etree.cElementTree as ET


def term_manage(term, stops):
    trantab = str.maketrans(dict.fromkeys(string.punctuation, ''))
    term = term.translate(trantab)
    term = term.lower()
    if term in stops:
        term = ''
    term = stem(term)
    return term


def one_term_search(my_index, one_term):
    # flag = 2
    # results = 'No result'
    if my_index.get(one_term):
        return my_index[one_term]
    else:
        return 'No results'


def bool_term_search(my_index, bool_term_a, sear_type, bool_term_b): # AND = 1, OR = 2, AND NOT = 3
    # if flag == 'AND': sear_type = 1
    # elif flag == 'OR': sear_type = 2
    # elif flag == 'AND NOT': sear_type = 3

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


def comp_bool_search(my_index, term_long, term_short, sear_type):
    # if flag == 'AND': sear_type = 1
    # elif flag == 'OR': sear_type = 2
    # long_term 'AND NOT' short_term : sear_type = 3
    # short_term 'AND NOT' long_term, long yes : sear_type = 4
    # short_term 'AND NOT' long_term, long no : sear_type = 4
    results = 0
    temp = term_long.split()
    term_a = temp[0]
    term_b = temp[1]
    short_docid = []
    long_docid = []
    d = []
    if my_index.get(term_short):
        short_docid = my_index[term_short].keys()

    if phrase_search(my_index, term_a, term_b) != 'No result':
        long_docid = phrase_search(my_index, term_a, term_b)

    if sear_type == 1:
        d = list(set(short_docid).intersection(set(long_docid)))
        if d:
            results = 1
    elif sear_type == 2:
        d = list(set(short_docid).union(set(long_docid)))
        if d:
            results = 1
    elif sear_type == 3:  # and whether_long == 1:
        d = list(set(long_docid).difference(set(short_docid)))
        if d:
            results = 1
    elif sear_type == 4:
        d = list(set(short_docid).difference(set(long_docid)))
        if d:
            results = 1
    if results == 1:
        d = sorted(list(set(d)))
        return d
    else:
        return 'No result'


def search_active(stops, my_index):
    str_input = input("Please input: ")
    hash_ = re.compile('#')
    whether_hash = hash_.match(str_input)
    whether_space = 0
    # if whether_hash:
    for i in str_input:
        if i == ' ':
            whether_space = 1
    if whether_hash:
        dis = []
        for i in str_input:
            if i == '(':
                break
            if i != '#':
                dis.append(i)
        dis_str = "".join(dis)
        dis_int = int(dis_str)
        pos1 = str_input.find('(')
        pos2 = str_input.find(',')
        pos3 = str_input.find(')')
        dis_a = str_input[pos1 + 1:pos2]
        dis_b = str_input[pos2 + 2:pos3]
        dis_a = term_manage(dis_a, stops)
        dis_b = term_manage(dis_b, stops)
        return distence_search(my_index, dis_a, dis_b, dis_int)
        # exit()
    if whether_space == 0:
        term_managed = term_manage(str_input, stops)
        return one_term_search(my_index, term_managed)
        # exit()
    double_quatation = re.compile('"')
    whether_double_quatiation = double_quatation.match(str_input)  # 若输入含"，则 whether_double_quatiation = 1
    if str_input[-1] == '"':
        phrase_str = str_input[1:-1]
        phrase_str.split()
        phrase_a = term_manage(phrase_str[0], stops)
        phrase_b = term_manage(phrase_str[1], stops)
        return phrase_search(my_index, phrase_a, phrase_b)
        # exit()
    if not whether_double_quatiation:
        if str_input.find('AND'):
            sear_type = 1
            pos1 = str_input.find('AND')
            bool_term_a = str_input[0:pos1 - 1]
            bool_term_b = str_input[pos1 + 4:]
            bool_term_a = term_manage(bool_term_a, stops)
            bool_term_b = term_manage(bool_term_b, stops)
            return bool_term_search(my_index, bool_term_a, 1, bool_term_b)
            # exit()
        elif str_input.find('OR'):
            sear_type = 2
            pos1 = str_input.find('OR')
            bool_term_a = str_input[0:pos1 - 1]
            bool_term_b = str_input[pos1 + 3:]
            bool_term_a = term_manage(bool_term_a, stops)
            bool_term_b = term_manage(bool_term_b, stops)
            return bool_term_search(my_index, bool_term_a, 2, bool_term_b)
            # exit()
        elif str_input.find('AND NOT'):
            sear_type = 3
            pos1 = str_input.find('AND NOT')
            bool_term_a = str_input[0:pos1 - 1]
            bool_term_b = str_input[pos1 + 8:]
            bool_term_a = term_manage(bool_term_a, stops)
            bool_term_b = term_manage(bool_term_b, stops)
            return bool_term_search(my_index, bool_term_a, 3, bool_term_b)
            # exit()
    if whether_double_quatiation:
        if str_input.find('AND'):
            if str_input[0] == '"':
                pos1 = str_input.find('AND')
                term_long = str_input[1:pos1-2]
                term_short = str_input[pos1+4:]
                return comp_bool_search(my_index, term_long, term_short, 1)
            else:
                pos1 = str_input.find('AND')
                term_long = str_input[pos1+5:-1]
                term_short = str_input[0:pos1-1]
                return comp_bool_search(my_index, term_long, term_short, 1)
        elif str_input.find('OR'):
            if str_input[0] == '"':
                pos1 = str_input.find('OR')
                term_long = str_input[1:pos1-2]
                term_short = str_input[pos1+3:]
                return comp_bool_search(my_index, term_long, term_short, 2)
            else:
                pos1 = str_input.find('OR')
                term_long = str_input[pos1+4:-1]
                term_short = str_input[0:pos1-1]
                return comp_bool_search(my_index, term_long, term_short, 2)
        elif str_input.find('AND NOT'):
            if str_input[0] == '"':
                pos1 = str_input.find('AND NOT')
                term_long = str_input[1:pos1-2]
                term_short = str_input[pos1+8:]
                return comp_bool_search(my_index, term_long, term_short, 3)
            else:
                pos1 = str_input.find('AND NOT')
                term_long = str_input[pos1+9:-1]
                term_short = str_input[0:pos1-1]
                return comp_bool_search(my_index, term_long, term_short, 4)
    else:
        return 'No result'


if __name__ == '__main__':
    str_xml = open('trec.sample.xml', 'r').read()
    root = ET.XML(str_xml)
    trantab = str.maketrans(dict.fromkeys(string.punctuation, ' '))
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

    while 1:
        print(search_active(stops, my_index))




