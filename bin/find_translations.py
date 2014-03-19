from sys import argv, stdin, stderr
from collections import defaultdict
import json


def read_table(fn):
    mapping = defaultdict(set)
    with open(fn) as f:
        for l in f:
            fd = l.decode('utf8').strip().split('\t')
            id_ = int(fd[0])
            for i, lang in enumerate(['en', 'hu', 'la', 'pl']):
                if fd[i + 1] == '#':
                    continue
                for word in fd[i + 1].split('/'):
                    mapping[(lang, word.replace('_', ' '))].add(id_)
    return mapping


def read_words(fn):
    words = set()
    with open(fn) as f:
        for l in f:
            fd = l.decode('utf8').strip().split('\t')
            if len(fd) >= 2:
                words.add((fd[0], fd[1]))
                if len(fd) >= 4:
                    words.add((fd[2], fd[3]))
    return words


def find_translations(words):
    iter_no = 0
    for l in stdin:
        iter_no += 1
        if iter_no % 1000000 == 0:
            stderr.write('{}\n'.format(iter_no))
        try:
            fd = l.decode('utf8').strip().split('\t')
            pair1 = (fd[0], fd[1])
            pair2 = (fd[2], fd[3])
            if pair1 in words:
                print('\t'.join(fd[0:4] + list(pair1)).encode('utf8'))
            if pair2 in words:
                print('\t'.join(fd[0:4] + list(pair2)).encode('utf8'))
        except ValueError:
            stderr.write('Error in line {}'.format(l))


def add_orig_bindings(mapping, translations):
    for (wc, word), ids in mapping.iteritems():
        for id_ in ids:
            translations[id_][wc].add(word)


def find_translations_to_table(mapping):
    iter_no = 0
    translations = defaultdict(lambda: defaultdict(set))
    add_orig_bindings(mapping, translations)
    for l in stdin:
        iter_no += 1
        if iter_no % 1000000 == 0:
            stderr.write('{}\n'.format(iter_no))
        try:
            fd = l.decode('utf8').strip().split('\t')
            wc1, w1, wc2, w2 = fd[0:4]
            if wc1 == 'roa_rup' or wc2 == 'roa_rup':
                continue
            wc1 = 'zh' if wc1 == 'cmn' else wc1
            wc2 = 'zh' if wc2 == 'cmn' else wc2
            pair1 = (wc1, w1)
            pair2 = (wc2, w2)
            for id_ in mapping[pair1]:
                translations[id_][wc2].add(w2)
            for id_ in mapping[pair2]:
                translations[id_][wc1].add(w1)
        except ValueError:
            stderr.write('Error in line {}'.format(l))
    for id_, trans in translations.iteritems():
        trans_to_dump = dict()
        for wc, words in trans.iteritems():
            trans_to_dump[wc] = sorted(words)
        print('{0}\t{1}'.format(id_, json.dumps(trans_to_dump)))
        #out_str = [str(id_)]
        #for wc, words in sorted(trans.iteritems()):
            #out_str.append(u'{0}:{1}'.format(wc, ','.join(sorted(words))))
        #print('\t'.join(out_str).encode('utf8'))


def main():
    mode = argv[2] if len(argv) > 2 else 'direct'
    if mode == 'direct':
        words = read_words(argv[1])
        find_translations(words)
    elif mode == 'collect':
        table = read_table(argv[1])
        find_translations_to_table(table)

if __name__ == '__main__':
    main()
