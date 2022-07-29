#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Main file. Run from here. """
import logging
from typing import Optional
import dist_utils
import import_file
from classes import Repository, Movie, Rating

logging.basicConfig(level=logging.DEBUG)

repository = Repository()


def init_repository() -> None:
    """ Load data from csv file into the repository. Alert if no data present. """

    repository.import_movies()
    repository.import_ratings()

    if not repository.movies:
        print(dist_utils.msg_box("You movie repository is empty. You will need to import data."))


def database_upgrade() -> None:
    """ Offers the user to proceed to a database upgrade. """

    # Database update
    update_database = dist_utils.ask_yes_no("Do you wish to update the databases?")
    if update_database or not repository.movies:
        dist_utils.multiline_msg_box([
            "All databases are found at: https://datasets.imdbws.com/.",
            "DB used for base movie: title.basics.tsv.gz.",
            "DB used for ratings: title.ratings.tsv.gz",
            "You will need to extract the .tsv file first.",
            "NOTE: Base movie should be imported first.",
            "NOTE: If you import a new movie DB you need to update the rating."
            ])
        import_answer_choices = ["Base Movie", "Rating", "Cancel"]
        import_answer = dist_utils.ask_selection(
            "What database would you like to update?",
            dist_utils.generate_answer_selector(import_answer_choices),
            dist_utils.generate_answer_selector_description(import_answer_choices)
        )
        if import_answer != "Cancel":
            if import_answer == "Base Movie":
                import_file.import_and_convert_tsv("title_basic.csv", Movie)
                repository.import_movies()
            if import_answer in ["Base Movie", "Rating"]:
                import_file.import_and_convert_tsv("rating.csv", Rating, repository)
                repository.import_ratings()


def ask_search_type(search_type_choices: list[str]) -> list[str]:
    """ Prompt user for desired type of search to pass to the query. """

    primary_search_type = current_search_type = dist_utils.ask_selection(
        "What criteria would you like to use for your search?",
        dist_utils.generate_answer_selector(search_type_choices),
        dist_utils.generate_answer_selector_description(search_type_choices)
    )
    selected_search_types = [primary_search_type]

    while True:
        search_type_choices.pop(search_type_choices.index(current_search_type))
        if not selected_search_types:
            break
        add_criteria = dist_utils.ask_yes_no("Do you want to add a criteria to your search?")
        if not add_criteria:
            break
        current_search_type = dist_utils.ask_selection(
            "What additional criteria would you like to use for your search?",
            dist_utils.generate_answer_selector(search_type_choices),
            dist_utils.generate_answer_selector_description(search_type_choices)
        )
        selected_search_types.append(current_search_type)

    return selected_search_types


def ask_title(result: Optional[list[Movie]] = None) -> list[Movie]:
    """ Ask for information contained in the title and return corresponding movies. """

    title_string = input(
        "Please enter the [Title] (or part of it) of the movie(s) you are searching for.\n")
    return repository.search_title(title_string, result)


def define_boundary(criteria: str,
                    output_format: type = int) -> tuple[int, int] | tuple[float, float]:
    """ Ask the user to specify boundary type and value(s). Return min, max. """

    boundary_types = ["Lower", "Upper", "Both"]
    _min = _max = None
    selected_boundary = dist_utils.ask_selection(
        f"What boundary do you wish to specify for your [{criteria}] criteria?",
        dist_utils.generate_answer_selector(boundary_types),
        dist_utils.generate_answer_selector_description(boundary_types)
    )
    if selected_boundary in ["Lower", "Both"]:
        _min = dist_utils.prompt_number(
            f"Please specify the LOWER boundary of your [{criteria}] criteria.\n", output_format)
    if selected_boundary in ["Upper", "Both"]:
        _max = dist_utils.prompt_number(
            f"Please specify the UPPER boundary of your [{criteria}] criteria.\n", output_format)

    return _min, _max


def ask_year(result: Optional[list[Movie]] = None) -> list[Movie]:
    """ Ask criteria for year search. Return movie list. """

    min_year, max_year = define_boundary("Year", int)
    return repository.search_year(min_year, max_year, result)


def ask_rating(result: Optional[list[Movie]] = None) -> list[Movie]:
    """ Ask criteria for rating search. Return movie list. """

    min_rating, max_rating = define_boundary("Rating", float)
    return repository.search_rating(min_rating, max_rating, result)


def select_quicksort(selected_search_types: list[str]) -> tuple[str, str]:
    """ Ask user the criteria to sort result by.  """
    selected_sort_type = selected_search_types[0]
    if len(selected_search_types) > 1:
        sort_types = ["Title", "Year", "Rating"]
        selected_sort_type = dist_utils.ask_selection(
            "How do you want to sort your result?",
            dist_utils.generate_answer_selector(sort_types),
            dist_utils.generate_answer_selector_description(sort_types)
        )

    type_to_attribute = {
        "Title": "primaryTitle",
        "Year": "startYear",
        "Rating": "averageRating"
    }
    return selected_sort_type, type_to_attribute[selected_sort_type]


def movie_search():
    """ Main program loop. """

    init_repository()
    database_upgrade()

    keep_searching = True
    while keep_searching:
        search_type_choices = ["Title", "Year", "Rating"]
        selected_search_types = ask_search_type(search_type_choices)

        result = []
        if "Title" in selected_search_types:
            result = ask_title(result)

        if "Year" in selected_search_types:
            result = ask_year(result)

        if "Rating" in selected_search_types:
            result = ask_rating(result)

        selected_sort_type, sort_attribute = select_quicksort(selected_search_types)
        Repository.quicksort(result, sort_attribute, selected_sort_type == "Rating")

        if result:
            for i, movie in enumerate(result):
                print(movie)
                if (i + 1) % 10 == 0:
                    dist_utils.press_to_continue()
        else:
            print("Sorry, no movie was found.")
            dist_utils.press_to_continue()

        keep_searching = dist_utils.ask_yes_no("Do you wish to make another search?")

    print("Thank you for using Movie Search!")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    movie_search()
