#!/usr/bin/env python3
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


def compiler(instream, instream_name, outstream):
    labels = defaultdict(label_generator().__next__)
    errors = False
    for lineno, line in enumerate(instream, start=1):
        if BLANK_LINE_REGEX.match(line):
            continue

        match = CODE_LINE_REGEX.match(line)
        if not match:
            print('{}:{}: Unparsable line "{}"'.format(instream_name,
                                                       lineno,
                                                       line.strip()),
                  file=sys.stderr)
            errors = True
            continue

        instruction_label, param = match.groups()

        try:
            instruction = instructions.INSTRUCTIONS[instruction_label]
        except KeyError:
            print('{}:{}: Unrecognized instruction "{}"'.format(
                    instream_name,
                    lineno,
                    instruction_label),
                  file=sys.stderr)
            errors = True
            continue

        if instruction.has_number:
            try:
                num = int(param)
            except ValueError:
                print('{}:{}: Unparsable number "{}"'.format(instream_name,
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
                    instream_name,
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


if __name__ == '__main__':
    sys.exit(compiler(sys.stdin, '-', sys.stdout))
