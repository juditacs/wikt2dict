from sys import argv, stderr, path
path.append('../src')


from handlers import ConfigHandler
from triangulator import Triangulator

def main():
    cfg_fn = argv[1]
    cfg = ConfigHandler("general", cfg_fn)
    with open(cfg['wikicodes']) as wc_f:
        wikicodes = set([w.strip() for w in wc_f])
    triangulator = Triangulator(cfg_fn=cfg_fn, all_wc=wikicodes)
    out_base = argv[2]
    for pairs in set(argv[3:]):
        stderr.write(pairs + '\n')
        wc1, wc2 = pairs.split('-')
        if wc1 < wc2:
            out_fn = out_base + wc1 + '_' + wc2 + '.tri.dict'
        else:
            out_fn = out_base + wc2 + '_' + wc1 + '.tri.dict'
        triangulator.set_two_langs(wc1, wc2)
        triangulator.collect_50_triangles()
        triangulator.write_50_triangles(out_fn, wc1, wc2)

if __name__ == '__main__':
    main()

