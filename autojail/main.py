#!/usr/bin/env python3
# main.py

import argparse


from autojail import OpenFileBuilder, StringBuilder, NumberBuilder, get_all_tokens, get_all_matches


def main():
    parser = argparse.ArgumentParser(
        description="Autojail is a tool for automatically solving python jail CTF challenges.")
    parser.add_argument("-b", "--blacklist", nargs="*",
                        help="A list of blacklisted kwds not allowed.")
    parser.add_argument("-w", "--whitelist", nargs="*",
                        help="A list of whitelisted kwds allowd to use.")

    parser.add_argument("-s", "--string", type=str,
                        help="Create a string.")
    parser.add_argument("-n", "--number", type=int,
                        help="Create a number.")

    parser.add_argument("-o", "--open", type=str, metavar="FILE_PATH",
                        help="Open a file and read it.")

    args = parser.parse_args()

    # Blacklist and whitelist can have regex matches in them
    whitelist = set(args.whitelist) if args.whitelist else get_all_tokens()
    blacklist = set(args.blacklist) if args.blacklist else set()

    usable_tokens = get_all_matches(whitelist, blacklist, get_all_tokens())

    if (args.string):
        sBuilder = StringBuilder()
        code = sBuilder.generate(args.string, usable_tokens)
        print(code)

    if (args.number):
        nBuilder = NumberBuilder()
        code = nBuilder.generate(args.number, usable_tokens)
        print(code)

    if (args.open):
        oBuilder = OpenFileBuilder()
        code = oBuilder.generate(args.open, usable_tokens)
        print(code)


if __name__ == "__main__":
    main()
