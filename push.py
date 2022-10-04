from subprocess import run
import os
import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Pushes a Dir to a remote Host via SCP')
    parser.add_argument('-lPath', type=str, default="./", help='local path')
    parser.add_argument('-rPath', type=str, default="/home/pi/temp", help='remote path')
    parser.add_argument('-r', type=str, default="192.168.178.40", help='remote IP address')
    parser.add_argument('-rUser', type=str, default="pi", help='remote user')
    parser.add_argument('-i', type=str, default="to_ignore.ini", help='files to ignore, seperated by linebreaks')
    args = parser.parse_args()

    with open(args.i, "r") as f:
        to_ignore = f.readlines()

    to_move = []
    for (dirpath, dirnames, filenames) in os.walk(args.lPath):
        for filename in filenames:
            if filename in to_ignore:
                continue
            to_move.append(os.path.join(dirpath, filename))
        break

    for file in to_move:
        run(["scp", file, f"{args.rUser}@{args.r}:{args.rPath}"])
