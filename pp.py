from bs4 import BeautifulSoup
import json
import  os,sys
from os import makedirs
from os.path import exists
import requests
import logging
import re
from urllib.parse import urljoin
import multiprocessing
from bs4 import BeautifulSoup
from requests import Request, Session

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')

RESULTS_DIR = 'results'
exists(RESULTS_DIR) or makedirs(RESULTS_DIR)



def scrape_page(url):
    """
    scrape page by url and return its html
    :param url: page url
    :return: html of page
    """
    logging.info('scraping %s...', url)
    cookie = 'buvid3=56AB3A23-E097-2CBA-857D-9FB7C041677B30516infoc; b_nut=1668522330; i-wanna-go-back=-1; _uuid=D3999E4B-1D910-92AE-43610-43AE1CDC6B5932744infoc; buvid4=382A326A-FC4A-A391-11BA-E10D1DAD8EDA31817-022111522-HJHOGEcBB83neGNRDAkcxA%3D%3D; CURRENT_FNVAL=4048; buvid_fp_plain=undefined; DedeUserID=71623954; DedeUserID__ckMd5=3982e0834640e29f; b_ut=5; rpdid=0zbfVFJdGt|LsmAghLe|42m|3w1OVGh4; nostalgia_conf=-1; LIVE_BUVID=AUTO2416686977395880; hit-new-style-dyn=0; hit-dyn-v2=1; CURRENT_QUALITY=0; blackside_state=1; fingerprint=b47dccb0fe8b71403889170988886713; buvid_fp=b47dccb0fe8b71403889170988886713; SESSDATA=d15bc7a5%2C1685261481%2C35f22%2Ab2; bili_jct=7e31108c50b3732509768f2c6eae788a; sid=7in6oi43; b_lsid=5F7E2FE5_184C36C67A2; innersign=1; PVID=1; bp_video_offset_71623954=733961575500611600; bsource=search_bing'
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.56'
    headers = {
    'User-Agent': user_agent,
    'cookie':cookie
    }
    # s = Session()
    try:
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.text
        logging.error('get invalid status code %s while scraping %s',
                      response.status_code, url)
    except requests.RequestException:
        logging.error('error occurred while scraping %s', url, exc_info=True)

def main(page):
    """
    main process
    :return:
    """
    index_html = scrape_index(page)
    

if __name__ == '__main__':
    # pool = multiprocessing.Pool()
    # pages = range(1, TOTAL_PAGE + 1)
    # pool.map(main, pages)
    # pool.close()
    url = 'https://api.bilibili.com/x/web-interface/view/detail?platform=web&bvid=BV1Dh41167W4&aid=206719735&need_operation_card=1&web_rm_repeat=1&need_elec=1&out_referer=&page_no=1&p=1'
    basurl,baseurl_tail = 'https://www.bilibili.com/video/BV1Dh41167W4?p=','&vd_source=1a432a45372ea0a0d1ec88a20d9cef2c'
    res = scrape_page(url)
    res = json.loads(res)
    for id,i in enumerate(res['data']['View']['pages']):
        print(i['part'],id+1)
        id_ = str(id+1)
        url = basurl+id_+baseurl_tail
        cmd_call = 'you-get --format=dash-flv360  -o  "'+os.getcwd()+'\\'+RESULTS_DIR+'"\t'+url
        # print(cmd_call)
        os.system(cmd_call)
    files_  = []
    path = os.getcwd()+'\\'+RESULTS_DIR
    for root, dirs, files in os.walk(path):
        for i in files:
            if('.mp4' in i):
                files_.append(i)
                name = path+'\\'+i.split('.mp4')[0]
                cmd_call = 'ffmpeg -i "'+name+'.mp4" -f mp3 -vn "'+name+'.mp3"'
                # print(cmd_call)
                os.system(cmd_call)