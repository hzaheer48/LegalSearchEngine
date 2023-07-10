import math

def generate_dictionary(my_dict,my_another_dict,N):
    with open("log_term_frequencies.txt") as f:
        for line in f:
            line = line.strip().split()
            key = line[0]
            values = {}
            for value in line[1:]:
                value = value.split(":")
                values[value[0]] = value[1]
            my_dict[key] = values

def generate_tf_idf_values(my_dict,my_another_dict):
    for outer_key,outer_value in my_dict.items():
        for inner_key,inner_value in outer_value.items():
            my_dict[outer_key][inner_key] = round(float(inner_value)*float(my_another_dict[outer_key]),3)

def read_from_file(my_file):
    my_dict = {}
    with open(my_file, 'r') as file:
        for line in file:
            value, key = line.strip().split()
            my_dict[key] = value
    return my_dict

def read_from_file_another(my_file):
    my_dict = {}
    with open(my_file, 'r') as file:
        for line in file:
            value, key = line.strip().split()
            my_dict[value] = key
    return my_dict


if __name__ == '__main__':
    term_indexes = dict()
    inverted_indexes = dict()
    doc_dict = read_from_file('doc_index.txt')
    inverted_indexes = read_from_file_another('inverted_index_frequencies.txt')
    N = len(doc_dict)
    generate_dictionary(term_indexes,inverted_indexes,N)
    generate_tf_idf_values(term_indexes,inverted_indexes)
    tf_idf_file = open('tf_idf_frequencies.txt','w')
    for outer_key,outer_value in term_indexes.items():
        my_string = ''
        for inner_key,inner_value in outer_value.items():
            my_string += str(inner_key)+':'+str(inner_value)+' '
        tf_idf_file.write(str(outer_key)+' '+my_string+'\n')