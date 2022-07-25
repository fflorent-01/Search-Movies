#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Various printing functions
- warning_msg
- box_msg
"""


def warning_msg(msg: str, symbol: str = "*", repeat: int = 5) -> str:
    """
    Adds a decorator to a single line message.
    :param msg: Message you want to decorate
    :param symbol: Decorator character
    :param repeat: Number of repetition at beginning and end fo the string
    :return: Decorated string (*** msg ***)
    """
    decorator = symbol * repeat
    return "\n" + decorator + " " + msg + " " + decorator


def msg_box(msg: str, symbol: str = "#") -> str:
    """
    Creates a box around your message
    :param msg: Message you want in the box
    :param symbol: Decorator you want to use to create your box
    :return: Decorated string (box)
    """
    top = bottom = symbol * (len(msg) + 4)
    text = symbol + " " + msg + " " + symbol
    print("\n" + "\n".join([top, text, bottom]) + "\n")


def multiline_msg_box(msg: list[str], symbol: str = "#") -> str:
    """
    Create a box around a multiline message

    :param msg: List of string containing each line of your message
    :param symbol: Decorator you want to use to create your box
    :return: Decorated string (box)
    """
    length = len(max(msg, key=len))
    top = bottom = symbol * (length + 4)
    text = "\n".join([(symbol + " " + string).ljust(length+3) + symbol for string in msg])
    print("\n".join([top, text, bottom]))
