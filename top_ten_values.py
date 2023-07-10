import random

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

def generate_top_values(my_dict):
    for outer_key,outer_value in my_dict.items():
        summing = 0
        for inner_key,inner_value in outer_value.items():
            summing += float(inner_value)
        my_dict[outer_key] = round(summing,3)
    sorted_dict = dict(sorted(my_dict.items(), key=lambda item: item[1], reverse=True)[:10])
    return sorted_dict

def read_from_file(my_file):
    my_dict = {}
    with open(my_file, 'r') as file:
        for line in file:
            value, key = line.strip().split()
            my_dict[value] = key
    return my_dict

def write_to_file(my_file,my_dict,vocab_dict):
    with open(my_file, 'w') as file:
        for key,value in my_dict.items():
            file.write(str(vocab_dict[key])+' '+str(value)+'\n')

def creating_set(my_dict_1,my_dict_2,vocab_dict):
    my_set = set()
    for key in my_dict_1:
        my_set.add(vocab_dict[key])
    for key in my_dict_2:
        my_set.add(vocab_dict[key])
    return my_set

def generate_query_terms(query_term):
    query_dict = dict()
    for i in range(5):
        generating_list = random.sample(list(query_term), 2)
        sentence = ' '.join(generating_list)
        query_dict[i+1] = sentence
    for i in range(5):
        generating_list = random.sample(list(query_term), 3)
        sentence = ' '.join(generating_list)
        query_dict[i+6] = sentence
    return query_dict

if __name__ == '__main__':
    tf_idf_values = dict()
    bm25_values = dict()
    vocab_dict = dict()
    vocab_dict = read_from_file('vocb_index.txt')
    generate_dictionary('tf_idf_frequencies.txt',tf_idf_values)
    generate_dictionary('bm25_frequenices.txt',bm25_values)
    tf_idf_values = generate_top_values(tf_idf_values)
    bm25_values = generate_top_values(bm25_values)
    write_to_file('top_ten_tf_idf_values.txt',tf_idf_values,vocab_dict)
    write_to_file('top_ten_bm25_values.txt',bm25_values,vocab_dict)
    query_terms = creating_set(tf_idf_values,bm25_values,vocab_dict)
    query_dict = generate_query_terms(query_terms)
    with open('query_terms.txt', 'w') as file:
        for key,value in query_dict.items():
            file.write(str(key)+' '+str(value)+'\n')