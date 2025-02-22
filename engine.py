# apply in sample.xml
import string
import json
import re
from stemming.porter2 import stem
from collections import defaultdict
import xml.etree.cElementTree as ET


def term_manage(term, stops):
    trantab = str.maketrans(dict.fromkeys(string.punctuation, ' '))
    term = term.translate(trantab)
    term = term.lower()
    if term in stops:
        term = ''
    term = stem(term)
    return term


def one_term_search(my_index, one_term):
    # flag = 2
    # results = 'No result'
    d = []
    if my_index.get(one_term):
        for docid in my_index[one_term]:
            d.append(docid)
        return d
    else:
        return 'No results'


def bool_term_search(my_index, dict1, sear_type, dict2): # AND = 1, OR = 2, AND NOT = 3
    d = []
    results = 0
    if sear_type == 1:
        d = list(set(dict1).intersection(set(dict2)))
        if d:
            results = 1

    elif sear_type == 2:
        d = list(set(dict1).union(set(dict2)))
        if d:
            results = 1

    elif sear_type == 3:
        d = list(set(dict1).difference(set(dict2)))
        if d:
            results = 1
    if results == 1:
        d = sorted(list(set(d)))
        return d
    else:
        return 'No result'


def phrase_search(my_index, phrase_a, phrase_b):
    results = 0
    if my_index.get(phrase_a) and my_index.get(phrase_b):
        dict1 = my_index[phrase_a].copy()
        dict2 = my_index[phrase_b].copy()
        d = []
        for docid in dict1.keys():
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
    results = 0
    if my_index.get(dis_a) and my_index.get(dis_b):
        dict1 = my_index[dis_a].copy()
        dict2 = my_index[dis_b].copy()
        d = []
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


def search_active(stops, my_index):
    f_ = open('./query_bool.txt')
    f__ = open('boolean.txt', 'w')
    lines = f_.readlines()
    for line in lines:
        line = line.strip('\n')
        pos1 = line.find(' ')
        query_number = line[0:pos1]
        str_input = line[pos1+1:]
        result = []

        # str_input = input("Please input: ")
        hash_ = re.compile("#")
        whether_hash = hash_.match(str_input)
        whether_space = 0
        whether_and = str_input.find('AND')
        whether_or = str_input.find('OR')
        whether_not = str_input.find('AND NOT')
        whether_bool = 0
        if whether_and > 1 or whether_or > 1 or whether_not > 1:
            whether_bool = 1

        for i in str_input:
            if i == ' ':
                whether_space = 1
        if whether_hash:  # 距离搜索
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
            result = distence_search(my_index, dis_a, dis_b, dis_int)
            # exit()
        elif whether_space == 0:  # 单个单词搜索
            term_managed = term_manage(str_input, stops)
            result = one_term_search(my_index, term_managed)
        elif str_input[0] == '"' and str_input[-1] == '"' and whether_bool == 0:  # phrase_search短语搜索
            phrase_str = str_input[1:-1]
            phrase_str = phrase_str.split()
            phrase_a = term_manage(phrase_str[0], stops)
            phrase_b = term_manage(phrase_str[1], stops)
            result = phrase_search(my_index, phrase_a, phrase_b)

        elif whether_bool == 1:
            dict1 = []
            dict2 = []
            if whether_and > 0 and whether_not < 0:  # AND
                sear_type = 1
                pos = whether_and
                if str_input[0] == '"':
                    phrase_part = str_input[1:pos-2]
                    phrase_part = phrase_part.split()
                    phrase_a = term_manage(phrase_part[0], stops)
                    phrase_b = term_manage(phrase_part[1], stops)
                    dict1 = phrase_search(my_index, phrase_a, phrase_b)
                elif str_input[0] != '"':
                    term_a = str_input[0:pos-1]
                    term_a = term_manage(term_a, stops)
                    dict1 = one_term_search(my_index, term_a)
                if str_input[-1] == '"':
                    phrase_part = str_input[pos+5:-1]
                    phrase_part = phrase_part.split()
                    phrase_a = term_manage(phrase_part[0], stops)
                    phrase_b = term_manage(phrase_part[1], stops)
                    dict2 = phrase_search(my_index, phrase_a, phrase_b)
                elif str_input[-1] != '"':
                    term_b = str_input[pos+4:]
                    term_b = term_manage(term_b, stops)
                    dict2 = one_term_search(my_index, term_b)
                result = bool_term_search(my_index, dict1, sear_type, dict2)
            elif whether_or > 0:  # OR
                sear_type = 2
                pos = whether_or
                if str_input[0] == '"':
                    phrase_part = str_input[1:pos-2]
                    phrase_part = phrase_part.split()
                    phrase_a = term_manage(phrase_part[0], stops)
                    phrase_b = term_manage(phrase_part[1], stops)
                    dict1 = phrase_search(my_index, phrase_a, phrase_b)
                elif str_input[0] != '"':
                    term_a = str_input[0:pos-1]
                    term_a = term_manage(term_a, stops)
                    dict1 = one_term_search(my_index, term_a)
                if str_input[-1] == '"':
                    phrase_part = str_input[pos+4:-1]
                    phrase_part = phrase_part.split()
                    phrase_a = term_manage(phrase_part[0], stops)
                    phrase_b = term_manage(phrase_part[1], stops)
                    dict2 = phrase_search(my_index, phrase_a, phrase_b)
                elif str_input[-1] != '"':
                    term_b = str_input[pos+3:]
                    term_b = term_manage(term_b, stops)
                    dict2 = one_term_search(my_index, term_b)
                result = bool_term_search(my_index, dict1, sear_type, dict2)
            elif whether_not > 0:
                sear_type = 3
                pos = whether_not
                if str_input[0] == '"':
                    phrase_part = str_input[1:pos - 2]
                    phrase_part = phrase_part.split()
                    phrase_a = term_manage(phrase_part[0], stops)
                    phrase_b = term_manage(phrase_part[1], stops)
                    dict1 = phrase_search(my_index, phrase_a, phrase_b)
                elif str_input[0] != '"':
                    term_a = str_input[0:pos - 1]
                    term_a = term_manage(term_a, stops)
                    dict1 = one_term_search(my_index, term_a)
                if str_input[-1] == '"':
                    phrase_part = str_input[pos + 9:-1]
                    phrase_part = phrase_part.split()
                    phrase_a = term_manage(phrase_part[0], stops)
                    phrase_b = term_manage(phrase_part[1], stops)
                    dict2 = phrase_search(my_index, phrase_a, phrase_b)
                elif str_input[-1] != '"':
                    term_b = str_input[pos + 8:]
                    term_b = term_manage(term_b, stops)
                    dict2 = one_term_search(my_index, term_b)
                result = bool_term_search(my_index, dict1, sear_type, dict2)

        else:
            result = 'No result'

        if result == 'No result':
            f__.write(query_number + ' 0 0 0 1 0\n')
        else:
            for ii in result:
                f__.write(query_number + ' 0 ' + str(ii) + ' 0 1 0')
                f__.write('\n')
    f_.close()
    f__.close()


if __name__ == '__main__':
    trantab = str.maketrans(dict.fromkeys(string.punctuation, ' '))

    stopwords = open('englishST.txt')
    stops = stopwords.read()
    stops = stops.split()
    stopwords.close()

    with open('index.json', 'r') as f:
        my_index = json.load(f)
    f.close()
    search_active(stops, my_index)




