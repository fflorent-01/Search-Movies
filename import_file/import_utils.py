#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Import related class and function """

import csv
from typing import Optional
from pathlib import Path
from dist_utils import PromptSelectionWindow, warning_msg
from classes import Movie, Rating, Repository


class TsvFileSelection(PromptSelectionWindow):
    """ Open a filedialog window to select a file and retrieve its path """
    def __init__(self,
                 title: Optional[str] = None,
                 priority_type: Optional[tuple | list] = None,
                 initial_dir: Optional[str] = None):
        kwargs = {}
        if title:
            kwargs["title"] = title
        if initial_dir:
            kwargs["initial_dir"] = initial_dir

        if priority_type:
            if isinstance(priority_type, tuple):
                priority_type = [priority_type, ("TSV Files (Tab)", ".tsv")]
                print(priority_type)
            elif isinstance(priority_type, list):
                priority_type.append(("TSV Files (Tab)", ".tsv"))
        else:
            priority_type = ("TSV Files (Tab)", ".tsv")
        kwargs["priority_type"] = priority_type

        super().__init__(**kwargs)


def import_and_convert_tsv(
        filename: str, obj_type: [Movie | Rating],
        repository: Optional[Repository] = None) -> None:
    """
    Import raw basic title data from IMBD then:

    - Filters only movies
    - Selects only the fields relevant to Movie
    - Write into csv file

    :return:
    """
    file_type = "TITLE BASIC" if obj_type == Movie else "RATING"
    prompt_message = "Please select a " + file_type + " file"

    with open(TsvFileSelection(prompt_message).full_path_to_file, encoding="utf8") as input_file:
        reader = csv.DictReader(input_file, delimiter='\t')
        fieldnames = [key for key in reader.fieldnames if key in dir(obj_type) + ["tconst"]]

        if "titleType" not in reader.fieldnames and obj_type == Movie:
            print(warning_msg(
                "Looks like you selected the wrong file. [titleType] could not be found."))
            import_and_convert_tsv(filename=filename, obj_type=obj_type)
            return

        if "averageRating" not in reader.fieldnames and obj_type == Rating:
            print(warning_msg(
                "Looks like you selected the wrong file. [averageRating] could not be found."))
            import_and_convert_tsv(filename=filename, obj_type=obj_type)
            return

        with open(Path(__file__).parent.parent.joinpath('data', filename), "w",
                  encoding="utf8") as output_file:
            writer = csv.DictWriter(output_file, fieldnames, extrasaction="ignore")
            writer.writeheader()

            for row in reader:
                # Filter for Movie:
                if obj_type == Movie:
                    if not row.get("titleType") == "movie":
                        continue
                elif obj_type == Rating:
                    if row.get("tconst") not in repository.movies:
                        continue
                writer.writerow(row)

    print("Successfully imported the " + file_type + " file.")

if __name__ == "__main__":
    import_and_convert_tsv("title_basic.csv", Movie)
    import_and_convert_tsv("rating.csv", Rating)
