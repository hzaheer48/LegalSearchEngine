import os
import re
import string
import PyPDF2
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer 

def extracting_text_from_pdf(pdf_file_path):
    pdf_file = open(pdf_file_path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    num_pages = len(pdf_reader.pages)
    text = ''
    for page in range(num_pages):
        pdf_page = pdf_reader.pages[page]
        text += pdf_page.extract_text()
    pdf_file.close()
    return text

def total_files(folder):
    files = os.listdir(folder)
    num_files = len(files)
    return num_files

def preprocessing_step(words):
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
    return tokens

def sort_dictionary(my_dict):
    my_keys = list(my_dict.keys())
    my_keys = list(map(int, my_keys))
    my_keys.sort()
    my_keys = list(map(str, my_keys))
    sorted_dict = {i: my_dict[i] for i in my_keys}
    return sorted_dict

def read_from_file(my_file):
    my_dict = {}
    with open(my_file, 'r') as file:
        for line in file:
            value, key = line.strip().split()
            my_dict[key] = value
    return my_dict

if __name__ == '__main__':
    vocab_dict = read_from_file('vocb_index.txt')
    doc_dict = read_from_file('doc_index.txt')
    corrupt_dict = read_from_file('corrupt_index.txt')
    term_indexes = dict()
    case_types = ['C.A','C.M.A','C.P','Const.P','Crl.A','Crl.P','S.M.C']
    for case_type in case_types:
        files = total_files(case_type)
        for i in range(files):
            current_file = case_type+'.'+str(i+1)+'.pdf'
            if current_file not in corrupt_dict:
                words = extracting_text_from_pdf(case_type+'/'+current_file)
                tokens = preprocessing_step(words)
                ps = PorterStemmer()
                for token in tokens:
                    tok = ps.stem(token)
                    if tok in vocab_dict:
                        my_term_key = vocab_dict[tok]
                        my_doc_key = doc_dict[current_file]
                        if my_term_key not in term_indexes:
                            doc_term_frequencies = dict()
                            doc_term_frequencies[my_doc_key] = 1
                            term_indexes[my_term_key] = doc_term_frequencies
                        else:
                            currect_dictionary = term_indexes[my_term_key]
                            if my_doc_key not in currect_dictionary:
                                currect_dictionary[my_doc_key] = 1
                            else:
                                currect_dictionary[my_doc_key] += 1
                            term_indexes[my_term_key] = currect_dictionary
                print('Done with file ',current_file)
    term_indexes = sort_dictionary(term_indexes)
    term_frequencies_file = open('term_frequencies.txt','w')
    for outer_key,outer_value in term_indexes.items():
        my_string = ''
        for inner_key,inner_value in outer_value.items():
            my_string += str(inner_key)+':'+str(inner_value)+' '
        term_frequencies_file.write(str(outer_key)+' '+my_string+'\n')
    

    