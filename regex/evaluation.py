from regex import util 
from regex import excptions as E
import random

class Character:
    def __init__(self, string = None , quantifier = None, is_dot = False):
        """
            constructor
        """
        self.string = string
        self.quantifier = quantifier
        self.evaluated_string = None
        self.is_dot = is_dot

    def set_quantifier(self, regex, index):
        """
            sets the quantifier based on the regex string for the current Character object
        """
        if regex[index] in util.QUANTIFIER: # if the quantifier is among ?, +, *
            self.quantifier = regex[index]
            return index  
        elif regex[index] == '{': # if the quantifier is of type {a,b}
            temp_quantifier = ""
            index += 1
            try:
                while(regex[index] != '}'):
                    temp_quantifier += regex[index]
                    index += 1
                self.quantifier = temp_quantifier
                return index
            except IndexError:
                raise E.MinMaxQuantifierMismatchExcetpion() # raise excpetion if the quantifier doesn't have closing braces.
        return index-1

    def set_string(self, regex, index):
        """
            sets the string based on the regex string for the current Character object.
        """
        try:
            temp_string = ""
            while(regex[index] != ']'):
                temp_string += regex[index]
                index += 1
            self.string = temp_string
            return index
        except IndexError:
            raise E.ImproperCharacterConstructor()
    
    def __str__(self):
        """
            Helps in printing the object of Character class.
        """
        if(self.quantifier):
            return ("string = " + self.string + ", quantifier = " + self.quantifier)
        else:
            return  ("string = " + self.string + ", quantifier = None " )
    
    def evaluate (self):
        """
            evaluates the Character constructor using the string and the quantifier, and set the evaluated string of the object.
        """
        self.evaluated_string = ''
        options = util.get_options_from_constructor_string(self) # get the options out of which we can select from.
        if self.quantifier == None:
            return chr(random.choice(options)) # chosing from the 
        else:   
            quantify = util.get_number_of_repetition(self.quantifier)
            for i in range(0, quantify):
                self.evaluated_string += chr(random.choice(options))
            return self.evaluated_string

class Branch:
    def __init__(self):
        """
            constructor
        """
        self.character_constructors = []
        self.evaluated_string = ""
    
    def __str__(self):
        string = ""
        for i in self.character_constructors:
            string += i.__str__()
        return string

class Subpattern:
    def __init__(self):
        self.branches = []
        self.evaluated_string = None
        self.quantifier = None

    def single_evaluation(self):
        """
            evaluates the subpattern, once. Giving a matching result.
            Logic: Select any of the branches at random, and evaluate list of Character constructor in them.
        """
        number_of_branches = len(self.branches)
        random_branch = self.branches[random.randint(0, number_of_branches - 1)]
        final_string = ""
        for i in random_branch.character_constructors:
            final_string += i.evaluate()
        return final_string

    def evaluate(self):
        """
            Evaluate the subpattern based of the quantifier.
            Logic: If there is no quantifier then, just do a single evaluation of the subpattern, else evaluate the quantifier, and based on that quantity, do the signle evaluation that many number of times.
        """
        if self.quantifier == None:
            self.evaluated_string = self.single_evaluation()
        else:   
            quantify = util.get_number_of_repetition(self.quantifier)
            self.evaluated_string = ""
            for i in range(0, quantify):
                self.evaluated_string += self.single_evaluation()

        return self.evaluated_string

    def add_branch(self, branch):
        """
            add a new branch
        """
        self.branches.append(branch)
    
    def set_quantifier(self, regex, index):
        """
            set the quantifier
        """
        if regex[index] in util.QUANTIFIER:
            self.quantifier = regex[index]
            return index  
        elif regex[index] == '{':
            temp_quantifier = ""
            index += 1
            try:
                while(regex[index] != '}'):
                    temp_quantifier += regex[index]
                    index += 1
                self.quantifier = temp_quantifier
                return index
            except IndexError:
                raise E.MinMaxQuantifierMismatchExcetpion()
        return index-1
    
    def __str__(self):
        string = ""
        for i in self.branches:
            string += i.__str__()
        if(self.quantifier):
            string += "; subpattern quantifier = " + self.quantifier
        else:
            string += "; subpattern quantifier = None "
        return string

def get_any_character_except_newline(regex, index, length):
    """
    If '.' is encountered. Will create a Character() object with '.' as string. 
    params: 
        regex : the subpattern string
        index : the current index that needs to be operated.
        length: the length of the subpattern regex.
    return: 
        index : the index that was last operated by the function.
        Character : the Character constructor.
    """
    character_construct = Character('.')
    character_construct.is_dot = True # To treat [.] and . differently.
    if index + 1 >= length:
        return (False, index, character_construct)
    index = character_construct.set_quantifier(regex, index + 1) # chcking the quantifier for the Character object 
    return (False, index, character_construct)

def evaluate_character_class_definition(regex, index, length):
    """
    If '[' is encountered. Will check the rest of string to construct the Character object.
    params: 
        regex : the subpattern string
        index : the current index that needs to be operated.
        length: the length of the subpattern regex.
    return: 
        index : the index that was last operated by the function.
        Character : the Character constructor.
    """
    character_construct = Character()
    index = character_construct.set_string(regex, index + 1) # finding the string for the Character object
    if(index + 1>= length):
        return(False, index, character_construct)
    index = character_construct.set_quantifier(regex, index + 1) # chcking the quantifier for the Character object 
    return (False, index, character_construct)

def identify(regex, index, length):
    """
    based on the character, identify the operation needed.
    param: 
        regex : the subpattern string
        index : the current index that needs to be operated.
        length: the length of the subpattern regex.
    return: (is_branched, index, Character)
        is_branched : True, if we encountered a '|', indicating a new branch needs to be made
        index : the index that was last operated by the function.
        Character : the Character constructor.
    """
    if regex[index] == '.':
        return get_any_character_except_newline(regex, index, length)
    elif regex[index] == '[':
        return evaluate_character_class_definition(regex, index, length)
    elif regex[index] == '|':
        return (True, index, None)
    else:
        return (False, index, Character(regex[index]))

def evaluate_subpattern(regex):
    """
    evaluate a subpattern.
    param : subpattern that has to be evaluated.
    reutrn : list of branches for the subpattern
    """
    index, regex_size = 0, len(regex)
    branches = []
    branch = Branch()
    while(index < regex_size):
        is_branched, index, character_constructor = identify(regex, index, regex_size)
        if is_branched:
            branches.append(branch)
            branch = Branch()
        else:
            branch.character_constructors.append(character_constructor)
        index += 1
    branches.append(branch)
    return branches


def evaluate_regex(regex):
    """
    Evaluates the regex provided, based on basic regex rules.
    param : regex string.
    return : string satisying the regex string.
    """
    stack = []
    index = 1
    stack.append('(')
    while(index < len(regex)):
        if regex[index] != ')':
            stack.append(regex[index])
        else:
            subpattern_text = ""
            subpattern = Subpattern()
            if(index + 1 < len(regex)):
                index = subpattern.set_quantifier(regex, index+1)
            while(stack[-1] != '('):
                subpattern_text = stack[-1] + subpattern_text
                stack.pop()
            stack.pop()
            subpattern.branches = evaluate_subpattern(subpattern_text)
            subpattern.evaluate()
            stack.append(subpattern.evaluated_string)
        index += 1
    if(len(stack) != 1):
        raise E.InavlidRegexExpression()
    return(stack[0])

