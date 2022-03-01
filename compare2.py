
import argparse


def get_args():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('-ll', '--logleft', required=True, action='store', default='.', help="log file")
    parser.add_argument('-lr', '--logright', required=True, action='store', default='.', help="log file")

    return parser.parse_args()

def parse(line):
    d = line.split()
    frame = int(d[0])
    id = int(d[1])
    return frame, id

def readlog(log):
    seen = []
    with open(log, 'r+') as logfile:
        lines = logfile.readlines()
        for line in lines:
            frameid, idx = parse(line)
            if idx != 10:
                seen.append(frameid, id)

    return seen
            

def compare(leftlog, rightlog):
    leftdata = readlog(leftlog)
    rightdata = readlog(rightlog)
    inleft = set(leftdata)
    inboth = []
    for frameid, idx in rightdata:
        if (frameid, idx) in inleft:
            inboth.append((frameid, idx))
    seen = set()
    for frameid, _ in inboth:
        seen.add(frameid)
    print(len(seen))

def main():
    args = get_args()
    leftlog = args.logleft
    rightlog = args.logright

    compare(leftlog, rightlog)

if __name__ == '__main__':
    main()