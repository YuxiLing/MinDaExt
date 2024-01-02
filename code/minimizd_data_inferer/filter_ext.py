import json
import nltk
import csv
from tqdm import tqdm
import pandas as pd
from langdetect import detect
import shutil
from pathlib import Path

source_code_path='../sitemap_crawler/chrome_ext_source_code'
non_en_path='../sitemap_crawler/chrome_ext_non_en'
en_path='../sitemap_crawler/chrome_ext_en'

# target by category
# no longer use
def get_target_ext_list(input_file_path,output_file_path):
    input_list=json.load(open(input_file_path,'r'))
    categories=['Accessibility','Blogging','Developer Tools','Fun',
                'News & Weather','Photos','Productivity','Search Tools','Shopping',
                'Social & Communication','Sports']
    res={'full':{},'onlyId':{}}
    for cat in categories:
        count=0
        tmp=[]
        tmp_id=[]
        for ext in input_list:
            if ext['category']==cat:
                tmp.append(ext)
                tmp_id.append(ext['id'])
                count+=1
            if count>20:
                break
        res['full'][cat]=tmp
        res['onlyId'][cat]=tmp_id
    # save the ext list
    json.dump(res,open(output_file_path,'w'))
    return res

def build_empty_description_list(source_file,res,output_file_path):
    des_list=[]
    # tmp={"id":"","category":"","description":""}
    categories=['Accessibility','Blogging','Developer Tools','Fun',
                'News & Weather','Photos','Productivity','Search Tools','Shopping',
                'Social & Communication','Sports']
    all_ext_content=json.load(open(source_file,'r'))

    for cate in categories:
        for it in res['onlyId'][cate]:
            for ext in all_ext_content:
                intro=""
                if ext['id']==it:
                    # find the complete introduction
                    intro=ext['introduction']
                    break
            tmp={'id':it,'category':cate,'description':intro.encode("ascii", "ignore").decode()}
            des_list.append(tmp)
    # save the ext list
    json.dump(des_list,open(output_file_path,'w'))

def cut_description_to_csv(target_des_list,output_file):
    target_des_content=json.load(open(target_des_list,'r'))
    res=[]
    count=0
    for item in target_des_content:
        tmp=[item['id'],item['category']]
        # sent_text = nltk.sent_tokenize(item['description'])
        sent_text = nltk.sent_tokenize(item['introduction'])
        cut_list=[]
        for sent in sent_text:
            cut_sent=sent.splitlines()
            cut_list+=cut_sent
        sent_text_purify=[se.encode("ascii", "ignore").decode() for se in cut_list if len(se.encode("ascii", "ignore").decode())>15]
        # if len(sent_text)<5:
        #     print('explict ext',item['id'],item['category'])
        #     continue
        
        for sent in sent_text_purify:
            sent_tmp=tmp+[sent]
            res.append(sent_tmp)
        # count+=1
        # if count>10:
        #     break
    with open(output_file,'w') as f:
        csv_f=csv.writer(f)
        csv_f.writerows(res)

def convert_all_description_to_csv(target_des_list,output_file):
    nltk.download('punkt')
    target_des_content=json.load(open(target_des_list,'r'))
    res=[['id','description']]
    count=0
    for item in tqdm(target_des_content):
        tmp=[item['id']]
        # sent_text = nltk.sent_tokenize(item['description'])
        sent_text = nltk.sent_tokenize(item['introduction'])
        cut_list=[]
        for sent in sent_text:
            cut_sent=sent.splitlines()
            cut_list+=cut_sent
        sent_text_purify=[se.encode("ascii", "ignore").decode() for se in cut_list if len(se.encode("ascii", "ignore").decode())>15]
        # if len(sent_text)<5:
        #     print('explict ext',item['id'])
        #     continue
        sentes_purify='.'.join(sent_text_purify)
        sent_tmp=tmp+[sentes_purify]
        res.append(sent_tmp)
        # count+=1
        # if count>10:
        #     break
    with open(output_file,'w') as f:
        csv_f=csv.writer(f)
        csv_f.writerows(res)

def cut_firefox_description_to_csv(target_des_list,output_file):
    target_des_content=json.load(open(target_des_list,'r'))
    res=[['id','category','description']]
    count=0
    for item in target_des_content:
        format_id=item['id'].encode("ascii", "ignore").decode()
        if format_id!=item['id']:
            continue
        tmp=[item['id'],""]
        # sent_text = nltk.sent_tokenize(item['description'])
        sent_text_purify=[]
        for intro_part in item['introduction']:
            sent_text = nltk.sent_tokenize(intro_part.replace('\n',''))
            cut_list=[]
            for sent in sent_text:
                cut_sent=sent.splitlines()
                cut_list+=cut_sent
            sent_text_purify+=[se.encode("ascii", "ignore").decode() for se in cut_list if len(se.encode("ascii", "ignore").decode())>15]
        # if len(sent_text)<5:
        #     print('explict ext',item['id'],item['category'])
        #     continue
        
        for sent in sent_text_purify:
            sent_tmp=tmp+[sent]
            res.append(sent_tmp)
        # count+=1
        # if count>10:
        #     break
    with open(output_file,'w') as f:
        csv_f=csv.writer(f)
        csv_f.writerows(res)

def tmp_operate(file_path,output_path):
    df = pd.read_json(file_path)
    # with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    #     print(df['category'].value_counts().to_string)
    
    list_mapping=[
        ['Accessibility','Utilities','Board & Card','Admin & Management','Tabs & Bookmarks',
        'Bookmarks'],
        ['Blogging'],
        ['Developer Tools'],
        ['Fun','Puzzle & Brain','Games','Role-Playing & Strategy','Arcade & Action',
        'Entertainment','Sports Games','Astrology','Virtual Worlds'],
        ['News & Weather','News Reporting','Weather Forecasts','Social News'],
        ['Photos','Music & Radio','TV & Movies','Online Video','Books'],
        ['Productivity','Office Applications','Creative Tools','Task Management',
        'Foreign Languages','Calculators','Alarms & Clocks','Dictionaries',
        'Notepads'],
        ['Search Tools','Search & Browsing Tools'],
        ['Shopping','Sales & CRM'],
        ['Social & Communication','Social Networking','Chat & IM','Phone & SMS',
        'Email & Contacts'],
        ['Sports'],
        ['Education','Academic Resources','Teacher & Admin Tools'],
        ['Food & Health','Lifestyle','Travel','Family','Religion'],
        ['Business Tools','Marketing & Analytics','Accounting & Finance','Money','HR & Legal',
        'ERP & Logistics'],
        ['Extensions','Apps','Appearance','Themes']
    ]
    cate_name=['Accessibility','Blogging','Developer Tools','Fun','News & Weather',
                'Photos','Productivity','Search Tools','Shopping','Social & Communication',
                'Sports','Education','Lifestyle','Business','Excluded']
    # for num, row in tqdm(df.iterrows()):
    #     for idx, cate in enumerate(list_mapping):
    #         if row['category'] in cate:
    #             df.at[num,'category']=cate_name[idx]
    #             # row['category']=cate_name[idx]
    #             break
    for idx, cate_list in tqdm(enumerate(list_mapping)):
        condition = (df['category'].isin(cate_list))
        df.loc[condition, 'category'] = cate_name[idx]

    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(df['category'].value_counts().to_string) 
    df.to_json(output_path,orient='records')

def firefox_fullist_combing_intro(input_file,output_file):
    with open(input_file,'r') as f:
        firefox_data=json.load(f)
    for item in firefox_data:
        intro_list=item['introduction']
        intro_string=''
        for i in intro_list:
            if i != '\n':
                intro_string+=i
        item['introduction']=intro_string

        categories=item['categories']
        cate_list=categories.split(' -- ')
        item['categories']=cate_list
    with open(output_file,'w') as f:
        json.dump(firefox_data,f)

def firefox_tmp_operate(file_path,output_path):
    df = pd.read_json(file_path)

    firefox_cate=['Other','Bookmarks','Language Support','Privacy & Security','Shopping',
            'Download Management','Search Tools','Alerts & Updates',
            'Social & Communication','Photos, Music & Videos','Tabs','Appearance',
            'Games & Entertainment','Feeds, News & Blogging','Web Development','Lifestyle']

    # with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    #     print(df['categories'].value_counts().to_string)
    #     cate_list=df['categories'].explode().unique()
    #     print('\n'.join(cate_list))

    new_df = pd.DataFrame(columns=df.columns)
    for num, row in tqdm(df.iterrows()):
        cate_list=row['categories']
        for cat in cate_list:
            if cat in firefox_cate:
                row['categories']=cat
                new_df.loc[len(new_df.index)]=row
            elif cat=='Scenery':
                row['categories']='Appearance'
                new_df.loc[len(new_df.index)]=row
            elif cat=='Music' or cat=='Film and TV':
                row['categories']='Photos, Music & Videos'
                new_df.loc[len(new_df.index)]=row
            elif cat=='Fashion':
                row['categories']='Shopping'
                new_df.loc[len(new_df.index)]=row
            elif cat=='Websites':
                row['categories']='Web Development'
                new_df.loc[len(new_df.index)]=row
            elif cat=='Sports' or cat=='Nature' or cat=='Holiday' or cat=='Seasonal':
                row['categories']='Web Development'
                new_df.loc[len(new_df.index)]=row
    new_df.to_json(output_path,orient='records')

def get_firefox_id():
    file_path='firefox_ext_data_categories_2023.json'
    output_path='firefox_ext_id_list.txt'
    ext_list=[]
    id_list=[]
    with open(file_path,'r') as f:
        ext_list=json.load(f)
    for item in ext_list:
        id_list.append(item['key'])
    with open(output_path,'w') as f:
        for i in id_list:
            f.write(i+'\n')
    
def filter_non_english(ext_list):
    res_list=[]
    non_en_list=[]
    no_desc=[]
    count=0
    for ext in tqdm(ext_list):
        try:
            # Detect the language of the string
            if ext['introduction']!="":
                language = detect(ext['introduction'])
                # If the detected language is English, add it to the result list
                if language == 'en':
                    res_list.append(ext)
                    count+=1
                else:
                    non_en_list.append(ext)
                    # remove_code(ext['id'])
            else:
                no_desc.append(ext)
        except:
            print(ext['id'],ext['introduction'])
            non_en_list.append(ext)
            # remove_code(ext['id'])
    print("total number after filtering non english ext",count)
    print("en ext",len(res_list))
    print("non en ext", len(non_en_list))
    return res_list,non_en_list

def remove_code(id):
    old_path=source_code_path+'/'+id+'.crx'
    new_path=non_en_path+'/'+id+'.crx'
    try:
        shutil.move(old_path,new_path)
        # print('move the ext',id)
    except Exception as e:
        pass
        # exit()

def remove_no_source_code_ext(filtered_list):
    print('origin ext in en',len(filtered_list))
    res_list=[]
    for ext in tqdm(filtered_list):
        id=ext['id']
        ext_path=source_code_path+'/'+id+'.crx'
        ext_file=Path(ext_path)
        if ext_file.is_file():
            res_list.append(ext)
            old_path=ext_path
            new_path=en_path+'/'+id+'.crx'
            shutil.move(old_path,new_path)
    print('ext with source code',len(res_list))
    return res_list

if __name__=='__main__':

    

    # # Step 1: remove non-English extension
    # input='../sitemap_crawler/chrome_fulllist_Oct_2023.json'
    # output='../sitemap_crawler/chrome_fulllist_Oct_2023_non_en.json'
    # input_list = json.load(open(input,'r'))
    # res,non_en_list=filter_non_english(input_list)
    # json.dump(non_en_list, open(output,'w'))

    # # Step 2: remove no source code ext from full-list
    # en_list='../sitemap_crawler/chrome_fulllist_Oct_2023_en.json'
    # with_code='../sitemap_crawler/chrome_fulllist_Oct_2023_en_with_code.json'
    # filtered_list=json.load(open(en_list,'r'))
    # res_list=remove_no_source_code_ext(filtered_list)
    # json.dump(res_list, open(with_code,'w'))
    
    # # Step 3: category info
    # res=get_target_ext_list(input,output)
    # template_output='./tmp_descript_20_each_cate_detail.json'
    # res = json.load(open(output,'r'))
    # build_empty_description_list(input,res,template_output)

    # Step 4: get description in csv
    full_list='../sitemap_crawler/chrome_fulllist_Oct_2023_en_with_code.json'
    csv_output='./chrome_desc_Oct_2023.csv'
    convert_all_description_to_csv(full_list,csv_output)

    # Step 5: firefox, no longer use
    # firefox_full_list='./firefox_ext_fulllist_2022_Aug.json'
    # csv_firefox_output='./firefox_ext_full_sentences_2022_Aug.csv'
    # cut_firefox_description_to_csv(firefox_full_list,csv_firefox_output)

    # output_file='./sitemap_crawler/chrome_fulllist_Jan_2023_new_category.json'
    # tmp_operate(input,output_file)

    # combine intro sentence for firefox
    # input='firefox_ext_data_categories_2023.json'
    # firefox_fulllist='firefox_ext_fulllist_cate_well_structured_intro_2023.json'

    # # firefox_fullist_combing_intro(input,firefox_fulllist)

    # firefox_modified_cate='firefox_fulllist_cate_well_structured_intro_2023_new_category.json'

    # firefox_tmp_operate(firefox_fulllist,firefox_modified_cate)

    # get_firefox_id()