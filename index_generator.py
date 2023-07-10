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

def checking_for_valid_pdf(words):
    try:
        words_splitter = words.split()
        urdu_document = re.findall(r'[\u0600-\u06ff]+',words)
        if(len(words_splitter)==0):
            return False
        if(len(urdu_document)>0):
            return False
        return True
    except:
        print('Error reading file')
        return False

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

if __name__ == '__main__':
    vocab_index = set()
    doc_index = list()
    case_types = ['C.A','C.M.A','C.P','Const.P','Crl.A','Crl.P','S.M.C']
    corrupt_files = 1
    for case_type in case_types:
        files = total_files(case_type)
        for i in range(files):
            try:
                words = extracting_text_from_pdf(case_type+'/'+case_type+'.'+str(i+1)+'.pdf')
                if not words:
                    with open("corrupt_index.txt", "a") as f:
                        f.write(str(corrupt_files)+' '+case_type+'.'+str(i+1)+'.pdf'+'\n')
                        corrupt_files+=1
                    continue
                if checking_for_valid_pdf(words):
                    tokens = preprocessing_step(words)
                    ps = PorterStemmer()
                    for token in tokens:
                        tok = ps.stem(token)
                        vocab_index.add(tok)
                    doc_index.append(case_type+'.'+str(i+1)+'.pdf')
                    print('Done with file',case_type+'.'+str(i+1)+'.pdf')
            except Exception as e:
                print(f"Error reading {case_type+'.'+str(i+1)+'.pdf'}: {e}")
                with open("corrupt_index.txt", "a") as f:
                    f.write(str(corrupt_files)+' '+case_type+'.'+str(i+1)+'.pdf'+'\n')
                    corrupt_files+=1
                continue
    with open("vocb_index.txt", "w") as f:
        i = 1
        for index in vocab_index:
            f.write(str(i)+' '+index+'\n')
            i+=1
    with open("doc_index.txt", "w") as f:
        i = 1
        for index in doc_index:
            f.write(str(i)+' '+index+'\n')
            i+=1



