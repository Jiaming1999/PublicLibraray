import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, abort, request, render_template

import query_author
import query_book
from ScraperApp import db_handler
from ScraperApp import scraper

app = Flask(__name__)


@app.route('/')
def default_route():
    """
    app.route('/'), default route
    """
    return jsonify("_")


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', title='404NotFound'), 404


@app.errorhandler(400)
def page_not_found(error):
    return render_template('400.html', title='400BadRequest'), 400


@app.route('/search', methods=['GET'])
def search_books():
    """
    search books with query language
    :return:
    """
    insert_query = request.args.get('q')
    if not query_book:
        abort(400, "Bad Request: Not valid search")
    res = query_book.query_handler_book(insert_query)
    return jsonify(res), 201


@app.route('/search', methods=['GET'])
def search_authors():
    """
    search authors with query language
    :return:
    """
    insert_query = request.args.get('q')
    if not query_author:
        abort(400, "Bad Request: Not valid search")
    res = query_author.query_handler_author(insert_query)
    return jsonify(res), 201


@app.route('/book', methods=['GET'])
def get_book_by_attr():
    """
    get book by attribute
    """
    dbh = db_handler.DbHandler()
    docs_book = dbh.fetch_books()
    is_id = request.args.get('id')
    is_title = request.args.get('title')
    is_isbn = request.args.get('isbn')
    if is_id:
        for obj in docs_book:
            if obj['_id'] == is_id:
                print(obj)
                return jsonify(obj), 200
        abort(404, "Page Not Found: no such id")
    if is_isbn:
        for obj in docs_book:
            if obj['isbn'] == is_isbn:
                print(obj)
                return jsonify(obj), 200
        abort(404, "Page Not Found: no such isbn")
    if is_title:
        for obj in docs_book:
            if obj['book_title'] == is_title:
                print(obj)
                return jsonify(obj), 200
        abort(404, "Page Not Found: no such title")
    abort(404, "Page Not Found: failed get book")


@app.route('/author', methods=['GET'])
def get_author_by_attr():
    """
    get author by attribute
    """
    dbh = db_handler.DbHandler()
    docs_author = dbh.fetch_author()
    is_id = request.args.get('id')
    is_name = request.args.get('name')
    if is_id:
        for obj in docs_author:
            if obj['_id'] == is_id:
                return jsonify(obj), 200
        abort(404, "Page Not Found: No such id")
    if is_name:
        for obj in docs_author:
            if obj['author_name'] == is_name:
                return jsonify(obj), 200
        abort(404, "Page Not Found: No such name")
    abort(404, "Page Not Found: failed get author")


@app.route('/book', methods=['PUT'])
def put_book():
    """
    Create books by PUT method
    :return:
    """
    dbh = db_handler.DbHandler()
    docs_book = dbh.fetch_books()
    book = {}
    is_id = request.args.get('id')
    if not is_id:
        abort(400, "Bad Request: Invalid id input")
    if not request.json:
        abort(400, "Bad Request: Invalid json input")
    if is_id:
        for obj in docs_book:
            if obj['_id'] == is_id:
                book = obj
    if book == {}:
        abort(404, "Page Not Found: No such a book")
    input_json = request.get_json(force=True)
    for key in input_json:
        if key == 'book_rating':
            book['book_rating'] = int(input_json[key])
        elif key == 'isbn':
            book['isbn'] = input_json[key]
        elif key == 'book_title':
            book['book_title'] = input_json[key].replace(" ", "")
        elif key == 'book_rating_count':
            book['book_rating_count'] = int(input_json[key])
        elif key == 'book_review_count':
            book['book_review_count'] = int(input_json[key])
        elif key == 'book_url':
            book['book_url'] = input_json[key]
        else:
            abort(400, "Bad Request: Invalid key")
    dbh.insert_book(book)
    return jsonify(book), 201


@app.route('/author', methods=['PUT'])
def put_author():
    """
    Create Author or Update Author with PUT method
    :return:
    """
    author = {}
    is_id = request.args.get('id')
    dbh = db_handler.DbHandler()
    docs_author = dbh.fetch_author()

    if not is_id:
        abort(400, "Bad Request: Invalid id input")
    if not request.json:
        abort(400, "Bad Request: Invalid json input")
    if is_id:
        for obj in docs_author:
            if obj['_id'] == is_id:
                author = obj
                break
    if author == {}:
        abort(404, "Page Not Found: No such an author")

    input_json = request.get_json()

    for key in input_json:
        if key == 'author_name':
            author['author_name'] = input_json[key]
        elif key == 'author_rating':
            author['author_rating'] = input_json[key]
        elif key == 'author_rating_counts':
            author['author_rating_counts'] = input_json[key]
        elif key == 'author_review_counts':
            author['author_review_counts'] = input_json[key]
        elif key == 'author_url':
            author['author_url'] = input_json[key]
        else:
            abort(400, "Bad Request: Invalid key")
    dbh.insert_author(author)
    return jsonify(author), 201


@app.route('/book', methods=['POST'])
def post_one_book():
    """
    Post request to ADD a book to backend
    :return:
    """
    dbh = db_handler.DbHandler()
    book_insert = request.get_json()
    if book_insert is None:
        abort(400, "Bad Request: Invalid insert book")
    res = dbh.insert_book(book_insert)
    return jsonify({"Post Acknowledged": bool(res.acknowledged)}), 201


@app.route('/author', methods=['POST'])
def post_one_author():
    """
    Post request to ADD a author to backend
    :return:
    """
    dbh = db_handler.DbHandler()
    author_insert = request.get_json()
    if author_insert is None:
        abort(400, "Bad Request: Invalid insert author")
    res = dbh.insert_author(author_insert)
    return jsonify({"Post Acknowledged": bool(res.acknowledged)}), 201


@app.route('/scrape', methods=['POST'])
def post_scrape():
    """
    Post request to ADD based on scrape
    :return:
    """
    url = request.args.get('attr')
    dbh = db_handler.DbHandler()
    if "book" in url:
        insert_url = "https://www.goodreads.com/" + url
        start_page = requests.get(insert_url).text
        start_page_soup = BeautifulSoup(start_page, 'lxml')
        scraper.scrape_book(insert_url, start_page_soup)
    elif "author" in url:
        insert_url = "https://www.goodreads.com/" + url
        scraper.get_author(insert_url)
    else:
        abort(400, "Bad Request: Invalid post scrape")
    return "Scrape Success", 201


@app.route('/books', methods=['POST'])
def post_many_book():
    """
    Post request to ADD many books
    :return:
    """
    dbh = db_handler.DbHandler()
    docs_to_insert = request.get_json()
    if docs_to_insert is None:
        abort(400, "Bad Request: Invalid insert books")
    res = dbh.insert_books(docs_to_insert)
    return jsonify({"Post Acknowledged": bool(res.acknowledged)}), 201


@app.route('/authors', methods=['POST'])
def post_many_author():
    """
    Post request to ADD many authors
    :return:
    """
    dbh = db_handler.DbHandler()
    docs_to_insert = request.get_json()
    if docs_to_insert is None:
        abort(400, "Bad Request: Invalid insert authors")
    res = dbh.insert_authors(docs_to_insert)
    return jsonify({"Post Acknowledged": bool(res.acknowledged)}), 201


@app.route('/book', methods=['DELETE'])
def delete_book_by_id():
    """
    delete a book from database by id
    :return:
    """
    dbh = db_handler.DbHandler()
    docs_book = dbh.fetch_books()
    book_id = request.args.get('id')
    deleted_doc = None
    for obj in docs_book:
        if obj['_id'] == book_id:
            deleted_doc = obj
    if deleted_doc is None:
        abort(400, "Delete a none existing file")
    res = dbh.delete_book(deleted_doc)
    return jsonify({"Delete Acknowledged": bool(res.acknowledged)}), 201


@app.route('/author', methods=['DELETE'])
def delete_author_by_id():
    """
    delete a author from database by id
    :return:
    """
    dbh = db_handler.DbHandler()
    docs_author = dbh.fetch_author()
    author_id = request.args.get('id')
    deleted_doc = None
    for obj in docs_author:
        if obj['_id'] == author_id:
            deleted_doc = obj
    if deleted_doc is None:
        abort(400, "Delete a none existing file")
    res = dbh.delete_author(deleted_doc)
    return jsonify({"Delete Acknowledged": bool(res.acknowledged)}), 201


@app.route('/books', methods=['GET'])
def get_all_books():
    """
    get all books
    :return:
    """
    dbh = db_handler.DbHandler()
    docs_book = dbh.fetch_books()
    res = {}
    for book in docs_book:
        if book['book_rating'] is None or book['book_title'] is None:
            continue
        res[book['book_title']] = book['book_rating']
    return jsonify(res), 200


@app.route('/authors', methods=['GET'])
def get_all_authors():
    """
    get all authors
    :return:
    """
    dbh = db_handler.DbHandler()
    docs_author = dbh.fetch_author()
    res = {}
    for author in docs_author:
        if author['author_rating'] is None or author['author_name'] is None:
            continue
        res[author['author_name']] = author['author_rating']
    return jsonify(res), 200


@app.after_request
def after_request(response):
    """
    @https://github.com/corydolphin/flask-cors/issues/200
    To solve connection blocked by cors
    :param response:
    :return:
    """
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response


if __name__ == '__main__':
    app.run(debug=True)
