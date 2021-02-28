from regex import evaluation
from regex import excptions as E

if __name__ == '__main__':
    """
    Takes input from the user in the form of generate command, and prints the output.
    Throws appropriate exception if raised.
    """
    while(True):
        print("Enter generate command with syntax generate(/<regex>/, <number of string satisfying the regex>)")
        _input = input() # take generate command as input
        if("generate(" not in _input):
            print("Invalid command") # if command is not valid
        else:
            command = _input.split("/")
            try:
                # evaluate the regex. Add extra surrounding parenthesis if not present.
                for i in range(int(command[2][1:-1].strip())):
                    if(command[1].strip()[0] == '('):
                        print(evaluation.evaluate_regex(command[1].strip()))
                    else:
                        print(evaluation.evaluate_regex('('+ command[1].strip() + ')'))
            except Exception as e:
                print(e)
