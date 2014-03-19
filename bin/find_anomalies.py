""" Wikt2Dict - Find anomalies

Usage:
    find_anomalies.py punct [--num=N]
    find_anomalies.py unigram <unigram_file> [--whitelist=<whlist>...] [--] <prob_threshold>

Options:
    -n --num=N          Number of weird characters [default: 1].
    -h                  Show this screen.
"""
from sys import stdin, stderr
from docopt import docopt
from collections import defaultdict
import re
import string
import math

punct_ok = set('-\'.,?"')
punct = ''.join(set(string.punctuation) - punct_ok)
punct_re = re.compile(r'[{0}]'.format(re.escape(punct)),
                      re.UNICODE)

unigrams = defaultdict(lambda: defaultdict(int))
sum_ = defaultdict(int)


def scan_stdin(args):
    stats = {'punct': 0, 'punct ok': 0, 'sum': 0, 'invalid': 0}
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
                if not wc1 in sum_ or not wc2 in sum_:
                    stderr.write('INVALID, unknown language: {0}'.format(l))
                    continue
                if wc1 in args['--whitelist'] or wc2 in args['--whitelist']:
                    continue
                prob1 = 0.0
                prob2 = 0.0
                for c in w1:
                    prob1 += math.log(float(unigrams[wc1][c]) / sum_[wc1])
                prob1 /= len(w1)
                for c in w2:
                    prob2 += math.log(float(unigrams[wc2][c]) / sum_[wc2])
                prob2 /= len(w2)
                if prob1 < int(args['<prob_threshold>']) or prob2 < int(args['<prob_threshold>']):
                    print('UNIGRAM: {0}\t{1}\t{2}'.format(prob1, prob2, l.strip()))
        except ValueError:
            stats['invalid'] += 1
            stderr.write('INVALID: {0}'.format(l))


def read_unigrams(fn):
    with open(fn) as f:
        for l in f:
            wc, c, cnt = l.decode('utf8').split('\t')
            unigrams[wc][c] = int(cnt)
            sum_[wc] += int(cnt)

def main():
    args = docopt(__doc__, version="Wikt2Dict - Find anomalies 1.0")
    if args['unigram']:
        read_unigrams(args['<unigram_file>'])
    scan_stdin(args)

if __name__ == '__main__':
    main()
