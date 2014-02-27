""" Wikt2Dict - Polygons

Usage:
    find_polygons.py (polygons|clicks) [--wc-filter=<file>] [--k=<int>] [<input>...]

Options:
    --wc-filter=<file>      Filter input to wikicodes specified in file.
    -h --help               Show this screen.
    --k=<int>               Length of polygons [default: 4].
    --output=<file>         Output location.
"""
from docopt import docopt
from sys import stdin, stderr
from collections import defaultdict
from copy import copy


def read_pairs(wc_filter=None, input_files=None, use_stdin=False):
    tri = defaultdict(set)
    if use_stdin:
        for l in stdin:
            add_pair(l, tri, wc_filter)
    elif input_files:
        for fn in input_files:
            with open(fn) as f:
                for l in f:
                    add_pair(l, tri, wc_filter)
    return tri


def add_pair(l, tri, wc_filter):
    try:
        wc1, w1, wc2, w2 = l.decode('utf8').strip().split('\t')[0:4]
        if wc_filter and (not wc1 in wc_filter or not wc2 in wc_filter):
            return
        tri[(wc1, w1)].add((wc2, w2))
        tri[(wc2, w2)].add((wc1, w1))
    except ValueError:
        stderr.write('Invalid line: {0}'.format(l))


def find_and_print_polygons(pairs, found=None, k=4, mode='polygons'):
    if not found:
        for w1, words in pairs.iteritems():
            found = [w1]
            find_and_print_polygons(pairs, found=found, mode=mode)
    else:
        last = found[-1]
        for w2 in pairs[last]:
            if len(found) == k and w2 == found[0]:
                found.append(w2)
                output(pairs, found, mode=mode)
            elif len(found) >= k:
                return
            else:
                if w2 in found:
                    continue
                found.append(w2)
                find_and_print_polygons(pairs, found=copy(found), mode=mode)


def output(pairs, found, mode):
    edge_density, new_pairs = edge_density_and_new_pairs(pairs, found)
    if mode == 'clicks' and edge_density == 1.0:
        for pair in new_pairs:
            print('\t'.join(pair[0]).encode('utf8') + '\t' + str(edge_density) + '\t' +
                  (' --> '.join(', '.join(i) for i in found)).encode('utf8'))
    elif mode == 'polygons':
        for pair in new_pairs:
            print('\t'.join(pair[0]).encode('utf8') + '\t' +
                  '\t'.join(pair[1]).encode('utf8') + '\t' +
                  str(edge_density) + '\t' +
                  (' --> '.join(', '.join(i) for i in found)).encode('utf8'))


def edge_density_and_new_pairs(pairs, cycle):
    new_pairs = list()
    all_pairs = list()
    n = (len(cycle) - 1) * (len(cycle) - 2) / 2
    for i, e1 in enumerate(cycle):
        for e2 in cycle[i+1:-1]:
            all_pairs.append(sorted([e1, e2]))
            if not e2 in pairs[e1]:
                new_pairs.append(sorted([e1, e2]))
    print len(all_pairs), len(new_pairs)
    return float(len(new_pairs)) / n, new_pairs


def main():
    arguments = docopt(__doc__, version="Wikt2dict/Polygons 0.1")
    if arguments['--wc-filter']:
        with open(arguments['--wc-filter']) as f:
            wc_filter = set([wc.strip() for wc in f])
    else:
        wc_filter = None
    k = int(arguments['--k'])
    if arguments['<input>']:
        pairs = read_pairs(wc_filter, input_files=arguments['<input>'])
    else:
        pairs = read_pairs(wc_filter, use_stdin=True)
    stderr.write('Pairs read\n')
    stderr.write('Number of pairs {0}\n'.format(
        sum(len(v) for v in pairs.values()) / 2))
    if arguments['polygons']:
        find_and_print_polygons(pairs, k=k, mode='polygons')
    else:
        find_and_print_polygons(pairs, k=k, mode='clicks')

if __name__ == '__main__':
    main()
