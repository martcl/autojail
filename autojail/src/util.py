import re
import string
import keyword

UNICODE_NORMALIZED = {
    "a": "ª",
    "b": "ᵇ",
    "c": "ᶜ",
    "d": "ᵈ",
    "e": "ᵉ",
    "f": "ᶠ",
    "g": "ᵍ",
    "h": "ʰ",
    "i": "ᵢ",
    "j": "ʲ",
    "k": "ᵏ",
    "l": "ˡ",
    "m": "ᵐ",
    "n": "ⁿ",
    "o": "º",
    "p": "ᵖ",
    "q": "ｑ",
    "r": "ʳ",
    "s": "ſ",
    "t": "ᵗ",
    "u": "ᵘ",
    "v": "ᵛ",
    "w": "ʷ",
    "x": "ˣ",
    "y": "ʸ",
    "z": "ᶻ",
}


def create_unicode_alternatives(string):
    """
    Creates a string using unicode characters
    input: "globals"
    return: "ᵍˡºᵇªˡſ"
    """
    return "".join([UNICODE_NORMALIZED.get(c, c) for c in string])


def de_normalize_set(s):
    return {create_unicode_alternatives(string) for string in s}


def is_regex(string):
    """
    This function checks if a string is a regex.
    """
    if string[0:2] == "r#":
        return True
    return False


def get_all_matches(string_list, string_set):
    matches = []

    for string in string_list:
        if is_regex(string):
            matches += [string_set for string_set in string_set if re.match(
                string[2:], string_set)]
        else:
            matches += [string_set for string_set in string_set if string in string_set]
    return matches


def get_all_tokens():
    everything = set(__builtins__.keys()).union(
        set(string.printable)).union(de_normalize_set(__builtins__.keys())).union(set(keyword.kwlist)).union(de_normalize_set(set(keyword.kwlist)))

    everything.add("builtins")
    everything.add("globals")
    everything.add("._[]")
    everything.add("self")
    everything.add("read")

    return everything


def get_all_matches(whitelist, blacklist, every_token):
    matches = set()

    # whitelist
    for token in every_token:
        if all(char in whitelist for char in token):
            matches.add(token)

    # blacklist
    matches = {token for token in matches if not any(
        l in token for l in blacklist)}

    return matches
