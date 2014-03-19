from sys import argv

from evaluator import Evaluator


def main():
    mode = argv[1]
    e = Evaluator()
    if mode == 'wikt':
        e.read_all_wiktionary()
        e.compare_with_triangles_stdin()
    elif mode == 'feat':
        e.write_labels(argv[2])
        e.featurize_and_uniq_triangles_stdin()

if __name__ == '__main__':
    main()
