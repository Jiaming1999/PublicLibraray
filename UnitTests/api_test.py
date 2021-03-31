from unittest import TestCase
import json
import app


class ApiUnitTest(TestCase):
    def setUp(self):
        self.app = app.app.test_client()

    def test_get_book_id(self):
        response = self.app.get('http://127.0.0.1:5000/book?id=3735293')
        self.assertEqual(response.status_code, 200)

    def test_get_book_isbn(self):
        response = self.app.get('http://127.0.0.1:5000/book?isbn=9780132350884')
        self.assertEqual(response.status_code, 200)

    def test_get_book_title(self):
        response = self.app.get('http://127.0.0.1:5000/book?title=CleanCode:AHandbookofAgileSoftwareCraftsmanship')
        self.assertEqual(response.status_code, 200)

    def test_get_author_id(self):
        response = self.app.get('http://127.0.0.1:5000/author?id=45372')
        self.assertEqual(response.status_code, 200)

    def test_get_author_name(self):
        response = self.app.get('http://127.0.0.1:5000/author?name=Kent%20Beck')
        self.assertEqual(response.status_code, 200)

    def test_put_book_isbn(self):
        url = 'http://127.0.0.1:5000/book?id=85039'
        response = self.app.put(url, data=json.dumps({'isbn': '12345678'}), content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_put_book_name(self):
        url = 'http://127.0.0.1:5000/book?id=85039'
        response = self.app.put(url, data=json.dumps({'book_title': 'I am CS Student'}),
                                content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_put_author_name(self):
        url = 'http://127.0.0.1:5000/author?id=45372'
        response = self.app.put(url, data=json.dumps({'author_name': 'Jiaming Zhang'}), content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_post_many_books(self):
        url = 'http://127.0.0.1:5000/books'
        response = self.app.post(url, data=json.dumps(
            [{'book_id': "1234", 'book_title': 'Jiaming Zhangs Book', 'book_rating': 2.2}]),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_post_one_author(self):
        url = 'http://127.0.0.1:5000/author'
        response = self.app.post(url, data=json.dumps({'author_id': "1234", 'author_name': 'Jiaming Zhangs', 'author_rating': 2.2}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_post_one_book(self):
        url = 'http://127.0.0.1:5000/book'
        response = self.app.post(url, data=json.dumps({'book_id': "12121", 'book_title': 'Jiaming Zhangs', 'book_rating': 3.3}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_search_book(self):
        response = self.app.get('http://127.0.0.1:5000/search?q=book.book_id%3A12')
        self.assertEqual(response.status_code, 201)

    def test_delete_none_exist_book(self):
        response = self.app.delete("http://127.0.0.1:5000/book?id=9829800212")
        self.assertEqual(response.status_code, 500)

    def test_delete_none_exist_author(self):
        response = self.app.delete("http://127.0.0.1:5000/author?id=9829800212")
        self.assertEqual(response.status_code, 500)

    def test_scrape_author_post(self):
        response = self.app.post("http://127.0.0.1:5000/scrape?attr=author/show/45370.Frank_Buschmann")
        self.assertEqual(response.status_code, 201)

    def test_book_scrape_post(self):
        response = self.app.post("http://127.0.0.1:5000/scrape?attr=book/show/4099.The_Pragmatic_Programmer")
        self.assertEqual(response.status_code, 201)



