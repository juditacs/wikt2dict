from sys import stdin, stderr, stdout
from collections import defaultdict
from optparse import OptionParser

def read_triangles(cfg):
    val = None
    type_ = None
    i = 0
    pair = None
    for l in stdin:
        i += 1
        if i % 100000 == 0:
            stderr.write(str(i) + '\n')
        try:
            l_ = l.decode('utf8').strip()
            if cfg.lower:
                fd = l_.lower().split('\t')
            else:
                fd = l_.split('\t')
            if not pair:
                pair = tuple(fd[0:4])
            if not val:
                if len(fd) < 6:
                    val = 0
                    type_ = 'conf'
                else:
                    val = defaultdict(int)
                    type_ = 'src'
            if pair == tuple(fd[0:4]):
                if type_ == 'conf':
                    val += int(fd[4])
                elif type_ == 'src':
                    val[tuple(fd[4:8])] += 1
                continue
            print_merged(pair, val, type_, cfg)
            pair = tuple(fd[0:4])
            if len(fd) < 6:
                val = int(fd[4])
                type_ = 'conf'
            else:
                val = defaultdict(int)
                val[tuple(fd[4:8])] += 1
                type_ = 'src'
        except ValueError as e:
            stderr.write('ValueError, is the current line well-formed? {0} {1}'.format(
                l, e.message))
        except Exception:
            raise

def print_merged(pair, val, type_, cfg):
    # if only conf appears in the output
    if type_ == 'conf':
        stdout.write('\t'.join(pair).encode('utf8') + '\t' + str(val) + '\n')
    # if you chose simple summarization
    elif cfg.summarize:
        stdout.write('\t'.join(pair).encode('utf8') + '\t' + 
                     str(sum(val.values())) + '\n')
    # just print everything we have with the number of times it appears
    elif cfg.print_all_sources:
        for k, v in val.iteritems():
            stdout.write('\t'.join(pair).encode('utf8') + '\t' + 
                         '\t'.join(k).encode('utf8') + '\t' + str(v) + '\n')
    # smart filtering of different sources
    elif cfg.smart:
        conf = get_smart_filter(val)
        stdout.write('\t'.join(pair).encode('utf8') + '\t' + str(conf) + '\n')

def get_smart_filter(sources):
    if len(sources) == 1:
        return 1
    hits = [set(), set()]
    for src in sources:
        hits[0].add(tuple(src[0:2]))
        hits[1].add(tuple(src[2:4]))
    return min([len(h) for h in hits])

def parse_opts():
    p = OptionParser()
    p.add_option('-l', '--lower', dest='lower', action='store_true',
                 default=False, help='lower all words')
    p.add_option('-s', '--summarize', dest='summarize', action='store_true',
                 default=False, help='')
    p.add_option('-p', '--print-all-sources', dest='print_all_sources', 
                 action='store_true', default=False, help='')
    p.add_option('-f', '--smart-filter', dest='smart', 
                 action='store_true', default=False, help='')
    return p.parse_args()[0]

def main():
    cfg = parse_opts()
    read_triangles(cfg)
    
if __name__ == '__main__':
    main()
