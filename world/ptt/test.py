import re

s = "第 01~22 行"
print(re.search(r"第 ([0-9]+)~([0-9]+) 行", s).group(1))

def findnth(string, substring, n):
    parts = string.split(substring, n)
    if len(parts) <= n or n <= 0:
        return -1
    return len(string) - len(parts[-1]) - len(substring)

s2 = "aaabbbbbbbaaabbbbbbbaaa"
print(findnth(s2, "aaa", 4))
