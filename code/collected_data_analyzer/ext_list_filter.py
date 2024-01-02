import json
import nltk
# nltk.download('punkt')
import csv
from tqdm import tqdm
import pandas as pd

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
    target_des_content=json.load(open(target_des_list,'r'))
    res=[['id','category','description']]
    count=0
    for item in tqdm(target_des_content):
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
        sentes_purify='.'.join(sent_text_purify)
        sent_tmp=tmp+[sent]
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

if __name__=='__main__':
    # input='./chrome_ext_fulllist_2022_Aug.json'
    # output='./chrome_ext_full_sentences_2022_Aug.json'

    # input='./sitemap_crawler/chrome_fulllist_Jan_2023.json'
    # output='./sitemap_crawler/chrome_fulllist_Jan_2023_formated.csv'

    # res=get_target_ext_list(input,output)
    # template_output='./tmp_descript_20_each_cate_detail.json'
    # res = json.load(open(output,'r'))
    # build_empty_description_list(input,res,template_output)

    # template_output='./chrome_ext_fulllist_2022_Aug.json'
    # csv_output='./chrome_ext_full_sentences_2022_Aug.csv'
    # convert_all_description_to_csv(input,output)

    # firefox_full_list='./firefox_ext_fulllist_2022_Aug.json'
    # csv_firefox_output='./firefox_ext_full_sentences_2022_Aug.csv'
    # cut_firefox_description_to_csv(firefox_full_list,csv_firefox_output)

    # output_file='./sitemap_crawler/chrome_fulllist_Jan_2023_new_category.json'
    # tmp_operate(input,output_file)

    # combine intro sentence for firefox
    input='firefox_ext_data_categories_2023.json'
    firefox_fulllist='firefox_ext_fulllist_cate_well_structured_intro_2023.json'

    # firefox_fullist_combing_intro(input,firefox_fulllist)

    firefox_modified_cate='firefox_fulllist_cate_well_structured_intro_2023_new_category.json'

    firefox_tmp_operate(firefox_fulllist,firefox_modified_cate)