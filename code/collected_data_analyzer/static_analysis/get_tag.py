import os
import json
import csv
from bs4 import BeautifulSoup

count=0
register_count=0
def save_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f)

def check_registration(dirPath):
    extList = next(os.walk(dirPath))[1]
    for ext in extList:
        global count,register_count
        count+=1
        extPath = dirPath+'/'+ext
        extInfo = []
        register_list=[]
        for home, dirs, files in os.walk(extPath):
            for filename in files:
                if filename[-5:] == '.html':
                    try:
                        htmlInfo = { "file_name": filename, "user_input_tages": [] }
                        userInputTags=["form","input","button","textarea","select","option",
                                    "optgroup","fieldset","legend","datalist","output"]
                        with open(os.path.join(home, filename), 'r') as f:
                            tmp = f.read()
                            soup = BeautifulSoup(tmp, 'html.parser')
                        # handle the html, extract specific tags
                        # currently, we ignore the dynamic generated html tags
                        for inputTag in userInputTags:
                            # register0=soup.find(lambda tag:tag.name==inputTag and "LOGIN" in tag.text)
                            register1=soup.find_all(inputTag,string="register")
                            register2=soup.find_all(inputTag,string="Register")
                            register3=soup.find_all(inputTag,string="REGISTER")
                            register4=soup.find_all(inputTag,string="sign up")
                            register5=soup.find_all(inputTag,string="SignUp")
                            register6=soup.find_all(inputTag,string="SignUp")
                            register7=soup.find_all(inputTag,string="enroll")
                            register8=soup.find_all(inputTag,string="Enroll")
                            register9=soup.find_all(inputTag,string="login")
                            register10=soup.find_all(inputTag,string="Login")
                            register11=soup.find_all(inputTag,string="LOGIN")
                            register12=soup.find_all(inputTag,string="sign in")
                            register_list+=register1+register2+register3+register4+register5+ \
                                            register6+register7+register8+register9+register10+register11+register12

                    except Exception as e:
                        print(e)
                        print(count,'cannot handle file',filename)
        # has traversed all the html files in an extension    
        # extTagPath=dirPath+'/'+ext+"_userinput_tags.json"
        # save_json(extTagPath,extInfo)
        if len(register_list)!=0:
            print(count,"need to login",ext)
            register_count+=1
    print("final statistics, need login or register:",register_count,"/",count)

def traverFile(dirPath):
    extList = next(os.walk(dirPath))[1]
    for ext in extList:
        extPath = dirPath+'/'+ext
        extInfo = []

        for home, dirs, files in os.walk(extPath):
            for filename in files:
                if filename[-5:] == '.html':
                    try:
                        global count
                        count+=1
                        htmlInfo = { "file_name": filename, "user_input_tages": [] }
                        userInputTags=["form","input","button","textarea","select","option",
                                    "optgroup","fieldset","legend","datalist","output"]
                        with open(os.path.join(home, filename), 'r') as f:
                            tmp = f.read()
                            soup = BeautifulSoup(tmp, 'html.parser')
                        # handle the html, extract specific tags
                        # currently, we ignore the dynamic generated html tags
                        for inputTag in userInputTags:
                            collectTag=soup.find_all(inputTag)
                            for tagItem in collectTag:
                                tmpItem={"tag_name": inputTag, "class": tagItem.get('class'), "id": tagItem.get('id'),
                                        "text": tagItem.string, "placeholder":tagItem.get('placeholder'),"raw_html": str(tagItem)}
                                htmlInfo["user_input_tages"].append(tmpItem)
                        extInfo.append(htmlInfo)    
                    except Exception as e:
                        print(e)
                        print(count,'cannot handle file',filename)
        # has traversed all the html files in an extension    
        extTagPath=dirPath+'/'+ext+"_userinput_tags.json"
        save_json(extTagPath,extInfo)

if __name__ == "__main__":
    dirPath='../chrome_ext/pages'
    traverFile(dirPath)
    # check_registration(dirPath)
