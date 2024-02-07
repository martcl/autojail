from .index import Strategy, Builder
from .strings import StringBuilder

class GetBuiltinsNormal(Strategy):
    def custom_token_validator(self, token, tokens):
        if token not in set(__builtins__.keys()):
            return False
        if token not in tokens:
            return False
        return True

    def execute(self, token, tokens):
        """
        Gets the builtins module from global functions
        """

        return f"{token}"


class GetBuiltinsFunctionWithGlobalFunctions(Strategy):
    required_tokens = set("._[]").union(set(["call", "builtins"]))
    require_least_one = [set(["help", "license", "credits"])]

    def execute(self, token, tokens):
        """
        Gets the builtins module from global functions
        """
        tfunc = self.get_token(0, tokens)

        sbuilder = StringBuilder()

        return f"{tfunc}.__call__.__builtins__[{sbuilder.generate(token, tokens)}]"


class GetBuiltinsWithFunctionAttribute(Strategy):
    required_tokens = set("(),").union(set(["getattr"]))
    require_least_one = [set(['abs', 'aiter', 'all', 'anext', 'any', 'ascii', 'bin', 'bool', 'breakpoint', 'bytearray', 'bytes', 'callable', 'chr', 'classmethod', 'compile', 'complex', 'copyright', 'credits', 'delattr', 'dict', 'dir', 'divmod', 'enumerate', 'eval', 'exec', 'exit', 'filter', 'float', 'format', 'frozenset', 'getattr', 'globals', 'hasattr',
                              'hash', 'help', 'hex', 'id', 'input', 'int', 'isinstance', 'issubclass', 'iter', 'len', 'license', 'list', 'locals', 'map', 'max', 'memoryview', 'min', 'next', 'object', 'oct', 'open', 'ord', 'pow', 'print', 'property', 'quit', 'range', 'repr', 'reversed', 'round', 'set', 'setattr', 'slice', 'sorted', 'staticmethod', 'str', 'sum', 'super', 'tuple', 'type', 'vars', 'zip'])]

    def execute(self, token, tokens):
        """
        Gets the builtins module from global functions
        """
        tfunc = self.get_token(0, tokens)

        sbuilder = StringBuilder()

        return f"getattr(getattr({tfunc},{sbuilder.generate('__self__', tokens)}),{sbuilder.generate(token, tokens)})"

class GetBuiltinsFunctionWithGlobalFunctions(Strategy):
    required_tokens = set("._[]").union(set(["builtins", "dict"]))

    def execute(self, token, tokens):
        """
        Gets the builtins module from global functions
        """
        tfunc = self.get_token(0, tokens)

        sbuilder = StringBuilder()

        return f"__builtins__.__dict__[{sbuilder.generate(token, tokens)}]"


class GetBuiltinsFunctionWithLocalSelf(Strategy):
    required_tokens = set("._[]").union(set(["self", "dict"]))
    require_least_one = [set(['abs', 'aiter', 'all', 'anext', 'any', 'ascii', 'bin', 'bool', 'breakpoint', 'bytearray', 'bytes', 'callable', 'chr', 'classmethod', 'compile', 'complex', 'copyright', 'credits', 'delattr', 'dict', 'dir', 'divmod', 'enumerate', 'eval', 'exec', 'exit', 'filter', 'float', 'format', 'frozenset', 'getattr', 'globals', 'hasattr',
                              'hash', 'help', 'hex', 'id', 'input', 'int', 'isinstance', 'issubclass', 'iter', 'len', 'license', 'list', 'locals', 'map', 'max', 'memoryview', 'min', 'next', 'object', 'oct', 'open', 'ord', 'pow', 'print', 'property', 'quit', 'range', 'repr', 'reversed', 'round', 'set', 'setattr', 'slice', 'sorted', 'staticmethod', 'str', 'sum', 'super', 'tuple', 'type', 'vars', 'zip'])]

    def execute(self, token, tokens):
        """
        Gets the builtins module from local self
        """
        tfunc = self.get_token(0, tokens)

        sbuilder = StringBuilder()

        return f"{tfunc}.self.__dict__[{sbuilder.generate(token, tokens)}]"


class BuiltinsBuilder(Builder):
    strategies = [
        GetBuiltinsNormal(),
        GetBuiltinsFunctionWithGlobalFunctions(),
        GetBuiltinsFunctionWithLocalSelf(),
        GetBuiltinsWithFunctionAttribute(),
        GetBuiltinsFunctionWithGlobalFunctions(),
    ]
