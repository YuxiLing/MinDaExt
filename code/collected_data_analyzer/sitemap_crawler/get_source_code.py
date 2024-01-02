import os,shutil
import requests
import json
from tqdm import tqdm
from queue import Queue
import threading
lock = threading.Lock()

headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Length": "0",
        "Cache-Control": "no-cache",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
        # "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"
    }

class Download_thread(threading.Thread):
    def __init__(self, thread_id, id_queue,failed_log, finished_log,download_path):
        threading.Thread.__init__(self)
        self.thread_id=thread_id
        self.id_queue=id_queue
        self.failed_log=failed_log
        self.finished_log=finished_log
        self.download_path=download_path

    def run(self) -> None:
        while not self.id_queue.empty():
            id=self.id_queue.get()
            dst_path = os.path.join(self.download_path, '%s.crx' % id)
            if os.path.isfile(dst_path)==False:
                _DownloadCrxFromCws(id,self.download_path,self.failed_log,self.finished_log)
            else:
                print('file exists')

def _DownloadCrxFromCws(ext_id, dst, failed_log_file,finished_log_file):
    """Downloads CRX specified from Chrome Web Store.
    Retrieves CRX (Chrome extension file) specified by ext_id from Chrome Web
    Store, into directory specified by dst.
    Args:
        ext_id: id of extension to retrieve.
        dst: directory to download CRX into
    Returns:
        Returns local path to downloaded CRX.
        If download fails, return None.
    """
    dst_path = os.path.join(dst, '%s.crx' % ext_id)
    # cws_url = ('https://clients2.google.com/service/update2/crx?response='
    #            'redirect&os=mac&arch=x64&os_arch=x86_64&nacl_arch=x86-64&'
    #            'prod=chromecrx&prodchannel=&prodversion=88.0.4324.146&lang=en-US&acceptformat=crx3&x=id%%3D'
    #            '%s%%26installsource%%3D'
    #            'ondemand%%26uc' % ext_id)
    cws_url=('https://clients2.google.com/service/update2/crx?response=redirect&os=linux&arch=x64&os_arch=x86_64&nacl_arch=x86-64&'
             'prod=chromium&prodchannel=unknown&prodversion=103.0.5060.53&lang=en-US&acceptformat=crx2,crx3&x=id%3D'+ext_id+'%26uc')
    try:
        req = requests.get(cws_url,headers=headers)
        res = req.content
        if req.status_code!= 200:
            # download failled
            print( ext_id, file=failed_log_file)
        else:
            with open(dst_path, 'wb') as f:
                f.write(res)
            print( ext_id, file=finished_log_file)
    except Exception as e:
        print( ext_id, file=failed_log_file)
        print(e, file=failed_log_file)
        print(e)


def _DownloadXPIFromFws(ext_id, link, dst, log_file):
    """Downloads XPI specified from Chrome Web Store.
    Retrieves XPI (Chrome extension file) specified by ext_id from Firefox Web Store
    Store, into directory specified by dst.
    Args:
        ext_id: id of extension to retrieve.
        dst: directory to download XPI into
    Returns:
        Returns local path to downloaded XPI.
        If download fails, return None.
    """
    dst_path = os.path.join(dst, '%s.xpi' % ext_id)
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',

    }
    req0 = urllib.request.Request(url=link, headers=headers)
    req = urllib.request.urlopen(url=req0, timeout=10)
    res = req.read()
    if req.getcode() != 200:
        print('download failed: ', ext_id, 'the code:', req.getcode())
        print('download failed: ', ext_id, file=open("./firefox_log.txt", "a"))
        return False
    #   print(res)
    with open(dst_path, 'wb') as f:
        f.write(res)
    print('download successful: ', ext_id)
    return True

def start_multi_thread_download(full_list, failed_log_file,finished_log_file,download_path):
    open(failed_log_file, 'w').close()
    open(finished_log_file, 'w').close()
    # if os.path.isdir(download_path):
    #     shutil.rmtree(download_path)
    # os.mkdir(download_path)

    failed_log=open(failed_log_file,'a')
    finished_log=open(finished_log_file,'a')
    id_queue=Queue(len(full_list))
    for item in tqdm(full_list):
        id_queue.put(item['id'])
    downloader_thread_list=[]
    for thread_id in range(50):
        thread=Download_thread(thread_id,id_queue,failed_log,finished_log,download_path)
        thread.start()
        downloader_thread_list.append(thread)
    while not id_queue.empty():
        pass
    for t in downloader_thread_list:
        t.join()

    failed_log.close()
    finished_log.close()

if __name__=='__main__':
    download_dir='./download_log'
    # if os.path.isdir(download_dir):
    #     shutil.rmtree(download_dir)
    # os.mkdir(download_dir)
    browser='chrome'
    failed_log_file='./download_log/%s_failed.txt' % browser
    finished_log_file='./download_log/%s_finished.txt' % browser
    download_path='./ext_source_code'
    fulllist_file='./%s_fulllist_Jan_2023.json' % browser
    f=open(fulllist_file,'r')
    full_list=json.load(f)
    print('total download',len(full_list))
    start_multi_thread_download(full_list,failed_log_file,finished_log_file,download_path)