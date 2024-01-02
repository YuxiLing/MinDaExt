import json
import csv
import pandas as pd
import re

#pattern = r' ([A-Za-z\-]+)="(?:(?:(?!(?<!\\)").)*)"'
pattern1 = r' ([A-Za-z\-]+)="(.*?)"'
pattern2 = r' ([A-Za-z\-]+)=""(.*?)""'


csv_header=['ext','UPI','HI','FPI','AI','PCI','LI','WHI','UAI','WCI','DI','PS','FS']
keywords_map={
    'UPI':["name", "age", "birthday", "phone", "email", "address", "home address",
            "business address", "bill address", "building", "community",
            "city", "country", "postal code", "door number", "unit number", "street",
            "marriage", "marrital", "nationality", "race", "religion", "passport", "IC"],
    'HI':["insurance", "diet", "weight", "height", "blood sugar",
            "blood pressure", "fitness", "symptom", "case", "medicine", "drug"],
    'FPI':["credit cards", "card number", "CVV", "security code", "expiry date",
            "expiration date", "bank", "SWIFT code", "IBAN number", "branch name",
            "payment", "financial", "money", "fund", "income", "expense", "receipt"],
    'AI':["username", "id", "account", "password", "pass word", "pwd", "otp",
            "seed phrases", "backup words", "mnemonics", "certificate", "key"],
    'PCI':["whatsapp", "telegram", "wechat", "facebook", "twitter", "linkin", "chat",
            "message", "communication", "conversation", "session", "dialogue",],
    'LI':["longitude", "latitude", "coordinate", "axis", "gps", 
            "location", "position", "geographic"],
    'WHI':[],
    'UAI':[],
    'WCI':[],
    'DI':["ip", "mac", "ip address", "mac address", "device id", "instance id",
            "browser", "wifi password", "wifi", "memory", "cpu", "network", "storage"],
    'PS':["privacy", "notification", "history", "accessibility settings", "security"],
    'FS':["upload", "choose file", "select file", "local file", "import"]
}
data_types=['UPI','HI','FPI','AI','PCI','LI','WHI','UAI','WCI','DI','PS','FS']

def save_csv(res_csv_path,res):
    with open(res_csv_path,'w') as f:
        csv_f=csv.writer(f)
        csv_f.writerow(csv_header)
        csv_f.writerows(res)
        
def lower_word(word):
    return word.lower()

def add_head_tail_whitespace(word):
    return ' ' + word + ' ' 

def match_keyword(val):
    for key in keywords_map:
        for potential in keywords_map[key]:
            if lower_word(val) == lower_word(potential) or add_head_tail_whitespace(potential) in add_head_tail_whitespace(val):
                return True, key
    return False, ''
            
            
def read_csv(csv_path):
    data = pd.read_csv(csv_path)
    return data

def detect_row(column):
    count_num = {
        'UPI': 0,
        'HI': 0,
        'FPI': 0,
        'AI': 0,
        'PCI': 0,
        'LI': 0,
        'WHI': 0,
        'UAI': 0,
        'WCI': 0,
        'DI': 0,
        'PS': 0,
        'FS': 0,
        
    }
    matched1 = re.findall(pattern1, str(column))
    matched2 = re.findall(pattern2, str(column))
    
    matched1.extend(matched2)
    
    for m in matched1:
        val = m[1]
        f, potential =  match_keyword(val)
        if f:
            #print('matched',potential, val, m)
            count_num[potential] += 1
    return count_num

info_cl = [
    'UPI',
    'HI',
    'FPI',
    'AI',
    'PCI',
    'LI',
    'WHI',
    'UAI',
    'WCI',
    'DI',
    'PS',
    'FS',
]

global_count_num = dict()

def merge(ext_id, count_num):
    if ext_id not in global_count_num:
        global_count_num[ext_id] = [0,0,0,0,0,0,0,0,0,0,0,0]
    for index,cl in enumerate(info_cl):
        global_count_num[ext_id][index] += count_num[cl]      
        
        
def format_print():
    for key in global_count_num:
        count = [str(x) for x in global_count_num[key]]
        
        print(key + ',' + ','.join(count))
        
def save_in_csv(csv_path):
    res_data=[]
    for key in global_count_num:
        count = [str(x) for x in global_count_num[key]]
        tmp=[key]+count
        res_data.append(tmp)
    save_csv(csv_path,res_data)

if __name__=='__main__':
    dynamic_path = 'dynamic_input_tag_conclude_chrome_d-g.csv'
    csv_path='./input_tag_d-g.csv'
    #dynamic_path = 'small.csv'
    df = pd.read_csv(dynamic_path)
    df = df.reset_index(csv_path)
    
    for index, row in df.iterrows(): 
        count_num = detect_row(row['raw_html'])
        merge(row['ext'], count_num)
    print(','.join(csv_header))
    format_print()
    save_in_csv()
    pass
    