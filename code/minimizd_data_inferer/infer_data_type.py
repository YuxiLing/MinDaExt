import pandas as pd
import numpy as np
import re
import nltk
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.preprocessing import LabelEncoder
from collections import defaultdict
from nltk.corpus import wordnet as wn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import model_selection, naive_bayes, svm
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
import pickle
from sklearn.model_selection import StratifiedKFold
import csv

import ast
from tqdm import tqdm

np.random.seed(500)

tag_map = defaultdict(lambda: wn.NOUN)
tag_map['J'] = wn.ADJ
tag_map['V'] = wn.VERB
tag_map['R'] = wn.ADV

REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')

def text_preprocessing(text):
    text = text.lower()
    text = REPLACE_BY_SPACE_RE.sub(' ', text)
    text = BAD_SYMBOLS_RE.sub('', text)
    text = text.replace('x', '')

    text_words_list = word_tokenize(text)

    Final_words = []
    word_Lemmatized = WordNetLemmatizer()
    for word, tag in pos_tag(text_words_list):
        if word not in stopwords.words('english') and word.isalpha():
            word_Final = word_Lemmatized.lemmatize(word, tag_map[tag[0]])
            Final_words.append(word_Final)
    return str(Final_words)

infer_dataset = pd.read_csv('others.csv', encoding='utf-8')
infer_dataset.dropna(inplace=True)
infer_dataset.head()

f = open('description.csv', 'w')
writer = csv.writer(f, delimiter = ',')
writer.writerow(['extension', 'description', 'label'])
labelencode_Bi = pickle.load(open('result/labelencoder_fitted_binary.pkl', 'rb'))
labelencode = pickle.load(open('result/labelencoder_fitted_multi.pkl', 'rb'))

# Loading TF-IDF Vectorizer
Tfidf_vect = pickle.load(open('result/Tfidf_vect_fitted.pkl', 'rb'))

# Loading models
SVM_Bi = pickle.load(open('result/svm_trained_model_binary.sav', 'rb'))
SVM_Multi = pickle.load(open('result/svm_trained_model_multi.sav', 'rb'))

predictions_SVM=[]
svm_pred_labels=[]
index = 0
for sentence in tqdm(infer_dataset['description']): 
    sample_text_processed = text_preprocessing(sentence)
    sample_text_processed.replace('\d+', '')
    sample_text_processed_vectorized = Tfidf_vect.transform([sample_text_processed])
    #print(sample_text_processed_vectorized)
    prediction_SVM_Bi = SVM_Bi.predict(sample_text_processed_vectorized)
    svm_label=labelencode_Bi.inverse_transform(prediction_SVM_Bi)[0]
    svm_pre_labels = []
    if svm_label == 1:
        prediction_SVM = SVM_Multi.predict(sample_text_processed_vectorized)
        final_label = labelencode.inverse_transform(prediction_SVM)[0]
    else:
        final_label = 0
    #print(final_label)
    svm_pred_labels.append(final_label)
    writer.writerow([infer_dataset['extension'][index], sentence, final_label])
    index += 1