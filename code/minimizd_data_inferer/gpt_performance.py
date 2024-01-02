import os
import csv
import time
import pandas as pd
import numpy as np
from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score

def compare_res(cor_path,gpt_path):
    cor_df=pd.read_csv(cor_path)
    gpt_df=pd.read_csv(gpt_path)
    gpt_df.index=cor_df.index
    # print(cor_df)
    # print(gpt_df)
    gpt_df['corpus']=cor_df['label']
    # UPI,HI,FPI,AI,PCI,LI,WHI,UAI,WCI,DI,PS,FS
    gpt_df['gpt']=0
    gpt_df.loc[(gpt_df['UPI']==1) & (gpt_df['HI']!=1) & (gpt_df['FPI']!=1) & (gpt_df['AI']!=1) & (gpt_df['PCI']!=1) & (gpt_df['LI']!=1) & (gpt_df['WHI']!=1) & (gpt_df['UAI']!=1) & (gpt_df['WCI']!=1) & (gpt_df['DI']!=1) & (gpt_df['PS']!=1) & (gpt_df['FS']!=1) ,'gpt'] = 1
    gpt_df.loc[(gpt_df['UPI']!=1) & (gpt_df['HI']==1) & (gpt_df['FPI']!=1) & (gpt_df['AI']!=1) & (gpt_df['PCI']!=1) & (gpt_df['LI']!=1) & (gpt_df['WHI']!=1) & (gpt_df['UAI']!=1) & (gpt_df['WCI']!=1) & (gpt_df['DI']!=1) & (gpt_df['PS']!=1) & (gpt_df['FS']!=1) ,'gpt'] = 2
    gpt_df.loc[(gpt_df['UPI']!=1) & (gpt_df['HI']!=1) & (gpt_df['FPI']==1) & (gpt_df['AI']!=1) & (gpt_df['PCI']!=1) & (gpt_df['LI']!=1) & (gpt_df['WHI']!=1) & (gpt_df['UAI']!=1) & (gpt_df['WCI']!=1) & (gpt_df['DI']!=1) & (gpt_df['PS']!=1) & (gpt_df['FS']!=1) ,'gpt'] = 3
    gpt_df.loc[(gpt_df['UPI']!=1) & (gpt_df['HI']!=1) & (gpt_df['FPI']!=1) & (gpt_df['AI']==1) & (gpt_df['PCI']!=1) & (gpt_df['LI']!=1) & (gpt_df['WHI']!=1) & (gpt_df['UAI']!=1) & (gpt_df['WCI']!=1) & (gpt_df['DI']!=1) & (gpt_df['PS']!=1) & (gpt_df['FS']!=1) ,'gpt'] = 4
    gpt_df.loc[(gpt_df['UPI']!=1) & (gpt_df['HI']!=1) & (gpt_df['FPI']!=1) & (gpt_df['AI']!=1) & (gpt_df['PCI']==1) & (gpt_df['LI']!=1) & (gpt_df['WHI']!=1) & (gpt_df['UAI']!=1) & (gpt_df['WCI']!=1) & (gpt_df['DI']!=1) & (gpt_df['PS']!=1) & (gpt_df['FS']!=1) ,'gpt'] = 5
    gpt_df.loc[(gpt_df['UPI']!=1) & (gpt_df['HI']!=1) & (gpt_df['FPI']!=1) & (gpt_df['AI']!=1) & (gpt_df['PCI']!=1) & (gpt_df['LI']==1) & (gpt_df['WHI']!=1) & (gpt_df['UAI']!=1) & (gpt_df['WCI']!=1) & (gpt_df['DI']!=1) & (gpt_df['PS']!=1) & (gpt_df['FS']!=1) ,'gpt'] = 6
    gpt_df.loc[(gpt_df['UPI']!=1) & (gpt_df['HI']!=1) & (gpt_df['FPI']!=1) & (gpt_df['AI']!=1) & (gpt_df['PCI']!=1) & (gpt_df['LI']!=1) & (gpt_df['WHI']==1) & (gpt_df['UAI']!=1) & (gpt_df['WCI']!=1) & (gpt_df['DI']!=1) & (gpt_df['PS']!=1) & (gpt_df['FS']!=1) ,'gpt'] = 7
    gpt_df.loc[(gpt_df['UPI']!=1) & (gpt_df['HI']!=1) & (gpt_df['FPI']!=1) & (gpt_df['AI']!=1) & (gpt_df['PCI']!=1) & (gpt_df['LI']!=1) & (gpt_df['WHI']!=1) & (gpt_df['UAI']==1) & (gpt_df['WCI']!=1) & (gpt_df['DI']!=1) & (gpt_df['PS']!=1) & (gpt_df['FS']!=1) ,'gpt'] = 8
    gpt_df.loc[(gpt_df['UPI']!=1) & (gpt_df['HI']!=1) & (gpt_df['FPI']!=1) & (gpt_df['AI']!=1) & (gpt_df['PCI']!=1) & (gpt_df['LI']!=1) & (gpt_df['WHI']!=1) & (gpt_df['UAI']!=1) & (gpt_df['WCI']==1) & (gpt_df['DI']!=1) & (gpt_df['PS']!=1) & (gpt_df['FS']!=1) ,'gpt'] = 9
    gpt_df.loc[(gpt_df['UPI']!=1) & (gpt_df['HI']!=1) & (gpt_df['FPI']!=1) & (gpt_df['AI']!=1) & (gpt_df['PCI']!=1) & (gpt_df['LI']!=1) & (gpt_df['WHI']!=1) & (gpt_df['UAI']!=1) & (gpt_df['WCI']!=1) & (gpt_df['DI']==1) & (gpt_df['PS']!=1) & (gpt_df['FS']!=1) ,'gpt'] = 10
    gpt_df.loc[(gpt_df['UPI']!=1) & (gpt_df['HI']!=1) & (gpt_df['FPI']!=1) & (gpt_df['AI']!=1) & (gpt_df['PCI']!=1) & (gpt_df['LI']!=1) & (gpt_df['WHI']!=1) & (gpt_df['UAI']!=1) & (gpt_df['WCI']!=1) & (gpt_df['DI']!=1) & (gpt_df['PS']==1) & (gpt_df['FS']!=1) ,'gpt'] = 11
    gpt_df.loc[(gpt_df['UPI']!=1) & (gpt_df['HI']!=1) & (gpt_df['FPI']!=1) & (gpt_df['AI']!=1) & (gpt_df['PCI']!=1) & (gpt_df['LI']!=1) & (gpt_df['WHI']!=1) & (gpt_df['UAI']!=1) & (gpt_df['WCI']!=1) & (gpt_df['DI']!=1) & (gpt_df['PS']!=1) & (gpt_df['FS']==1) ,'gpt'] = 12
    # print(gpt_df)
    gpt_df['perf']=np.where(gpt_df['gpt']==gpt_df['corpus'],1,0)
    corr=gpt_df['perf'].sum()
    print(corr,corr/2421)

    f1=f1_score(gpt_df['corpus'], gpt_df['gpt'], average='weighted')
    acc=accuracy_score(gpt_df['corpus'], gpt_df['gpt'])
    pre=precision_score(gpt_df['corpus'], gpt_df['gpt'],average='weighted')
    recall=recall_score(gpt_df['corpus'], gpt_df['gpt'],average='weighted')
    print('f1',f1)
    print('acc',acc)
    print('pre',pre)
    print('recall',recall)
    
    

if __name__=='__main__':

    cor_path='./corpus.csv'
    gpt_path='./gpt_results_one_label_gpt4.csv'
    compare_res(cor_path,gpt_path)