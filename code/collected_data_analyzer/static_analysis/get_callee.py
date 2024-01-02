import os
import json
import csv
'''
input: result of get_all_function.mjs 
output: csv file
'''
privacy_chrome_api_1layer = ["accessibilityFeatures", "browsingData", "commands",
                             "contentSettings", "cookies", "declarativeNetRequest",
                             "desktopCapture", "devtools",
                             "enterprise", "fileBrowserHandler", "history",
                             "identity", "instanceID", "permissions", "platformKeys","power", "privacy", "proxy", "runtime",
                             "scripting", "storage", "sessions","system",
                             "tabGroups","tab","tabs","wallpaper","webRequest","windows"]
privacy_ext_api_1layer=["action","bookmarks","browserSettings","browsingData","captivePortal","commands","cookies","devtools",
                        "event","extension","find","history","identity","management"]
privacy_chrome_api_devtools = ["inspectedWindow", "network", "panels"]
privacy_chrome_api_enterprise = [
    "deviceAttributes", "hardwarePlatform", "networkingAttributes"]

dom_tree_get_api=["getElementsById","getElementsByTagName","getElementsByClassName","body","documentElement","forms"]
dom_tree_creation_api=["createElement","removeChild","appendChild","replaceChild","write"]

def save_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f)

def traverseAllCalleeFile(dir_path):
    ext_list=next(os.walk(dir_path))[1]
    for ext in ext_list:
        ext_path=dir_path+'/'+ext
        ext_info={
            "privacy_related_api":0,
            "privacy_related_callee_times":0,
            "privacy_unrelated_callee_times":0,
            "call":[]
        }

        for home, dirs, files in os.walk(ext_path):
            for filename in files:
                if filename[-9:] == '_api.json':
                    try:
                        with open(os.path.join(home, filename), 'r') as f:
                            funcs = json.load(f)
                        for func in funcs:
                            func_names = func["name"].split('.')
                            if len(func_names)>1 and func_names[1] in privacy_chrome_api_1layer:
                                # privacy related api
                                ext_info['privacy_related_callee_times']+=1
                                tmp_api_info={
                                        'file_name':filename,
                                        'api_name':func["name"]
                                    }
                                ext_info["call"].append(tmp_api_info)
                                if func_names[1] in ext_info.keys():
                                    ext_info[func_names[1]]+=1
                                else:
                                    ext_info['privacy_related_api']+=1
                                    ext_info[func_names[1]]=1
                            else:
                                # privacy unlrelated api
                                ext_info['privacy_unrelated_callee_times']+=1
                    except Exception as e:
                        print(e)
                        print('cannot handle file ',filename)
        ext_api_res_path=dir_path+'/'+ext+"_privacy_api.json"
        save_json(ext_api_res_path,ext_info)

def traverseAllDOMTreeFile(dir_path):
    ext_list=next(os.walk(dir_path))[1]
    for ext in ext_list:
        ext_path=dir_path+'/'+ext
        ext_info={"get_element_operation_times":0,"create_element_operation_times":0,"other_operation_times":0,
                    "get_element":[],"create_element":[]}

        for home, dirs, files in os.walk(ext_path):
            for filename in files:
                if filename[-14:] == '_dom_tree.json':
                    try:
                        with open(os.path.join(home, filename), 'r') as f:
                            funcs = json.load(f)
                        for func in funcs:
                            func_names = func["name"].split('.')
                            func["file_name"]=filename[0:-14]
                            if len(func_names)>1:
                                if func_names[1] in dom_tree_get_api:
                                    # get dom element operation
                                    ext_info["get_element_operation_times"]+=1
                                    ext_info["get_element"].append(func)
                                    
                                elif func_names[1] in dom_tree_creation_api:
                                    # create dom element operation
                                    ext_info["create_element_operation_times"]+=1
                                    ext_info["create_element"].append(func)
                                if func_names[1] in ext_info.keys():
                                    ext_info[func_names[1]]+=1
                                else:
                                    ext_info[func_names[1]]=1
                            else :
                                # not target funcion/api
                                ext_info["other_operation_times"]+=1
                                pass
                    except Exception as e:
                        print(e)
                        print('cannot handle file ',filename)
        ext_api_res_path=dir_path+'/'+ext+"_dom_operation.json"
        save_json(ext_api_res_path,ext_info)


def handle_all_callee():
    global all_chrome_api
    callee_path = './'
    traverseAllCalleeFile(callee_path)
    # traverseAllDOMTreeFile(callee_path)


if __name__ == '__main__':
    handle_all_callee()

