#!/usr/bin/env python

from collections import defaultdict
import argparse
import sys


def counter(gen, flags):
    default = not flags
    counts = defaultdict(int)
    for buffer in gen:
        if 'lines' in flags or default:
            counts['lines'] += buffer.count(b'\n')
        if 'words' in flags or default:
            counts['words'] += len(buffer.split())
        if 'chars' in flags:
            counts['chars'] += len(buffer.decode())
        if 'bytes' in flags or default:
            counts['bytes'] += len(buffer)
    return counts


def gen_file_reader(file):
    # If input is from stdin, convert to binary
    if file.name == '<stdin>':
        for line in file:
            yield line
    for chunk in file:
        yield chunk


def main():
    parser = argparse.ArgumentParser(
        prog='ccwc',
        description='python implementation of Unix wc command',
        epilog='https://codingchallenges.fyi/challenges/challenge-wc/'
    )

    parser.add_argument('file', nargs='?', type=argparse.FileType(
        mode='rb', bufsize=1024 * 1024), default=sys.stdin.buffer)
    parser.add_argument('-l', '--lines', action='store_true',
                        help='print the newline counts')
    parser.add_argument('-w', '--words', action='store_true',
                        help='print the word counts')
    parser.add_argument('-m', '--chars', action='store_true',
                        help='print the character counts')
    parser.add_argument('-c', '--bytes', action='store_true',
                        help='print the byte counts')

    args = parser.parse_args()

    # Get set flags
    flags = {key for (key, value) in vars(args).items() if value == True}

    try:
        data = gen_file_reader(args.file)
        counts = counter(data, flags)

        output = []
        if len(flags) > 1:
            output.append(' ')
        # Convert integers to strings and add to output array
        output.extend(map(str, counts.values()))
        if args.file.name != '<stdin>':
            output.append(args.file.name)

        sys.stdout.write(' '.join(output) + '\n')
    except Exception as e:
        sys.stderr.write(f'Error: {e}\n')


if __name__ == "__main__":
    main()
