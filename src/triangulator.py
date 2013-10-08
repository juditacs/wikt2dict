from os import path, listdir, makedirs
from collections import defaultdict
from itertools import product

from handlers import ConfigHandler, LogHandler

class Triangulator(object):

    def __init__(self, triangle_wc, cfg_fn):
        self.wikicodes = set(triangle_wc)
        self.cfg_general = ConfigHandler("general", cfg_fn)
        self.log_handler = LogHandler(self.cfg_general)
        self.pairs = defaultdict(lambda: defaultdict(lambda:
                     defaultdict(lambda: defaultdict(list))))
        self.triangles = defaultdict(list)
        self.read_three_configs(cfg_fn)
        self.read_pairs_in_three_langs()

    def read_pairs_in_three_langs(self):
        for wc in self.wikicodes:
            if not self.cfg[wc]:
                continue
            fn = self.cfg_general['dumpdir'] + '/' + self.cfg[wc]['fullname'] + \
                    '/' + self.cfg_general['word_pairs_outfile']
            if not path.exists(fn):
                continue
            self.read_pairs_in_lang(wc, fn)

    def read_pairs_in_lang(self, wc, fn):
        f = open(fn)
        for l in f:
            fd = l.decode('utf8').strip().split('\t')
            if len(fd) < 6:
                continue
            wc1, w1, wc2, w2, src_wc, src_art = fd[0:6]
            # converting Mandarin Chinese to Chinese 
            if wc1 == 'cmn':
                wc1 = 'zh'
            if wc2 == 'cmn':
                wc2 = 'zh'
            if wc1 < wc2:
                self.pairs[wc1][w1][wc2][w2].append((src_wc, src_art))
            else:
                self.pairs[wc2][w2][wc1][w1].append((src_wc, src_art))
            
    def read_three_configs(self, cfg_fn):
        self.cfg = dict()
        for wc in self.wikicodes:
            self.cfg[wc] = ConfigHandler(wc, cfg_fn)

    def collect_triangles(self):
        for wc2 in self.wikicodes: # this is the bridge language
            wc1, wc3 = sorted([w for w in self.wikicodes if not w == wc2])
            for w2, tr in self.pairs[wc2].iteritems():
                for w1, src1_l in tr[wc1].iteritems():
                    for w3, src3_l in tr[wc3].iteritems():
                        for pair in product(src1_l, src3_l):
                            if wc1 < wc3:
                                self.triangles[(wc1, w1, wc3, w3)].append((
                                    pair[0][0], pair[0][1], wc2, w2, pair[1][0], pair[1][1]))
                            else:
                                self.triangles[(wc3, w3, wc1, w1)].append((
                                    pair[0][0], pair[0][1], wc2, w2, pair[1][0], pair[1][1]))

    def write_triangles(self):
        dir_ = self.get_dir()
        if not path.exists(dir_):
            makedirs(dir_)
        for wc2 in self.wikicodes:
            wc1, wc3 = sorted([w for w in self.wikicodes if not w == wc2])
            fn = dir_ + '/' + '_'.join([wc1, wc2, wc3])
            f = open(fn, 'w+')
            min_cnt = int(self.cfg_general['triangle_threshold'])
            for tri, sources in self.triangles.iteritems():
                if not tri[0] == wc1 or not tri[2] == wc3:
                    continue
                # skip if appears in the original data
                if self.cfg_general['only_new_triangles'] and \
                   tri[3] in self.pairs[wc1][tri[1]][wc3]:
                    continue
                if len(sources) >= min_cnt:
                    for s in set(sources):
                        f.write('\t'.join(tri).encode('utf8') + '\t' + 
                                '\t'.join(s).encode('utf8') + '\n')
            f.close()

    def get_dir(self):
        i = 0
        file_cnt = 1000
        while file_cnt >= 998:
            dir_ = self.cfg_general['triangle_dir'] + '/' + str(i)
            i += 1
            if not path.exists(dir_):
                break
            file_cnt = len([name for name in listdir(dir_)])
        return dir_

