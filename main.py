import argparse
import json
import random
import sys
import time
import requests
from ScraperApp import json_handler, scraper
import query_author
import query_book
import app

"""
Set up parser for command line interface
"""


def set_up_parser():
    parser = argparse.ArgumentParser(description='scraping the website')
    parser.add_argument('-a', '--author', type=int, help='author limit of scraping')
    parser.add_argument('-b', '--book', type=int, help='book limit of scraping')
    parser.add_argument('-i', '--insert', type=str, help='insert url')
    parser.add_argument('-j', '--json', type=str, help='json file to insert')
    parser.add_argument('-bq', '--bookquery', type=str, help='book query language')
    parser.add_argument('-aq', '--authorquery', type=str, help='author query language')
    parser.add_argument('-g', '--get', type=str, help='get from API')
    parser.add_argument('-p', '--put', type=str, help='put from API')
    parser.add_argument('-po', '--post', type=str, help='post from API')
    parser.add_argument('-d', '--delete', type=str, help='delete from API')
    return parser.parse_args()


# set up basic functionality of scraper
args = set_up_parser()


def validate_book_page(url):
    """
    validate whether the url is referring to a book page
    :param url:
    :return:
    """
    if "goodreads" not in url:
        print("The website is not pointing to Goodreads")
        return False
    if "book" not in url or "show" not in url:
        print("The website is not pointing to a potential book page")
        return False
    if len(url.split("/")) != 6:
        print("Invalid url format")
        return False
    return True


def is_start_url_valid(url):
    """
    Check if input url is valid to scrape
    throw exception and error message if not valid and restart the program
    :param url: The input url
    :return: None
    """
    if validate_book_page(url) is False:
        sys.exit()
    try:
        requests.get(url)
    except requests.exceptions.ConnectionError:
        print("There is an issue on network, connection failed", file=sys.stderr)
        sys.exit()
    except requests.exceptions.Timeout:
        print("request time out", file=sys.stderr)
        sys.exit()
    except requests.exceptions.HTTPError:
        print("invalid HTTP response", file=sys.stderr)
        sys.exit()
    except requests.exceptions.MissingSchema:
        print("Invalid URL, Please reenter", file=sys.stderr)
        sys.exit()


def start():
    """
    The loop for program to run with terminal interface
    run with command line:
    python main.py
    -a <author_limit>
    -b <book_limit>
    -i <insert_url>
    -j <json_file>
    :return: None
    """
    my_app = app.app.test_client()

    book_count = 0
    author_count = 0
    insert_url = args.insert or ""
    book_limit = args.book or 1
    author_limit = args.author or 1
    file_name = args.json or "exit"
    book_query = args.bookquery or ''
    author_query = args.authorquery or ''
    get_url = args.get or ''
    put_url = args.put or ''
    post_url = args.post or ''
    delete_url = args.delete or ''

    if get_url != '':
        my_app.get(get_url)
    if put_url != '':
        my_app.put(put_url, data=json.dumps(json_handler.validate_json(file_name)),
                   content_type='application/json')
    if post_url != '':
        if "scrape" in post_url:
            my_app.post(post_url)
        else:
            my_app.post(post_url, data=json.dumps(json_handler.validate_json(file_name)),
                        content_type='application/json')
    if delete_url != '':
        my_app.delete(delete_url)
    if book_query != '':
        res = query_book.query_handler_book(book_query)
        print(res)

    if author_query != '':
        res = query_author.query_handler_author(author_query)
        print(res)

    if book_limit > 2000:
        print("book limit too big, more than 2000", file=sys.stderr)
        sys.exit()
    if book_limit > 50:
        print("Warning: scraping more than 50 could be very costly and take a long time")
    if author_limit > 2000:
        print("author limit too big, more than 2000", file=sys.stderr)
        sys.exit()
    if author_limit > 200:
        print("Warning: scraping more than 200 could be very costly and take a long time")
    is_start_url_valid(insert_url)
    while book_count < book_limit and author_count < author_limit:
        try:
            author_num, next_url = scraper.run_scraper(insert_url)
        except TypeError:
            print("Invalid input url", file=sys.stderr)
            sys.exit()
        book_count += 1
        author_count += author_num
        insert_url = next_url
        time.sleep(random.randint(5, 15))
    try:
        json_handler.insert_with_json(file_name)
    except TypeError:
        print("invalid json file", file=sys.stderr)
    print("exporting from database as JSON file...")
    export_json_file()
    sys.exit()


def export_json_file():
    """
    export the database collection as json file
    :return:
    """
    json_data_book, json_data_author = json_handler.export_with_json()
    with open('collection.json', 'w') as file:
        file.write("{ \"book details\":")
        file.write(json_data_book)
        file.write(", \"author details\":")
        file.write(json_data_author)


if __name__ == '__main__':
    start()
