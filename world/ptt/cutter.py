import jieba
import jieba.analyse
import os
import re
import os.path
import time
import pymongo
from pymongo import MongoClient

ARTICLE_DIR = "article/"
ARTICLE_SPLIT_DIR = "article_split/"
ARTICLE_TFIDF_DIR = "article_tfidf/"


def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def article_insert_mongodb(*args, **kwargs):
    board = kwargs.get("board", "Gossiping")
    aid = kwargs.get("aid", "M0000000000A")
    title = kwargs.get("title", "XD")
    ts = kwargs.get("ts", "0000000000")
    author = kwargs.get("author", "JAQQ")
    content = kwargs.get("content", "AAAAAAAA")
    article_content = kwargs.get("article_content", "AAAAAAAA")
    push_content = kwargs.get("push_content", "XD")
    ip = kwargs.get("ip", "111111111111")
    keyword = kwargs.get("keyword", "111111111111")

    client = MongoClient('mongodb://localhost:27017/')
    db = client.JAQQ
    collection = db.PTTArticle
    post = {
            "board": board,
            "aid": aid,
            "title": title,
            "ts": ts,
            "author": author,
            "content": content,
            "article_content": article_content,
            "push_content": push_content,
            "ip": ip,
            "keyword": keyword
           }

    post_id = collection.insert_one(post).inserted_id
    print("id", post_id)

def findnth(string, substring, n):
    parts = string.split(substring, n)
    if len(parts) < n or n <= 0:
        return -1
    return len(string) - len(parts[-1]) - len(substring)

while True:
    article_list = os.listdir(ARTICLE_DIR)

    files = []

    for filename in article_list:
        files += [filename]

    files = sorted(files)

    for filename in files:
        f = open(ARTICLE_DIR + filename, 'r')

        if os.path.exists(ARTICLE_TFIDF_DIR + filename):
            continue        

        content = f.read()

        p = re.compile(r"※ 文章網址: https:\/\/www.ptt.cc\/bbs\/Gossiping\/M\.([0-9]+)\.A.*?\.html")
        for m in p.finditer(content):
            start_idx = m.start()

            newline_4th = findnth(content, "\n", 4)
            article_content = content[newline_4th + 1:start_idx]


            push_content = content[start_idx + len(m.group()) + 1:]
            aid = re.search(r"M\.[0-9]+\.A", m.group(0)).group(0)
            ts = m.group(1)            
        
        left_parenthesis = findnth(content, "(", 1)
        author = content[5:left_parenthesis]
        find_pattern = "※ 發信站: 批踢踢實業坊(ptt.cc), 來自: "
        find_ip = findnth(content, find_pattern, 1)        
        ip = content[find_ip + len(find_pattern):find_ip + len(find_pattern) + 20]
        
        ip = re.search(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", ip)
        if ip:
            ip = ip.group(0)
        else:
            continue

        n1 = findnth(content, '\n', 1)
        n2 = findnth(content, '\n', 2)
        title = content[n1 + 6:n2]

        print('----------------------------')
        print(title)
        print(article_content)
        print(push_content)
        print(aid)
        print(ts)
        print(author)
        print(ip)


        words = jieba.cut(article_content, cut_all=False)
        split_f = open(ARTICLE_SPLIT_DIR + filename, 'w')
        for word in words:
            if word == ' ' or word == '\n':
                continue
            #print(bytes(word,'big5'))
            print(word)
            split_f.write(word + '\n')

        split_f.close()

        print("-----------------")

        tfidf_f = open(ARTICLE_TFIDF_DIR + filename, 'w')
        tfidf = jieba.analyse.extract_tags(article_content, 30)
        keyword = []
        for word in tfidf:
            if is_float(word):
                continue
            #print(bytes(word,'big5'))
            print(word)
            tfidf_f.write(word + '\n')
            keyword += [word]
            
        tfidf_f.close()
    
        

        board = "Gossiping"
        aid = aid
        title = title
        ts = ts
        author = author
        content = content
        article_content = article_content
        push_content = push_content
        ip = ip

        article_insert_mongodb( 
                                board = board,
                                aid = aid,
                                title = title,
                                ts = ts,
                                author = author,
                                content = content,
                                article_content = article_content,
                                push_content = push_content,
                                ip = ip,
                                keyword = keyword
                              )

    time.sleep(10)
