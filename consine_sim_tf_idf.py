import numpy as np
import math

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
            final_dict[vocab_dict[key]] = round((1 + math.log10(float(value)))*(float(inverted_index[query_dict[key]])),3)
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


if __name__ == '__main__':
    rows,columns = 1225,32627
    doc_index = dict()
    query = dict()
    tf_idf_values = dict()
    normalized_tf_idf_values = dict()
    consine_dict = dict()
    file = open('tf_idf_each_document.txt','w')
    another_file = open('tf_idf_top_10.txt','w')
    with open('query_terms.txt', 'r') as f:
        for line in f:
            line = line.strip()
            key, value = line.split(maxsplit=1)
            query[key] = value
    generate_dictionary('tf_idf_frequencies.txt',tf_idf_values)
    doc_index = read_from_file('doc_index.txt',2)
    document_vectorized_form = document_vectorization('tf_idf_frequencies.txt',rows,columns)   
    for keys in query:
        query_vectorized_form = np.zeros(columns)
        normalized_query_value = process_query(query[keys])
        for key, value in normalized_query_value.items():
            query_vectorized_form[int(key)-1] = float(value)
        dot_products = np.dot(document_vectorized_form, query_vectorized_form)
        top_10_indices = np.argsort(dot_products)[::-1][:10]
        top_10_dot_products = dot_products[top_10_indices]
        top_10_rows = document_vectorized_form[top_10_indices]
        top_10_row_numbers = [np.where((document_vectorized_form == row).all(axis=1))[0][0] for row in top_10_rows]
        file.write('Query Term: '+ str(keys)+'\n')
        file.write('Weighting Scheme: TFIDF'+'\n')
        for i in range(rows):
             file.write(str(i+1) +' '+doc_index[str(i+1)] +' '+ str(round(dot_products[i],3))+'\n') 
        file.write('\n')
        another_file.write('Query Term: '+ str(keys)+'\n')
        another_file.write('Weighting Scheme: TFIDF'+'\n')
        for i in range(10):
            another_file.write(str(top_10_row_numbers[i]+1) +' '+doc_index[str(top_10_row_numbers[i]+1)] +' '+ str(round(top_10_dot_products[i],3))+'\n') 
        another_file.write('\n')