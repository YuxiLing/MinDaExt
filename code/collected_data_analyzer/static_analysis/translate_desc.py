import pandas as pd
import sys
import json
from tqdm import tqdm
import ast

def read_source_csv(chrome_f, firefox_f):
    chrome_list_f='./table8-11_data/chrome_ext_list.txt'
    firefox_list_f='./table8-11_data/firefox_ext_list.txt'
    with open(chrome_list_f,'r') as f:
        chrome_ext_list=f.readlines()
    chrome_ext_list=[ext.replace('\n','') for ext in chrome_ext_list]

    with open(firefox_list_f,'r') as f:
        firefox_ext_list=f.readlines()
    firefox_ext_list=[ext.replace('\n','') for ext in firefox_ext_list]

    chrome_pd = pd.read_csv(chrome_f)
    firefox_pd=pd.read_csv(firefox_f)

    chrome_pd=chrome_pd.fillna('')
    firefox_pd=firefox_pd.fillna('')

    chrome_drop_id=[]
    for index, row in chrome_pd.iterrows():
        if row['Extension'] not in chrome_ext_list:
            chrome_drop_id.append(index)
    # print(chrome_drop_id)
    chrome_pd.drop(chrome_drop_id,inplace=True)

    firefox_drop_id=[]
    for index, row in firefox_pd.iterrows():
        if row['Extension'] not in firefox_ext_list:
            firefox_drop_id.append(index)
    firefox_pd.drop(firefox_drop_id,inplace=True)

    return chrome_pd,firefox_pd

header=['ext','cat','UPI', 'HI', 'FPI', 'AI', 'PCI',
              'LI', 'WHI', 'UAI', 'WCI', 'DI', 'PS', 'FS']
def transfer_dp(data_pd):
    res=[]
    for index, row in data_pd.iterrows():
        tmp=[row['Extension'],row['Category'].replace(' ',''),0,0,0,0,0,0,0,0,0,0,0,0]
        if row['Labels']!='':
            # print(row['Labels'])
            labels=row['Labels'].split(',')
            for item in labels:
                tmp[int(item)]=1
        res.append(tmp)
    res=pd.DataFrame(res,columns=header)
    return res

header_firefox_cat=['ext','cat','UPI', 'HI', 'FPI', 'AI', 'PCI',
              'LI', 'WHI', 'UAI', 'WCI', 'DI', 'PS', 'FS']

def transfer_add_cat_dp(ext_full_list,data_pd):
    # create a map from ext to category
    ext_cat_mapper={}
    ext_list=json.load(open(ext_full_list,'r'))
    for item in tqdm(ext_list):
        cats=item['categories'].split(' -- ')
        ext_cat_mapper[item['id']]=cats

    res=[]
    empty_index=[]
    # leave empty if no category
    for index, row in tqdm(data_pd.iterrows()):
        ext_id=row['Extension']
        tmp=[ext_id,[],0,0,0,0,0,0,0,0,0,0,0,0]
        if ext_id in ext_cat_mapper.keys():
            tmp[1]=ext_cat_mapper[ext_id]
        else:
            empty_index.append(index)
        if row['Labels']!='':
            # print(row['Labels'])
            labels=row['Labels'].split(',')
            for item in labels:
                tmp[int(item)+1]=1
        res.append(tmp)
    res=pd.DataFrame(res,columns=header_firefox_cat)
    return res

firefox_cat_mapper={'Alerts & Updates':['UAI', 'WCI', 'PS'], 
                'Appearance':['UAI', 'WCI', 'PS'],
                'Bookmarks':['UAI', 'WCI', 'PS', 'WHI'],
                'Download Management':['UAI', 'WCI', 'FS', 'WHI'],
                'Feeds, News & Blogging':['UAI', 'WCI', 'AI', 'FS'],
                'Games & Entertainment':['UAI', 'WCI', 'PCI'], 
                'Language Support':['UAI', 'WCI'],
                'Photos, Music & Videos':['UAI', 'WCI', 'PCI', 'AI', 'PS', 'FS'],
                'Privacy & Security':['UAI', 'WCI', 'WHI', 'DI', 'PS', 'FS'],
                'Search Tools':['UAI', 'WCI', 'PS'],
                'Shopping':['UAI', 'WCI', 'UPI', 'FPI'],
                'Social & Communication':['UAI', 'WCI', 'PCI', 'AI', 'PS', 'FS'], 
                'Tabs':['UAI', 'WCI', 'PS'], 
                'Web Development':['UAI', 'WCI', 'WHI', 'DI', 'PS', 'FS'], 
                'Other':[]
                }

chrome_cat_mapper={'Accessibility':['UAI', 'WCI'], 
                'Blogging':['AI','FS','UAI', 'WCI'],
                'DeveloperTools':['UAI', 'WCI', 'PS', 'WHI'],
                'DownloadManagement':['UAI', 'WCI'],
                'Fun':['UAI', 'WCI', 'UPI'],
                'News&Weather':['UAI', 'WCI', 'LI'], 
                'Photos':['UAI', 'WCI','FS'],
                'Productivity':['UAI', 'WCI', 'UPI', 'AI', 'PS'],
                'SearchTools':['UAI', 'WCI', 'PS','AI'],
                'Shopping':['UAI', 'WCI', 'AI','LI','WHI','UPI', 'FPI'],
                'Social&Communication':['UAI', 'WCI', 'PCI', 'AI', 'UPI'], 
                'Sports':['UAI', 'WCI']
                }

chrome_cat_with_practice_mapper={'Accessibility':['UAI', 'WCI'], 
                'Blogging':['AI','FS','UAI', 'WCI','DI'],
                'DeveloperTools':['UAI', 'WCI', 'PS', 'WHI'],
                'DownloadManagement':['UAI', 'WCI'],
                'Fun':['UAI', 'WCI', 'UPI'],
                'News&Weather':['UAI', 'WCI', 'LI'], 
                'Photos':['UAI', 'WCI','FS'],
                'Productivity':['UAI', 'WCI', 'UPI', 'AI', 'PS'],
                'SearchTools':['UAI', 'WCI', 'PS','AI'],
                'Shopping':['UAI', 'WCI', 'AI','LI','WHI','UPI', 'FPI'],
                'Social&Communication':['UAI', 'WCI', 'PCI', 'AI', 'UPI'], 
                'Sports':['UAI', 'WCI']
                }

def chrome_add_desc_benchmark(cat_pd):
    for index, row in tqdm(cat_pd.iterrows()):
        ext_id=row['ext']
        # print(str(row['cat']))
        citem=row['cat']
        # print(cat_list)
        cat_full=[]
        if citem!='' and citem in chrome_cat_with_practice_mapper.keys():
            # print(citem)
            cat_full=list(chrome_cat_with_practice_mapper[citem])

        # print(cat_full)
        for cat in cat_full:
            if int(row[cat])==0:
                cat_pd.at[index,cat]=1
                # print('add a type')
    cat_pd.drop('cat', axis=1,inplace=True)
    return cat_pd

def firefox_add_desc_benchmark(cat_pd):
    for index, row in tqdm(cat_pd.iterrows()):
        ext_id=row['ext']
        # print(str(row['cat']))
        cat_list=ast.literal_eval(row['cat'])
        # print(cat_list)
        cat_full=[]
        for citem in cat_list:
            if citem!='' and citem in firefox_cat_mapper.keys():
                # print(citem)
                cat_full+=list(firefox_cat_mapper[citem])
        
        cat_full=list(set(cat_full))
        # print(cat_full)
        for cat in cat_full:
            if int(row[cat])==0:
                cat_pd.at[index,cat]=1
                # print('add a type')
    cat_pd.drop('cat', axis=1,inplace=True)
    return cat_pd


data_types = ['UPI', 'HI', 'FPI', 'AI', 'PCI',
              'LI', 'WHI', 'UAI', 'WCI', 'DI', 'PS', 'FS']

def reducer(api_pd):
    ext_count = dict()
    # initialize
    for dt in data_types:
        ext_count[dt] = 0

    api_pd = api_pd.reset_index()
    for index, row in api_pd.iterrows():
        for dt in data_types:
            # api_pd[dt]=api_pd[dt].astype(int)
            if row[dt] != 0:
                ext_count[dt] += 1
    return ext_count

def format_print(ext_count):
    for ext in ext_count:
        print(ext, ext_count[ext])

if __name__ == '__main__':
    # chrome_f = 'extension_predictions/chrome_pred_only.csv'
    # firefox_f='extension_predictions/firefox_predictions.csv'
    # chrome_pd,firefox_pd=read_source_csv(chrome_f,firefox_f)
    # chrome_res=transfer_dp(chrome_pd)
    # chrome_res.to_csv('./extension_predictions/chrome_pred_only_format.csv', index=False)

    # ext_full_list='table8-11_data/firefox/firefox_with_cat.json'
    # firefox_res=transfer_add_cat_dp(ext_full_list,firefox_pd)
    # firefox_res.to_csv('./extension_predictions/firefox_with_cat.csv', index=False)
    # firefox_with_cat_pd=pd.read_csv('./extension_predictions/firefox_with_cat.csv')
    # firefox_with_benchmark_pd=firefox_add_desc_benchmark(firefox_with_cat_pd)
    # firefox_with_benchmark_pd.to_csv('table8-11_data/firefox/desc_final_all.csv', index=False)

    chrome_with_cat_pd=pd.read_csv('./extension_predictions/chrome_pred_only_format.csv')
    chrome_with_benchmark_pd=chrome_add_desc_benchmark(chrome_with_cat_pd)
    chrome_with_benchmark_pd.to_csv('table8-11_data/chrome/desc_final_all_v2.csv', index=False)

    chrome_count=reducer(chrome_with_benchmark_pd)
    # firefox_res=pd.read_csv('table8-11_data/firefox/desc_final_all.csv')
    # firefox_count=reducer(firefox_res)

    print("chrome count")
    format_print(chrome_count)
    # print("firefox count")
    # format_print(firefox_count)