from .index import Strategy, Builder
from .strings import StringBuilder
from .builtin import BuiltinsBuilder

class OpenFileNormal(Strategy):
    required_tokens = set("().")
    require_least_one = [set(["open"]), set(["read"])]
    required_builders = [StringBuilder]

    def execute(self, token, tokens):
        """
        Opens a file and reads it using normal open and read
        """
        topen = self.get_token(0, tokens)
        tread = self.get_token(1, tokens)

        sbuilder = StringBuilder()

        return f"{topen}({sbuilder.generate(token, tokens)}).{tread}()"
    

class OpenFileStar(Strategy):
    required_tokens = set("()*")
    require_least_one = [set(["open"]), set(["print"])]
    required_builders = [StringBuilder]

    def execute(self, token, tokens):
        """
        Opens a file and reads it using normal open and read
        """
        topen = self.get_token(0, tokens)
        tprint = self.get_token(1, tokens)

        sbuilder = StringBuilder()

        return f"{tprint}(*{topen}({sbuilder.generate(token, tokens)}))"
    

class OpenFileNoOpen(Strategy):
    required_tokens = set("()*")
    require_least_one = [set(["print"])]
    required_builders = [BuiltinsBuilder, StringBuilder]

    def execute(self, token, tokens):
        """
        Opens a file and reads it using normal open and read
        """
        tprint = self.get_token(0, tokens)

        bBuilder = BuiltinsBuilder()
        sBuilder = StringBuilder()

        return f"{tprint}(*{bBuilder.generate('open', tokens)}({sBuilder.generate(token, tokens)}))"
    
class OpenFileBuilder(Builder):
    strategies = [
        OpenFileNormal(),
        OpenFileStar(),
        OpenFileNoOpen(),
    ]
