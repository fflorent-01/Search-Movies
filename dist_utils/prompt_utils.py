#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Various prompt functions
- prompt_question
- ask_continue
- ask_selection
"""
from dist_utils import warning_msg


def prompt_number(msg: str, number_type: [int, float] = int) -> int | float:
    """ Prompt a value and force specific type return. """

    result = None
    while not result:
        try:
            result = number_type(input(msg))
        except ValueError:
            print(f"You must provide a {'decimal' if number_type is float else 'integer'} number.")

    return result


def prompt_question(msg: str, answer_list: dict, separator: str = None):
    """
    Prompt a question with possible answer being the first character of the key of a dictionary.
    Returns the selected value from the list.

    :param msg: Message of the prompt
    :param answer_list: Dictionary matching answer choices (key) to value
    :param separator: You can specify separator between key and value if the answer
    choice is not included in the message.
    :return: Selected value
    """
    possible_answer: list[str] = list(answer_list.keys())
    prompt_msg: str = msg + "\n"
    if separator:
        prompt_msg += f"{separator}".join(possible_answer) + ": "
    answer = input(prompt_msg).upper()
    while answer not in answer_list:
        print(warning_msg("Your selection is not in the list!"))
        answer = input(prompt_msg).upper()

    return answer_list[answer]


def ask_yes_no(msg: str) -> bool:
    """Prompt a simple yes/no question."""
    return prompt_question(msg, {"Y": True, "N": False}, " \\ ")


def ask_continue() -> bool:
    """Prompt a frequent yes/no question with predetermined message."""
    return ask_yes_no("Do you want to continue?")


def ask_selection(msg: str, answer_list: dict, answer_description: str):
    """Prompt a question, but a description of the answer choices is provided."""
    return prompt_question(msg + "\n" + answer_description, answer_list)


def press_to_continue() -> None:
    """Helper function to create a stop in the console."""
    input("\nPress ENTER to continue.\n")
