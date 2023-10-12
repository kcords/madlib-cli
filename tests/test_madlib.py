import pytest
import os
from collections import namedtuple
import sys

from madlib_cli.madlib import show_header, show_divider, read_template, parse_template, merge


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
    divider = "==="
    show_header()
    assert text_in_captured_output(divider, capsys)


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


def test_merge():
    actual = merge("It was a {} and {} {}.", ("dark", "stormy", "night"))
    expected = "It was a dark and stormy night."
    assert actual == expected


def test_read_template_raises_exception_with_bad_path():
    with pytest.raises(FileNotFoundError):
        path = "missing.txt"
        read_template(path)
