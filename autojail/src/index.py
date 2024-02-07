from abc import ABC, abstractmethod
from .util import de_normalize_set


class Strategy(ABC):
    """
    Abstract base class for a Strategy. This class is meant to be inherited by other classes.
    It provides a mechanism to execute a strategy based on a set of tokens.
    """

    def __init__(self):
        """
        Constructor for the Strategy class. Initializes the required_tokens, require_least_one, and required_builders attributes.
        """
        self.required_tokens = getattr(self, 'required_tokens', set())
        self.require_least_one = [s.union(de_normalize_set(
            s)) for s in getattr(self, 'require_least_one', [])]
        self.required_builders = getattr(self, 'required_builders', [])

    def custom_token_validator(self, token: int | str, tokens: set[str] = None):
        """
        Custom validator for tokens. By default, it does nothing and returns None.
        This method should be overridden in subclasses to provide custom validation logic.

        Parameters:
        token (int | str): The token to validate.
        tokens (set[str]): The set of tokens to validate.

        Returns:
        None by default. This method should be overridden in subclasses.
        """
        return None

    def can_execute(self, token: str | int, my_tokens: set[str]):
        """
        Checks if the strategy can be executed with the given token and set of tokens.

        Parameters:
        token (str | int): The token to check.
        my_tokens (set[str]): The set of tokens to check.

        Returns:
        bool: True if the strategy can be executed, False otherwise.
        """
        # Check if at least one token from each set in require_least_one is in my_tokens
        if self.require_least_one:
            for token_set in self.require_least_one:
                if not any(token in my_tokens for token in token_set):
                    return False

        # Check if all required tokens are in my_tokens
        if self.custom_token_validator(token, my_tokens) == None:
            if not self.required_tokens.issubset(my_tokens):
                return False

        # Check if the custom token validator returns False
        elif not self.custom_token_validator(token, my_tokens):
            return False

        return True

    def get_token(self, index: int, tokens: set[str]):
        """
        Returns a valid token from the require_least_one set 
        at pos index if it exists, else returns None. 

        Parameters:
        index (int): The index of the token to get.
        tokens (set[str]): The set of tokens to get the token from.

        Returns:
        The token at the given index if it exists, None otherwise.
        """
        if self.require_least_one:
            if index < len(self.require_least_one) and (usableTokens := self.require_least_one[index].intersection(tokens)):
                return usableTokens.pop()
            else:
                return None
        else:
            return None

    def generate(self, token: int | str, tokens: set[str] = None):
        """
        Executes the strategy with the given token and set of tokens.

        Parameters:
        token (int | str): The token to use.
        tokens (set[str]): The set of tokens to use.

        Returns:
        The result of the executed strategy.

        Raises:
        Exception: If the strategy cannot be executed.
        """
        if not self.can_execute(token, tokens):
            raise Exception("Cannot execute method with given tokens")
        else:
            return self.execute(token, tokens)

    @abstractmethod
    def execute(self, token: int | str, tokens: set[str] = None):
        """
        Abstract method for executing the strategy. This method should be implemented in subclasses.

        Parameters:
        token (int | str): The token to use.
        tokens (set[str]): The set of tokens to use.

        Returns:
        The result of the executed strategy. The return type depends on the implementation in subclasses.
        """
        pass


class Builder(ABC):
    """
    Abstract base class for a Builder. This class is meant to be inherited by other classes.
    It provides a mechanism to generate something based on a set of strategies.
    """

    def __init__(self):
        """
        Constructor for the Builder class. Initializes the strategies attribute.
        """
        self.strategies = getattr(self, 'strategies', set())

    def can_generate(self, token: str | int, tokens: set[str]) -> bool:
        """
        Checks if any of the strategies can be executed with the given token and tokens.

        Parameters:
        token (str | int): The token to check.
        tokens (set[str]): The set of tokens to check.

        Returns:
        bool: True if any strategy can be executed, False otherwise.
        """
        for strategy in self.strategies:
            if strategy.can_execute(token, tokens):
                return True
        return False

    def generate(self, token: str | int, tokens: set[str]):
        """
        Executes the first strategy that can be executed with the given token and tokens.

        Parameters:
        token (str | int): The token to use.
        tokens (set[str]): The set of tokens to use.

        Returns:
        The result of the executed strategy.

        Raises:
        Exception: If no strategy can be executed.
        """
        for strategy in self.strategies:
            if strategy.can_execute(token, tokens):
                return strategy.generate(token, tokens)

        raise Exception(
            f"Found no method to achieve: {self.__class__.__name__} with token {token}")
