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


def lex_string(dataString):
    # Identify the String component and return the remaining string plus the string component
    json_string = ''

    if dataString[0] == JSON_QUOTE:
        string = dataString[1:]
    else:
        return None, dataString

    for c in dataString:
        if c == JSON_QUOTE:
            return json_string, string[len(json_string) + 1:]
        else:
            json_string += c

    raise Exception("Expected end-of-string quote")


def lex_number(dataString):
    # identify the number and return string and number
    json_number = ''

    number_characters = [str(d) for d in range(0, 10)] + ['-', 'e', '.']

    for c in dataString:
        if c in number_characters:
            json_number += c
        else:
            break
    rest = dataString[len(json_number):]

    if not len(json_number):
        return None, dataString

    if '.' in json_number:
        return float(json_number), rest

    return int(json_number), rest


def lex_null(dataString):
    # identify the null and return string and null
    string_len = len(dataString)

    if string_len >= NULL_LEN and dataString[:NULL_LEN] == 'null':
        return True, dataString[NULL_LEN:]

    return None, dataString


def lex_bool(dataString):
    # Identify the boolean and return string and boolean
    string_len = len(dataString)

    if string_len >= TRUE_LEN and dataString[:TRUE_LEN] == 'true':
        return True, dataString[TRUE_LEN:]
    elif string_len >= FALSE_LEN and dataString[:FALSE_LEN] == 'false':
        return False, dataString[FALSE_LEN:]

    return None, dataString


def parse_array(tokens):
    json_array = []

    t = tokens[0]
    if t == JSON_RIGHTBRACKET:
        return json_array, tokens[1:]

    while True:
        json, tokens = parse(tokens)
        json_array.append(json)

        t = tokens[0]
        if t == JSON_RIGHTBRACKET:
            return json_array, tokens[1:]
        elif t != JSON_COMMA:
            raise Exception('Expected comma after object in array')
        else:
            tokens = tokens[1:]

    raise Exception('Expected end-of-array bracket')


def parse_object(tokens):
    json_object = {}

    t = tokens[0]
    if t == JSON_RIGHTBRACE:
        return json_object, tokens[1:]

    while True:
        json_key = tokens[0]
        if type(json_key) is str:
            tokens = tokens[1:]
        else:
            raise Exception('Expected string key, got: {}'.format(json_key))

        if tokens[0] != JSON_COLON:
            raise Exception('Expected colon after key in object, got: {}'.format(t))

        json_value, tokens = parse(tokens[1:])

        json_object[json_key] = json_value

        t = tokens[0]
        if t == JSON_RIGHTBRACE:
            return json_object, tokens[1:]
        elif t != JSON_COMMA:
            raise Exception('Expected comma after pair in object, got: {}'.format(t))

        tokens = tokens[1:]

    raise Exception('Expected end-of-object bracket')


def parse(tokens, is_root=False):
    t = tokens[0]

    if is_root and t != JSON_LEFTBRACE:
        raise Exception('Root must be an object')

    if t == JSON_LEFTBRACKET:
        return parse_array(tokens[1:])
    elif t == JSON_LEFTBRACE:
        return parse_object(tokens[1:])
    else:
        return t, tokens[1:]


if __name__ == '__main__':
    JSON_COMMA = ','
    JSON_COLON = ':'
    JSON_LEFTBRACKET = '['
    JSON_RIGHTBRACKET = ']'
    JSON_LEFTBRACE = '{'
    JSON_RIGHTBRACE = '}'
    JSON_QUOTE = '"'

    JSON_WHITESPACE = [' ', '\t', '\b', '\n', '\r']
    JSON_SYNTAX = [JSON_COMMA, JSON_COLON, JSON_LEFTBRACKET, JSON_RIGHTBRACKET,
                   JSON_LEFTBRACE, JSON_RIGHTBRACE]

    FALSE_LEN = len('false')
    TRUE_LEN = len('true')
    NULL_LEN = len('null')

    with open('tests/tests/step1/valid.json', mode='r') as data:
        JsonDataString = data.read()
        print(JsonDataString)
