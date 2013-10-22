from sys import argv, path
path.append('../src')

from evaluator import Evaluator
from handlers import ConfigHandler

def main():
    mode = argv[2]
    cfg = ConfigHandler('general', argv[1])
    e = Evaluator(cfg)
    if mode == 'wikt':
        e.read_all_wiktionary()
        e.compare_with_triangles_stdin()
    elif mode == 'feat':
        e.write_labels(argv[3])
        e.featurize_and_uniq_triangles_stdin()

if __name__ == '__main__':
    main()
