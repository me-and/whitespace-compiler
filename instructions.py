class Instruction(object):
    def __init__(self, tokens, has_number=False, has_label=False):
        self.tokens = tokens
        self.has_number = has_number
        self.has_label = has_label


INSTRUCTIONS = {'PUSH': Instruction('  ', has_number=True),
                'DUPE': Instruction(' \n '),
                'SWAP': Instruction(' \n\t'),
                'DROP': Instruction(' \n\n'),
                'ADD': Instruction('\t   '),
                'SUB': Instruction('\t  \t'),
                'MUL': Instruction('\t  \n'),
                'DIV': Instruction('\t \t '),
                'MOD': Instruction('\t \t\t'),
                'STORE': Instruction('\t\t '),
                'RETRV': Instruction('\t\t\t'),
                'LABEL': Instruction('\n  ', has_label=True),
                'GOSUB': Instruction('\n \t', has_label=True),
                'JMP': Instruction('\n \n', has_label=True),
                'JEZ': Instruction('\n\t ', has_label=True),
                'JLZ': Instruction('\n\t\t', has_label=True),
                'RETURN': Instruction('\n\t\n'),
                'END': Instruction('\n\n\n'),
                'PUTC': Instruction('\t\n  '),
                'PUTN': Instruction('\t\n \t'),
                'GETC': Instruction('\t\n\t '),
                'GETN': Instruction('\t\n\t\t')}

MIN_INSTRUCTION_LEN = min(map(len, INSTRUCTIONS))
MAX_INSTRUCTION_LEN = max(map(len, INSTRUCTIONS))
