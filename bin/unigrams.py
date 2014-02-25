from collections import defaultdict
from sys import stdin, stderr

def main():
    unigrams = defaultdict(lambda: defaultdict(int))
    for l in stdin:
        try:
            wc1, w1, wc2, w2 = l.decode('utf8').strip().split('\t')[0:4]
            for c in w1:
                unigrams[wc1][c] += 1
            for c in w2:
                unigrams[wc2][c] += 1
        except ValueError:
            stderr.write('Invalid line: {0}'.format(l))
    for wc, chars in unigrams.iteritems():
        for c, cnt in sorted(((k, v) for k, v in chars.iteritems()), key=lambda x: -x[1]):
            print(u'{0}\t{1}\t{2}'.format(wc, c, cnt).encode('utf8'))

            
if __name__ == '__main__':
    main()
