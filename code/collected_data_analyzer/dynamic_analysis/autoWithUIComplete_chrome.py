from genericpath import isfile
from logging import StringTemplateStyle
import os
import shutil
import json
import random
import subprocess
from subprocess import Popen, PIPE, STDOUT
import signal
import time
import tkinter
import datetime
from tkinter import *
from bs4 import BeautifulSoup
from matplotlib.pyplot import close
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from multiprocessing.dummy import Pool as ThreadPool
import timeout_decorator
import time
import hashlib

DATE="9_8"

current_index = 0
#crx_folder_name='../chrome_ext/install_test'
crx_folder_name='../chrome_ext/unzip'
pages_save_folder='../chrome_ext/pages'
log_file_path='../chrome_ext/log.txt'
finished_file_path='../chrome_ext/finished_list.txt'
BUF_SIZE = 128*1024

def get_default_page_path(path_to_extension):
    manifest_path=path_to_extension+'manifest.json'
    with open(manifest_path,'r') as f:
        settings=json.load(f)
    try:
        default_path=settings["browser_action"]["default_popup"]
    except:
        print("there is no initial popup page")
        print("there is no initial popup page",file=open(log_file_path,'a'))
        default_path=""
    return default_path

def reset_dir(path):
    if os.path.exists(path) and os.path.isdir(path):
        shutil.rmtree(path)
    os.mkdir(path)

def sha256sum(page_content):
    sha256 = hashlib.sha256()
    sha256.update(page_content.encode())
    return sha256.hexdigest()

def save_page(origin_id,page_content,button_len,page_url):
    hash_file_name=sha256sum(str(button_len)+str(page_url))
    file_path=pages_save_folder+'/'+origin_id+'_pages/'+hash_file_name+'.html'
    if not os.path.isfile(file_path):
        with open(file_path,'w') as f:
            f.write(page_content)
        print(origin_id, "save an unique page")
        return True
    else:
        #print(origin_id, "existing page")
        return False
        
@timeout_decorator.timeout(seconds=120,use_signals=False)
def start_extension(driver,foldername):
    
    extension_folder=crx_folder_name
    path_to_extension = extension_folder+'/'+foldername+'/'
    origin_id=foldername
    
    #driver = webdriver.Chrome(options=chrome_options)
    try:
        driver.create_options()
        # open the manager page of the chrome extension
        driver.get("chrome://extensions/")
        driver.switch_to.window(driver.window_handles[0])
        
        # get the real id of the extension
        element=driver.find_element(By.CSS_SELECTOR,"extensions-manager")
        shadow_root1 = driver.execute_script('return arguments[0].shadowRoot', element)
        element2=shadow_root1.find_element(By.CSS_SELECTOR,"extensions-item-list")
        shadow_root2 = driver.execute_script('return arguments[0].shadowRoot', element2)
        element3=shadow_root2.find_element(By.CSS_SELECTOR,"#container")
        element4=element3.find_element(By.ID,"content-wrapper")
        element5=element4.find_element(By.CLASS_NAME,"items-container")
        element6=element5.find_element(By.CSS_SELECTOR,'extensions-item')
        extension_id=element6.get_attribute('id')
        print(extension_id)
        print(extension_id,file=open(log_file_path,'a'))
        
        # get the initial page of the extension
        # extension_id="***"
        popup_page=get_default_page_path(path_to_extension)
        if popup_page=="":
            print("No popup page")
            print("No popup page",file=open(log_file_path,'a'))
            driver.quit()
            return
    
        initial_page="chrome-extension://"+extension_id+'/'+popup_page
                
        driver.get(initial_page)
        current_windows = driver.window_handles
        driver.switch_to.window(current_windows[-1]) 
        while len(current_windows)>1:
            driver.close()
            current_windows = driver.window_handles
            driver.switch_to.window(current_windows[-1]) 
        # wait the page to be loaded
        time.sleep(1)
        def check_button_clickable(button_list,button_idx):
            try:
                num=len(button_list)
                if button_idx<num-1:
                    cur_name= button_list[button_idx].tag_name
                    next_name = button_list[button_idx+1].tag_name
                    skip_list=["option",'tr','td','li']
                    if cur_name==next_name and cur_name in skip_list:
                        #print("checking button with type",type(button_list[button_idx]),cur_name)
                        return False
            except Exception as e:
                #print("error in checking button",e)
                pass
            return True
        def recursive_click_button(driver,level,action_list):
            # all_pages_reached=True
            level+=1
            if level>5:
                # define the deepest path level:3
                return driver
            # set to action list status
            print("LEVEL",level,"START",str(action_list))
            
            driver.get(initial_page)
            for act in action_list:
                buttons=driver.find_elements(By.XPATH,"//*")
                for i in range(act-1):
                    button=buttons[i]
                    try:
                        if check_button_clickable(buttons,i):
                            button.click()
                            time.sleep(0.1)
                        #print(type(button))
                    except Exception as e:
                        #print("cannot click",e)
                        continue
                    try:
                        current_win=driver.current_window_handle
                        alert = driver.switch_to.alert
                        alert.accept()
                        driver.switch_to.window(current_win)
                        print("alert accepted")
                    except Exception as e:
                        #print("error alert",e)
                        pass
            
            # start new click action
            buttons=driver.find_elements(By.XPATH,"//*")
            button_count=len(buttons)
            url_begin=str(driver.current_url)
            print("level",level,"number of available buttons",button_count)
            print("number of available buttons",file=open(log_file_path,'a'))
            try:
                for i in range(button_count):
                    page_url=str(driver.current_url)
                    current_btn_count=len(driver.find_elements(By.XPATH,"//*"))
                    
                    if save_page(origin_id,driver.execute_script("return document.body.innerHTML"),current_btn_count,page_url):
                        # the page content change
                        # new element is created, a new page
                        if current_btn_count!=button_count:
                        # new page structure
                            print("detect button number change")                        
                        action_list.append(i)
                        driver = recursive_click_button(driver,level,action_list)
                        # recover the status
                        print("recover the page status")
                        del action_list[-1]
                        #driver.refresh()
                        driver.get(initial_page)
                        for act in action_list:
                            buttons=driver.find_elements(By.XPATH,"//*")
                            for p in range(act-1):
                                button=buttons[p]
                                try:
                                    if check_button_clickable(buttons,p):
                                        button.click()
                                        time.sleep(0.1)
                                    #print(type(button))
                                except Exception as e:
                                    #print("cannot click",e)
                                    continue
                                try:
                                    current_win=driver.current_window_handle
                                    alert = driver.switch_to.alert
                                    alert.accept()
                                    driver.switch_to.window(current_win)
                                    print("alert accepted")
                                except Exception as e:
                                    #print("error alert",e)
                                    pass
                        if url_begin==driver.current_url and button_count==len(driver.find_elements(By.XPATH,"//*")):
                            print("really recover the page at",i)
                            
                    new_buttons=driver.find_elements(By.XPATH,"//*")
                    if url_begin!=driver.current_url or button_count!=len(new_buttons):
                        # reached pages
                        # recall the click action, bypass this page
                        #print("reached page at button",i)
                        driver.get(initial_page)
                        for act in action_list:
                            buttons=driver.find_elements(By.XPATH,"//*")
                            for i in range(act-1):
                                button=buttons[i]
                                try:
                                    if check_button_clickable(buttons,i):
                                        button.click()
                                        time.sleep(0.1)
                        
                                except Exception as e:
                                    #print("cannot click",e)
                                    continue
                                try:
                                    current_win=driver.current_window_handle
                                    alert = driver.switch_to.alert
                                    alert.accept()
                                    driver.switch_to.window(current_win)
                                    print("alert accepted")
                                except Exception as e:
                                    #print("error alert",e)
                                    pass
                    else:
                        button=new_buttons[i]
                        try:
                            button.click()
                            time.sleep(0.1)
                        except Exception as e:
                            continue
                        try:
                            current_win=driver.current_window_handle
                            alert = driver.switch_to.alert
                            alert.accept()
                            driver.switch_to.window(current_win)
                            print("alert accepted")
                        except Exception as e:
                            pass
                        
                        new_page=driver.window_handles
                        if len(new_page)>1:
                            print("open a new page")
                            print("open a new page",file=open(log_file_path,'a'))
                            driver.switch_to.window(new_page[0])
                  
            except Exception as e:
                # no change in the pages
                print("error in recursive func at i",i,"all button",len(new_buttons),e)
                pass
            print("LEVEL",level,"FINISH",str(action_list))
            return driver
        
        #reset_dir(crx_folder_name+'/'+origin_id+'_pages/')
        reset_dir(pages_save_folder+'/'+origin_id+'_pages/')
        while len(driver.window_handles)!=0:
            driver.switch_to.window(driver.window_handles[0])
            page_content=driver.execute_script("return document.body.innerHTML")
            buttons=driver.find_elements(By.XPATH,"//*")
            button_count=len(buttons)
            page_url=str(driver.current_url)
            save_page(origin_id,page_content,button_count,page_url)
            if page_url[0:4]=="http":
                print("open an outside page, no need to click")
            else:
                print("start clicking one page")
                driver=recursive_click_button(driver,0,[])
                print("finish one page")
            driver.close()
            print("close one page successfully")
            #break
            
        
        driver.quit()
    except Exception as e:
        print(foldername,"timeout",str(e))
        print(foldername+" timeout "+str(e),file=open(log_file_path,'a'))
        driver.quit()
    # close the mitmproxy by CTL_C signal
    # mitm.send_signal(signal.SIGINT)

def mainGUIinterface(folder_list):
    global current_index
    # current_index = folder_list.index('hcfhemgkgbfonoagglgjcjhaolkacoec')
    current_index=1
    # extension_folder = crx_folder_name
    foldername = folder_list[current_index]
    start_extension(foldername)
    def prev():
        print('prev')
        global current_index
        current_index = current_index - 1
        foldername1 = folder_list[current_index]
        start_extension(foldername1)
    def next():
        print('next')
        global current_index
        current_index += 1
        foldername1 = folder_list[current_index]
        start_extension(foldername1)
        current_number.set(str(current_index))
        current_name.set(foldername1)
    mainUserInterfaceWindow = tkinter.Tk()
    mainUserInterfaceWindow.title("selection tool")
    mainUserInterfaceWindow.geometry("500x200")

    current_number = tkinter.StringVar()
    current_name = tkinter.StringVar()
    selectioncountmainlabel = tkinter.Label(mainUserInterfaceWindow, text="count: ")
    selectioncountcurrentnumber = tkinter.Label(mainUserInterfaceWindow,textvariable=current_number)
    selectioncounttotalnumber = tkinter.Label(mainUserInterfaceWindow,text="")
    currentnamemainlable = tkinter.Label(mainUserInterfaceWindow,text="current name: ")
    currentnamedispalylabel = tkinter.Label(mainUserInterfaceWindow,textvariable=current_name)

    selectioncountmainlabel.pack()
    selectioncountcurrentnumber.pack()
    selectioncounttotalnumber.pack()
    currentnamemainlable.pack()
    currentnamedispalylabel.pack()

    ###Buttoms
    prevbuttom = tkinter.Button(mainUserInterfaceWindow,text="prev",command=prev)
    nextbuttom = tkinter.Button(mainUserInterfaceWindow,text="next",command=next)

    prevbuttom.pack()
    nextbuttom.pack()

    mainUserInterfaceWindow.mainloop()


def time_record(foldername):
    try:  
        extension_folder=crx_folder_name
        path_to_extension = extension_folder+'/'+foldername+'/'
        origin_id=foldername
        if foldername[-6:]=="_pages":
            print(foldername, "skip a page folder")
            print(foldername+" skip a page folder",file=open(log_file_path,'a'))
            return
    
        # valid ext id
        print(origin_id,file=open(finished_file_path,'a'))
        chrome_options = Options()
        chrome_options.add_argument('load-extension=' + path_to_extension)
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation']) 

        driver = webdriver.Chrome(options=chrome_options)
        
        # start the mitmproxy
        # the script for the mitmproxy mitm_req_res.py should be in the same path as the current file
        #import os
        #os.P_NOWAIT,
        
        #mitm=os.spawnlp('gnome-terminal', '-e', 'bash', '-c','mitmdump', '--listen-port','8080','-s', 'mitm_req_res.py')
        #mitm.communicate(input=origin_id.encode())
        #mitm=subprocess.Popen(['bash', 'dump.sh', origin_id.encode()],stdout=PIPE, stdin=PIPE,stderr=PIPE,close_fds=True)
        #mitm.wait()      
        #mitm_stdout=mitm.communicate(input=origin_id.encode())
        #print(mitm_stdout)
        #mitm.send_signal(signal.SIGINT)
        # trigger all the buttons and collect page elements
        with open("traffic_data/request_all_in_one.txt",'a') as f:
            f.write("-----monitoring start-----"+str(datetime.datetime.now())+'\n')
            f.write(origin_id+'\n')
        with open("traffic_data/response_all_in_one.txt",'a') as f:
            f.write("-----monitoring start-----"+str(datetime.datetime.now())+'\n')
            f.write(origin_id+'\n')
        time.sleep(0.3)
        # start the test automatically
        start_extension(driver,foldername)
        #mitm.send_signal(signal.SIGINT)
        #mitm.terminate()
        #mitm.wait()
        time.sleep(0.3)
        with open("traffic_data/request_all_in_one.txt",'a') as f:
            f.write("-----monitoring end-----"+str(datetime.datetime.now())+'\n')
            f.write(origin_id+'\n')
        with open("traffic_data/response_all_in_one.txt",'a') as f:
            f.write("-----monitoring end-----"+str(datetime.datetime.now())+'\n')
            f.write(origin_id+'\n')
    except Exception as e:
        print(e)
        try:
            driver.quit()
        except Exception as e:
            print("erro in last quit",e)
            
        try:
            time.sleep(0.3)
            with open("traffic_data/request_all_in_one.txt",'a') as f:
                f.write("-----monitoring end-----"+str(datetime.datetime.now())+'\n')
                f.write(origin_id+'\n')
            with open("traffic_data/response_all_in_one.txt",'a') as f:
                f.write("-----monitoring end-----"+str(datetime.datetime.now())+'\n')
                f.write(origin_id+'\n')
        except Exception as e:
            print("erro in last quit mitmproxy",e)
        print("OUT OF TIME "+foldername,file=open(log_file_path,'a'))

def mainWithoutGUIAuto(folder_list):
    # global current_index
    # current_index = folder_list.index('hcfhemgkgbfonoagglgjcjhaolkacoec')
    # current_index=1
    extension_folder = crx_folder_name
    # foldername = folder_list[current_index]
    print("========start extension analysis========")
    print("========start extension analysis========",file=open(log_file_path,'a'))
    '''
    pool=ThreadPool(1)
    pool.map(start_extension,folder_list)
    pool.close()
    pool.join()
    '''
    
    for foldername in folder_list:
        time_record(foldername)
        #break
       
    
def init():
    extension_folder = crx_folder_name
    print("============start===========")
    f_list = os.listdir(extension_folder)
    print(str(len(f_list)) + ' folders found')
    print(str(len(f_list)) + ' folders found',file=open(log_file_path,'a'))
    f_list.sort()
    return f_list

if __name__=='__main__':
    #mainGUIinterface()
    flist = init()
    #mainGUIinterface(flist)
    mainWithoutGUIAuto(flist)
