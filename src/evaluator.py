from collections import defaultdict
import logging

class Evaluator(object):

    def __init__(self):
        self.dicts = dict()
        pass

    def read_all_dicts(self, dicts_fn):
        for dict_fn in dicts_fn:
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
                    self.dicts[key][(fd[0:4])]['rest'] = fd[4:]
                    self.dicts[key][(fd[0:4])]['cnt'] += 1
                else:
                    self.dicts[key][(wc2, w2, wc1, w1)]['rest'] = fd[4:]
                    self.dicts[key][(wc2, w2, wc1, w1)]['cnt'] += 1

            f.close()

    def get_dict_name(self, fn):
        return fn.split('/')[-1].split('.')[0]


