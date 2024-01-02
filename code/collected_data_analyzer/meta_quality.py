import pandas
import json
from pathlib import Path
from tqdm import tqdm
from langdetect import detect
import re
import matplotlib.pyplot as plt 
import math
from collections import Counter

source_code_path1='../sitemap_crawler/chrome_ext_source_code'
source_code_path2='../sitemap_crawler/chrome_ext_non_en'
source_code_path3='../sitemap_crawler/chrome_ext_en'

def count_policy(full_list):
    res_list=[]
    policy_dict=[]
    for item in tqdm(full_list):
        if item['privacy_link']!="":
            res_list.append(item)
            policy_dict.append(item['privacy_link'])
    print(len(res_list))

    policy_data=Counter(policy_dict)
    policy_data={k: v for k, v in sorted(policy_data.items(), key=lambda item: item[1],reverse=True)}
    print(len(policy_data.keys()))
    count=0
    repe_dict={"1":0,"2":0,"3":0,"4":0,"5":0,"6":0,"7":0,"8":0}
    for key,val in policy_data.items():
        if val==1:
            repe_dict['1']+=1
        elif val==2:
            repe_dict['2']+=1
        elif val<=5:
            repe_dict['3']+=1
        elif val<=10:
            repe_dict['4']+=1
        elif val<=20:
            repe_dict['5']+=1
        elif val<=50:
            repe_dict['6']+=1
        elif val<=100:
            repe_dict['7']+=1
        else:
            repe_dict['8']+=1
    print(repe_dict)

def get_ext_with_desc(full_list):
    res=[]
    for item in tqdm(full_list):
        if item['introduction']!="":
            res.append(item)
    return res

def get_ext_with_code(full_list):
    res=[]
    for ext in tqdm(full_list):
        id=ext['id']
        ext_path1=source_code_path1+'/'+id+'.crx'
        ext_path2=source_code_path2+'/'+id+'.crx'
        ext_path3=source_code_path3+'/'+id+'.crx'

        ext_file1=Path(ext_path1)
        ext_file2=Path(ext_path2)
        ext_file3=Path(ext_path3)

        if ext_file1.is_file() or ext_file2.is_file() or ext_file3.is_file():
            res.append(ext)
    return res

def count_desc(ext_with_code_desc):
    print('with code desc',len(ext_with_code_desc))
    res={}
    res['NA']=0
    words={}
    for ext in tqdm(ext_with_code_desc):
        try:
            language = detect(ext['introduction'])
            # If the detected language is English, add it to the result list
            if language in res.keys():
                res[language]+=1
            else:
                res[language]=1
        except:
            res['NA']+=1
    print(res)
    # {'NA': 20, 'en': 122886, 'ja': 3110, 'ru': 3360, 'vi': 3424, 'de': 1051, 'fr': 2177, 'zh-cn': 2774, 'bg': 1462, 'pt': 2474, 'pl': 497, 'ro': 148, 'es': 2036, 'nl': 445, 'it': 652, 'hu': 127, 'id': 245, 'no': 315, 'af': 57, 'cs': 198, 'tr': 955, 'ko': 1587, 'ar': 552, 'et': 131, 'hr': 91, 'da': 210, 'el': 72, 'th': 148, 'cy': 30, 'sv': 191, 'fi': 58, 'he': 236, 'fa': 85, 'ca': 113, 'so': 30, 'sk': 71, 'sl': 35, 'tl': 38, 'sq': 21, 'uk': 121, 'lt': 42, 'ur': 1, 'hi': 15, 'zh-tw': 65, 'ml': 2, 'sw': 18, 'bn': 3, 'mk': 12, 'lv': 15, 'ta': 5, 'mr': 1}

def handle_desc_lang():
    dist={'NA': 20, 'en': 122886, 'ja': 3110, 'ru': 3360, 'vi': 3424, 'de': 1051, 'fr': 2177, 'zh': 2774, 'bg': 1462, 'pt': 2474, 'pl': 497, 'ro': 148, 'es': 2036, 'nl': 445, 'it': 652, 'hu': 127, 'id': 245, 'no': 315, 'af': 57, 'cs': 198, 'tr': 955, 'ko': 1587, 'ar': 552, 'et': 131, 'hr': 91, 'da': 210, 'el': 72, 'th': 148, 'cy': 30, 'sv': 191, 'fi': 58, 'he': 236, 'fa': 85, 'ca': 113, 'so': 30, 'sk': 71, 'sl': 35, 'tl': 38, 'sq': 21, 'uk': 121, 'lt': 42, 'ur': 1, 'hi': 15, 'tw': 65, 'ml': 2, 'sw': 18, 'bn': 3, 'mk': 12, 'lv': 15, 'ta': 5, 'mr': 1}
    # data={k: math.log10(v) for k, v in sorted(dist.items(), key=lambda item: item[1],reverse=True)}
    data={k: v for k, v in sorted(dist.items(), key=lambda item: item[1],reverse=True)}
    courses = list(data.keys())
    values = list(data.values())
    
    fig = plt.figure(figsize = (13, 4))
    
    # creating the bar plot
    plt.bar(courses, values, color ='maroon', 
            width = 0.5)
    
    plt.xlabel("Language types")
    plt.ylabel("No. of extensions / log10 ")
    plt.savefig('./desc_lan.png')

def count_desc_len(ext_with_code_desc):
    res_dict={"1":0,"2":0,"3":0,"4":0,"5":0}
    for ext in tqdm(ext_with_code_desc):
        res = len(re.findall(r'\w+', ext["introduction"]))
        if res<=10:
            res_dict['1']+=1
        elif res<=50:
            res_dict['2']+=1
        elif res<=100:
            res_dict['3']+=1
        elif res<=200:
            res_dict['4']+=1
        else:
            res_dict['5']+=1
    print(res_dict)

if __name__=='__main__':
    # Step 1
    full_list_path='../sitemap_crawler/chrome_fulllist_Oct_2023.json'
    # non_en_path='../sitemap_crawler/chrome_fulllist_Oct_2023_non_en.json'
    
    full_list=json.load(open(full_list_path,'r'))
    ext_with_code=get_ext_with_code(full_list)

    # Step 2: description
    # ext_with_code_desc=get_ext_with_desc(ext_with_code)
    # count_desc_len(ext_with_code_desc)
    # count_desc(ext_with_code_desc)

    count_policy(ext_with_code)

    # Step 2: plot
    # handle_desc_lang()