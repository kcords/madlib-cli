import pytest
import os
from collections import namedtuple

from madlib_cli.madlib import show_header, show_divider, show_templates, get_path_from_template_title, choose_template, read_template, parse_template, gather_prompt_inputs, merge, generate_madlib, save_to_file


def emulate_terminal_size(monkeypatch, columns=20, lines=10):
    terminal_size = namedtuple('TerminalSize', ['columns', 'lines'])
    monkeypatch.setattr(os, 'get_terminal_size', lambda: terminal_size(columns=columns, lines=lines))


def text_in_captured_output(text, capsys):
    captured = capsys.readouterr()
    return text in captured.out


def test_displays_a_valid_header(monkeypatch, capsys):
    emulate_terminal_size(monkeypatch)
    welcome_msg = "Welcome to madlibs!"
    show_header()
    assert text_in_captured_output(welcome_msg, capsys)


def test_displays_a_valid_divider(monkeypatch, capsys):
    emulate_terminal_size(monkeypatch)
    default_divider = "==="
    show_divider()
    assert text_in_captured_output(default_divider, capsys)


def test_displays_template_list(capsys):
    expected = "Dark and Stormy Night"
    show_templates()
    assert text_in_captured_output(expected, capsys)


def test_returns_path_from_template_title():
    template_title = "Dark and Stormy Night"
    expected = "./assets/dark_and_stormy_night_template.txt"
    actual = get_path_from_template_title(template_title)
    assert expected == actual


def test_chooses_correct_template_from_selection(monkeypatch, capsys):
    user_input = "3"
    monkeypatch.setattr('builtins.input', lambda _: user_input)
    expected_return = "./assets/dark_and_stormy_night_template.txt"
    actual_return = choose_template()
    expected_print = "let's get started creating Dark and Stormy Night..."
    assert text_in_captured_output(expected_print, capsys) and expected_return == actual_return


def test_prints_error_msg_with_invalid_input(monkeypatch, capsys):
    user_inputs = ["0", "xyz", "1"]
    def mock_user_input(prompt):
        return user_inputs.pop(0)
    monkeypatch.setattr('builtins.input', mock_user_input)
    choose_template()
    expected_error_msg = "The selection you provided is not valid, please try again."
    assert text_in_captured_output(expected_error_msg, capsys)


def test_read_template_returns_stripped_string():
    actual = read_template("assets/dark_and_stormy_night_template.txt")
    expected = "It was a {Adjective} and {Adjective} {Noun}."
    assert actual == expected


def test_parse_template():
    actual_stripped, actual_parts = parse_template(
        "It was a {Adjective} and {Adjective} {Noun}."
    )
    expected_stripped = "It was a {} and {} {}."
    expected_parts = ("Adjective", "Adjective", "Noun")

    assert actual_stripped == expected_stripped
    assert actual_parts == expected_parts


def test_gather_user_inputs(monkeypatch):
    template = "It was a {Adjective} and {Adjective} {Noun}."
    user_inputs = ["dark", "stormy", "night"]
    def mock_user_input(prompt):
        return user_inputs.pop(0)
    monkeypatch.setattr('builtins.input', mock_user_input)
    expected_stripped = "It was a {} and {} {}."
    actual_stripped, actual_user_inputs = gather_prompt_inputs(template)
    assert actual_stripped == expected_stripped and all(a == b for a, b in zip(user_inputs, actual_user_inputs))


def test_merge():
    actual = merge("It was a {} and {} {}.", ("dark", "stormy", "night"))
    expected = "It was a dark and stormy night."
    assert actual == expected


def test_read_template_raises_exception_with_bad_path():
    with pytest.raises(FileNotFoundError):
        path = "missing.txt"
        read_template(path)


def test_valid_generated_madlib(monkeypatch):
    emulate_terminal_size(monkeypatch)
    expected = "It was a dark and stormy night."
    blank_madlib = "It was a {} and {} {}."
    mocked_inputs = ["dark", "stormy", "night"]
    actual = generate_madlib(blank_madlib, mocked_inputs)
    assert expected == actual


def test_file_saved_successfully():
    expected = "It was a dark and stormy night."
    save_to_file(expected)
    actual = ""
    with open('./generated/madlib.txt', 'r') as file:
        actual = file.read()
    assert actual == expected