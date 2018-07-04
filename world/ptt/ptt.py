import telnetlib
import sys
import time
import re
import sys

class PTTTelnet(object):
    HOST = 'ptt.cc'
    USER = 'jaqqxd'
    PASSWORD = ''
    content = b""
    content_big5 = "" 
    content_big5_no_c = "" # without color
    
    def __init__(self, *args, **kwargs):
        
        self.USER = kwargs.get("user", self.USER)
        self.PASSWORD = kwargs.get("password", self.PASSWORD)
        self.telnet = telnetlib.Telnet(self.HOST)
        time.sleep(1)
        self.console_log("連線中...")

    def login(self):

        # user
        input_key = self.to_bytes_big5(self.USER + "\r\n")
        self.user_input(input_key, 1)

        # password
        input_key = self.to_bytes_big5(self.PASSWORD + "\r\n")
        self.user_input(input_key, 1)
        
        # continue
        self.user_input()

        self.check_screen()

        while self.is_blocked():
            pass

        self.console_log("登入成功!")

    def is_blocked(self):
        self.read()
        self.check_screen()
        content = self.content_big5_no_c

        if u"您想刪除其他重複登入的連線嗎" in content:
            input_key = self.to_bytes_big5("N" + "\r\n")
            self.user_input(input_key, 3)

            return True

        if u"您要刪除以上錯誤嘗試的記錄嗎" in content:
            input_key = self.to_bytes_big5("Y" + "\r\n")
            self.user_input(input_key, 3)

            return True
        
        if u"請按任意鍵繼續" in content:
            input_key = self.to_bytes_big5("Y")
            self.user_input(input_key, 1)

            return True

        return False

    def read(self):
        self.content = self.telnet.read_very_eager()
        self.content_big5 = self.content.decode('big5','ignore')
        self.content_big5_no_c = self.color_filter(self.content).decode('big5','ignore')

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
        input("Press Enter to continue...")
        return content

    def switch_board(self, board_name):
        
        input_key = self.to_bytes_big5("s")
        self.user_input(input_key, 1)
 
        input_key = self.to_bytes_big5(board_name + "\r\n")
        self.user_input(input_key, 1)

        while self.is_blocked():
            pass


    def is_article_bottom(self):

        if "100%" in self.content_big5_no_c:
            return True

        return False

    def console_log(self, tag, content = ""):
        print("\n\n\n\n\n\n\n\n" + str(tag) + " " + str(content))

    def get_article(self):

        self.read()

        input_key = b"\r\n"
        self.user_input(input_key, 1)

        self.read()
        article = self.remove_last_line(self.content_big5_no_c)

        f = open('article.txt', 'w')
        while not self.is_article_bottom():
            input_key = b"\x1bOC"
            self.user_input(input_key, 1)
            
            self.read()            
            self.check_screen()   
            self.console_log("bottom", self.is_article_bottom())

            article += self.remove_last_line(self.content_big5_no_c)

        p = re.compile("\x1b\[.*?H")
        article = p.sub('', article)

        p = re.compile("\x1b\[K")
        article = p.sub('', article)
        
        article = re.sub(r'\r', '', article)
        f.write(article)
        f.close()

    def remove_last_line(self, s):
        return s[:s.rfind('\n')]

if __name__ == "__main__":

    PTT = PTTTelnet(password=sys.argv[1])

    PTT.login()
    PTT.check_screen()
    PTT.switch_board("Gossiping")
    PTT.get_article()    

