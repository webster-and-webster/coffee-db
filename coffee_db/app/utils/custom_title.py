import re


def make_title(string_input):
    return re.sub("_", " ", string_input).title()


def revert_title(string_input):
    return re.sub(" ", "", string_input).lower()
