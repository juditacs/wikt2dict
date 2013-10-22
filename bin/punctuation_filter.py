import re
import string

punct = re.escape(''.join(set(string.punctuation) - set('.-,\'\"')))
print punct

alpha_re = re.compile(r'[' + punct + ']', re.UNICODE)

from sys import stdin

for l in stdin:
    if alpha_re.search(l.decode('utf8')):
        print l.strip()
