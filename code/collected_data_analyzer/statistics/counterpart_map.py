import pandas as pd
from tqdm import tqdm

data_types = ['UPI', 'HI', 'FPI', 'AI', 'PCI',
                  'LI', 'WHI', 'UAI', 'WCI', 'DI', 'PS', 'FS','Total Finded']

def mapping(input_path,ext_practice,output_path,output2):
    count_df = pd.read_csv(input_path)
    prac_df=pd.read_csv(ext_practice)
    res=[]
    res_with_practice_data=[]
    prac_mapp={}
    for num,row in tqdm(prac_df.iterrows()):
        prac_mapp[row['ext']]=row[1:]
    
    count_total=0
    count_count_nonempty=0
    count_exist=0
    for num,row in tqdm(count_df.iterrows()):
        count_ext=eval(row['counterparts'])
        ext_id=row['id']
        category=row['category']
        data_collect=[0,0,0,0,0,0,0,0,0,0,0,0,0]
        count_total+=1
        for item in count_ext:
            counterpart_id=item[0]
            # counterpart_data_prac=prac_df.loc[prac_df['ext'] == counterpart_id]
            # if counterpart_data_prac.empty!=True:
                # for idx,i in enumerate(counterpart_data_prac):
                #     if str(i) !=str(0):
                #         data_collect[idx]+=1
            if counterpart_id in prac_mapp.keys():
                for idx,i in enumerate(prac_mapp[counterpart_id]):
                    if str(i) !=str(0):
                        data_collect[idx]+=1
                data_collect[-1]+=1
        if data_collect[-1]!=0:
            count_count_nonempty+=1    
        tmp=[ext_id,category]+data_collect
        res.append(tmp)
        if ext_id in prac_mapp.keys():
            count_exist+=1
            res_with_practice_data.append(tmp)
    res_df=pd.DataFrame(res,columns =['id','category']+data_types)
    res_df.to_csv(output_path,index=False)

    res_df=pd.DataFrame(res_with_practice_data,columns =['id','category']+data_types)
    res_df.to_csv(output2,index=False)

    print('total',count_total)
    print('non empty counterpar',count_count_nonempty)
    print("ext exists",count_exist)
    # result is res

def counterpart_to_benchmark(input_path, output_path):
    count_df=pd.read_csv(input_path)
    dtype_list=['UPI', 'HI', 'FPI', 'AI', 'PCI',
                  'LI', 'WHI', 'UAI', 'WCI', 'DI', 'PS', 'FS']
    for dtype in dtype_list:
        count_df[dtype] = count_df.apply(lambda x: 1 if x[dtype] >= x['Total Finded']*0.5 else 0, axis=1)
    count_df.drop(columns='Total Finded', axis=1)
    count_df.to_csv(output_path,index=False)

def combine_desc_with_counterpart(desc_input_path,count_input_path, output_path):
    desc_df=pd.read_csv(desc_input_path)
    count_df=pd.read_csv(count_input_path)
    desc_df = desc_df.reset_index()
    count_df = count_df.reset_index()

    dtype_list=['UPI', 'HI', 'FPI', 'AI', 'PCI',
                  'LI', 'WHI', 'UAI', 'WCI', 'DI', 'PS', 'FS']
    
    for index, row in tqdm(count_df.iterrows()):
        ext_name = row['ext']
        for dt in dtype_list:
            if row[dt] != 0:
                desc_df.loc[desc_df['ext'] == ext_name, dt] = 1
    
    desc_df.to_csv(output_path,index=False)    

    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print(desc_df.sum())


if __name__=='__main__':
    # from counterpart extension id to counterpart data type collections
    # categories=['Accessibility','Blogging','Developer Tools','Fun','News & Weather',
    #             'Photos','Productivity','Search Tools','Social & Communication',"Shopping",
    #             'Sports','Education','Lifestyle','Business']
    # frames=[]
    # for cat in categories:
    #     count_path='/Users/a057/Downloads/counterpart_new/counterpart_new/chrome_counterparts_%s_2301.csv' % cat
    #     df=pd.read_csv(count_path)
    #     frames.append(df)
    # df_all=pd.concat(frames)
    # df_all.to_csv('table8-11_data/results/chrome_counterpart/counterpart_ext.csv')

    # count_path='table8-11_data/results/chrome_counterpart/counterpart_ext.csv'
    # prac_path='table8-11_data/results/chrome/practice_final_all.csv'
    # output_path='table8-11_data/results/chrome_counterpart/counterpart_data_types.csv'
    # output2='table8-11_data/results/chrome_counterpart/counterpart_data_types_found_in_practice.csv'
    # mapping(count_path,prac_path,output_path,output2)

    # # from counterpart number to data type benchmark
    # counterpart_file='table8-11_data/results/chrome_counterpart/counterpart_data_types_found_in_practice.csv'
    # benchamrk_file='table8-11_data/results/chrome/desc_counterpart.csv'
    # counterpart_to_benchmark(counterpart_file,benchamrk_file)

    # combine counterpart with benchmark
    desc_path='extension_predictions/chrome_pred_only_format.csv'
    counterpart_path='table8-11_data/chrome/desc_counterpart.csv'
    final_benchmark_file='table8-11_data/chrome/desc_count_benchmark.csv'
    combine_desc_with_counterpart(desc_path, counterpart_path,final_benchmark_file)

    # # Firefox: from counterpart extension id to counterpart data type collections
    # firefox_cate=['Other','Bookmarks','Language Support','Privacy & Security','Shopping',
    #         'Download Management','Search Tools','Alerts & Updates',
    #         'Social & Communication','Photos, Music & Videos','Tabs','Appearance',
    #         'Games & Entertainment','Feeds, News & Blogging','Web Development']
    # frames=[]
    # for cat in firefox_cate:
    #     count_path='/Users/a057/Downloads/firefox_counterparts/counterparts/firefox_counterparts_%s_2301.csv' % cat
    #     df=pd.read_csv(count_path)
    #     frames.append(df)
    # df_all=pd.concat(frames)
    # df_all.to_csv('table8-11_data/results/firefox_counterpart/counterpart_ext.csv')

    # count_path='table8-11_data/results/firefox_counterpart/counterpart_ext.csv'
    # prac_path='table8-11_data/results/firefox/practice_final_all.csv'
    # output_path='table8-11_data/results/firefox_counterpart/counterpart_data_types.csv'
    # output2='table8-11_data/results/firefox_counterpart/counterpart_data_types_found_in_practice.csv'
    # mapping(count_path,prac_path,output_path,output2)

    # # Firefox: from counterpart number to data type benchmark
    # counterpart_file='table8-11_data/results/firefox_counterpart/counterpart_data_types_found_in_practice.csv'
    # benchamrk_file='table8-11_data/results/firefox/desc_counterpart.csv'
    # counterpart_to_benchmark(counterpart_file,benchamrk_file)

    # Firefox: combine counterpart with benchmark
    desc_path='table8-11_data/firefox/desc_final_all_without_cat.csv'
    counterpart_path='table8-11_data/firefox/desc_counterpart.csv'
    final_benchmark_file='table8-11_data/firefox/desc_count_benchmark.csv'
    combine_desc_with_counterpart(desc_path, counterpart_path,final_benchmark_file)