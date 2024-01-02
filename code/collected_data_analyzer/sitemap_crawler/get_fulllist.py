import json
import urllib.request
import xml.etree.ElementTree as ET
from tqdm import tqdm
import datetime
import requests
from queue import Queue
import threading


headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Length": "0",
        "Cache-Control": "no-cache",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
        # "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"
    }

def get_raw_list_from_url(theURL):
    res=urllib.request.urlopen(url=theURL)
    xml_tree=ET.fromstring(res.read())
    partial_url_list=[]
    for ele in xml_tree:
        url=ele[0].text
        partial_url_list.append(url)
    return partial_url_list

def get_full_list(partial_url_list_file_path,res_file_path,fail_log):
    url_list=json.load(open(partial_url_list_file_path,'r'))
    res_full_list=[]
    with open(res_file_path,'w') as f:
        f.write('')
    with open(fail_log,'w') as f:
        f.write('')
    for url_item in tqdm(url_list):
        try:
            res=urllib.request.urlopen(url=url_item)
            res_raw_tree=ET.fromstring(res.read())
        except:
            with open(fail_log,'a') as f:
                f.write(url_item)    
                f.write('\n')
            continue
        for item in res_raw_tree:
            # sub_list.append(item[0].text)
            with open(res_file_path,'a') as f:
                f.write(item[0].text)    
                f.write('\n')

    return res_full_list

def get_fail_ext_list(fail_path,res_file_path,full_list_path):
    with open(fail_path) as f:
        url_list=f.readlines()
    url_list=[r.replace('\n','') for r in url_list]
    sub_list=[]
    with open(res_file_path,'w') as f:
        f.write('')
    for url_item in tqdm(url_list):
        res=urllib.request.urlopen(url=url_item)
        res_raw_tree=ET.fromstring(res.read())
        for item in res_raw_tree:
            sub_list.append(item[0].text)
            with open(res_file_path,'a') as f:
                f.write(item[0].text)    
                f.write('\n')
    # combine all list together to a full list
    with open(full_list_path,'a') as f:
        f.writelines('\n'.join(sub_list))
    
def get_fulllist_from_url(full_list_url_path,full_list_content_path):
    fail_log='./get_detial_fail_log_step2.txt'
    with open(fail_log,'w') as f:
        f.write('')
    with open(full_list_url_path,'r') as f:
        url_list=f.readlines()
    url_list=[i.replace('\n','') for i in url_list]
    # unique_ids=[]
    # unique_keys=[]
    # for url_item in tqdm(url_list):
    #     item_list=url_item.split('/')
    #     key=item_list[5]
    #     id=item_list[6].split('?')[0]
        
    #     unique_ids.append(id)
    #     unique_keys.append(key)
    # uniques_ids=list(set(unique_ids))
    # unique_keys=set(unique_keys)
    # print(len(uniques_ids))
    # print(len(unique_keys))

    full_content=[]
    for id in tqdm(url_list):

        detail_url='https://chrome.google.com/webstore/ajax/detail?hl=en&gl=CN&pv=20210820&mce=atf%2Cpii%2Crtr%2Crlb%2Cgtc%2Chcn%2Csvp%2Cwtd%2Chap%2Cnma%2Cdpb%2Cutb%2Chbh%2Cebo%2Chqb%2Cifm%2Cndd%2Cntd%2Coiu%2Cuga%2Cc3d%2Cncr%2Chns%2Cctm%2Cac%2Chot%2Chsf%2Chfi%2Cdtp%2Cmac%2Cbga%2Cepb%2Cfcf%2Crai%2Crma%2Clrc%2Cspt%2Cirt%2Cscm%2Cibg%2Cder%2Cbgi%2Cbem%2Cdda%2Crae%2Cshr%2Cesl%2Cdha%2Chib%2Cdsq%2Cpot%2Cevt%2Chsp%2Cess&'+\
            'id=%s&container=CHROME&_reqid=7774014&rt=j' % id
        try:
            res=requests.post(detail_url,headers=headers)
            raw_detail=res.text
        except:
            open(fail_log,'a').write(id)
            open(fail_log,'a').write('\n')
            continue

        # raw_decoded = raw_detail.decode('utf-8', errors="ignore")
        removed=raw_detail.replace(')]}\'', '')
        detail_json=json.loads(removed)
        record_time=str(datetime.datetime.now())
        try:
            name=detail_json[0][1][1][0][1]
            rating=detail_json[0][1][1][0][12]
            user_number=detail_json[0][1][1][0][23]
            creator=detail_json[0][1][1][0][2]
            category=detail_json[0][1][1][0][10]
            first_half_intro=detail_json[0][1][1][0][6]
        except:
            open(fail_log,'a').write(id)
            open(fail_log,'a').write('\n')
            continue
        try:
            key=detail_json[0][1][1][0][61]
        except:
            key=''
        try:
            privacy_link = detail_json[0][1][1][35][2]
        except:
            privacy_link=''

        contact_email = detail_json[0][1][1][35][0]
        privacy_set = detail_json[0][1][1][39]
        
        last_updated=detail_json[0][1][1][33]
        
        last_half_intro=detail_json[0][1][1][1]
        
        tmp= {
            'platform': "chrome",
            'id': id,
            'key': key,
            'name': name,
            'rating': rating,
            'user_numbers': user_number,
            'creator': creator,
            'last_updated': last_updated,
            'record_time': record_time,
            'category':category,
            'introduction': first_half_intro+last_half_intro,
            'privacy': privacy_set,
            'privacy_link': privacy_link,
            'email': contact_email,
        }
        full_content.append(tmp)
        with open('./tmp_full_list.json','w') as f:
            json.dump(full_content,f)

    with open(full_list_content_path,'w') as f:
        json.dump(full_content,f)

class Crawler_thread(threading.Thread):
    def __init__(self,thread_id,id_queue,res_output,fail_log,finished_log):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.id_queue = id_queue
        self.file=res_output
        self.fail_log=fail_log
        self.finished_log=finished_log
    
    def run(self):
        while True:
            if self.id_queue.empty():
                break
            else:
                id=self.id_queue.get()
                detail_url='https://chrome.google.com/webstore/ajax/detail?hl=en&gl=CN&pv=20210820&mce=atf%2Cpii%2Crtr%2Crlb%2Cgtc%2Chcn%2Csvp%2Cwtd%2Chap%2Cnma%2Cdpb%2Cutb%2Chbh%2Cebo%2Chqb%2Cifm%2Cndd%2Cntd%2Coiu%2Cuga%2Cc3d%2Cncr%2Chns%2Cctm%2Cac%2Chot%2Chsf%2Chfi%2Cdtp%2Cmac%2Cbga%2Cepb%2Cfcf%2Crai%2Crma%2Clrc%2Cspt%2Cirt%2Cscm%2Cibg%2Cder%2Cbgi%2Cbem%2Cdda%2Crae%2Cshr%2Cesl%2Cdha%2Chib%2Cdsq%2Cpot%2Cevt%2Chsp%2Cess&'+\
                    'id=%s&container=CHROME&_reqid=7774014&rt=j' % id
                try:
                    res=requests.post(detail_url,headers=headers)
                    raw_detail=res.text
                    removed=raw_detail.replace(')]}\'', '')
                    detail_json=json.loads(removed)
                    record_time=str(datetime.datetime.now())
                    key=detail_json[0][1][1][0][61]
                    # key=''
                    privacy_link = detail_json[0][1][1][35][2]
                    contact_email = detail_json[0][1][1][35][0]
                    privacy_set = detail_json[0][1][1][39]
                    name=detail_json[0][1][1][0][1]
                    rating=detail_json[0][1][1][0][12]
                    user_number=detail_json[0][1][1][0][23]
                    creator=detail_json[0][1][1][0][2]
                    last_updated=detail_json[0][1][1][33]
                    first_half_intro=detail_json[0][1][1][0][6].replace('\n',' ')
                    last_half_intro=detail_json[0][1][1][1].replace('\n',' ')
                    category=detail_json[0][1][1][0][10]
                    
                except:
                    self.fail_log.write(id)
                    self.fail_log.write('\n')
                    continue
                tmp= {
                    'platform': "chrome",
                    'id': id,
                    'key': key,
                    'name': name,
                    'rating': rating,
                    'user_numbers': user_number,
                    'creator': creator,
                    'last_updated': last_updated,
                    'record_time': record_time,
                    'category':category,
                    'introduction': first_half_intro+last_half_intro,
                    'privacy': privacy_set,
                    'privacy_link': privacy_link,
                    'email': contact_email,
                }
                json.dump(tmp,fp=self.file)
                self.file.write(',\n')
                self.finished_log.write(id)
                self.finished_log.write('\n')

def start_multi_thread_crawler(full_list_url_path,full_list_content_path):
    fail_log_path='./get_detial_fail_log.txt'
    finished_log_path='./get_detail_finished_log.txt'
    
    with open(fail_log_path,'w') as f:
        f.write('')
    with open(finished_log_path,'w') as f:
        f.write('')
    with open(full_list_content_path,'w') as f:
        f.write('')
    with open(full_list_url_path,'r') as f:
        url_list=f.readlines()
    url_list=[i.replace('\n','') for i in url_list]
    unique_ids=[]
    for url_item in url_list:
        item_list=url_item.split('/')
        id=item_list[6].split('?')[0]
        
        unique_ids.append(id)
    uniques_ids=list(set(unique_ids))
    print(len(uniques_ids))
    
    res_output=open(full_list_content_path,'a')
    fail_log=open(fail_log_path,'a')
    finished_log=open(finished_log_path,'a')
    id_queue = Queue(len(uniques_ids))
    for id in tqdm(uniques_ids):
        id_queue.put(id)
    crawler_thread_list=[]
    for thread_id in range(50):
        tmp_intermediate_file='./intermediate_files/thread_%s.json' % thread_id
        tmp_res_output=open(tmp_intermediate_file,'a')
        tmp_res_output.write('[')
        thread=Crawler_thread(thread_id,id_queue,tmp_res_output,fail_log,finished_log)
        thread.start()
        crawler_thread_list.append(thread)

    while not id_queue.empty():
        pass
    for idx in range(50):
        tmp_intermediate_file='./intermediate_files/thread_%s.json' % idx
        tmp_res_output=open(tmp_intermediate_file,'a')
        tmp_res_output.write(']')

    for t in crawler_thread_list:
        t.join()

    res_output.close()

def combine_all_list(full_list_final_path):
    res=[]
    for idx in tqdm(range(50)):
        tmp_intermediate_file='./intermediate_files/thread_%s.json' % idx
        tmp_cont=json.load(open(tmp_intermediate_file,'r'))
        res+=tmp_cont
    print('number with detials: ',len(res))
    json.dump(res,open(full_list_final_path,'w'))

if __name__=='__main__':
    # step1: get partial list
    # sitemap_path='https://chrome.google.com/webstore/sitemap'
    # firefox_sitemap_path='https://addons.mozilla.org/sitemap.xml'
    # partial_url_list=get_raw_list_from_url(sitemap_path)
    # json.dump(partial_url_list,open('./partial_list_url.json','w'))

    # step2: get full list of extensions
    # partial_url_list_file_path='./partial_list_url.json'
    # res_file_path='./fulllist_url.txt'
    # fail_log='./fail_url.txt'
    # res_full_list=get_full_list(partial_url_list_file_path,res_file_path,fail_log)

    #step3: get failed list
    # fail_path='./fail_url.txt'
    # res_file_path='./supplement_list.txt'
    # full_list_path='./fulllist_url.txt'
    # get_fail_ext_list(fail_path,res_file_path,full_list_path)

    #step4: get meta info of full list
    # full_list_url_path='./fulllist_url.txt'
    # browser_type='chrome'
    # full_list_content_path='./%s_fulllist.json' % browser_type
    # start_multi_thread_crawler(full_list_url_path,full_list_content_path)

    #step5: get meta info for failed ext from the last step
    # failed_list_url_path='./get_detial_fail_log.txt'
    # browser_type='chrome'
    # full_list_content_path='./intermediate_files/thread_50.json'
    # get_fulllist_from_url(failed_list_url_path,full_list_content_path)

    #step5: combine all result
    full_list_final_path='./chrome_fulllist_Jan_2023.json'
    combine_all_list(full_list_final_path)