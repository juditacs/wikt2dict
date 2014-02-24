from sys import stdin, argv, stderr
from collections import defaultdict
from copy import copy

k = int(argv[-1])

def read_triangles(wc_filter):
    tri = defaultdict(set)
    for l in stdin:
        wc1, w1, wc2, w2 = l.decode('utf8').strip().split('\t')[0:4]
        if wc_filter and (not wc1 in wc_filter or not wc2 in wc_filter):
            continue
        tri[(wc1, w1)].add((wc2, w2))
        tri[(wc2, w2)].add((wc1, w1))
    return tri


def find_and_print_quads(triangles, found=None):
    if not found:
        for w1, words in triangles.iteritems():
            found = [w1]
            find_and_print_quads(triangles, found=found)
    else:
        last = found[-1]
        for w2 in triangles[last]:
            if len(found) == k and w2 == found[0]:
                found.append(w2)
                output(triangles, found)
            elif len(found) >= k:
                return
            else:
                if w2 in found:
                    continue
                found.append(w2)
                find_and_print_quads(triangles, copy(found))


def output(triangles, found, wc_filter=None):
    new_pair1 = found[0] + found[2]
    new_pair2 = found[1] + found[3]
    edge_density = get_edge_density(triangles, found)
    if not (new_pair1[0], new_pair1[1]) in triangles[(new_pair1[2], new_pair1[3])]:
        print('\t'.join(new_pair1).encode('utf8') + '\t' + str(edge_density) + '\t' +
              (' --> '.join(', '.join(i) for i in found)).encode('utf8'))
    if not (new_pair2[0], new_pair2[1]) in triangles[(new_pair2[2], new_pair2[3])]:
        print('\t'.join(new_pair2).encode('utf8') + '\t' + str(edge_density) + '\t' +
              (' --> '.join(', '.join(i) for i in found)).encode('utf8'))


def get_edge_density(triangles, cycle):
    n = len(cycle) - 1
    s = n * (n-1) / 2
    d = 0
    for i, e1 in enumerate(cycle):
        for e2 in cycle[i+1:-1]:
            if e2 in triangles[e1]:
                d += 1
    return float(d)/s


def main():
    if len(argv) > 1:
        with open(argv[1]) as f:
            wc_filter = set([wc.strip() for wc in f])
    else:
        wc_filter = None
    triangles = read_triangles(wc_filter)
    stderr.write('Triangles read\n')
    stderr.write('Number of triangles {0}\n'.format(
        sum(len(v) for v in triangles.values()) / 2))
    find_and_print_quads(triangles)

if __name__ == '__main__':
    main()
