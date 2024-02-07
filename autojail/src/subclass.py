from .index import Strategy, Builder
from .strings import StringBuilder


class GetSubClassesWithAttribute(Strategy):
    required_tokens = set("(),")
    require_least_one = [set(["getattr"])]

    def execute(self, token, tokens):
        """
        Gets subclasses of a class with an attribute
        token, does not matter
        """
        tfunc = self.get_token(0, tokens)

        sbuilder = StringBuilder()

        return f"getattr(getattr(getattr((),{sbuilder.generate('__class__', tokens)}),{sbuilder.generate('__base__', tokens)}),{sbuilder.generate('__subclasses__', tokens)})()"


class SubclassBuilder(Builder):
    strategies = [
        GetSubClassesWithAttribute()
    ]

