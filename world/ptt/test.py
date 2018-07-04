import re

f = open("article.txt", "r")
b = f.read()

#print(b)
p = re.compile("\x1b\[.*?H")
b = p.sub('', b)
a = re.sub(r'\r', '', b)
print(a)
