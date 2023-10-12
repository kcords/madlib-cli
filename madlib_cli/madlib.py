import re
import os


def create_madlib():
    show_header()
    path = choose_template()
    template = read_template(path)
    blank_madlib, user_inputs = gather_prompt_inputs(template)
    madlib = generate_madlib(blank_madlib, user_inputs)


def show_header():
    show_divider()
    print(strings["welcome"])
    show_divider()


def choose_template():
    show_templates()
    choice = None
    while choice is None:
        choice = input(strings['make_selection'])
        try:
            choice = int(choice)
            if int(choice) <= 0 or int(choice) > len(templates):
                raise ValueError
        except ValueError:
            print(strings["selection_error"])
            choice = None
            continue
        selected_template = templates[choice - 1]
    print(strings["selected_prefix"].format(selected_template))
    path = get_path_from_template_title(selected_template)
    return path


def show_templates():
    for num in range(1, len(templates) + 1):
        print(f"{num}) {templates[num - 1]}")


def get_path_from_template_title(template_title):
    path = "./assets/{}_template.txt"
    return path.format(template_title.replace(' ', '_').lower())


def read_template(path):
    with open(path) as file:
        return file.read()


def gather_prompt_inputs(template):
    stripped, parts = parse_template(template)
    user_inputs = []
    for prompt in parts:
        response = input(strings['prompt_prefix'].format(
            prompt.lower().strip()))
        user_inputs.append(response)
    return (stripped, user_inputs)


def parse_template(text):
    regex = r'\{(.*?)\}'
    parts = tuple(re.findall(regex, text))
    stripped = re.sub(regex, '{}', text)
    return stripped, parts


def generate_madlib(blank_madlib, user_inputs):
    show_divider()
    generated = merge(blank_madlib, user_inputs)
    print(generated)
    return generated


def merge(madlib, user_inputs):
    return madlib.format(*user_inputs)


def show_divider(character="="):
    terminal_width = os.get_terminal_size().columns
    divider_line = character * terminal_width
    print(divider_line)


templates = [
    "Adventurous Tale",
    "Crazy Day at the Office",
    "Dark and Stormy Night",
]

strings = {
    "welcome": """Hey there! Welcome to madlibs!\n\nYou will be prompted to select a madlib template.\n\nYou will then be given a series of prompts. Fill in each to create your madlib.\n\nReady to have some fun? Lets get started...""",
    "make_selection": "\nPlease select a madlib: ",
    "selection_error": "The selection you provided is not valid, please try again.",
    "selected_prefix": "\nOkay then, let's get started creating {}...",
    "prompt_prefix": "Please provide a(n) {}: ",
}

if __name__ == "__main__":
    create_madlib()
