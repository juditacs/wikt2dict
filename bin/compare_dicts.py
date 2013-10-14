from sys import argv, path
path.append('../src')

from evaluator import Evaluator
from handlers import ConfigHandler

def main():
    cfg = ConfigHandler('general', argv[1])
    e = Evaluator(cfg)
    e.read_all_wiktionary()
    e.compare_with_triangles_stdin()

if __name__ == '__main__':
    main()
