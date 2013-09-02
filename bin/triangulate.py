from sys import argv, stderr, path
path.append('../src')

from itertools import combinations
import logging

from handlers import ConfigHandler, LogHandler
from triangulator import Triangulator

def main():
    if len(argv) > 2 and not argv[2] == 'all':
        filter_wc = set([wc.strip() for wc in argv[2:]])
    else:
        filter_wc = None
    cfg_fn = argv[1]
    logger = logging.getLogger('wikt2dict')
    cfg = ConfigHandler("general", cfg_fn)
    logger = LogHandler(cfg)
    with open(cfg['wikicodes']) as wc_f:
        wikicodes = set([w.strip() for w in wc_f])
    n = len(wikicodes)
    if filter_wc:
        m = n - len(filter_wc)
    else:
        m = 0
    num_of_tr = n * (n-1) * (n-2) / 6 - m * (m-1) * (m-2) / 6
    i = 1
    for triangle_wc in combinations(wikicodes, 3):
        if filter_wc and len(set(triangle_wc) & filter_wc) == 0:
            continue
        stderr.write(str(i) + '/' + str(num_of_tr) + repr(triangle_wc) + '\n')
        i += 1
        logger.info(' '.join(triangle_wc) + ' triangle')
        triangulator = Triangulator(triangle_wc, cfg_fn)
        triangulator.collect_triangles()
        triangulator.write_triangles()

if __name__ == '__main__':
    main()

