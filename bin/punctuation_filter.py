import re
import string

punct = re.escape(''.join(set(string.punctuation) - set('.-,\'\"')))

alpha_re = re.compile(r'[' + punct + ']', re.UNICODE)

from sys import stdin, stderr, argv

cnt = 0
mode = argv[1]

for l in stdin:
    cnt += 1
    if cnt % 100000 == 0:
        stderr.write('{0}\n'.format(cnt))
    if mode == 'pos':
        if alpha_re.search(l.decode('utf8')):
            print l.strip()
    elif mode == 'neg':
        if not alpha_re.search(l.decode('utf8')):
            print l.strip()
