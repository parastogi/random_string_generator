## Random String Generator

A string generator that takes a regular expression as argument and returns strings that match the given regular expression.

Commands should be in the form:
 
    generate(/- [-+]?[0-9]{1,16}[.][0-9]{1,6}/, 10)

The features supported by the generator, and their functions are as follows:
- ```.``` Match any character except newline
- ```[``` Start character class definition
- ```]``` End character class definition
- ```?``` 0 or 1 quantifier
- ```*``` 0 or more quantifiers
- ```+``` 1 or more quantifier
- ```{``` Start min/max quantifier
- ```}``` End min/max quantifier
- ```|``` Start of alternative branch
- ```(``` Start subpattern
- ```)``` End subpattern (Nested suppatterns are supported.)

The only requirement for the generator to work is **Python version > 3.6**

In order to run the Random String Generator, use the following command inside the random_string_generator folder:
    ``` python __main__.py```
