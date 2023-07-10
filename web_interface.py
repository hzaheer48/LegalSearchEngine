# plt.imshow(wordcloud, interpolation='bilinear')
# plt.axis("off")
# plt.show()
# from flask import Flask, render_template, request
# import re
# import string
# import math
# import numpy as np
# from wordcloud import WordCloud
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize
# from nltk.stem import PorterStemmer
# from nltk.stem.wordnet import WordNetLemmatizer 
# from PIL import Image, ImageDraw, ImageFont
# app = Flask(__name__)


# def read_abstract():
#     doc_index = dict()
#     abstracts = dict()
#     final_abstracts = dict()
#     categories = ['C.A.','C.M.A.','C.P.','Const.P.','Crl.A.','Crl.P.','S.M.C.']
#     my_list = list()
#     final_list = list()
#     my_string = ''
#     with open('abstracts.txt', 'r') as file:
#         for i,line in enumerate(file):
#             if i < 1:
#                 continue
#             words = line.split()
#             for word in words:
#                 if word in categories:
#                     my_list.append(my_string)
#                     my_string = ''
#                 else:
#                     my_string += word.strip() + ' '
#     my_list.append(my_string)
#     my_list.pop(0)
#     pattern = r"\.Dated: (\d{2}-\d{2}-\d{4}|N/A)"
#     for items in my_list:
#         parts = re.split(pattern,items)
#         parts.pop()
#         del parts[1::2]
#         for i in range(len(parts)):
#             words = parts[i].split()
#             parts[i] = ' '.join(words[1:])
#         final_list.append(parts)
#     i = 0
#     for category in final_list:
#         my_index = 1
#         for cat in category:
#             abstracts[categories[i]+str(my_index)+'.pdf'] = cat
#             my_index+=1
#         i+=1
#     doc_index = read_from_file('doc_index.txt',1)
#     i = 1
#     for keys in doc_index:
#         final_abstracts[i] = abstracts[keys]
#         i+=1
#     return final_abstracts
        

# def preprocessing_step(words):
#     final_list = list()
#     lmtzr = WordNetLemmatizer() 
#     words = words.lower().replace('\n',' ')
#     words =  re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '',words)
#     words = re.sub('['+string.punctuation+']', ' ', words)
#     words = re.sub(r'\b\w{1,3}\b', '', words)
#     words  = re.sub(r'[^\x00-\x7F]+','',words)
#     stop_words = set(stopwords.words('english'))
#     tokens = word_tokenize(words)
#     tokens = [word for word in tokens if word.lower() not in stop_words]
#     tokens = [word for word in tokens if word.isalpha()]
#     tokens = [lmtzr.lemmatize(word) for word in tokens]
#     ps = PorterStemmer()
#     for token in tokens:
#         tok = ps.stem(token)
#         final_list.append(tok)
#     result = ' '.join(final_list)
#     return result

# def generate_dictionary(file,my_dict):
#     with open(file) as f:
#         for line in f:
#             line = line.strip().split()
#             key = line[0]
#             values = {}
#             for value in line[1:]:
#                 value = value.split(":")
#                 values[value[0]] = value[1]
#             my_dict[key] = values

# def read_from_file(my_file,n):
#     my_dict = {}
#     with open(my_file, 'r') as file:
#         for line in file:
#             key, value = line.strip().split()
#             if n==1:
#                 my_dict[value] = key
#             else:
#                 my_dict[key] = value
#     return my_dict

# def process_query(query):
#     query_dict = dict()
#     occurrences_dict = dict()
#     final_dict = dict()
#     vocab_dict = read_from_file('vocb_index.txt',1)
#     inverted_index = read_from_file('inverted_index_frequencies.txt',2)
#     query = query.split()
#     for que in query:
#         if que in vocab_dict:
#             query_dict[que] = vocab_dict[que]
#             if que in occurrences_dict:
#                 occurrences_dict[que] += 1
#             else:
#                 occurrences_dict[que] = 1    
#         else:
#             occurrences_dict[que] = 0
#     for key,value in occurrences_dict.items():
#         if occurrences_dict[key] > 0 :
#             final_dict[vocab_dict[key]] = round((1 + math.log10(float(value)))*(float(inverted_index[query_dict[key]])),3)
#     sum_squares = sum([value ** 2 for value in final_dict.values()])
#     sqrt_sum_squares = math.sqrt(sum_squares)
#     for key,value in final_dict.items():
#         final_dict[key] = round(value/sqrt_sum_squares,3)
#     return final_dict

# def document_vectorization(file_name,rows,columns,n):    
#     arr_2d = np.zeros((rows, columns))
#     with open(file_name, "r") as f:
#         for line in f:
#             values = line.split()
#             col = int(values[0]) - 1  
#             for value in values[1:]:
#                 row, val = value.split(":")
#                 col = int(col)  
#                 val = float(val)
#                 row = int(row) - 1
#                 arr_2d[row, col] = val
#     if n==1:
#         row_norms = np.sqrt(np.sum(arr_2d**2, axis=1))
#         arr_normalized = (arr_2d / row_norms[:, np.newaxis])
#         return arr_normalized
#     else:
#         return arr_2d

# @app.route('/')
# def index():
#     return render_template('index.html')


# @app.route('/search')
# def search():
#     my_list = list()
#     word_dict = dict()
#     query = request.args.get('query')
#     query = preprocessing_step(query)
#     normalized_query_value = process_query(query)
#     for key, value in normalized_query_value.items():
#             query_vectorized_form[int(key)-1] = float(value)
#     dot_products = np.dot(document_vectorized_form, query_vectorized_form)
#     top_100_indices = np.argsort(dot_products)[::-1][:100]
#     top_100_rows = document_vectorized_form[top_100_indices]
#     top_100_row_numbers = [np.where((document_vectorized_form == row).all(axis=1))[0][0] for row in top_100_rows]
#     page = int(request.args.get('page', 1))
#     start_index = (page - 1) * 10
#     end_index = start_index + 10
#     my_list = [abstracts[top_100_row_numbers[i]+1] for i in range(start_index, end_index)]
#     num_pages = int(np.ceil(len(top_100_row_numbers) / 10))
#     selected_docs = word_clouds[top_100_indices]
#     word_frequencies = np.sum(selected_docs, axis=0)
#     for i,elem in enumerate(word_frequencies):
#         word_dict[vocab_index[str(i+1)]] = elem
#     word_dict = {k: v for k, v in word_dict.items() if v != 0}
#     wordcloud = WordCloud(width=800, height=400,font_path='./ariblk.ttf').generate_from_frequencies(word_dict)
#     wordcloud_image = wordcloud.to_image()
#     wordcloud_image.save('wordcloud.png')
#     print(word_dict)
#     return render_template('search_results.html', check=True, my_list=my_list, page=page, num_pages=num_pages)

# if __name__ == '__main__':
#     rows,columns = 1225,32627
#     doc_index = dict()
#     query = dict()
#     tf_idf_values = dict()
#     normalized_tf_idf_values = dict()
#     consine_dict = dict()
#     vocab_index = read_from_file('vocb_index.txt',2)
#     generate_dictionary('tf_idf_frequencies.txt',tf_idf_values)
#     doc_index = read_from_file('doc_index.txt',2)
#     document_vectorized_form = document_vectorization('tf_idf_frequencies.txt',rows,columns,1)
#     word_clouds = document_vectorization('term_frequencies.txt',rows,columns,0)
#     query_vectorized_form = np.zeros(columns)
#     abstracts = read_abstract()
#     app.run()
