""" Wikt2Dict - Find anomalies

Usage:
    find_anomalies.py punct [--num=N]
    find_anomalies.py unigram 

Options:
    -n --num=N          Number of weird characters [default: 1].
    -h                  Show this screen.
"""
from sys import stdin 
from docopt import docopt
from collections import defaultdict
import re
import string

punct_ok = set('-\'.')
punct = ''.join(set(string.punctuation) - punct_ok)
punct_re = re.compile(r'[{0}]'.format(re.escape(punct)),
                     re.UNICODE)

def scan_stdin(args):
    stats = {'punct': 0, 'punct ok': 0, 'sum': 0, 'invalid': 0}
    unigrams = defaultdict(lambda: defaultdict(int))
    for l in stdin:
        stats['sum'] += 1
        try:
            wc1, w1, wc2, w2 = l.decode('utf8').strip().split('\t')[0:4]
            if args['punct']:
                if abs(len(punct_re.findall(w1)) - len(punct_re.findall(w2))) >= int(args['--num']):
                    print('PUNCTUATION: {0}'.format(l.strip()))
                    stats['punct'] += 1
                else:
                    stats['punct ok'] += 1
            if args['unigram']:
                for c in w1:
                    unigrams[wc1][c] += 1
                for c in w2:
                    unigrams[wc2][c] += 1
        except ValueError:
            stats['invalid'] += 1
            #print('INVALID: {0}'.format(l.strip()))
    #print(stats)
    if args['unigram']:
        print_unigrams(unigrams)


def print_unigrams(unigrams):
    for wc, chars in unigrams.iteritems():
        for c, cnt in sorted(((k, v) for k, v in chars.iteritems()), key=lambda x: -x[1]):
            print(u'{0}\t{1}\t{2}'.format(wc, c, cnt).encode('utf8'))


def main():
    args = docopt(__doc__, version="Wikt2Dict - Find anomalies 1.0")
    scan_stdin(args)

if __name__ == '__main__':
    main()
