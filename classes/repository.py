#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Contain the Repository class and Movie definition """
import csv
from pathlib import Path
from typing import NamedTuple, Optional


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
                strings += extra_info

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
        if rating.uid not in self.movies:
            print("Movie not found")
            return
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
                row["uid"] = row.pop("tconst")
                self.add_rating(Rating(**row))

    def search_title(self, title) -> list[Movie]:
        """ Allow to search if string is in  """
        result = []
        for movie in self.movies.values():
            if title.upper() in movie.primaryTitle.upper() or title in movie.originalTitle.upper():
                result.append(movie)
        return result
