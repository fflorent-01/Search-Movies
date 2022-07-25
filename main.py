#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Main file. Run from here. """

import dist_utils
import import_file
from classes import Repository, Movie, Rating

repository = Repository()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # TODO review this part
    try:
        repository.import_movies()
        repository.import_ratings()

    except Exception as e:
        print(e)

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

    # Select search type
    search_type_choices = ["Title", "Year", "Rating"]
    search_type = dist_utils.ask_selection(
        "What criteria would you like to use for your search?",
        dist_utils.generate_answer_selector(search_type_choices),
        dist_utils.generate_answer_selector_description(search_type_choices)
    )

    if search_type == "Title":
        title_string = input(
            "Please enter the title (or part of it) of the movie(s) you are searching for.\n")
        title_result = repository.search_title(title_string)
        for title in title_result:
            print(title)
