import math

def generate_dictionary(my_dict,my_another_dict):
    with open("term_frequencies.txt") as f:
        for line in f:
            line = line.strip().split()
            key = line[0]
            df_t = len(line)-1
            my_another_dict[key] = df_t
            values = {}
            for value in line[1:]:
                value = value.split(":")
                values[value[0]] = value[1]
            my_dict[key] = values

def generate_bm25_frequencies(my_dict,my_another_dict,N):
    k = 5
    for outer_key,outer_value in my_dict.items():
        for inner_key,inner_value in outer_value.items():
            bm25 = ((k+1) * int(inner_value)) / (int(inner_value) + k)
            inverted_i = (N+1) / my_another_dict[outer_key]
            bm25 = bm25 * math.log10(inverted_i)
            bm25 = round(bm25, 3)
            my_dict[outer_key][inner_key] = round(bm25,3)

def read_from_file(my_file):
    my_dict = {}
    with open(my_file, 'r') as file:
        for line in file:
            value, key = line.strip().split()
            my_dict[key] = value
    return my_dict

if __name__ == '__main__':
    term_indexes = dict()
    inverted_indexes = dict()
    doc_dict = read_from_file('doc_index.txt')
    N = len(doc_dict)
    generate_dictionary(term_indexes,inverted_indexes)
    generate_bm25_frequencies(term_indexes,inverted_indexes,N)
    bm25_file = open('bm25_frequenices.txt','w')
    for outer_key,outer_value in term_indexes.items():
        my_string = ''
        for inner_key,inner_value in outer_value.items():
            my_string += str(inner_key)+':'+str(inner_value)+' '
        bm25_file.write(str(outer_key)+' '+my_string+'\n')