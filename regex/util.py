import random
from regex import excptions as E

MAX_REPITION = 20
ASCII_CHARACTER = list(range(33,127))
ASCII_CHARACTER_SET = set(range(33, 127))
QUANTIFIER = {'*', '+', '?'}

def get_random_ascii_character():
    return chr(random.choice(ASCII_CHARACTER))
    
def is_contructor_negated(regex):
    if regex[0] == '^':
        return 1
    else:
        return 0

def get_range_between(start, end):
    _start = ord(start)
    _end = ord(end)
    if(_start > _end):
        raise E.InvalidRangeException()
    return set(range(_start, _end + 1))

def get_options_from_constructor_string(character_constructor):
    options = set()
    string = character_constructor.string
    if(character_constructor.is_dot and string =='.'):
        return ASCII_CHARACTER
    is_negated = is_contructor_negated(string)
    size = len(string)
    i, previous = is_negated, ''
    while i < size: 
        if(string[i] == '-' and previous != ''):
            options = options.union(get_range_between(previous, string[i+1]))
            i += 2
            previous = ''
        else:
            options.add(ord(string[i]))
            previous = string[i]
            i += 1
    if is_negated == 1:
        options = list(ASCII_CHARACTER_SET - options)
    else:
        options = list(options)
    return options

def get_number_of_repetition(quantifier):
    if quantifier == '?':
        return random.choice([0,1])
    elif quantifier == '+':
        return random.choice(list(range(1, MAX_REPITION)))
    elif quantifier == '*':
        return random.choice(list(range(0, MAX_REPITION)))
    else:
        if "," in quantifier:
            start, end = quantifier.split(",")
            return random.choice(list(range(int(start), int(end) + 1)))
        else:
            if quantifier.isnumeric():
                return int(quantifier);
            else:
                raise E.InvalidQuantifierException()

