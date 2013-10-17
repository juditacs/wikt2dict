from collections import defaultdict
from os import listdir
from sys import stdin
import logging

class Evaluator(object):
    """ This is a collection of methods for evaluating the results of 
    triangulation. Most methods add features to the triangles """

    def __init__(self, cfg):
        self.wikt = defaultdict(lambda: defaultdict(lambda:
                     defaultdict(lambda: defaultdict(int))))

        self.cfg = cfg
        self.edge_gran = range(11) + [20, 30]
        self.pivot_gran = self.edge_gran

        with open(self.cfg['wikicodes']) as f:
            self.wikicodes = sorted([w.strip() for w in f])
        self.feat_order = []
        self.feat_order.extend(['left_' + wc for wc in self.wikicodes])
        self.feat_order.extend(['right_' + wc for wc in self.wikicodes])
        self.feat_order.extend(['pivot_' + str(i) for i in self.pivot_gran])
        self.feat_order.extend(['left_' + str(i) for i in self.edge_gran])
        self.feat_order.extend(['right_' + str(i) for i in self.edge_gran])
        self.feat_order.extend(['pivot_langs_' + str(i) for i in self.pivot_gran])
        self.feat_order.extend(['left_langs_' + str(i) for i in self.edge_gran])
        self.feat_order.extend(['right_langs_' + str(i) for i in self.edge_gran])
        for wc in self.wikicodes:
            self.feat_order.extend([wc + '_pivot_' + str(i) for i in self.pivot_gran])
        for wc in self.wikicodes:
            self.feat_order.extend([wc + '_left_' + str(i) for i in self.edge_gran])
        for wc in self.wikicodes:
            self.feat_order.extend([wc + '_right_' + str(i) for i in self.edge_gran])

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
        """ Order pairs alphabetically by Wiktionary codes. 
        TODO this method should be moved to a static class containing 
        often used methods """
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
                logging.exception('Exception at line: {0}'.format(l.strip()))

    def featurize_and_uniq_triangles_stdin(self):
        tri_group = set()
        tri_group_head = None
        for l in stdin:
            try:
                l_ = l.decode('utf8').strip().split('\t')
                this_tri = '\t'.join(l_[0:4])
                if not tri_group_head:
                    tri_group_head = this_tri
                    tri_group.add(tuple(l_))
                elif tri_group_head == this_tri:
                    tri_group.add(tuple(l_))
                else:
                    if tri_group:
                        feat, pair = self.featurize_group(tri_group)
                        self.print_pair_with_features(pair, feat)
                    tri_group = set()
                    tri_group.add(tuple(l_))
                    tri_group_head = this_tri
            except:
                logging.exception('Exception at line: {0}'.format(l.strip()))
        feat, pair = self.featurize_group(tri_group)
        self.print_pair_with_features(pair, feat)
               
    def print_pair_with_features(self, pair, feat):
        out = u''
        out += '\t'.join(pair)
        for f in self.feat_order:
            if not f in feat:
                logging.info('%s not in features' % f)
            out += '\t{0}'.format(feat[f])
        print out.encode('utf8')

    def featurize_group(self, group):
        feats = defaultdict(int)
        feats['total'] = len(group)
        left = set()
        right = set()
        pivots = set()
        pair = list()
        for i in group:
            left.add(tuple(i[4:6]))
            pivots.add(tuple(i[6:8]))
            right.add(tuple(i[8:10]))
            pair = i[0:4]
            if len(i) > 10:
                feats['in_wikt'] = int(i[10])
        self.map_int_feature_to_binaries('left', len(left), self.edge_gran, feats)
        self.map_int_feature_to_binaries('right', len(right), self.edge_gran, feats)
        self.map_int_feature_to_binaries('pivot', len(pivots), self.pivot_gran, feats)
        pivot_langs = len(set([lang for lang, _ in pivots]))
        self.map_int_feature_to_binaries('pivot_langs', pivot_langs, 
                                         self.pivot_gran, feats)
        left_langs = len(set([lang for lang, _ in left]))
        self.map_int_feature_to_binaries('left_langs', left_langs, 
                                         self.edge_gran, feats)
        right_langs = len(set([lang for lang, _ in right]))
        self.map_int_feature_to_binaries('right_langs', right_langs, 
                                         self.edge_gran, feats)
        self.add_wc_features(pair, feats)

        self.map_int_feature_to_binaries_by_wc('_pivot', pivots, 
                                               self.pivot_gran, feats)
        self.map_int_feature_to_binaries_by_wc('_left', left, 
                                               self.edge_gran, feats)
        self.map_int_feature_to_binaries_by_wc('_right', right, 
                                               self.edge_gran, feats)
        return feats, pair

    def map_int_feature_to_binaries_by_wc(self, pre, vals, granularity, feat_dict):
        val_wc = defaultdict(int)
        for wc, _ in vals:
            val_wc[wc] += 1
        for wc in self.wikicodes:
            self.map_int_feature_to_binaries(wc + pre, val_wc[wc], 
                                             granularity, feat_dict)

    def add_wc_features(self, pair, feat_dict):
        for wc in self.wikicodes:
            if wc == pair[0]:
                feat_dict[wc + '_left'] = 1
            else:
                feat_dict[wc + '_left'] = 0
            if wc == pair[2]:
                feat_dict[wc + '_right'] = 1
            else:
                feat_dict[wc + '_right'] = 0

    def map_int_feature_to_binaries(self, feat_prefix, val, granularity, feat_dict, 
                                    mode='le'):
        for i in granularity:
            feat_name = feat_prefix + '_' + str(i)
            if mode == 'le' and i <= val:
                feat_dict[feat_name] = 1
            elif mode == 'eq' and val == i:
                feat_dict[feat_name] = 1
            else:
                feat_dict[feat_name] = 0


