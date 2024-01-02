import os
import json
import csv
from bs4 import BeautifulSoup

count=0
def save_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f)

def traverFile(dirPath):
    extList = next(os.walk(dirPath))[1]
    classifications = dict()
    for num, ext in enumerate(extList):
        # if num > 2000:
        #     break
        extPath = dirPath+'/'+ext
        extInfo = []
        classification = []
        for home, dirs, files in os.walk(extPath):
            fileSizeList = []
            for filename in files:
                filePath = extPath + '/' + filename
                size = os.path.getsize(filePath)
                fileSizeList.append([filename, size])
            fileSizeList = sorted(fileSizeList, key=lambda i: i[1])
            
            pointer = 0
            for i in range(len(fileSizeList)):
                fileSize = fileSizeList[i]
                if len(classification) <= pointer:
                    classification.append([])
                classification[pointer].append(fileSize[0])

                if i < len(fileSizeList) - 1 and fileSizeList[i + 1][1] - fileSize[1] >= 1024:
                    pointer += 1
        classification = sorted(classification, key=lambda i: -1 * len(i))
        classificationDict = dict()
        for i, group in enumerate(classification):
            classificationDict[i + 1] = group
        classifications[ext] = classificationDict

    save_json('result_with_help.json', classifications)
        #         if filename[-5:] == '.html':
        #             try:
        #                 global count
        #                 count+=1
        #                 htmlInfo = { "file_name": filename, "user_input_tages": [] }
        #                 userInputTags=["form","input","button","textarea","select","option",
        #                             "optgroup","fieldset","legend","datalist","output"]
        #                 with open(os.path.join(home, filename), 'r') as f:
        #                     tmp = f.read()
        #                     soup = BeautifulSoup(tmp, 'html.parser')
        #                 # handle the html, extract specific tags
        #                 # currently, we ignore the dynamic generated html tags
        #                 for inputTag in userInputTags:
        #                     collectTag=soup.find_all(inputTag)
        #                     for tagItem in collectTag:
        #                         tmpItem={"tag_name": inputTag, "class": tagItem.get('class'), "id": tagItem.get('id'),
        #                                 "text": tagItem.string, "placeholder":tagItem.get('placeholder'),"raw_html": str(tagItem)}
        #                         htmlInfo["user_input_tages"].append(tmpItem)
        #                 extInfo.append(htmlInfo)    
        #             except Exception as e:
        #                 print(e)
        #                 print(count,'cannot handle file',filename)

        # # has traversed all the html files in an extension    
        # # extTagPath=dirPath+'/'+ext+"_userinput_tags.json"
        # # save_json(extTagPath,extInfo)

def count_pages_each_ext(dirPath):
    extList = next(os.walk(dirPath))[1]
    classifications = dict()
    page1=0
    page2_5=0
    page6_10=0
    page_11_more=0

    for num, ext in enumerate(extList):
        # if num > 2000:
        #     break
        extPath = dirPath+'/'+ext
        num_pages=len(os.listdir(extPath))
        if num_pages==1:
            page1+=1
        if num_pages>=2 and num_pages<=5:
            page2_5+=1
        if num_pages>=6 and num_pages<=10:
            page6_10+=1
        if num_pages>=11:
            page_11_more+=1
    print(page1,page2_5,page6_10,page_11_more)
def check_registration(page_folder_path):
    
    register_list=[]
    for home, dirs, files in os.walk(page_folder_path):
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

    if len(register_list)!=0:
        return 1
    return 0

# data = {'ext_id': 
#             {
#             'compliance': 0/1,   
#             'ui_pages': 0/1/2/3/4,
#             'login':0/1,
#             'downloads':0-10000,
#             'rating':0.0,
#             'desc_len':0,
#             'ext_size':1}
#         }
def count_pages_each_ext_to_json(dirPath,suffix):
    extList = next(os.walk(dirPath+'/zip'))[1]
    res_data={}
    for num, ext in enumerate(extList):
        file_size=os.path.getsize(dirPath+'/zip/'+ext+'.'+suffix)/1000 # ***KB
        res_data[ext]={'ui_pages':0,'ext_size':file_size,'login':0}
        extPath = dirPath+'/pages/'+ext
        if os.path.exists(extPath):
            login=check_registration(extPath)
            res_data[ext]['login']=1
            num_pages=len(os.listdir(extPath))
            if num_pages==1:
                res_data[ext]['ui_pages']=1
            if num_pages>=2 and num_pages<=5:
                res_data[ext]['ui_pages']=2
            if num_pages>=6 and num_pages<=10:
                res_data[ext]['ui_pages']=3
            if num_pages>=11:
                res_data[ext]['ui_pages']=4

    return res_data

def stat_pages():
    content=json.load(open('result_with_help.json','r'))
    count = 0
    third_count=0
    for c in content.keys():
        if "2" not in content[c]:
            count += 1
        else:
            # has more than one layer of UI
            idx=2
            while str(idx) in content[c]:
                clickableTags=["button"]
                find_third=False
                home='chrome_data/dynamic_pages_further_process/'+c
                for page in content[c][str(idx)]:
                    with open(os.path.join(home, page), 'r') as f:
                        tmp = f.read()
                        soup = BeautifulSoup(tmp, 'html.parser')
                    # handle the html, extract specific tags
                    # currently, we ignore the dynamic generated html tags
                    
                    collectTag=soup.find_all("button")
                    if len(collectTag)>2:
                        # there is a next page
                        find_third=True
                        break
                if find_third:
                    third_count+=1
                    print('find a thrid in',c)
                    break
                idx+=1

    print(count)
    print(len(content.keys()))
    print(third_count)

if __name__ == "__main__":
    # dirPath='./chrome_data/dynamic_pages_further_process'
    # traverFile(dirPath)
    # stat_pages()
    # count_pages_each_ext(dirPath)
    dirPath='../chrome_ext'
    res_data=count_pages_each_ext_to_json(dirPath)
    json.dump(res_data,open('./dynamic_meta_info.json','w'))
