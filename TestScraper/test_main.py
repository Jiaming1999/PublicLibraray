# Test file read from downloaded html to test mongodb writing and getting

from bs4 import BeautifulSoup
from ScraperApplication import db_handler

insert_url = "https://www.goodreads.com/book/show/3735293-clean-code?from_search=true&qid=HhMDV0vMa5&rank=1"


def get_similar_author():
    related_authors_ = []
    with open("../DownloadedHTML/TestSimilarAuthor.html", "r") as similar_html:
        related_author_page = similar_html.read()
        related_author_soup = BeautifulSoup(related_author_page, 'lxml')
        related_authors_container = related_author_soup.find_all('div', class_='responsiveAuthor')
        for related_author in related_authors_container:
            related_author_name = related_author.find('span', itemprop='name').text
            related_authors_.append(related_author_name)
        return related_authors_


def get_author_id(url):
    return url.split("/")[-1].split(".")[0]


def get_book_id(url):
    return url.split("/")[-1].split("-")[0]


book_count = 0

with open("../DownloadedHTML/TestBook.html", "r") as html_file:
    dbh = db_handler.DbHandler()
    start_page = html_file.read()
    start_page_soup = BeautifulSoup(start_page, 'lxml')
    authors = start_page_soup.find_all('div', class_='authorName__container')
    book_author = []
    book_author_url = []
    similar_books = []
    try:
        book_isbn = start_page_soup.find('meta', property='books:isbn')['content']
    except TypeError:
        book_isbn = ""
    print(len(authors))
    for author in authors:
        author_book = []
        author_url = author.a['href']
        author_name = author.a.span.text
        book_author.append(author_name)
        book_author_url.append(author_url)
        author_id = get_author_id(author_url)
        with open("../DownloadedHTML/TestAuthor3.htm", "r") as html_author:
            author_page = html_author.read()
            author_page_soup = BeautifulSoup(author_page, 'lxml')
            author_image_url = author_page_soup.find('div', class_='leftContainer authorLeftContainer').img['src']
            related_book_body = author_page_soup.find('table', class_="stacked tableList")
            related_books_container = related_book_body.find_all('tr')
            for book in related_books_container:
                book_name = book.span.text
                author_book.append(book_name)
            author_rating = author_page_soup.find('span', class_="average").text.replace(" ", "")
            author_rating_counts = author_page_soup.find('span', class_="votes").span.text.replace(" ", "")
            author_review_counts = author_page_soup.find('span', class_="count").span.text.replace(" ", "")
            author_post = {
                "author_name": author_name,
                "author_book": author_book,
                "similar_author": get_similar_author(),
                "author_url": author_url,
                "author_id": author_id,
                "author_rating": author_rating,
                "author_rating_counts": author_rating_counts,
                "author_review_counts": author_review_counts,
                "author_image_url": author_image_url,
            }
            dbh.insert(author_post)
            dbh.insert(author_post)
    book_url = "book_url"
    book_title = start_page_soup.find('div', class_='last col').find('h1', class_='gr-h1--serif').text.replace(" ", "")
    image_url = start_page_soup.find('div', class_='editionCover').img['src']
    book_id = get_book_id(insert_url)
    book_rating_container = start_page_soup.find('div', class_="uitext stacked")
    book_rating = book_rating_container.find('span', itemprop="ratingValue").text.replace(" ", "")
    review_rating = book_rating_container.find_all('a', class_="gr-hyperlink")
    book_rating_count = review_rating[0].text.split()[0]
    book_review_count = review_rating[1].text.split()[0]
    all_similar_books_soup = start_page_soup.find('div', class_="carouselRow")
    all_similar_books = all_similar_books_soup.find_all('li', class_="cover")
    for similar_book in all_similar_books:
        similar_books.append(similar_book.a.img['alt'])
    book_post = {
        "isbn": book_isbn,
        "book_url": book_url,
        "book_title": book_title,
        "book_author": book_author,
        "book_author_url": book_author_url,
        "book_rating": book_rating,
        "book_rating_count": book_rating_count,
        "book_review_count": book_review_count,
        "image_url": image_url,
        "related_books": similar_books,
    }
    dbh.insert(book_post)
    dbh.insert(book_post)


