import re
content = b"\x1b[0;33;43m \x1b[41m\xa2e\xa2m\x1b[31;43m\xa2e\xa2\x1b[33me  \x1b[31m\xa2m       \r\n\x1b[m    \x1b[31m\xa2i\x1b[30m\xa2\x1b[31me\xa2e\xa2i\x1b[30;41m\xa2e\x1b[0;1;37m \xa1Y       \x1b[0;33m\xa2m  \x1b[1;36m\xac\xdb     \x1b[0;44m \x1b[30m\xa2x \x1b[1;34m\xa2\xa8\xa2\xab"

print(content)
content = bytes(str(content), encoding='big5')
print(content)
exit()
content = str(re.sub(r'\\x1b', '', content))
content = str(re.sub(r'\\x', '', content))
print(content, "------------")
content = str(re.sub(r'\\r\\n', '', content))
content = str(re.sub(r'1b\[.*?m', '', content))
content = str(re.sub(r'\s', '', content))
print(content, "..................")
content = str(content)[2:-1]
print(content)
content = bytes.fromhex(str(content)[2:-1])
print(content)
exit()
print("----------------")
print(content)
print("===============")
print(str(re.sub(r'\\x1b\[.*?m', '', content)))

