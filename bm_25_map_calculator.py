import re
import string
import math
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer

def preprocessing_step(words):
    final_list = list()
    lmtzr = WordNetLemmatizer()
    words = words.lower().replace('\n',' ')
    words =  re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '',words)
    words = re.sub('['+string.punctuation+']', ' ', words)
    words = re.sub(r'\b\w{1,3}\b', '', words)
    words  = re.sub(r'[^\x00-\x7F]+','',words)
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(words)
    tokens = [word for word in tokens if word.lower() not in stop_words]
    tokens = [word for word in tokens if word.isalpha()]
    tokens = [lmtzr.lemmatize(word) for word in tokens]
    ps = PorterStemmer()
    for token in tokens:
        tok = ps.stem(token)
        final_list.append(tok)
    result = ' '.join(final_list)
    return result

def generate_dictionary(file,my_dict):
    with open(file) as f:
        for line in f:
            line = line.strip().split()
            key = line[0]
            values = {}
            for value in line[1:]:
                value = value.split(":")
                values[value[0]] = value[1]
            my_dict[key] = values

def read_from_file(my_file,n):
    my_dict = {}
    with open(my_file, 'r') as file:
        for line in file:
            key, value = line.strip().split()
            if n==1:
                my_dict[value] = key
            else:
                my_dict[key] = value
    return my_dict

def process_query(query):
    query_dict = dict()
    occurrences_dict = dict()
    final_dict = dict()
    vocab_dict = read_from_file('vocb_index.txt',1)
    inverted_index = read_from_file('inverted_index_frequencies.txt',2)
    query = query.split()
    for que in query:
        if que in vocab_dict:
            query_dict[que] = vocab_dict[que]
            if que in occurrences_dict:
                occurrences_dict[que] += 1
            else:
                occurrences_dict[que] = 1    
        else:
            occurrences_dict[que] = 0
    for key,value in occurrences_dict.items():
        if occurrences_dict[key] > 0 :
            final_dict[vocab_dict[key]] = occurrences_dict[key]
        #    final_dict[vocab_dict[key]] = round((1 + math.log10(float(value)))*(float(inverted_index[query_dict[key]])),3)
    sum_squares = sum([value ** 2 for value in final_dict.values()])
    sqrt_sum_squares = math.sqrt(sum_squares)
    for key,value in final_dict.items():
        final_dict[key] = round(value/sqrt_sum_squares,3)
    return final_dict

def document_vectorization(file_name,rows,columns):    
    arr_2d = np.zeros((rows, columns))
    with open(file_name, "r") as f:
        for line in f:
            values = line.split()
            col = int(values[0]) - 1  
            for value in values[1:]:
                row, val = value.split(":")
                col = int(col)  
                val = float(val)
                row = int(row) - 1
                arr_2d[row, col] = val
    row_norms = np.sqrt(np.sum(arr_2d**2, axis=1))
    arr_normalized = (arr_2d / row_norms[:, np.newaxis])
    return arr_normalized

def calculate_recall(expected,result):
    recall = list()
    total = 0
    for r in result:
        if expected in r:
            total+=1
        recall.append(total/len(result))
    return recall[-1]


def calculate_precision(expected,result):
    precision = list()
    total = 0
    for i,r in enumerate(result):
        if expected in r:
            total+=1
        precision.append(round((total/(i+1)),3))
    return precision[-1]

def calculate_average_percision(expected,result):
    average_percision = list()
    total = 0
    for i,r in enumerate(result):
        if expected in r:
            total+=1
            average_percision.append(round((total/(i+1)),3))
    return average_percision

def calculate_f1_score(recall,precision):
    f1_score = round(((2*recall*precision)/(recall+precision)),3)
    return f1_score

if __name__ == '__main__':
    my_categories = ['C.A.','C.M.A.','C.P.','Const.P.','Crl.A.','Crl.P.','S.M.C.','Crl.A.','Const.P.','C.A.']
    mean_average_percision = 0
    index = 1
    rows,columns = 1225,32627
    doc_index = dict()
    query = dict()
    tf_idf_values = dict()
    normalized_tf_idf_values = dict()
    consine_dict = dict()
    another_file = open('bm25_map_calculator.txt','w')
    with open('query_terms.txt', 'r') as f:
        for line in f:
            line = line.strip()
            key, value = line.split(maxsplit=1)
            query[key] = value
    generate_dictionary('bm25_frequenices.txt',tf_idf_values)
    doc_index = read_from_file('doc_index.txt',2)
    document_vectorized_form = document_vectorization('bm25_frequenices.txt',rows,columns)   
    for keys in query:
        query_vectorized_form = np.zeros(columns)
        my_query = preprocessing_step(query[keys])
        normalized_query_value = process_query(my_query)
        for key, value in normalized_query_value.items():
            query_vectorized_form[int(key)-1] = float(value)
        dot_products = np.dot(document_vectorized_form, query_vectorized_form)
        top_10_indices = np.argsort(dot_products)[::-1][:10]
        top_10_dot_products = dot_products[top_10_indices]
        top_10_rows = document_vectorized_form[top_10_indices]
        top_10_row_numbers = [np.where((document_vectorized_form == row).all(axis=1))[0][0] for row in top_10_rows]
        top_10_categories = list()
        for i in range(len(top_10_row_numbers)):
            top_10_categories.append(doc_index[str(top_10_row_numbers[i]+1)])
        recall = calculate_recall(my_categories[0],top_10_categories)
        precision = calculate_precision(my_categories[0],top_10_categories)
        f1_score = calculate_f1_score(recall,precision)
        average_percision = calculate_average_percision(my_categories[0],top_10_categories)
        if len(average_percision)>0:
            final_average_percision = sum(average_percision)/len(average_percision)
        else:
            final_average_percision = 0
        mean_average_percision += final_average_percision
        another_file.write('Query Term:'+ str(index)+'\t'+'BM25'+'\t'+str(precision)+'\t'+str(recall)+'\t'+str(f1_score)+'\t'+str(round(final_average_percision,3))+'\t'+'\n')
        my_categories.pop(0)
        index+=1
    another_file.write('Mean Average Precision for 10 queries:'+str(round((mean_average_percision/10),3)))