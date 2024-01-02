
import os
import json
import csv

csv_header=['ext','UPI','HI','FPI','AI','PCI','LI','WHI','UAI','WCI','DI','PS','FS']
keywords_map={
    'UPI':["name", "\"age\"", "birthday", "phone", "email", "address", "home address",
            "business address", "bill address", "building", "community",
            "city", "country", "postal code", "door number", "unit number", "street",
            "marriage", "marrital", "nationality", "race", "religion", "passport", "\"ic\""],
    'HI':["insurance", "diet", "weight", "height", "blood sugar",
            "blood pressure", "fitness", "symptom", "case", "medicine", "drug"],
    'FPI':["credit cards", "card number", "CVV", "security code", "expiry date",
            "expiration date", "bank", "SWIFT code", "IBAN number", "branch name",
            "payment", "financial", "money", "fund", "income", "expense", "receipt"],
    'AI':["username", "\"id\"", "account", "password", "pass word", "\"pwd\"", "otp",
            "seed phrases", "backup words", "mnemonics", "certificate", "key"],
    'PCI':["whatsapp", "telegram", "wechat", "facebook", "twitter", "linkin", "chat",
            "message", "communication", "conversation", "session", "dialogue",],
    'LI':["longitude", "latitude", "coordinate", "axis", "\"gps\"", 
            "location", "position", "geographic"],
    'WHI':["\"hostory\""],
    'UAI':[],
    'WCI':[],
    'DI':["\"ip\"", "\"mac\"", "ip_address", "mac_address", "device_id", "instance_id",
            "browser", "wifi password", "wifi", "memory", "cpu", "network", "storage"],
    'PS':["privacy", "notification", "history", "accessibility settings", "security"],
    'FS':["upload", "choose file", "select file", "local file", "import"]
}
data_types=['UPI','HI','FPI','AI','PCI','LI','WHI','UAI','WCI','DI','PS','FS']

def translate_txt(file_path):
    res=[]
    with open(file_path,'r') as f:
        content = f.readlines()
    content = [co.replace('\n','') for co in content]
    tmp={
        'id':'',
        'requests':[],
    }
    request_tmp={
        'method':'',
        'host':'',
        'url':'',
        'query':{},
        'form':{}
    }
    idx=0
    while idx<len(content):
        idxl=-1
        idxr=-1
        if len(content[idx])>=26 and content[idx][0:26]=='-----monitoring start-----':
            idxl=idx
            for idx2 in range(idx,len(content)):
                if len(content[idx2])>=24 and content[idx2][0:24]=='-----monitoring end-----':
                    idxr=idx2
                    break
        if idxl!=-1 and idxr!=-1:
            # extract flows for one extension
            id=content[idxl+1]
            tmp['id']=id
            for quid in range(idxl,idxr):
                if content[quid]=='——TIME——':
                    # save a query
                    request_tmp['method']=content[quid+3]
                    request_tmp['host']=content[quid+5]
                    request_tmp['url']=content[quid+7]
                    # extract query and form
                    has_query=False
                    query_end=quid+7
                    for idx_query in range(quid+7,idxr):
                        if content[idx_query]=='——QUERY STRING——':
                            has_query=True
                        elif content[idx_query]=='' or content[idx_query][0:2]=='——':
                            # reach the end
                            query_end=idx_query
                            has_query=False
                            break
                        elif has_query==True:
                            try:
                                [the_key,the_value]=content[idx_query].split(':',1)
                                # print("has query",the_key,the_value)
                                request_tmp['query'][the_key]=the_value
                            except:
                                # print("cannot handle query",content[idx_query])
                                pass

                    has_form=False
                    for idx_form in range(query_end,idxr):
                        if content[idx_form]=='——FORM——':
                            has_form=True
                        elif content[idx_form]=='' or content[idx_form][0:2]=='——':
                            # reach the end
                            has_form=False
                            break
                        elif has_form==True:
                            try:
                                [the_key,the_value]=content[idx_form].split(':',1)
                                print("has form",the_key,the_value)
                                request_tmp['form'][the_key]=the_value
                            except:
                                print("cannot handle form",content[idx_form])

                    tmp['requests'].append(request_tmp)
                    request_tmp={
                        'method':'',
                        'host':'',
                        'url':'',
                        'query':{},
                        'form':{}
                    }
            idx=idxr
            res.append(tmp)
            tmp={
                'id':'',
                'requests':[],
            }
        else:
            idx+=1
    return res        

def keywords_matching(inter_json_path,res_csv_path):
    inter_data=json.load(open(inter_json_path,'r'))
    res=[]
    for ext in inter_data:
        ext_id=ext["id"]
        tmp_req=[0,0,0,0,0,0,0,0,0,0,0,0]
        for idx, data_tp in enumerate(data_types):
            founded=False
            for keys in keywords_map[data_tp]:
                for req in ext["requests"]:
                    if keys.lower() in str(req["query"]).lower() or keys.lower() in str(req["form"]).lower():
                        if keys.lower() in str(req["query"]).lower():
                            print("find",keys,'at',req["query"])
                        else:
                            print("find",keys,'at',req["form"])
                        # print()
                        founded=True
                        break
            if founded==True:
                tmp_req[idx]+=1
        tmp_res=[ext_id]+tmp_req
        res.append(tmp_res)
            
    with open(res_csv_path,'w') as f:
        csv_f=csv.writer(f)
        csv_f.writerow(csv_header)
        csv_f.writerows(res)

if __name__=='__main__':
    traffic_file='./traffic_data/request_all_in_one_d-g.txt'
    traffic_constructed_file='./traffic_result/d-g_request.json'
    # content=translate_txt(traffic_file)
    # json.dump(content,open(traffic_constructed_file,'w'))

    inter_json_path='./traffic_result/d-g_request.json'
    res_csv_path='./traffic_result/d-g_request.csv'
    keywords_matching(inter_json_path,res_csv_path)