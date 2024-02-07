from .index import Strategy, Builder
from .number import NumberBuilder
import string


class CreateStringNormal(Strategy):
    required_tokens = set(string.printable)
    require_least_one = [set("'\""),]

    def custom_token_validator(self, token, tokens):
        quote = self.get_token(0, tokens)
        if not quote:
            return False
        
        if len([a for a in token if a in tokens]) != len(token):
            return False
        
        return True

    def execute(self, string, tokens=None):
        """
        Uses a normal string
        sample: "hello"
        """
        quote = self.get_token(0, tokens)

        return quote + string + quote


class CreateStringOctal(Strategy):
    required_tokens = set("\\01234567")
    require_least_one = [set("'\""),]

    def execute(self, string, tokens=None):
        """
        Creates a string using octal escape sequences
        sample: "\150\145\154\154\157"
        """
        quote = self.get_token(0, tokens)
        return quote + "".join([f"\\{oct(ord(c))[2:]}" for c in string]) + quote


class CreateStringHex(Strategy):
    required_tokens = set("\\x0123456789abcdef")
    require_least_one = [set("'\""),]

    def execute(self, string, tokens=None):
        """
        Creates a string using hex escape sequences
        sample: "\x68\x65\x6c\x6c\x6f"
        """
        quote = self.get_token(0, tokens)
        return quote + "".join([f"\\x{hex(ord(c))[2:]}" for c in string]) + quote


class CreateStringFormatted(Strategy):
    required_tokens = set(["%", "c"]).union(set(string.digits))
    require_least_one = [set("'\""),]

    def execute(self, string, tokens=None):
        """
        Creates a string using the %c format specifier
        sample: "%c"%104+"%c"%101+"%c"%108+"%c"%108+"%c"%111
        """
        quote = self.get_token(0, tokens)
        return "+".join([f'{quote}%c{quote}%{ord(c)}' for c in string])


class CreateStringFormattedNoC(Strategy):
    required_tokens = set(["%", '\\', "+"]).union(set(string.digits))
    require_least_one = [set("'\""),]

    def execute(self, string, tokens=None):
        """
        Creates a string without using the character 'c'
        sample: "%\143"%104+"%\143"%101+"%\143"%108+"%\143"%108+"%\143"%111
        """
        quote = self.get_token(0, tokens)
        return "+".join([f'{quote}%\\143{quote}%{ord(c)}' for c in string])


class CreateStringFormattedWithNumberStrategy(Strategy):
    required_tokens = set(["%", '\\', "+", "(", ")", "c"])
    require_least_one = [set("'\""),]
    required_builders = [NumberBuilder]

    def execute(self, string, tokens):
        """
        Creates a string using formatting and number generator.
        see: CreateStringFormatted
        """
        quote = self.get_token(0, tokens)
        number = NumberBuilder()

        return "+".join([f'{quote}%c{quote}%({number.generate(ord(c), tokens)})' for c in string])


class CreateStringFormattedWithNumberStrategy2(Strategy):
    required_tokens = set(["%", '\\', "+", "(", ")", "1", "4", "3"])
    require_least_one = [set("'\""),]
    required_builders = [NumberBuilder]

    def execute(self, string, tokens):
        """
        Creates a string using formatting and number generator and no c.
        see: CreateStringFormattedNoC
        """
        quote = self.get_token(0, tokens)
        number = NumberBuilder()

        return "+".join([f'{quote}%\\143{quote}%({number.generate(ord(c), tokens)})' for c in string])

class CreateStringWithChr(Strategy):
    required_tokens = set("+()")
    require_least_one = [set(["chr"]),]
    required_builders = [NumberBuilder]

    def execute(self, string, tokens):
        """
        Creates a string using formatting and number strategy
        """
        chrfunc = self.get_token(0, tokens)
        number = NumberBuilder()

        return "+".join([f'{chrfunc}({number.generate(ord(c), tokens)})' for c in string])
    
class CreateStringWithReprOnlyNumberSingeDigit(Strategy):
    required_tokens = set("()")
    require_least_one = [set(["repr"]),]
    required_builders = [NumberBuilder]

    def custom_token_validator(self, token, tokens):
        if not token.isnumeric():
            return False
        if int(token) > 9:
            return False
        return True

    def execute(self, string, tokens):
        """
        Creates a string using repr
        THIS should be the last strategy
        """
        trepr = self.get_token(0, tokens)
        number = NumberBuilder()

        return f'{trepr}({number.generate(int(string), tokens)})'


class StringBuilder(Builder):
    strategies = [
        CreateStringNormal(),
        CreateStringOctal(),
        CreateStringHex(),
        CreateStringFormatted(),
        CreateStringFormattedNoC(),
        CreateStringFormattedWithNumberStrategy(),
        CreateStringFormattedWithNumberStrategy2(),
        CreateStringWithChr(),
        CreateStringWithReprOnlyNumberSingeDigit()
    ]
