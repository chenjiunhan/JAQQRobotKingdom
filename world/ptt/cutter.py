import jieba
import jieba.analyse
import os
import re
import os.path
import time
ARTICLE_DIR = "article/"
ARTICLE_SPLIT_DIR = "article_split/"
ARTICLE_TFIDF_DIR = "article_tfidf/"


def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

while True:
    time.sleep(10)
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

        print(content)

        p = re.compile(r"※ 文章網址: https:\/\/www.ptt.cc\/bbs\/Gossiping\/M\.([0-9]+)\.A.*?\.html")
        for m in p.finditer(content):
            start_idx = m.start()
            article_content = content[:start_idx]
            push_content = content[start_idx + len(m.group()) + 1:]    

        print(article_content)
        print(push_content)

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
        tfidf = jieba.analyse.extract_tags(article_content, 100)
        for word in tfidf:
            if is_float(word):
                continue
            #print(bytes(word,'big5'))
            print(word)
            tfidf_f.write(word + '\n')
            
        tfidf_f.close()

