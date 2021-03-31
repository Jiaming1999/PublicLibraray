"""
This is the python file for json_handler, handling json generation and inserting json
to data base.
"""
import json
from bson.json_util import dumps
from ScraperApp import db_handler


def validate_json(file):
    """
    validate if json file is good to open
    :param file: the file need to be insert to mongoDB
    :return: valid data posts to open
    """
    try:
        file = open(file)
    except FileNotFoundError or FileExistsError:
        raise TypeError
    try:
        data = json.load(file)
        file.close()
    except ValueError:
        print("invalid json file format")
        file.close()
        raise TypeError
    return data


def insert_with_json(file):
    """
    insert the json post to mongoDB
    :param file: valid transferred json file
    :return: none
    """
    try:
        data = validate_json(file)
    except TypeError:
        print("invalid json file open...")
        raise TypeError
    dbh = db_handler.DbHandler()
    for post in data['author_details']:
        print("inserting author details from json file...")
        dbh.insert_author(post)
    for post in data['book_details']:
        print("inserting book details from json file...")
        dbh.insert_book(post)
    return


def export_with_json():
    """
    export files with json
    :return:
    """
    dbh = db_handler.DbHandler()
    docs_author = dbh.fetch_author()
    json_data_author = dumps(docs_author, indent=2)
    docs_book = dbh.fetch_books()
    json_data_book = dumps(docs_book, indent=2)
    return json_data_book, json_data_author
