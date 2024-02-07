from autojail import NumberBuilder, CreateNumberHex,CreateNumberVariant2, CreateNumberNormal, CreateNumberVariant1, CreateNumberBinary

numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
           11, 12, 13, 111, 2, 255, 1924]


def test_generate_any_number_normal():
    my_tokens = set("0123456789")
    nBuilder = NumberBuilder()
    nBuilder.strategies = [CreateNumberNormal()]
    for number in numbers:
        assert eval(str(nBuilder.generate(number, my_tokens))) == number


def test_generate_number_no_numbers():
    my_tokens = set("()+*").union(set(["not", "int"]))
    nBuilder = NumberBuilder()
    nBuilder.strategies = [CreateNumberVariant1()]
    for number in numbers:
        assert eval(str(nBuilder.generate(number, my_tokens))) == number


def test_generate_number_binary():
    my_tokens = set("01b")
    nBuilder = NumberBuilder()
    nBuilder.strategies = [CreateNumberBinary()]
    for number in numbers:
        assert eval(str(nBuilder.generate(number, my_tokens))) == number


def test_generate_number_hex():
    my_tokens = set("0123456789abcdefx")
    nBuilder = NumberBuilder()
    nBuilder.strategies = [CreateNumberHex()]
    for number in numbers:
        assert eval(str(nBuilder.generate(number, my_tokens))) == number

def test_generate_number_brackets():
    numbers.remove(0)
    numbers.remove(1)
    my_tokens = set("[]=:,+2a")
    nBuilder = NumberBuilder()
    nBuilder.strategies = [CreateNumberVariant2()]
    for number in numbers:
        assert eval(str(nBuilder.generate(number, my_tokens))) == number
