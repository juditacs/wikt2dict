from sys import argv, stdin, stderr

def main():
    filt = set()
    mode = argv[2]
    with open(argv[1]) as f:
        for l in f:
            fd = l.decode('utf8').strip().lower().split('\t')
            if len(fd) < 4:
                stderr.write('Error on line {1}'. format(l))
                continue
            filt.add(tuple(fd[0:4]))
    stderr.write('Filter file read\n')
    cnt = 0
    for l in stdin:
        cnt += 1
        if cnt % 1000000 == 0:
            stderr.write('{0}\n'.format(cnt))
        fd = l.decode('utf8').strip().lower().split('\t')
        if len(fd) < 4:
            stderr.write('Error on line {1}'. format(l))
            continue
        if mode == 'pos' and tuple(fd[0:4]) in filt:
            print l.strip()
        elif mode == 'neg' and not tuple(fd[0:4]) in filt:
            print l.strip()


if __name__ == '__main__':
    main()
