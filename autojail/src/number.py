from .index import Builder, Strategy
import string

class CreateNumberNormal(Strategy):
    required_tokens = set(string.digits)

    def custom_token_validator(self, token, tokens):
        str_token = str(token)
        if not set(str_token).issubset(tokens):
            return False
        return True

    def execute(self, number, tokens=None):
        """
        Uses a normal number
        sample: 5
        """
        return number


class CreateNumberBinary(Strategy):
    required_tokens = set("01b")

    def execute(self, number, tokens=None):
        """
        Creates a number using binary
        sample: 0b101
        """
        return f"0b{bin(number)[2:]}"


class CreateNumberHex(Strategy):
    required_tokens = set("0123456789abcdefx")

    def custom_token_validator(self, token, tokens):
        if not set(hex(token)).issubset(tokens):
            return False
        return True

    def execute(self, number, tokens=None):
        """
        Creates a number using hex
        sample: 0x65
        """
        return f"0x{hex(number)[2:]}"


class CreateNumberVariant1(Strategy):
    required_tokens = set(["not", "(", ")", "int", "+", "*"])

    def execute(self, number, tokens=None):
        """
        Builds a int number from based on the binary representation of the number.
        sample: int(not())+(int(not())+int(not()))**(int(not())+int(not()))
        """
        binary = bin(number)[2:]
        revBinary = binary[::-1]
        out = []

        if number == 0:
            return "int()"
        if number == 1:
            return "+(not())"
        if number == 2:
            return "+(not())+(not())"
        if number == 3:
            return "+(not())+(not())+(not())"

        for pos, bit in enumerate(revBinary):
            if pos == 0 and bit == "1":
                out.append("int(not())")
            elif bit == "1" and pos == 1:
                out.append("(int(not())+int(not()))")
            elif bit == "1":
                out.append("(int(not())+int(not()))**(" + "+".join(
                    ["int(not())" for n in range(pos)]) + ")")
                  
        return "+".join(out)


class CreateNumberVariant2(Strategy):
    required_tokens = set(["[", "]", "=", ":", ",", "+"])
    require_least_one = [set(string.ascii_letters + "_"), set("123456789")]

    def execute(self, number, tokens):
        """
        Creates a number using boolean addition.
        sample: [a:=4==4,a,a,a,a+a+a+a+a+a+a+a+a+a][4]

        DO NOT handle 0 and 1
        """
        tvar = self.get_token(0, tokens)
        tnum = self.get_token(1, tokens)

        out = f"[{tvar}:={tnum}=={tnum},"
        for i in range(int(tnum)):
            if i != int(tnum) - 1:
                out += f"{tvar},"
            else:
                out += f"{tvar}+"*number
        out = out[:-1] + f"][{tnum}]"

        return out
    
class CreateNumberReprInt(Strategy):
    required_tokens = set("()+")
    require_least_one = [set(["int"]), set(["repr"])]

    def execute(self, number, tokens: set[str]):
        """
        Creates a zero using int
        sample: int()
        """
        sif = str(number)

        nBuilder = NumberBuilder()

        return f"int({'+'.join(['repr('+str(nBuilder.generate(int(i), tokens.difference(set(['repr']))))+')' for i in sif])})"

class CreateNumberZero(Strategy):
    required_tokens = set("()")
    require_least_one = [set(["int"])]

    def custom_token_validator(self, token, tokens):
        if int(token) != 0:
            return False
        return True

    def execute(self, number, tokens=None):
        """
        Creates a zero using int
        sample: int()
        """
        return "int()"

class NumberBuilder(Builder):
    strategies = [
        CreateNumberNormal(),
        CreateNumberReprInt(),
        CreateNumberBinary(),
        CreateNumberHex(),
        CreateNumberVariant1(),
        CreateNumberVariant2(),
        CreateNumberZero(),
        
    ]
