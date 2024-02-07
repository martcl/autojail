from autojail import StringBuilder,CreateStringHex, CreateStringNormal,CreateStringOctal
import string

test_strings = ["a", "", "b", "KakeErGodt", "æøå", "v_a(1ad)??&51", "../../../../etc/notpasswd"]

def test_generate_string_normal():
    tokens = set(string.printable + "øæå")
    sBuilder = StringBuilder()
    sBuilder.strategies = [CreateStringNormal()]

    for s in test_strings:
        assert eval(str(sBuilder.generate(s, tokens))) == s

def test_generate_string_octal():
    tokens = set("\\01234567'")
    sBuilder = StringBuilder()
    sBuilder.strategies = [CreateStringOctal()]

    for s in test_strings:
        assert eval(str(sBuilder.generate(s, tokens))) == s

def test_generate_string_hex():
    tokens = set("\\x0123456789abcdef'")
    sBuilder = StringBuilder()
    sBuilder.strategies = [CreateStringHex()]
    
    for s in test_strings:
        assert eval(str(sBuilder.generate(s, tokens))) == s
        
# TODO: add more tests