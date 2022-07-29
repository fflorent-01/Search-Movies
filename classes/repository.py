#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Contain the Repository class and Movie definition """
import csv
import logging
import unicodedata
from random import randrange
from pathlib import Path
from typing import NamedTuple, Optional

logging.basicConfig(level=logging.DEBUG)

class Rating(NamedTuple):
    """ Contain movie rating """
    uid: str
    averageRating: float
    numVotes: int


class Movie(NamedTuple):
    """ Contain the basic information of the movie """
    uid: str
    primaryTitle: str
    originalTitle: str
    isAdult: bool
    startYear: str
    genres: list[str]
    rating: Optional[Rating] = None

    def __str__(self):
        title = f"Title: {self.primaryTitle}, ({self.startYear if self.startYear else 'UNKNOWN'})"
        if self.primaryTitle != self.originalTitle:
            title += f"\nOriginal title: {self.originalTitle}"
        genre = f"Genre: {'•'.join(self.genres)}" if self.genres else "UNKNOWN"
        adult = " *** Adult Movie ***" if self.isAdult else ""
        rating = ""
        if self.rating:
            rating = f"Rating: {self.rating.averageRating} out of {self.rating.numVotes} votes"

        pad = 60 * "-"
        strings = [pad, title, genre]
        for extra_info in [adult, rating]:
            if extra_info:
                strings.append(extra_info)

        return "\n".join(strings + [""])


class Repository:
    """
    Repository that will contain the list of all movies and the method to manipulate them
    """

    def __init__(self):
        self.movies: dict[str, Movie] = {}

    def add_movie(self, movie: Movie) -> None:
        """ Add a movie to the Repository or replace it if it exists but is different """
        if movie.uid not in self.movies or self.movies[movie.uid] != movie:
            self.movies[movie.uid] = movie

    def add_rating(self, rating: Rating) -> None:
        """ Add rating to the movie if it finds a match """
        if self.movies[rating.uid].rating != rating:
            self.movies[rating.uid] = self.movies[rating.uid]._replace(rating=rating)

    def import_movies(self) -> None:
        """ Read title_basic.csv, create movie and try to add to the registry """
        file_path = Path(__file__).parent.parent.joinpath('data', "title_basic.csv")
        with open(file_path, encoding="utf8") as movie_file:
            reader = csv.DictReader(movie_file)
            for row in reader:
                for key, elem in row.items():
                    row[key] = elem.replace(r"\N", "")
                row["uid"] = row.pop("tconst")
                row["isAdult"] = bool(int(row["isAdult"]))
                if row["genres"]:
                    row["genres"] = row["genres"].split(",")

                self.add_movie(Movie(**row))

    def import_ratings(self) -> None:
        """ Read rating.csv, create ratings and try to add to the registry """
        file_path = Path(__file__).parent.parent.joinpath('data', "rating.csv")
        with open(file_path, encoding="utf8") as rating_file:
            reader = csv.DictReader(rating_file)
            for row in reader:
                for key, elem in row.items():
                    row[key] = elem.replace(r"\N", "")
                row["uid"] = row.pop("tconst")
                self.add_rating(Rating(**row))

    @staticmethod
    def _get_attrib(lst: list, attrib: str, index: int):
        if attrib in ["averageRating", "averageRating"]:
            return getattr(lst[index].rating, attrib)

        return getattr(lst[index], attrib)

    @staticmethod
    def quicksort(lst: list[Movie],
                  attrib: Optional[str] = "primaryTitle",
                  reverse: bool = False,
                  start: Optional[int] = 0,
                  end: Optional[int] = None) -> None:
        """
        Quicksort algorythm.

        - Allow choice of the attribute to be sorted
        - Allow reverse order
        """

        # Initialize end value
        if end is None:
            end = len(lst) - 1
        # Base case
        if start >= end or len(lst) == 1:
            return

        def compare(val_1, val_2):
            if reverse:
                return val_1 > val_2
            return val_1 < val_2

        def normalize_string(string: str) -> str:
            # https://stackoverflow.com/a/517974
            nfkd_form = unicodedata.normalize('NFKD', string)
            return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

        # Randomly select an item
        pivot_index = randrange(start, end + 1)
        # Ideally this would be decoupled, but I got to move on
        pivot_value = normalize_string(Repository._get_attrib(lst, attrib, pivot_index)).upper()

        # Put selected item at end of the list
        lst[end], lst[pivot_index] = lst[pivot_index], lst[end]

        pointer = start
        # Move the pointer from start to end
        for cursor in range(start, end):
            cursor_value = normalize_string(Repository._get_attrib(lst, attrib, cursor)).upper()

            if compare(cursor_value, pivot_value):
                lst[cursor], lst[pointer] = lst[pointer], lst[cursor]
                pointer += 1

        lst[end], lst[pointer] = lst[pointer], lst[end]

        Repository.quicksort(lst, attrib, reverse, start, pointer - 1)
        Repository.quicksort(lst, attrib, reverse, pointer + 1, end)

    def search_title(self, title: str, lst: Optional[list[Movie]] = None) -> list[Movie]:
        """ Return list of movies that match the provided string. """

        if not lst:
            lst = list(self.movies.values())
        result = [movie for movie in lst
                  if title in movie.primaryTitle or title in movie.originalTitle]

        return result

    def search_year(self,
                    min_year: Optional[int] = None,
                    max_year: Optional[int] = None,
                    lst: Optional[list[Movie]] = None) -> list[Movie]:
        """ Return a list of movies that have startYear within specified boundaries. """

        if not lst:
            lst = list(self.movies.values())

        if min_year and max_year:
            return [movie for movie in lst
                    if movie.startYear and min_year <= int(movie.startYear) <= max_year]
        if min_year:
            return [movie for movie in lst
                    if movie.startYear and min_year <= int(movie.startYear)]
        if max_year:
            return [movie for movie in lst
                    if movie.startYear and int(movie.startYear) <= max_year]
        return []

    def search_rating(self,
                      min_val: Optional[float] = None,
                      max_val: Optional[float] = None,
                      lst: Optional[list[Movie]] = None) -> list[Movie]:
        """ Return a list of movies that have rating.averageRating within specified boundaries. """

        if not lst:
            lst = list(self.movies.values())

        if min_val and max_val:
            return [movie for movie in lst
                    if movie.rating and min_val <= float(movie.rating.averageRating) <= max_val]
        if min_val:
            return [movie for movie in lst
                    if movie.rating and min_val <= float(movie.rating.averageRating)]
        if max_val:
            return [movie for movie in lst
                    if movie.rating and float(movie.rating.averageRating) <= max_val]
        return []
