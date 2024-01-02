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


#Train a 2-step SVM classifier
np.random.seed(500)

Corpus = pd.read_csv("corpus.csv", encoding='utf-8')
Corpus.dropna(inplace=True)

Corpus.label.value_counts()

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

Corpus['text_final'] = Corpus['description'].map(text_preprocessing)
Corpus['text_final'] = Corpus['text_final'].str.replace('\d+', '')

skf = StratifiedKFold(n_splits=10, shuffle=True, random_state=123)

for train_idx, valid_idx in skf.split(Corpus['text_final'], Corpus["label"]):
  train = Corpus.iloc[train_idx]
  valid = Corpus.iloc[valid_idx]

# train data set
train_datas = train['text_final'].values
train_labels = train['label'].values
# test data set
test_datas = valid['text_final'].values
test_labels = valid['label'].values

def generate_binary(labels):
    new_labels = []
    for label in labels:
      if label > 0 and label < 13:
        new_labels.append(1)
      else:
        new_labels.append(label)
    return new_labels

def extract_samples(datas, labels):
    train_datas = []
    train_labels = []
    for i in range(len(labels)):
      if labels[i] == 0:
        continue
      else:
        train_labels.append(labels[i])
        train_datas.append(datas[i])
    return train_datas, train_labels

test_labels_binary = generate_binary(test_labels)
train_labels_binary = generate_binary(train_labels)

train_datas_multi, train_labels_multi = extract_samples(train_datas, train_labels)

Encoder_Bi = LabelEncoder()
Encoder_Bi.fit(train_labels_binary)
train_labels_binary = Encoder_Bi.transform(train_labels_binary)
Encoder = LabelEncoder()
Encoder.fit(train_labels)
train_labels = Encoder.transform(train_labels)

Tfidf_vect = TfidfVectorizer(max_features=5000)
Tfidf_vect.fit(Corpus['text_final'])

train_datas_Tfidf = Tfidf_vect.transform(train_datas)
train_datas_multi_Tfidf = Tfidf_vect.transform(train_datas_multi)

SVM_Bi = svm.SVC(C=1.0, kernel='linear', degree=3, gamma='auto')
SVM_Bi.fit(train_datas_Tfidf, train_labels_binary)
SVM_Mul = svm.SVC(C=1.0, kernel='linear', degree=3, gamma='auto')
SVM_Mul.fit(train_datas_multi_Tfidf, train_labels_multi)

# saving encoder to disk
filename = 'result/labelencoder_fitted_binary.pkl'
pickle.dump(Encoder_Bi, open(filename, 'wb'))
filename = 'result/labelencoder_fitted_multi.pkl'
pickle.dump(Encoder, open(filename, 'wb'))

# saving TFIDF Vectorizer to disk
filename = 'result/Tfidf_vect_fitted.pkl'
pickle.dump(Tfidf_vect, open(filename, 'wb'))

# saving the both models to disk
filename = 'result/svm_trained_model_binary.sav'
pickle.dump(SVM_Bi, open(filename, 'wb'))
filename = 'result/svm_trained_model_multi.sav'
pickle.dump(SVM_Mul, open(filename, 'wb'))

print("Files saved to disk!")

#Classification
if __name__=='__main__':
    all_pred_label = []
    all_target_label = []
    # Loading Label encoder
    labelencode_Bi = pickle.load(open('result/labelencoder_fitted_binary.pkl', 'rb'))
    labelencode = pickle.load(open('result/labelencoder_fitted_multi.pkl', 'rb'))

    # Loading TF-IDF Vectorizer
    Tfidf_vect = pickle.load(open('result/Tfidf_vect_fitted.pkl', 'rb'))

    # Loading models
    SVM_Bi = pickle.load(open('result/svm_trained_model_binary.sav', 'rb'))
    SVM_Multi = pickle.load(open('result/svm_trained_model_multi.sav', 'rb'))

    predictions_SVM=[]
    svm_pred_labels=[]
    svm_correct=0
    test_binary_labels = []
    target= test_labels_binary
    multi_target = test_labels
    classification_dataset = []
    classification_label = []
    valid = valid.reset_index(drop=True)
    for sentence in tqdm(valid['text_final']):
        sample_text_processed = sentence
        sample_text_processed_vectorized = Tfidf_vect.transform([sample_text_processed])

        prediction_SVM = SVM_Bi.predict(sample_text_processed_vectorized)
        target_label=target[valid.index[valid['text_final'] == sentence].tolist()[0]]
        multi_target_label=multi_target[valid.index[valid['text_final'] == sentence].tolist()[0]]
        svm_label=labelencode_Bi.inverse_transform(prediction_SVM)[0]
        svm_pred_labels.append(svm_label)
        if svm_label == target_label:
            svm_correct+=1
        if svm_label == 1:
          classification_dataset.append(sentence)
          classification_label.append(multi_target_label)
        else:
          all_pred_label.append(0)
          all_target_label.append(multi_target_label)

    print("SVM Accuracy Score (Binary) -> ", svm_correct/len(test_datas)*100)
    report =classification_report(test_labels_binary, svm_pred_labels, output_dict=True)
    df_report = pd.DataFrame(report).transpose()
    df_report.to_csv('report_svm.csv',index=True)

    print(len(classification_dataset), len(classification_label))
    classification_dataset = np.expand_dims(np.array(classification_dataset),axis=1)
    classification_label = np.expand_dims(np.array(classification_label, dtype=np.uint8), axis=1)

    dataset = np.concatenate((classification_dataset, classification_label), axis=1)
    df = pd.DataFrame(dataset, columns=['text_final', 'label'])
    df['label'] = df['label'].astype('int')

    # Loading models
    SVM = pickle.load(open('result/svm_trained_model_multi.sav', 'rb'))

    predictions_SVM=[]
    svm_pred_labels=[]
    svm_correct=0
    target=df['label']
    for sentence in tqdm(df['text_final']):
      sample_text_processed = sentence
      sample_text_processed_vectorized = Tfidf_vect.transform([sample_text_processed])

      prediction_SVM = SVM.predict(sample_text_processed_vectorized)
        
      target_label=target[df.index[df['text_final'] == sentence].tolist()[0]]

      svm_label=labelencode.inverse_transform(prediction_SVM)[0]
      svm_pred_labels.append(svm_label)
      if svm_label == target_label:
        svm_correct+=1
      all_pred_label.append(svm_label)
      all_target_label.append(target_label)

    print("SVM Accuracy Score (Multi) -> ", svm_correct/len(df['text_final'])*100)
    report =classification_report(df['label'], svm_pred_labels, output_dict=True)
    df_report = pd.DataFrame(report).transpose()
    df_report.to_csv('report_svm_multi.csv',index=True)

    print("SVM Accuracy Score (Final) -> ", accuracy_score(all_target_label, all_pred_label) * 100)
    print("SVM Classification Report (Final) -> \n",classification_report(all_target_label, all_pred_label))
    report =classification_report(all_target_label, all_pred_label, output_dict=True)
    df_report = pd.DataFrame(report).transpose()
    df_report.to_csv('report_svm_final.csv',index=True)
    
    '''
    num = 0
    for i in range(len(all_target_label)):
       print(all_pred_label[i], all_target_label[i])
       if (all_target_label[i] == all_pred_label[i]):
         num += 1
         print(num)
    print(len(all_target_label))
    '''