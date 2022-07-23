#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Various selector functions
- generate_answer_selector(lst: list[str]) -> dict[str, str]
- generate_answer_selector_description(lst: list[str]) -> str
"""


def generate_answer_selector(lst: list[str]) -> dict[str, str]:
    """Generates a dictionary to match answer to elements in a prompt
    :param lst: List containing available answer choices
    :return: Dictionary matching answer choices to answers
    """
    return {elem[0].upper(): elem for elem in lst}


def generate_answer_selector_description(lst: list[str]) -> str:
    """Generates the text to be presented for answer choices in a prompt
    :param lst: List containing available answer choices
    :return: String to be printed to present choices
    """
    return "\n".join([elem[0].upper() + ": " + elem for elem in lst])
