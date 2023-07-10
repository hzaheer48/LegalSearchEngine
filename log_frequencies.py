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

def generate_log_term_frequenceis(my_dict):
    for outer_key,outer_value in my_dict.items():
        for inner_key,inner_value in outer_value.items():
            my_dict[outer_key][inner_key] = round(1 + math.log10(float(inner_value)),3)



if __name__ == '__main__':
    term_indexes = dict()
    generate_dictionary(term_indexes)
    generate_log_term_frequenceis(term_indexes)
    log_term_frequencies_file = open('log_term_frequencies.txt','w')
    for outer_key,outer_value in term_indexes.items():
        my_string = ''
        for inner_key,inner_value in outer_value.items():
            my_string += str(inner_key)+':'+str(inner_value)+' '
        log_term_frequencies_file.write(str(outer_key)+' '+my_string+'\n')