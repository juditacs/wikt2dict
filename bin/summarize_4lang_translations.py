from sys import argv, stdin
from collections import defaultdict
import json
import math


def main():
    stats = defaultdict(list)
    topN = int(argv[2])
    for l in stdin:
        fd = l.decode('utf8').split('\t')
        trans = json.loads(fd[1])
        for wc, words in trans.iteritems():
            stats[wc].append(len(words))
    s = 0
    fourlang_len = 3478.0
    for wc, stat in sorted(stats.iteritems(), key=lambda x: -len(x[1]))[0:topN]:
        s += len(stat)
        print('{} {}'.format(wc, len(stat) / fourlang_len))
    E = s / float(topN)
    var = 0.0
    for wc, stat in sorted(stats.iteritems(), key=lambda x: -len(x[1]))[0:topN]:
        var += (len(stat) - E) ** 2
    print E
    print 'var: ' + str(math.sqrt(var / float(topN)) / fourlang_len)
    print s / float(topN)
    print s / float(topN) / fourlang_len


if __name__ == '__main__':
    main()
