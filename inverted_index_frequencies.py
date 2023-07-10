import math

def generate_dictionary(my_dict):
    with open("term_frequencies.txt") as f:
        for line in f:
            line = line.strip().split()
            key = line[0]
            values = {}
            for value in line[1:]:
                value = value.split(":")
                values[value[0]] = value[1]
            my_dict[key] = values

def read_from_file(my_file):
    my_dict = {}
    with open(my_file, 'r') as file:
        for line in file:
            value, key = line.strip().split()
            my_dict[key] = value
    return my_dict

if __name__ == '__main__':
    term_indexes = dict()
    doc_dict = read_from_file('doc_index.txt')
    N = len(doc_dict)
    generate_dictionary(term_indexes)
    inverted_index_frequencies_file = open('inverted_index_frequencies.txt','w')
    for outer_key,outer_value in term_indexes.items():
        idf = round(math.log10(N/len(outer_value)),3)
        inverted_index_frequencies_file.write(str(outer_key)+' '+str(idf)+'\n')