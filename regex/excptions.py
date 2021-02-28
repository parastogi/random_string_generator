class MinMaxQuantifierMismatchExcetpion(Exception):
    def __init__(self, message="Wrong regex, There is no \'}\' for opening \'{\'"):
        self.message = message
        super().__init__(self.message)

class ImproperCharacterConstructor(Exception):
    def __init__(self, message="The character constructor is not proper."):
        self.message = message
        super().__init__(self.message)

class InvalidRangeException(Exception):
    def __init__(self, message="Range start is larger than Range end"):
        self.message = message
        super().__init__(self.message)

class InvalidQuantifierException(Exception):
    def __init__(self, message="The given quantifier is invalid"):
        self.message = message
        super().__init__(self.message)

class InvalidSubPatternException(Exception):
    def __init__(self, message="The given subpattern is invalid"):
        self.message = message
        super().__init__(self.message)
        
class InavlidRegexExpression(Exception):
    def __init__(self, message="The given regex is invalid"):
        self.message = message
        super().__init__(self.message)