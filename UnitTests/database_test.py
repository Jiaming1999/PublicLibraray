"""
Unit Tests
"""
import unittest
import json
from ScraperApp import json_handler
from ScraperApp import scraper
import main


class MyTestCase(unittest.TestCase):
    """
    Unit test for helper function of scrapper
    """

    def test_json_validate(self):
        """
        Test for valid json file transformation
        :return:
        """
        file = open("../TestJSON/test1.json")
        data = json.load(file)
        self.assertEqual(json_handler.validate_json("../TestJSON/test1.json"), data)
        file.close()

    def test_get_id_validate_book(self):
        """
        Test for get book id from url
        :return:
        """
        get_id = scraper.get_id("https://www.goodreads.com/book/show/3735293-clean-code")
        self.assertEqual("3735293", get_id)

    def test_get_id_validate_author(self):
        """
        Test for get author id from url
        :return:
        """
        get_id = scraper.get_id("https://www.goodreads.com/author/show/45372.Robert_C_Martin")
        self.assertEqual("45372", get_id)

    def test_other_url_validate(self):
        """
        Test for inputting other website url
        :return:
        """
        url = "https://www.w3schools.com/python/python_classes.asp"
        self.assertEqual(main.validate_book_page(url), False)

    def test_not_book_url_validate(self):
        """
        Test for goodreads url but not a book page
        :return:
        """
        url = "https://www.goodreads.com/"
        self.assertEqual(main.validate_book_page(url), False)

    def test_not_detail_page_validate(self):
        """
        Test for a incomplete url
        :return:
        """
        url = "https://www.goodreads.com/book/"
        self.assertEqual(main.validate_book_page(url), False)

    def test_run_author_first(self):
        """
        Start program with author page
        :return:
        """
        url = "https://www.goodreads.com/author/show/114059.Elbert_Hubbard"
        self.assertEqual(main.validate_book_page(url), False)


if __name__ == '__main__':
    unittest.main()
