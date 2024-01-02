#Read from Json file
import pandas as pd
import csv
import gcld3
import numpy as np
import nltk
nltk.download('stopwords')
nltk.download('punkt')

df_json = pd.read_json('/content/drive/MyDrive/firefox_fulllist_2023_new_category.json')
df_json.dropna(inplace=True)
df_json.head()

#print(len(df_json['id'].values))
#print(df_json.introduction.nunique())

df_csv = pd.DataFrame({'id': df['id'].tolist(), 'category': df['categories'].tolist(), 'description':df['introduction'].tolist()})
#df_csv.to_csv('chrome_fulllist_final_2301.csv', index=False)
df = df_csv

#Pre-processing texts
value_counts = df['category'].value_counts(dropna=True, sort=True)
print(value_counts)
value_counts.to_csv('category_value_counts.csv')

detector = gcld3.NNetLanguageIdentifier(min_num_bytes=0,max_num_bytes=1000)

count = 0
drop_index = []
length = len(df['id'].values)
for i in range(length):
  if df['category'][i] == 'Excluded':
    drop_index.append(i)
    continue
  sample = df['description'][i]
  result = detector.FindLanguage(text=sample)
  if result.language == 'en':
    count += 1
    print('Extension with ID:', df['id'][i], 'has description in English')
    print(result.language, result.is_reliable, result.proportion, result.probability)
    #writer.writerow([df['id'][i], df['category'][i], df['description'][i]])
  else:
    drop_index.append(i)
print('Success:', count)

from preprocess_nlp import preprocess_nlp
stages = {'remove_tags_nonascii': True,
      'lower_case':True,
      'expand_contractions':True,
      'remove_escape_chars':True,
      'remove_punctuation':True,
      'remove_stopwords':True,
      'remove_numbers':True,
      'lemmatize':False,
      'stemming':True,
      'min_word_len':2}
df_new = df.drop(drop_index)

df_new = df_new.reset_index(drop=True)
df_new.head()

processed_texts = preprocess_nlp(df_new['description'].tolist(), stages)
for i in range(len(df_stemmed['id'].values)):
  des = df_stemmed['description'][i]
  #print(des)
  desc = des.replace(' . ', ' ')
  df_stemmed.at[i, 'description'] = desc

df_stemmed.to_csv('firefox_fulllist_stemmed_2301.csv', index=False)
value_counts = df_stemmed['category'].value_counts(dropna=True, sort=True)
print(value_counts)
value_counts.to_csv('category_en_value_counts.csv')

#Calculate Similarity: split into different categories
category_list=[]
df = pd.read_csv('firefox_fulllist_stemmed_2301.csv')
df.dropna(inplace=True)
df.head()
df_sorted = df.sort_values(by = 'category')
df_sorted = df_sorted.reset_index(drop=True)
df_sorted.head()

value_counts = df_sorted['category'].value_counts(dropna=True, sort=True)
print(value_counts)
value_counts.to_csv('category_stemmed_value_counts.csv')

def create_new_csv(category):
  f = open('firefox_stemmed_'+category+'_2301.csv', 'w')
  return f

last_category = df_sorted['category'][0]
category_list.append(last_category)
#print(last_category)
f_csv = create_new_csv(last_category)
writer = csv.writer(f_csv, delimiter=',')
writer.writerow(['id', 'category', 'description'])
for i in range(len(df_sorted['id'].values)):
  category=df_sorted['category'][i]
  if category == last_category:
    writer.writerow([df_sorted['id'][i], df_sorted['category'][i], df_sorted['description'][i]])
  else:
    f_csv.close()
    category_list.append(category)
    f_csv = create_new_csv(category)
    writer = csv.writer(f_csv, delimiter=',')
    writer.writerow(['id', 'category', 'description'])
    writer.writerow([df_sorted['id'][i], df_sorted['category'][i], df_sorted['description'][i]])
  last_category=category
f_csv.close()

#Calculate Similarity: LDA model
from gensim.test.utils import common_texts
from gensim.corpora.dictionary import Dictionary
from gensim.models.ldamodel import LdaModel

def open_csv_per_category(category):
  df = pd.read_csv('firefox_stemmed_'+category+'_2301.csv')
  df.dropna(inplace=True)
  return df

def create_csv_per_category(category):
  f = open('firefox_counterparts_'+category+'_2301.csv', 'w')
  return f

def identify_counterparts(df, category):
  if df['category'].nunique() != 1:
    print('Error: firefox_stemmed_'+category+'_2301.csv has more than 1 category!!!')
    return

  texts = df['description'].tolist()
  common_texts = []
  for i in range(len(texts)):
    tokens = texts[i].split(' ')
    common_texts.append(tokens)
  
  common_dictionary = Dictionary(common_texts)
  common_corpus = [common_dictionary.doc2bow(text) for text in common_texts]
  lda = LdaModel(common_corpus, num_topics=30)

  saved_file = './model_'+category
  lda.save(saved_file)

  f = create_csv_per_category(category)
  writer = csv.writer(f, delimiter=',')
  writer.writerow(['id', 'category', 'counterparts'])

  num_exts = len(common_corpus)
  #print(num_exts)
  probability = [lda[corpus] for corpus in common_corpus]
  #print(probability)
  num_topics = 30
  vector = [[] for i in range(num_exts)]
  for i in range(num_exts):
    for j in range(num_topics):
      if len(probability[i]):
        topic_id, prob = probability[i][0]
        if topic_id == j:
          vector[i].append(prob)
          probability[i].pop(0)
        else:
          vector[i].append(0)
      else:
        vector[i].append(0)
  #print(vector)

  from numpy import dot
  from numpy.linalg import norm
  num_counterpart = 20
  List1 = np.array(vector)
  for i in range(num_exts):
    List2 = List1[i]
    id = df['id'][i]
    #print(List2)
    similarity_scores = List1.dot(List2)/ (np.linalg.norm(List1, axis=1) * np.linalg.norm(List2))
    similarity_scores[i] = 0
    #print(similarity_scores)
    index = np.argpartition(similarity_scores, -num_counterpart)[-num_counterpart:]
    counterparts = []
    for j in range(num_counterpart):
      ind = index[j]
      counterpart_id = df['id'][ind]
      similarity = similarity_scores[ind]
      counterpart = (counterpart_id, similarity)
      counterparts.append(counterpart)
    writer.writerow([id, category, counterparts])
  f.close()  

for category in category_list:
  df = open_csv_per_category(category)
  df.head()
  if len(df['id'].values) < 100:
    print(len(df['id'].values))
    continue
  else:
    identify_counterparts(df, category)