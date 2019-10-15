import string
import json
import re
from stemming.porter2 import stem
from collections import defaultdict
import xml.etree.cElementTree as ET
import math

def one_term_search(my_index, one_term):
    # flag = 2
    # results = 'No result'
    d = []
    if my_index.get(one_term):
        for docid in my_index[one_term]:
            d.append(docid)
        return d

if __name__ == '__main__':
    str_xml = open('trec.sample.xml', 'r').read()
    root = ET.XML(str_xml)
    trantab = str.maketrans(dict.fromkeys(string.punctuation, ' '))
    stopwords = open('englishST.txt')
    stops = stopwords.read()
    stops = stops.split()
    stopwords.close()
    id_count = 0
    for node in root:
        id_count = id_count + 1

    with open('index.json', 'r') as ff:
        my_index = json.load(ff)
    ff.close()

    f = open('./query.txt')
    file_result = open('ranked_retrieval.txt', 'w')
    lines = f.readlines()
    for line in lines:
        line = line.strip('\n')
        pos1 = line.find(' ')
        query_number = int(line[0:pos1])
        str_input = line[pos1 + 1:]
        str_input = str_input.split()
        my_query = []
        for term in str_input:
            trantab = str.maketrans(dict.fromkeys(string.punctuation, ' '))
            term = term.translate(trantab)
            term = term.lower()
            if term in stops:
                term = ''
            term = stem(term)
            if term:
                my_query.append(term)

        df_idf = defaultdict(list)
        n = id_count
        for term in my_query:
            df_idf.setdefault(term, [])
            df_count = len(my_index[term].keys())
            df_idf[term].append(df_count)
            idf_count = math.log10(n/df_count)
            df_idf[term].append(idf_count)

        term_all_docid = one_term_search(my_index, my_query[0])
        term2 = []
        for term in my_query:
            term2 = one_term_search(my_index, term)
            term_all_docid = list(set(term_all_docid).union(set(term2))) # term_all_docid 是一个list

        tf = defaultdict(dict)
        for docid in term_all_docid:
            tf.setdefault(docid, dict())
            for term in my_query:
                tf[docid].setdefault(term, list())
                if my_index[term].get(docid):
                    tf[docid][term].append(len(my_index[term][docid]))
                else:
                    tf[docid][term].append(0)

        score = {}
        for docid in term_all_docid:
            weight_total = 0
            for term in my_query:
                if tf[docid][term][0] != 0:
                    tf_count = tf[docid][term][0]
                    weight = (1 + math.log10(tf_count)) * df_idf[term][1]
                else:
                    weight = 0
                weight_total = weight_total + weight
            score[docid] = weight_total

        result = sorted(score.items(), key=lambda x: x[1], reverse=True)
        i = 2
        j = 0
        while i:
            file_result.write(str(query_number) + ' 0 ' + str(result[j][0]) + ' 0 ' + str(result[j][1]) + ' 0')
            file_result.write('\n')
            j += 1
            i -= 1

    file_result.close()
    f.close()