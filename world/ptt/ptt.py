import telnetlib
import sys
import time
import re

host = 'ptt.cc'
user = 'jaqqxd'
password = 'a1937490'

def check_screen(telnet, decode_bool = True):
    if decode_bool:
        content = telnet.read_very_eager().decode('big5','ignore')
    else:
        content = telnet.read_very_eager()

    print(content)
    input("Press Enter to continue...")
    return content

def switch_board(telnet, board_name):
    telnet.write("s".encode('big5'))
    telnet.write(board_name.encode('big5'))
    telnet.write("\r\n".encode('big5'))
    time.sleep(1)

def color_filter(content, decode_bool = True):
    p = re.compile(b'\x1b\[.*?m')
    content = p.sub(b'', content)
    if decode_bool:
        content = content.decode('big5','ignore')

    return content

def is_article_bottom(content):

    if "100%" in content:
        return True

    return False

telnet = telnetlib.Telnet(host)
time.sleep(1)
content = telnet.read_very_eager().decode('big5','ignore')

if u"請輸入代號" in content:
    
    # user
    telnet.write(user.encode('big5'))
    telnet.write("\r\n".encode('big5'))
    time.sleep(1)
    
    check_screen(telnet)

    # password
    telnet.write(password.encode('big5'))
    telnet.write("\r\n".encode('big5'))    
    time.sleep(1)

    check_screen(telnet)

    # continue
    telnet.write("\r\n".encode('big5'))
    time.sleep(1)
    
    content = check_screen(telnet)

    # exists login
    #telnet.write("\x0C".encode('ascii'))
    #content = telnet.read_very_eager().decode('big5','ignore')

    if u"您想刪除其他重複登入的連線嗎" in content:
        telnet.write("n".encode('big5'))
        time.sleep(1)
        check_screen(telnet)

        telnet.write("\r\n".encode('big5'))
        time.sleep(5)
        print("??????????????")
        content = check_screen(telnet)

    # switch_board
    switch_board(telnet, "Gossiping")
    content = check_screen(telnet)

    # entering picture
    if u"發表文章" not in content:
        telnet.write("\r\n".encode('big5'))
        time.sleep(1)
        content = check_screen(telnet)
    
    telnet.write(b"\r\n")
    time.sleep(1)
    content = check_screen(telnet, False)
    content = color_filter(content)

    article = content
    while not is_article_bottom(content):        
        telnet.write(b"\x1bOC")
        time.sleep(1)
        content = check_screen(telnet, False)   
        content = color_filter(content)
        print("bottom?", is_article_bottom(content))
        article += content


    f = open('article.txt', 'w')
    f.write(article)
    #telnet.write(b"\x1b[M")
    #time.sleep(1)

    #content = check_screen(telnet)   
    #print(content)

    '''telnet.write("\x0C".encode('ascii'))
    content = telnet.read_very_eager().decode('big5','ignore')
    if u"使用者條款" in content:
        telnet.write("\x1b[D".encode('ascii'))
        print('user')
        time.sleep(1)'''

    '''telnet.write("yes".encode('big5'))
    telnet.write("\r\n".encode('big5'))
    time.sleep(1)'''


