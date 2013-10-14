from collections import defaultdict
from os import listdir
from sys import stdin
import logging

class Evaluator(object):
    """ This class compares and evaluates exisiting dictionaries """

    def __init__(self, cfg):
        self.wikt = defaultdict(lambda: defaultdict(lambda:
                     defaultdict(lambda: defaultdict(int))))

        self.cfg = cfg

    def read_all_wiktionary(self):
        for lang in listdir(self.cfg['dumpdir']):
            logging.info(lang)
            self.read_wiktionary(self.cfg['dumpdir'] + '/' + lang + 
                                '/' + self.cfg['word_pairs_outfile'])

    def read_wiktionary(self, fn):
        try:
            f = open(fn)
        except IOError:
            logging.info('{0} does not exist'.format(fn))
            return
        for l in f:
            try:
                l_ = l.decode('utf8').strip().split('\t')
                if len(l_) < 4:
                    logging.warning('Line too short: {0}'.format(l.strip()))
                    continue
                wc1, w1, wc2, w2 = self.get_ordered_pair(l_[0:4])
                self.wikt[wc1][w1][wc2][w2] += 1
            except:
                logging.exception('Exception at line: {0}'.format(l.strip()))

    def get_ordered_pair(self, fields):
        wc1, w1, wc2, w2 = fields
        if wc1 == 'cmn':
            wc1 = 'zh'
        if wc2 == 'cmn':
            wc2 = 'zh'
        if wc1 < wc2 or (wc1 == wc2 and w1 < w2):
            return wc1, w1, wc2, w2
        return wc2, w2, wc1, w1

    def compare_with_triangles_stdin(self):
        for l in stdin:
            try:
                l_ = l.decode('utf8').strip().split('\t')
                if len(l_) < 10:
                    logging.warning('Line too short: {0}'.format(l.strip()))
                    continue
                wc1, w1, wc2, w2 = self.get_ordered_pair(l_[0:4])
                if self.wikt[wc1][w1][wc2][w2] > 0:
                    print l.strip() + '\t1'
                else:
                    print l.strip() + '\t0'
            except:
                raise



