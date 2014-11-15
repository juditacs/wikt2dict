""" Wikt2Dict - Polygons

Usage:
    find_polygons.py (polygons|clicks) [--illustrate] [--wc-filter=<file>] [--k=<int>] [<input>...]

Options:
    --wc-filter=<file>      Filter input to wikicodes specified in file.
    -h --help               Show this screen.
    --k=<int>               Length of polygons [default: 4].
    --output=<file>         Output location.
    --illustrate            Use ASCII art in output.
"""
from docopt import docopt
from sys import stdin, stderr
from collections import defaultdict
#from copy import copy


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


def find_k_long_polygons(pairs, k):
    if k == 1:
        for word in pairs.keys():
            yield [word]
    else:
        for polygon in find_k_long_polygons(pairs, k - 1):
            for word in pairs[polygon[-1]]:
                if not word in polygon[1:]:
                    yield polygon + [word]


def find_and_print_polygons(pairs, found=None, k=4, mode='polygons'):
    for polygon in find_k_long_polygons(pairs, k + 1):
        if polygon[0] == polygon[-1]:
            output(pairs, found=polygon, mode=mode)


def find_k_clicks(pairs, k):
    if k == 1:
        for word in pairs.keys():
            yield [word]
    else:
        for click in find_k_clicks(pairs, k - 1):
            if len(click) > k - 1:
                continue
            for word in pairs[click[-1]]:
                if word in click:
                    continue
                bad = False
                for c in click[:-2]:
                    if not word in pairs[c]:
                        bad = True
                if not bad:
                    click.append(word)
                    yield click


def find_and_print_clicks(pairs, k=4):
    for click in find_k_clicks(pairs, k):
        output(pairs, found=sorted(click), mode='clicks')


def output(pairs, found, mode):
    edge_density, new_pairs = edge_density_and_new_pairs(pairs, found)
    if mode == 'clicks' and edge_density == 1.0:
        if arguments['--illustrate']:
            print(' --> '.join(', '.join([i, j]) for i, j in found).encode('utf8'))
        else:
            print('\t'.join('\t'.join([i, j]) for i, j in found).encode('utf8'))
    elif mode == 'polygons':
        for pair in new_pairs:
            if arguments['--illustrate']:
                print('\t'.join(pair[0]).encode('utf8') + '\t' +
                      '\t'.join(pair[1]).encode('utf8') + '\t' +
                      str(edge_density) + '\t' +
                      (' --> '.join(', '.join(i) for i in found)).encode('utf8'))
            else:
                print('\t'.join(pair[0]).encode('utf8') + '\t' +
                      '\t'.join(pair[1]).encode('utf8') + '\t' +
                      str(edge_density) + '\t' +
                      ('\t'.join('\t'.join(i) for i in found)).encode('utf8'))


def edge_density_and_new_pairs(pairs, cycle):
    new_pairs = list()
    all_pairs = list()
    for i, e1 in enumerate(cycle):
        for e2 in cycle[i + 1:-1]:
            all_pairs.append(sorted([e1, e2]))
            if not e2 in pairs[e1] and not e1 in pairs[e2]:
                new_pairs.append(sorted([e1, e2]))
    n = len(all_pairs)
    return 1 - float(len(new_pairs)) / (n * (n - 1) / 2), new_pairs

arguments = docopt(__doc__, version="Wikt2dict/Polygons 0.1")


def main():
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
        #find_and_print_polygons(pairs, k=k, mode='clicks')
        find_and_print_clicks(pairs, k=k)

if __name__ == '__main__':
    main()
