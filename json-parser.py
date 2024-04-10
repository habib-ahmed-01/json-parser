def lexical_analysis(dataString):
    # Get the string and call the identification functions
    tokens = []

    while len(dataString):
        json_string, dataString = lex_string(dataString)
        if json_string is not None:
            tokens.append(json_string)
            continue

        json_number, dataString = lex_number(dataString)
        if json_number is not None:
            tokens.append(json_number)
            continue

        json_bool, dataString = lex_bool(dataString)
        if json_bool is not None:
            tokens.append(json_bool)
            continue

        json_null, dataString = lex_null(dataString)
        if json_null is not None:
            tokens.append(json_null)
            continue

        if dataString[0] in JSON_WHITESPACE:
            dataString = dataString[1:]

        elif dataString[0] in JSON_SYNTAX:
            tokens.append(dataString[0])
            dataString = dataString[1:]
        else:
            raise Exception('Unexpected Characters: {}'.format(dataString[0]))

    pass


def lex_string(dataString):
    # Identify the String component and return the remaining string plus the string component
    pass


def lex_number(dataString):
    # identify the number and return string and number
    pass


def lex_null(dataString):
    # identify the null and return string and null
    pass


def lex_bool(dataString):
    # Identify the boolean and return string and boolean
    pass


if __name__ == '__main__':
    JSON_SYNTAX = ['{', '}', '[', ']', ':']
    with open('tests/tests/step1/valid.json', mode='r') as data:
        dataString = data.read()
        print(dataString)
