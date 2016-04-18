#!/usr/bin/env python3
import argparse
from collections import defaultdict
from itertools import count, product
import re
import sys

import instructions

CODE_LINE_REGEX = re.compile(
    r'^\s*([A-Za-z]{{{},{}}})(?:\s+([-A-Za-z0-9_]+))?\s*(?:#.*)?$'.format(
        instructions.MIN_INSTRUCTION_LEN,
        instructions.MAX_INSTRUCTION_LEN))
BLANK_LINE_REGEX = re.compile(r'^\s*(?:#.*)?$')
LABEL_LINE_REGEX = re.compile(r'^\s*([-A-Za-z0-9_]+)\s*:\s*(?:#.*)?$')

BINARY_TO_WHITESPACE_TABLE = str.maketrans('01', ' \t')


def int_to_whitespace(num):
    '''Convert an integer to whitespace.'''
    if num >= 0:
        return ' ' + _pos_int_to_whitespace(num) + '\n'
    else:
        return '\t' + _pos_int_to_whitespace(-num) + '\n'


def _pos_int_to_whitespace(num):
    '''Convert a positive integer to whitespace.

    Does not include the leading space/tab to indicate sign, nor the trailing
    newline.
    '''
    return bin(num)[2:].translate(BINARY_TO_WHITESPACE_TABLE)


def label_generator():
    '''Generate whitespace labels.'''
    for length in count(1):
        for string in product(' \t', repeat=length):
            yield ''.join(string) + '\n'


def compiler(instream, outstream):
    labels = defaultdict(label_generator().__next__)
    errors = False
    for lineno, line in enumerate(instream, start=1):
        if BLANK_LINE_REGEX.match(line):
            continue

        match = CODE_LINE_REGEX.match(line)
        if match:
            instruction_label, param = match.groups()
        else:
            match = LABEL_LINE_REGEX.match(line)
            if match:
                instruction_label = 'LABEL'
                param = match.groups()[0]
            else:
                print('{}:{}: Unparsable line "{}"'.format(instream.name,
                                                           lineno,
                                                           line.strip()),
                      file=sys.stderr)
                errors = True
                continue


        try:
            instruction = instructions.INSTRUCTIONS[instruction_label]
        except KeyError:
            print('{}:{}: Unrecognized instruction "{}"'.format(
                    instream.name,
                    lineno,
                    instruction_label),
                  file=sys.stderr)
            errors = True
            continue

        if instruction.has_number:
            try:
                num = int(param)
            except ValueError:
                print('{}:{}: Unparsable number "{}"'.format(instream.name,
                                                             lineno,
                                                             param),
                      file=sys.stderr)
                errors = True
                continue
            param = int_to_whitespace(num)

        elif instruction.has_label:
            param = labels[param]

        elif param:
            print('{}:{}: Unexpected parameter "{}" to {}'.format(
                    instream.name,
                    lineno,
                    param,
                    instruction_label),
                  file=sys.stderr)
            errors = True
            continue

        outstream.write(instruction.tokens)
        if param:
            outstream.write(param)

    if errors:
        return 1
    else:
        return 0


def main(argv=None):
    if argv is None:
        argv = sys.argv

    parser = argparse.ArgumentParser(
        description="Compile code into Whitespace",
        epilog="See README.md for the code syntax")
    parser.add_argument("-o", type=argparse.FileType('w'), dest="outstream",
                        metavar="<ofile>", help="specify output destination",
                        default=sys.stdout)
    parser.add_argument("instream", type=argparse.FileType('r'),
                        metavar="<ifile>", help="specify input file")

    args = parser.parse_args(argv[1:])
    return compiler(args.instream, args.outstream)


if __name__ == '__main__':
    sys.exit(main())
