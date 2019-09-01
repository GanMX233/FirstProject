#time:  2019年9月1日17:36:06
import requests
import json
import random
import time
import os
import jieba
import wordcloud

#page表示爬取第几页
def getComment(page):
    try:
        url = "https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv9561&productId=100005297930&score=0&sortType=5&page="+str(page)+"&pageSize=10&isShadowSku=0&fold=1"
        kv = {"user-agent":"Mozilla/5.0",
              "referer":"https://item.jd.com/100005297930.html"}
        r = requests.get(url, headers=kv, timeout=8)
        r.raise_for_status()
    except:
        print("第{}页爬取失败！".format(page))
        return 0
    start_place = r.text.index('(') + 1
    obj = json.loads(r.text[start_place:-2])
    for i in obj['comments']:
        with open("realmex.txt", 'a+', encoding='utf-8') as f:
            f.write(i['content']+'\n')

#num表示共爬取多少页
def getComment_all(num):
    a = time.perf_counter()
    if os.path.exists("realmex.txt"):
        os.remove("realmex.txt")
    for i in range(num):
        getComment(i)
        time.sleep(random.random()*5)
    print("已爬取{}页京东评论，用时{:.2f}秒".format(num, time.perf_counter()-a))

def drawPhoto():
    '''
    stop_words: 排除词
    simsun.ttc: 可替换为本地自带字体
    '''
    stop_words = ["非常", "真的", "感觉", "就是", "没有"]
    a = time.perf_counter()
    w = wordcloud.WordCloud(width=1280, height=1080, max_words=35, font_path="simsun.ttc", background_color="white", stopwords=stop_words)
    with open("realmex.txt", encoding='utf-8') as f:
        txt = f.read()
    wordList = jieba.lcut(txt, cut_all=False)
    wl = " ".join(wordList)
    w.generate(wl)
    w.to_file("realmex.png")
    print("已生成realmex.png到软件目录，用时{:.2f}秒".format(time.perf_counter()-a))

if __name__ == '__main__':
    '''
    page -- 要爬取的页数
    '''
    page = 100
    getComment_all(page)
    drawPhoto()