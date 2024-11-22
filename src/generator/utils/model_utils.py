import re


def parse_stringed_input_shape(stringed_shape:str) -> tuple[int, ...]:
    """
    Parses a stringed list of numbers into a tuple

    :param stringed_shape: a stringed list of number in format "[x,y,z]"
    :return: a tuple of numbers, in format (x, y, z)
    """
    brackets = ["(", ")", "[", "]", "{", "}"]
    for b in brackets:
        stringed_shape = stringed_shape.replace(b, "")
    return tuple([int(n) for n in stringed_shape.split(",")])



if __name__ == "__main__":
    test = "(10,10,11)"
    print(parse_stringed_input_shape(test))
