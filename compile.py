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
    if num >= 0:
        return ' ' + pos_int_to_whitespace(num) + '\n'
    else:
        return '\t' + pos_int_to_whitespace(-num) + '\n'


def pos_int_to_whitespace(num):
    return bin(num)[2:].translate(BINARY_TO_WHITESPACE_TABLE)


def label_generator():
    for length in count(1):
        for string in product(' \t', repeat=length):
            yield ''.join(string) + '\n'


if __name__ == '__main__':
    labels = defaultdict(label_generator().__next__)
    for lineno, line in enumerate(sys.stdin, start=1):
        if BLANK_LINE_REGEX.match(line):
            continue
        match = CODE_LINE_REGEX.match(line)
        if not match:
            raise RuntimeError(
                'Compile error: line {}: "{}"'.format(lineno, line.strip()))
        instruction_label, param = match.groups()
        instruction = instructions.INSTRUCTIONS[instruction_label]
        if instruction.has_number:
            param = int_to_whitespace(int(param))
        elif instruction.has_label:
            param = labels[param]
        elif param:
            raise RuntimeError(
                'Unexpected parameter {} to instruction {}'.format(
                    param, instruction_label))
        sys.stdout.write(instruction.tokens)
        if param:
            sys.stdout.write(param)
