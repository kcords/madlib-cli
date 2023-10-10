import re

def read_template(path):
    with open(path) as file:
        return file.read()


def parse_template(text):
    regex = r'\{(.*?)\}'
    parts = tuple(re.findall(regex, text))
    stripped = re.sub(regex, '{}', text)
    return stripped, parts


