# get the TOP XX ext in each category
# revision for S&P submission
import json
import csv

def read_csv(file_path):
    res=[]
    with open(file_path, newline='') as csv_f:
        csv_reader=csv.reader(csv_f,delimiter=',')
        for row in csv_reader:
            res.append(row)
    return res

def save_csv(file_path,data):
    header=['cate','id','UPI','HI','FPI','AI','PCI','LI','WHI','UAI','WCI','DI','PS','FS']
    with open(file_path, 'w',newline='') as csv_f:
        csv_writer=csv.writer(csv_f,delimiter=',')
        csv_writer.writerow(header)
        csv_writer.writerows(data)

def get_top_ext(full_list,top_ext,cate_list):
    res_list=[]
    for cate in cate_list:
        res_map={}
        for ext in full_list:
            if ext['category']==cate:
                user_numbers=int(ext['user_numbers'].replace(',',''))
                ext_value=user_numbers*ext['rating']
                if res_map is None or len(res_map)<=top_ext:
                    res_map[ext['id']]=ext_value
                    continue
                # whether ext_value is greater than the smallest one in res_list
                min_ext=min(res_map,key=res_map.get)
                if ext_value>=res_map[min_ext]:
                    # replace the old one
                    res_map[ext['id']]=ext_value
                    res_map.pop(min_ext)
        res_tmp=list(res_map.keys())
        res_list.append(res_tmp)
    return res_list

def get_top_ext_firefox(full_list,top_ext,cate_list):
    res_list=[]
    for cate in cate_list:
        res_map={}
        for ext in full_list:
            ext_cat=ext['categories'].split(' -- ')[0]
            if ext_cat==cate:
                user_numbers=int(ext['user_numbers'].replace(',',''))
                ext_value=user_numbers*ext['rating']
                if res_map is None or len(res_map)<=top_ext:
                    res_map[ext['id']]=ext_value
                    continue
                # whether ext_value is greater than the smallest one in res_list
                min_ext=min(res_map,key=res_map.get)
                if ext_value>=res_map[min_ext]:
                    # replace the old one
                    res_map[ext['id']]=ext_value
                    res_map.pop(min_ext)
        res_tmp=list(res_map.keys())
        res_list.append(res_tmp)
    return res_list

def find_data_types(top_list,data_list,cate_list):
    res_list=[]
    for idx,top_item in enumerate(top_list):
        for ext in top_item:
            for i in data_list:
                # print(i)
                if i[0]==ext:
                    for ix in range(12):
                        if i[ix+1]!='0':
                            i[ix+1]='1'
                    res_list.append([cate_list[idx]]+i)
                    break
    return res_list

if __name__ == '__main__':
    # chrome
    # full_list_path='../construct_data_set/chrome_ext_fulllist_2022_Aug.json'
    # top_ext=100
    # cate_list=['Accessibility','Blogging','Developer Tools','Fun','News & Weather',
    #     'Photos','Productivity','Search Tools','Shopping',
    #     'Social & Communication','Sports','Tabs & Bookmarks','Extensions']
    # full_list=json.load(open(full_list_path,'r'))
    # top_list=get_top_ext(full_list,top_ext,cate_list)
    # print(top_list)
    # print(len(top_list))
    # desc_list_path='./table8-11_data/results/chrome/chrome_des_only_final.csv'
    # prac_list_path='./table8-11_data/results/chrome/practice_final_all.csv'
    
    # desc_top_list_path='./table8-11_data/results/chrome/desc_final_all_top.csv'
    # prac_top_list_path='./table8-11_data/results/chrome/practice_final_all_top.csv'

    # desc_data=read_csv(desc_list_path)
    # data_for_top_ext=find_data_types(top_list,desc_data,cate_list)
    # print(data_for_top_ext)
    # print(len(data_for_top_ext))
    # save_csv(desc_top_list_path,data_for_top_ext)

    # prac_data=read_csv(prac_list_path)
    # prac_for_top_ext=find_data_types(top_list,prac_data,cate_list)
    # print(prac_for_top_ext)
    # print(len(prac_for_top_ext))
    # save_csv(prac_top_list_path,prac_for_top_ext)

    #firefox
    full_list_path='table8-11_data/firefox/firefox_with_cat.json'
    top_ext=100
    cate_list=['Alerts & Updates', 'Appearance','Bookmarks','Download Management',
                'Feeds, News & Blogging','Games & Entertainment','Language Support',
                'Photos, Music & Videos','Privacy & Security','Search Tools',
                'Shopping','Social & Communication', 'Tabs', 
                'Web Development', 'Other']
    full_list=json.load(open(full_list_path,'r'))
    top_list=get_top_ext_firefox(full_list,top_ext,cate_list)
    print(top_list)
    print(len(top_list))
    # desc_list_path='./table8-11_data/results/firefox/chrome_des_only_final.csv'
    prac_list_path='./table8-11_data/results/firefox/practice_final_all.csv'
    
    # desc_top_list_path='./table8-11_data/results/firefox/desc_final_all_top.csv'
    prac_top_list_path='./table8-11_data/results/firefox/practice_final_all_top.csv'

    prac_data=read_csv(prac_list_path)
    prac_for_top_ext=find_data_types(top_list,prac_data,cate_list)
    print(prac_for_top_ext)
    print(len(prac_for_top_ext))
    save_csv(prac_top_list_path,prac_for_top_ext)