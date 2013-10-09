from sys import argv, path
path.append('../src')

from evaluator import Evaluator

def main():
    fn_l = argv[1:]
    e = Evaluator()
    e.read_all_dicts(fn_l)
    print e.dicts['quick_test']['alma']

if __name__ == '__main__':
    main()
