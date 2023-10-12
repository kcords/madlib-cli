import re
import os


def create_madlib():
    show_header()


def show_header():
    show_divider()
    print(strings["welcome"])
    show_divider()


def read_template(path):
    with open(path) as file:
        return file.read()


def parse_template(text):
    regex = r'\{(.*?)\}'
    parts = tuple(re.findall(regex, text))
    stripped = re.sub(regex, '{}', text)
    return stripped, parts


def merge(madlib, user_inputs):
    return madlib.format(*user_inputs)


def show_divider(character="="):
    terminal_width = os.get_terminal_size().columns
    divider_line = character * terminal_width
    print(divider_line)


strings = {
    "welcome": """Hey there! Welcome to madlibs!\n\nYou will be prompted to select a madlib template.\n\nYou will then be given a series of prompts. Fill in each to create your madlib.\n\nReady to have some fun? Lets get started..."""
}

if __name__ == "__main__":
    create_madlib()