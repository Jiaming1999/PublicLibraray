from ScraperApp import db_handler

dbh = db_handler.DbHandler()
docs_book = dbh.fetch_books()


def query_handler_book(query):
    """
    Handling book collection query language
    :param query:
    :return:
    """
    query = str(query)
    if "." not in query:
        raise ValueError("Invalid query format")
    else:
        if ":" in query:
            res = complex_book_query(query)
        else:
            res = simple_book_query(query)
    return res


def simple_book_query(query):
    """
    Book query of format book.attr
    :param query:
    :return:
    """
    args = query.split('.')
    res = {}
    if args[0] != "book":
        raise TypeError("This is not a book")
    for obj in docs_book:
        if obj.get(args[1]) is None:
            continue
        res[obj['book_title']] = obj[args[1]]
    if res == {}:
        raise ValueError("The field does not exist")
    return res


def complex_book_query(query):
    """
    Book query of format book.attr:content
    :param query:
    :return:
    """
    args = query.split(':')
    function = args[1]
    base = args[0].split('.')
    attr = base[1]
    if base[0] != 'book':
        raise TypeError("This is not a book")
    function = function.split(" ")
    if len(function) == 1:
        res = match_book(function[0], attr)
    elif len(function) == 2:
        op = function[0]
        value = function[1]
        res = not_query_book(op, value, attr)
    elif len(function) == 3:
        op = function[0]
        value_left = function[1]
        value_right = function[2]
        res = logical_query_book(op, value_left, value_right, attr)
    else:
        raise TypeError("Invalid Query")
    return res


def match_book(function, attr):
    """
    Matching pattern of book.attr:attr
    "" mark meaning exact match
    :param function:
    :param attr:
    :return:
    """
    res = {}
    if "\"" not in function:
        for obj in docs_book:
            if obj.get(attr) is None:
                continue
            if function[0] in obj[attr]:
                res[obj['book_title']] = obj[attr]
    else:
        function.replace("\"", "")
        for obj in docs_book:
            if obj.get(attr) is None:
                continue
            if function == obj[attr]:
                res[obj['book_title']] = obj[attr]
    if res == {}:
        raise ValueError("The search does not exist")
    return res


def not_query_book(op, value, attr):
    """
    Book query of format book.attr:Not value
    :param op:
    :param value:
    :param attr:
    :return:
    """
    res = {}
    if op.upper() != "NOT" and op != ">" and op != "<":
        raise ValueError("Invalid input")
    if op.upper() == 'NOT':
        for obj in docs_book:
            if obj.get(attr) is None:
                continue
            if value not in obj[attr]:
                res[obj['book_title']] = obj[attr]
    elif op == ">":
        for obj in docs_book:
            if obj.get(attr) is None:
                continue
            if int(value) < obj[attr]:
                res[obj['book_title']] = obj[attr]
    elif op == "<":
        for obj in docs_book:
            if obj.get(attr) is None:
                continue
            if int(value) > obj[attr]:
                res[obj['book_title']] = obj[attr]
    if res == {}:
        raise ValueError("Field does not exist")
    return res


def logical_query_book(op, value_left, value_right, attr):
    """
    book query of And and Or operator
    :param op:
    :param value_left:
    :param value_right:
    :param attr:
    :return:
    """
    if op.upper() != "AND" and op.upper() != "OR":
        raise ValueError("Invalid input")
    try:
        res_left = match_book(value_left, attr)
    except ValueError:
        print("")
    try:
        res_right = match_book(value_right, attr)
    except ValueError:
        print("")
    if op.upper() == "AND":
        res = dict(set(res_left.items()) & set(res_right.items()))
    else:
        res = dict(list(res_left.items()) + list(res_right.items()))
    if res == {}:
        raise ValueError("Field not exist")
    return res


