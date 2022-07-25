#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Contains prompt windows class """

import getpass
import os
from tkinter import filedialog
from typing import Optional

username = getpass.getuser()


class NoFileSelected(Exception):
    """ Raised when no file is selected in a selection window. """
    def __init__(self, message: str = "No file was selected."):
        super().__init__(f"{message}")


class PromptSelectionWindow:
    """ Open a filedialog window and retrieve information about the file that was selected. """
    def __init__(self,
                 title: str = "Select your file",
                 extension_type: Optional[list[tuple[str, str]] | tuple] = (),
                 initial_dir: str = "/home/" + username + "/Documents"):
        self.title: str = title
        self._extension_type: Optional[list[tuple[str, str]] | tuple] = extension_type
        self.extension_type: tuple = self.get_extension_type()
        self.initial_dir: str = initial_dir
        self.full_path_to_file: str = self.open_selection_window()

    def get_extension_type(self):
        """ Return correct tuple for filtering file per extension """
        filetype = []
        if self._extension_type and isinstance(self._extension_type, tuple):
            filetype.append(self._extension_type)
        if isinstance(self._extension_type, list):
            filetype.extend(self._extension_type)
        filetype.append(("Other files", "*.*"))

        return tuple(filetype)

    def open_selection_window(self):
        """ Open file selection window and return full path to file """
        result = filedialog.askopenfilename(
            initialdir=self.initial_dir,
            filetypes=self.extension_type,
            title=self.title)
        if not result:
            raise NoFileSelected

        return result

    def get_path(self):
        """ Return the path up to the file name """
        return os.path.split(self.full_path_to_file)[0]

    def get_file_full_name(self):
        """ Returns full file name with extension """
        return os.path.split(self.full_path_to_file)[1]

    def get_file_name(self):
        """ Return file name without extension """
        return ".".join(self.get_file_full_name().split(".")[:-1])

    def get_extension(self):
        """ Return file extension """
        return self.get_file_full_name().split(".")[-1]

    def __str__(self):
        strings = [
            f"Full path to file: {self.full_path_to_file}",
            f"File path: {self.get_path()}",
            f"File full name: {self.get_file_full_name()}",
            f"File name: {self.get_file_name()}",
            f"File extension: {self.get_extension()}"
        ]
        return "\n".join(strings)


if __name__ == "__main__":
    pass
