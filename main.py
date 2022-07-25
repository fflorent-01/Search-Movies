#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Main file. Run from here. """
import logging
import dist_utils
import import_file
from classes import Repository, Movie, Rating

logging.basicConfig(level=logging.DEBUG)

repository = Repository()

def init_repository():
    repository.import_movies()
    repository.import_ratings()

    if not repository.movies:
        print(dist_utils.msg_box("You movie repository is empty. You will need to import data."))

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


def movie_search():
    keep_searching = True
    while keep_searching:
        search_type_choices = ["Title", "Year", "Rating"]
        primary_search_type = current_search_type = dist_utils.ask_selection(
            "What criteria would you like to use for your search?",
            dist_utils.generate_answer_selector(search_type_choices),
            dist_utils.generate_answer_selector_description(search_type_choices)
        )
        search_types = [primary_search_type]

        while True:
            search_type_choices.pop(search_type_choices.index(current_search_type))
            if not search_types:
                break
            add_criteria = dist_utils.ask_yes_no("Do you want to add a criteria to your search?")
            if not add_criteria:
                break
            current_search_type = dist_utils.ask_selection(
                "What additional criteria would you like to use for your search?",
                dist_utils.generate_answer_selector(search_type_choices),
                dist_utils.generate_answer_selector_description(search_type_choices)
            )
            search_types.append(current_search_type)

        result = []
        if "title" in search_types:
            title_string = input(
                "Please enter the [Title] (or part of it) of the movie(s) you are searching for.\n")
            result = repository.search_title(title_string)

        if "Year" in search_types:
            boundary_types = ["Lower", "Upper", "Both"]
            min_year = max_year = None
            selected_boundary = dist_utils.ask_selection(
                "What boundary do you wish to specify for your [Year] criteria?",
                dist_utils.generate_answer_selector(boundary_types),
                dist_utils.generate_answer_selector_description(boundary_types)
            )
            if selected_boundary in ["Lower", "Both"]:
                min_year = dist_utils.prompt_number(
                    "Please specify the LOWER boundary of your [Year] criteria.\n")
            if selected_boundary in ["Upper", "Both"]:
                max_year = dist_utils.prompt_number(
                    "Please specify the UPPER boundary of your [Year] criteria.\n")

            print(min_year, type(min_year), max_year, type(max_year))
            result = repository.search_year(min_year, max_year, result)

        if "Rating" in search_types:
            boundary_types = ["Lower", "Upper", "Both"]
            min_rating = max_rating = None
            selected_boundary = dist_utils.ask_selection(
                "What boundary do you wish to specify for your [Rating] criteria?",
                dist_utils.generate_answer_selector(boundary_types),
                dist_utils.generate_answer_selector_description(boundary_types)
            )
            if selected_boundary in ["Lower", "Both"]:
                min_year = dist_utils.prompt_number(
                    "Please specify the LOWER boundary of your [Rating] criteria.\n", float)
            if selected_boundary in ["Upper", "Both"]:
                max_year = dist_utils.prompt_number(
                    "Please specify the UPPER boundary of your [Rating] criteria.\n", float)

            result = repository.search_rating(min_rating, max_rating, result)

        # Implement quicksort

        for i, movie in enumerate(result):
            print(movie)
            if (i + 1) % 5 == 0:
                dist_utils.press_to_continue()

        keep_searching = dist_utils.ask_yes_no("Do you wish to make another search?")

    print("Thank you for suing Movie Search!")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    init_repository()
    movie_search()
