import json
import csv

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

if __name__=='__main__':
    pass