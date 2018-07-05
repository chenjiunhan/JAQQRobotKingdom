import telnetlib
import sys
import time
import re
import sys
import datetime
import os.path
class PTTTelnet(object):
    HOST = 'ptt.cc'
    USER = 'jaqqxd'
    PASSWORD = ''
    ARTICLE_DIR = 'article/'
    ARTICLE_BYTES_DIR = 'article_bytes/'

    content = b""
    content_big5 = "" 
    content_big5_no_c = "" # without color    

    previous_content = b""

    board = ""
    
    def __init__(self, *args, **kwargs):
        
        self.USER = kwargs.get("user", self.USER)
        self.PASSWORD = kwargs.get("password", self.PASSWORD)
        self.telnet = telnetlib.Telnet(self.HOST)
        time.sleep(1)
        self.console_log("連線中...")

    def login(self):

        # user
        input_key = self.to_bytes_big5(self.USER + "\r\n")
        self.user_input(input_key)

        # password
        input_key = self.to_bytes_big5(self.PASSWORD + "\r\n")
        self.user_input(input_key)
        
        # continue
        self.user_input()

        #self.check_screen()

        while self.is_blocked():
            pass

        self.console_log("登入成功!")

    def is_blocked(self):
        self.read()
        #self.check_screen()
        content = self.content_big5_no_c

        if u"您想刪除其他重複登入的連線嗎" in content:
            input_key = self.to_bytes_big5("N" + "\r\n")
            self.user_input(input_key, 5)

            return True

        if u"您要刪除以上錯誤嘗試的記錄嗎" in content:
            input_key = self.to_bytes_big5("Y" + "\r\n")
            self.user_input(input_key, 5)

            return True
        
        if u"請按任意鍵繼續" in content:
            input_key = self.to_bytes_big5("Y")
            self.user_input(input_key)

            return True

        return False

    def read(self):
        self.telnet.read_very_eager()
        self.user_input(b"\x0c")
        self.check_screen()
        self.previous_content = self.content
        self.content = self.telnet.read_very_eager()
        self.content_big5 = self.content.decode('big5','ignore')
        self.content_big5_no_c = self.color_filter(self.content).decode('big5','ignore')
        if self.previous_content == self.content:
            return False

        return True

    def clean_content(self):
        self.content = b""

    def user_input(self, key = b"\r\n", timeout = 1, *args, **kwargs):
        #timeout = kwargs.get("timeout", 0.1)
        #key = kwargs.get("key", b"\r\n")

        self.console_log("INPUT", key)

        self.telnet.write(key)        
        time.sleep(timeout)

    def to_bytes_big5(self, key):
        return bytes(key, 'big5')

    '''def get_bytes(self, *args, **kwargs):
        return self.content

    def get_big5(self):
        return self.content.decode('big5','ignore')'''

    def decode_big5(self, content):
        return content.decode('big5','ignore')
    
    def color_filter(self, content):
        p = re.compile(b'\x1b\[.*?m')
        content = p.sub(b'', content)
        return content

    def check_screen(self, *args, **kwargs):
        decode_bool = kwargs.get("decode_bool", True)
        if decode_bool:
            content = self.content.decode('big5','ignore')
        else:
            content = self.content

        print(content)
        #input("Press Enter to continue...")
        return content

    def switch_board(self, board_name):
        
        input_key = self.to_bytes_big5("s")
        self.user_input(input_key)
 
        input_key = self.to_bytes_big5(board_name + "\r\n")
        self.user_input(input_key)

        while self.is_blocked():
            pass

        self.board = board_name


    def is_article_bottom(self):
        
        if "100%" in self.content_big5_no_c[self.content_big5_no_c.rfind('\n') + 1:]:
            return True

        return False

    def console_log(self, tag, content = ""):
        print("\n\n\n\n\n\n\n\n" + str(tag) + " " + str(content))

    def get_articles(self, ts):
        
        while True:
            aid, a_ts, article, article_bytes = self.get_article()                 
            
            # up
            input_key = b"\x1bOA"
            self.user_input(input_key)

            if aid == False:
                continue

            if a_ts < ts:
                print("FINISH!!!!!!!!!!!!")
                break
            
            file_path = self.ARTICLE_DIR + aid

            if os.path.exists(file_path):
                continue

            f = open(file_path, 'w')
            f.write(article)
            f.close()

            file_path = self.ARTICLE_BYTES_DIR + aid

            if os.path.exists(file_path):
                continue

            f = open(file_path, 'wb')
            f.write(article_bytes)
            f.close()                       


    def get_article(self):        
        
        self.read()
        # enter article
        input_key = b"\r\n"
        self.user_input(input_key)
        

        if not self.read():
            self.console_log("Same!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            return False, False, False, False

        #self.user_input(b"\x0c")        
        self.read()

        last_line = self.get_last_line(self.content_big5_no_c)
        re_search = re.search(r"([0-9]+)~([0-9]+)", last_line)

        count_fail = 0
        while re_search == None:
            count_fail += 1
            if count_fail > 3:
                return False, False, False, False
            print("BBBBBBBBBBBBBBBB")
            time.sleep(1)
            
            self.read()
            last_line = self.get_last_line(self.content_big5_no_c)
            
            re_search = re.search(r"([0-9]+)~([0-9]+)", last_line)

        article = self.remove_last_line(self.content_big5_no_c)
        article_bytes = self.content


        previous_start_line = int(re_search.group(1))
        previous_end_line = int(re_search.group(2))

        #f = open('article.txt', 'w')
        while not self.is_article_bottom():
            input_key = b"\x1bOC"
            self.user_input(input_key)
            self.read()            

            
            #self.read()            

            #self.check_screen()   
            self.console_log("bottom", self.is_article_bottom())
         
            last_line = self.get_last_line(self.content_big5_no_c)

            re_search = re.search(r"([0-9]+)~([0-9]+)", last_line)
            
            count_fail = 0
            while re_search == None:
                count_fail += 1
                if count_fail > 3:
                    return False, False, False, False
                print("HHHHHHHHHHHHHH")
                time.sleep(1)
                
                self.read()
                last_line = self.get_last_line(self.content_big5_no_c)

                re_search = re.search(r"([0-9]+)~([0-9]+)", last_line)
            
            #self.check_screen()   

            start_line = int(re_search.group(1))
            end_line = int(re_search.group(2))

            num_line_to_remove = (previous_end_line - start_line + 1)
            start_idx = self.findnth(self.content_big5_no_c, '\n', num_line_to_remove) + 1
            article += self.remove_last_line(self.content_big5_no_c[start_idx:])
            article_bytes += self.content


            previous_start_line = start_line
            previous_end_line = end_line

        

        p = re.compile("\x1b\[.*?H")
        article = p.sub('', article)

        p = re.compile("\x1b\[K")
        article = p.sub('', article)

        p = re.compile("\x1b\[2J")
        article = p.sub('', article)
        
        article = re.sub(r'\r', '', article)

        re_search = re.search(r"M\.([0-9]+)\.A.*?\.html", article)
        
        count_fail = 0
        while re_search == None:
            count_fail += 1
            if count_fail > 3:
                 return False, False, False, False

            print("CCCCCCCCCCCCCC")
            time.sleep(1)
            
            self.read()

            re_search = re.search(r"※ 文章網址: https:\/\/www.ptt.cc\/bbs\/" + self.board + r"\/M\.([0-9]+)\.A.*?\.html", self.content_big5_no_c)


        a_ts = int(re_search.group(1))
        aid = re_search.group(0)[0:-5]
        
        # leave article
        input_key = b"\x1bOD"
        self.user_input(input_key)

        return aid, a_ts, article, article_bytes

    def remove_last_line(self, s):
        return s[:s.rfind('\n') + 1]

    def findnth(self, string, substring, n):
        parts = string.split(substring, n)
        if len(parts) <= n or n <= 0:
            return -1
        return len(string) - len(parts[-1]) - len(substring)

    def get_last_line(self, content):
        return content[content.rfind('\n') + 1:]

if __name__ == "__main__":

    PTT = PTTTelnet(password=sys.argv[1])

    PTT.login()
    #PTT.check_screen()
    PTT.switch_board("Gossiping")

    ts = datetime.datetime.strptime('2018-06-01 18:28:00', '%Y-%m-%d %H:%M:%S').timestamp()

    PTT.get_articles(ts)

