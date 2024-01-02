import pandas as pd
import tqdm

def read_source_csv():
    chrome_api_f = 'table8-11_data/chrome/api_final_all.csv'
    chrome_desc_f='table8-11_data/chrome/desc_count_benchmark.csv'
    chrome_tag_f='table8-11_data/chrome/tag_final_all.csv'
    chrome_traffic_f='table8-11_data/chrome/traffic_final_all.csv'

    firefox_api_f='table8-11_data/firefox/api_final_all.csv'
    firefox_desc_f='table8-11_data/firefox/desc_count_benchmark.csv'
    firefox_tag_f='table8-11_data/firefox/tag_final_all.csv'
    firefox_traffic_f='table8-11_data/firefox/traffic_final_all.csv'

    chrome_api_pd = pd.read_csv(chrome_api_f)
    chrome_desc_pd = pd.read_csv(chrome_desc_f)
    chrome_tag_pd = pd.read_csv(chrome_tag_f)
    chrome_traffic_pd = pd.read_csv(chrome_traffic_f)

    firefox_api_pd = pd.read_csv(firefox_api_f)
    firefox_desc_pd = pd.read_csv(firefox_desc_f)
    firefox_tag_pd = pd.read_csv(firefox_tag_f)
    firefox_traffic_pd = pd.read_csv(firefox_traffic_f)

    chrome_api_pd=chrome_api_pd.fillna('')
    chrome_desc_pd=chrome_desc_pd.fillna('')
    chrome_tag_pd=chrome_tag_pd.fillna('')
    chrome_traffic_pd=chrome_traffic_pd.fillna('')

    firefox_api_pd=firefox_api_pd.fillna('')
    firefox_desc_pd=firefox_desc_pd.fillna('')
    firefox_tag_pd=firefox_tag_pd.fillna('')
    firefox_traffic_pd=firefox_traffic_pd.fillna('')

    return [chrome_api_pd,chrome_desc_pd,chrome_tag_pd,chrome_traffic_pd,firefox_api_pd,firefox_desc_pd,firefox_tag_pd,firefox_traffic_pd]

def count_data_types(data_pd,count_name):
    count_pd=data_pd.set_index('ext').astype(bool).sum(axis=1)
    print(count_name)
    print(count_pd.value_counts())

    return count_pd

def table12_num_of_data_types(chrome_api_pd,chrome_desc_pd,chrome_tag_pd,chrome_traffic_pd,firefox_api_pd,firefox_desc_pd,firefox_tag_pd,firefox_traffic_pd):
    count_data_types(chrome_api_pd,'chrome api')
    count_data_types(chrome_desc_pd,'chrome desc')
    count_data_types(chrome_tag_pd,'chrome tag')
    count_data_types(chrome_traffic_pd,'chrome traffic')

    count_data_types(firefox_api_pd,'firefox api')
    count_data_types(firefox_desc_pd,'firefox desc')
    count_data_types(firefox_tag_pd,'firefox tag')
    count_data_types(firefox_traffic_pd,'firefox traffic')

data_types = ['UPI', 'HI', 'FPI', 'AI', 'PCI',
                  'LI', 'WHI', 'UAI', 'WCI', 'DI', 'PS', 'FS']

def union(api_pd, tag_pd, traffic_pd):
    # for d_t in data_types:
    #     api_pd[d_t] = 0

    tag_pd = tag_pd.reset_index()
    traffic_pd = traffic_pd.reset_index()
    for index, row in tag_pd.iterrows():
        ext_name = row['ext']

        for dt in data_types:
            if row[dt] != 0:
                api_pd.loc[api_pd['ext'] == ext_name, dt] += row[dt]

    for index, row in traffic_pd.iterrows():
        ext_name = row['ext']

        for dt in data_types:
            if row[dt] != 0:
                api_pd.loc[api_pd['ext'] == ext_name, dt] += row[dt]

    # print("size of final result",len(api_pd))
    return api_pd

header=['ext','UPI', 'HI', 'FPI', 'AI', 'PCI',
              'LI', 'WHI', 'UAI', 'WCI', 'DI', 'PS', 'FS']
def check_compliance_by_types(desc_pd, union_pd):
    compliance_status=[]
    # ext data_type1 2 ... 12
    # compliance:0
    # over-claim compliance: 1
    # incompliance: -1

    for index, row in tqdm.tqdm(desc_pd.iterrows()):
        exi_id=row['ext']
        tmp=[exi_id]
        for dt in data_types:
            practice=union_pd.loc[union_pd['ext'] == exi_id][dt]
            if (practice>=1).bool():
                if row[dt]==1:
                    tmp.append(0)
                else:
                    tmp.append(-1)
            else:
                if row[dt]==1:
                    tmp.append(1)
                else:
                    tmp.append(0)
            # print(union_pd.loc[union_pd['ext'] == exi_id][dt]>=1)
        compliance_status.append(tmp)
        # print(index)

    icp=0
    fcp=0
    ocp=0
    for idx,item in enumerate(compliance_status):
        if -1 in item:
            # incompliance object
            icp+=1
        elif item[1:]==[0,0,0,0,0,0,0,0,0,0,0,0]:
            fcp+=1
        else:
            ocp+=1
    print('fcp',fcp)
    print('ocp',ocp)
    print('icp',icp)

    compliance_status=pd.DataFrame(compliance_status,columns=header)
    return compliance_status

def check_compliance_by_type_num(desc_pd, union_pd,comp_pd):
    compliance_status=[[0,0,0] for i in range(13)]

    # data_type_num compliance over-claim compliance incompliance
    # 0 ext_num
    # 1
    # ...
    # 12
    data_types_all_ext={}
    for index, row in tqdm.tqdm(union_pd.iterrows()):
        exi_id=row['ext']
        num=0
        for dt in data_types:
            if row[dt]>=1:
                num+=1
        data_types_all_ext[exi_id]=num
    
    for index, row in tqdm.tqdm(comp_pd.iterrows()):
        exi_id=row['ext']
        data_type_num=data_types_all_ext[exi_id]
        data_status=[row[d] for d in data_types]
        # print(data_status)
        if -1 in data_status:
            # incompliance
            compliance_status[data_type_num][2]+=1
        elif 1 in data_status:
            compliance_status[data_type_num][1]+=1
        else:
            compliance_status[data_type_num][0]+=1
    
    print('\n'.join(str(c) for c in compliance_status))

    return compliance_status

def count_compliance_table11(status_pd):
    for c in status_pd.columns:
        print ("---- %s ---" % c)
        print (status_pd[c].value_counts())

cat_list=['Accessibility','Blogging','DeveloperTools','Fun','News&Weather',
        'Photos','Productivity','SearchTools','Shopping',
        'Social&Communication','Sports','Tabs&Bookmarks','Extensions']

def collect_practice_by_type(union_pd,cat_pd):
    ext_category={}
    for index, row in tqdm.tqdm(cat_pd.iterrows()):
        exi_id=row['Extension']
        ext_category[exi_id]=row['Category'].replace(' ','')

    empty_data=[[0]*13 for i in range(13)]
    col_pr_count=pd.DataFrame(data=empty_data,columns=data_types+['total'],index=cat_list)
    for index, row in tqdm.tqdm(union_pd.iterrows()):
        ext_id=row['ext']
        if ext_id not in ext_category.keys():
            # print(ext_id)
            ext_cat='Extensions'
            continue
        else:
            ext_cat=ext_category[ext_id]
            col_pr_count.at[ext_cat,'total']+=1
        for d in data_types:
            if row[d]>0:
                col_pr_count.at[ext_cat,d]+=1
        
    # print(col_pr_count)
    col_pr_count.loc['total'] = col_pr_count.sum()
    print(col_pr_count)
    return col_pr_count

firefox_cat_list=['Alerts&Updates', 'Appearance','Bookmarks','DownloadManagement',
                'Feeds,News&Blogging','Games&Entertainment','LanguageSupport',
                'Photos,Music&Videos','Privacy&Security','SearchTools',
                'Shopping','Social&Communication', 'Tabs', 
                'WebDevelopment', 'Other']


import json
import ast
def collect_practice_by_type_firefox(union_pd,cat_pd):
    ext_category={}
    for index, row in tqdm.tqdm(cat_pd.iterrows()):
        exi_id=row['ext']
        tmp=str(row['cat'].replace(' ',''))
        # print(tmp)
        if len(tmp)>1:
            ext_category[exi_id]=ast.literal_eval(tmp)
        else:
            ext_category[exi_id]=[]

    empty_data=[[0]*13 for i in range(15)]
    col_pr_count=pd.DataFrame(data=empty_data,columns=data_types+['total'],index=firefox_cat_list)

    for index, row in tqdm.tqdm(union_pd.iterrows()):
        ext_id=row['ext']
        if ext_id not in ext_category.keys():
            ext_cat='Extensions'
            continue
        else:
            for catitem in ext_category[ext_id]:
                if catitem in firefox_cat_list:
                    col_pr_count.at[catitem,'total']+=1
                    for d in data_types:
                        if row[d]>0:
                            col_pr_count.at[catitem,d]+=1
                else:
                    print(catitem)

    # print(col_pr_count)
    col_pr_count.loc['total'] = col_pr_count.sum()
    print(col_pr_count)
    return col_pr_count

if __name__ == '__main__':
    [chrome_api_pd,chrome_desc_pd,chrome_tag_pd,chrome_traffic_pd,firefox_api_pd,firefox_desc_pd,firefox_tag_pd,firefox_traffic_pd]=read_source_csv()

    # union tables
    # chrome_union_pd=union(chrome_api_pd,chrome_tag_pd,chrome_traffic_pd)
    # chrome_union_pd.to_csv('table8-11_data/chrome/union_final_all.csv', index=False)
    chrome_union_pd = pd.read_csv('table8-11_data/chrome/union_final_all.csv')
    # firefox_union_pd=union(firefox_api_pd,firefox_tag_pd,firefox_traffic_pd)
    # firefox_union_pd.to_csv('table8-11_data/firefox/union_final_all.csv', index=False)
    firefox_union_pd = pd.read_csv('table8-11_data/firefox/union_final_all.csv')

    # # table 11
    # # chrome
    # compliance_status=check_compliance_by_types(chrome_desc_pd,chrome_union_pd)
    # compliance_status.to_csv('table8-11_data/chrome/compliance_status_v3.csv', index=False)
    # compliance_status=pd.read_csv('table8-11_data/chrome/compliance_status_v3.csv')
    # print(compliance_status)
    # count_compliance_table11(compliance_status)
    # print(compliance_status.value_counts())
    # # firefox
    # compliance_status=check_compliance_by_types(firefox_desc_pd,firefox_union_pd)
    # compliance_status.to_csv('table8-11_data/firefox/compliance_status_v3.csv', index=False)
    # compliance_status=pd.read_csv('table8-11_data/firefox/compliance_status_v3.csv')
    # print(compliance_status)
    # count_compliance_table11(compliance_status)
    # print(compliance_status.value_counts())

    # table 13
    # comp_pd=pd.read_csv('table8-11_data/chrome/compliance_status_v3.csv')
    # compliance_status=check_compliance_by_type_num(chrome_desc_pd,chrome_union_pd,comp_pd)
    # # firefox
    # comp_pd=pd.read_csv('table8-11_data/firefox/compliance_status_v3.csv')
    # compliance_status=check_compliance_by_type_num(firefox_desc_pd,firefox_union_pd,comp_pd)

    # # table 14
    # chrome_cat_file='extension_predictions/chrome_predictions.csv'
    # chrome_cat_pd=pd.read_csv(chrome_cat_file)
    # col_pr_count=collect_practice_by_type(chrome_union_pd,chrome_cat_pd)
    # col_pr_count.to_csv('table8-11_data/result/table_10_data_chrome.csv')
    # # firefox
    # firefox_cat_file='extension_predictions/firefox_with_cat.csv'
    # firefox_cat_pd=pd.read_csv(firefox_cat_file)
    # col_pr_count=collect_practice_by_type_firefox(firefox_union_pd,firefox_cat_pd)
    # col_pr_count.to_csv('table8-11_data/result/table_10_data_firefox.csv')

    ## Number of Data Types Collected
    # table12_num_of_data_types(chrome_api_pd,chrome_desc_pd,chrome_tag_pd,chrome_traffic_pd,firefox_api_pd,firefox_desc_pd,firefox_tag_pd,firefox_traffic_pd)