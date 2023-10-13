import re
import os


def create_madlib():
    """Begins the application to walk through the user through terminal prompts to craft a new madlib"""
    show_header()
    path = choose_template()
    template = read_template(path)
    blank_madlib, user_inputs = gather_prompt_inputs(template)
    madlib = generate_madlib(blank_madlib, user_inputs)
    save_to_file(madlib)


def show_header():
    """Prints a header to the terminal"""
    show_divider()
    print(strings["welcome"])
    show_divider()


def choose_template():
    """Prompts the user to input a value corresponding to a provided madlib template list

    Raises:
        ValueError: Errors if the user provides a number outside of the range of selectable templates, or inputs a non-integer

    Returns:
        string: Path to the user selected template
    """
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
    """Prints a list of the available templates"""
    for num in range(1, len(templates) + 1):
        print(f"{num}) {templates[num - 1]}")


def get_path_from_template_title(template_title):
    """Converts a template title to a path string for a file matching the title

    Args:
        template_title (string): Format should precisely match an entry in the templates list

    Returns:
        string: Path to a template corresponding to the provided title
    """
    path = "./assets/{}_template.txt"
    return path.format(template_title.replace(' ', '_').lower())


def read_template(path):
    """Returns the contents of a file at the provided path

    Args:
        path (string): Path to a template file to be read

    Returns:
        string: Contents of a template file corresponding to the given path
    """
    with open(path) as file:
        return file.read()


def gather_prompt_inputs(template):
    """Takes in the contents of template text and returns the text stripped of placeholders and a list of user_inputs values

    Args:
        template (string): The provided unmodified template text

    Returns:
        tuple: The first entry contains the template text stripped of user_input placeholders, the second entry contains a list of the user_inputs
    """
    stripped, parts = parse_template(template)
    user_inputs = []
    for prompt in parts:
        response = input(strings['prompt_prefix'].format(
            prompt.lower().strip()))
        user_inputs.append(response)
    return (stripped, user_inputs)


def parse_template(text):
    """Takes in the contents of template text and separates the stripped text from the user_input placeholders

    Args:
        text (string): The provided unmodified template text

    Returns:
        tuple: The first entry contains the template text stripped of user_input placeholders, the second entry contains a list of the user_input placeholders
    """
    regex = r'\{(.*?)\}'
    parts = tuple(re.findall(regex, text))
    stripped = re.sub(regex, '{}', text)
    return stripped, parts


def generate_madlib(blank_madlib, user_inputs):
    """Generates madlib text based on the blank_madlib template, populated with user_inputs values

    Args:
        blank_madlib (string): The madlib text stripped of placeholder text
        user_inputs (list): A list of strings to be used in the corresponding empty placeholders

    Returns:
        string: The madlib text, formatted and populated with user_inputs values
    """
    show_divider()
    generated = merge(blank_madlib, user_inputs)
    print(generated)
    return generated


def merge(madlib, user_inputs):
    """Generates madlib text based on the blank_madlib template, populated with user_inputs values

    Args:
        madlib (string): The madlib text stripped of placeholder text
        user_inputs (list): A list of strings to be used in the corresponding empty placeholders

    Returns:
        string: The madlib text populated with the user input values
    """
    return madlib.format(*user_inputs)


def save_to_file(text):
    """Saves text to a file

    Args:
        text (string): Text to be saved to the file contents
    """
    with open('./generated/madlib.txt', 'w') as file:
        file.write(text)


def show_divider(character="="):
    """Generates a divider the width of the terminal window

    Args:
        character (str, optional): Character to be used as divider text. Defaults to "=".
    """
    terminal_width = os.get_terminal_size().columns
    divider_line = character * terminal_width
    print(divider_line)


templates = (
    "Adventurous Tale",
    "Crazy Day at the Office",
    "Dark and Stormy Night",
    "Make Me a Video Game"
)

strings = {
    "welcome": """Hey there! Welcome to madlibs!\n\nYou will be prompted to select a madlib template.\n\nYou will then be given a series of prompts. Fill in each to create your madlib.\n\nReady to have some fun? Lets get started...""",
    "make_selection": "\nPlease select a madlib: ",
    "selection_error": "The selection you provided is not valid, please try again.",
    "selected_prefix": "\nOkay then, let's get started creating {}...",
    "prompt_prefix": "Please provide a(n) {}: ",
}

if __name__ == "__main__":
    create_madlib()
