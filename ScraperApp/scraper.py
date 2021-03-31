"""
This is the main body for the scraper which is designed to
scrape the goodreads books and authors page.
"""
import time
import random
from bs4 import BeautifulSoup
import requests
from ScraperApp import db_handler
import sys


dbh = db_handler.DbHandler()


def eliminate_mark(word, mark):
    return word.replace(mark, "")


def get_similar_author(url):
    """
    Redirect to similar authors page to fetch similar author information
    :param url: the similar authors page
    :return: an Array of related author
    """
    time.sleep(random.randint(5, 15))
    related_authors_ = []
    related_author_page = requests.get(url).text
    related_author_soup = BeautifulSoup(related_author_page, 'lxml')
    related_authors_container = related_author_soup.find_all('div', class_='responsiveAuthor')
    for related_author in related_authors_container:
        related_author_name = related_author.find('span', itemprop='name').text
        related_authors_.append(related_author_name)
    return related_authors_


def get_id(url):
    """
    fetch id from url
    :param url: input url
    :return: id
    """
    return url.split("/")[-1].split("-")[0].split(".")[0]


def run_scraper(insert_url):
    """
    Main scraper running process
    Handling the scrapper running on the start book page
    :param insert_url: book page to start
    :return: length of scraped author and next book url to scrape
    """
    print("scraping book detail now...")
    start_page = requests.get(insert_url).text
    start_page_soup = BeautifulSoup(start_page, 'lxml')
    authors = start_page_soup.find_all('div', class_='authorName__container')
    for author in authors:
        author_url = author.a['href']
        get_author(author_url)
    next_url = scrape_book(insert_url, start_page_soup)
    return len(authors), next_url


def scrape_book(insert_url, start_page_soup):
    authors = start_page_soup.find_all('div', class_='authorName__container')
    book_author = []
    book_author_url = []
    similar_books = []
    if start_page_soup.find('title').text == 'Page not found':
        print("Page Not Found", file=sys.stderr)
        raise TypeError

    try:
        book_isbn = start_page_soup.find('meta', property='books:isbn')['content']
    except TypeError:
        book_isbn = ""
    for author in authors:
        author_url = author.a['href']
        author_name = author.a.span.text
        book_author.append(author_name)
        book_author_url.append(author_url)

    book_url = insert_url
    book_title = start_page_soup.find('div', class_='last col').find('h1', class_='gr-h1--serif').text.replace(" ", "")
    book_title = eliminate_mark(book_title, "\n")
    image_url = start_page_soup.find('div', class_='editionCover').img['src']
    book_id = get_id(insert_url)
    book_rating_container = start_page_soup.find('div', class_="uitext stacked")
    book_rating = book_rating_container.find('span', itemprop="ratingValue").text.replace(" ", "")
    review_rating = book_rating_container.find_all('a', class_="gr-hyperlink")
    book_rating_count = review_rating[0].text.split()[0]
    book_review_count = review_rating[1].text.split()[0]
    all_similar_books_soup = start_page_soup.find('div', class_="carouselRow")
    all_similar_books = all_similar_books_soup.find_all('li', class_="cover")
    next_url = ""
    book_rating = eliminate_mark(book_rating, "\n")
    book_rating_count = eliminate_mark(book_rating_count, "\n")
    book_rating_count = eliminate_mark(book_rating_count, ",")
    book_review_count = eliminate_mark(book_review_count, "\n")
    book_review_count = eliminate_mark(book_review_count, ",")
    for similar_book in all_similar_books:
        similar_books.append(similar_book.a.img['alt'])
        next_url = similar_book.a['href']
    book_post = {
        "book_title": book_title,
        "book_id": book_id,
        "isbn": book_isbn,
        "book_url": book_url,
        "book_author": book_author,
        "book_author_url": book_author_url,
        "book_rating": float(book_rating),
        "book_rating_count": int(book_rating_count),
        "book_review_count": int(book_review_count),
        "image_url": image_url,
        "related_books": similar_books,
    }
    dbh.insert_book(book_post)
    return next_url


def get_author(author_url):
    """
    Scraping the author page
    :param author_url:
    :return:
    """
    author_book = []
    author_id = get_id(author_url)
    time.sleep(random.randint(5, 15))
    print("Scraping author details now...")
    author_page = requests.get(author_url).text
    author_page_soup = BeautifulSoup(author_page, 'lxml')
    author_image_url = author_page_soup.find('div', class_='leftContainer authorLeftContainer').img['src']
    author_name = author_page_soup.find('h1', class_='authorName').span.text

    related_book_body = author_page_soup.find('table', class_="stacked tableList")
    related_books_container = related_book_body.find_all('tr')
    for book in related_books_container:
        book_name = book.span.text
        author_book.append(book_name)

    author_rating = author_page_soup.find('span', class_="average").text.replace(" ", "")
    author_rating_counts = author_page_soup.find('span', class_="votes").span.text.replace(" ", "")
    author_review_counts = author_page_soup.find('span', class_="count").span.text.replace(" ", "")
    similar_books_url = "https://www.goodreads.com/" + \
                        author_page_soup.find('div', class_="hreview-aggregate").find_all('a')[-1]['href']
    author_rating = eliminate_mark(author_rating, "\n")
    author_review_counts = eliminate_mark(author_review_counts, "\n")
    author_review_counts = eliminate_mark(author_review_counts, ",")
    author_rating_counts = eliminate_mark(author_rating_counts, "\n")
    author_rating_counts = eliminate_mark(author_rating_counts, ",")

    author_post = {
        "author_name": author_name,
        "author_id": author_id,
        "author_book": author_book,
        "similar_author": get_similar_author(similar_books_url),
        "author_url": author_url,
        "author_rating": float(author_rating),
        "author_rating_counts": int(author_rating_counts),
        "author_review_counts": int(author_review_counts),
        "author_image_url": author_image_url,
    }
    dbh.insert_author(author_post)
