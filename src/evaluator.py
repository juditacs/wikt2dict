from collections import defaultdict
import logging

class Evaluator(object):
    """ This class compares and evaluates exisiting dictionaries """

    def __init__(self, cfg):
        self.dicts = dict()
        self.wordlists = dict()
        self.cfg = cfg

    def read_all_dicts(self, dicts_fn):
        for dict_fn in dicts_fn:
            self.read_one_dict(dict_fn)

    def read_one_dict(self, dict_fn):
        f = open(dict_fn)
        key = self.get_dict_name(dict_fn)
        self.dicts[key] = defaultdict(lambda: {'cnt':0})
        for l in f:
            fd = l.decode('utf8').strip().split('\t')
            if len(fd) < 4:
                logging.error('Line too short in file {0}: {1}'.format(
                    dict_fn, l.strip()))
                continue
            wc1, w1, wc2, w2 = fd[0:4]
            if wc1 < wc2 or (wc1 == wc2 and w1 < w2):
                pair = (fd[0:4])
            else:
                pair = (wc2, w2, wc1, w1)
            self.dicts[key][pair]['rest'] = fd[4:]
            self.dicts[key][pair]['cnt'] += 1
        f.close()

    def get_dict_name(self, fn):
        return fn.split('/')[-1].split('.')[0]

    def compare_to_wordlist(self, wordlist_key, dict_key):
        if not wordlist_key in self.wordlists:
            logging.error('No such wordlist')
            return
        if not dict_key in self.dicts:
            logging.error('No such dictionary')
            return

