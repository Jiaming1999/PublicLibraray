from ScraperApp import db_handler

dbh = db_handler.DbHandler()
docs_author = dbh.fetch_author()


def query_handler_author(query):
    """
    handler for author query language
    :param query:
    :return:
    """
    query = str(query)
    if "." not in query:
        raise ValueError("Invalid query format")
    else:
        if ":" in query:
            res = complex_author_query(query)
        else:
            res = simple_author_query(query)
    return res


def simple_author_query(query):
    """
    author query for format author.attr
    :param query:
    :return:
    """
    args = query.split('.')
    res = {}
    if args[0] != "author":
        raise TypeError("This is not a author")
    for obj in docs_author:
        if obj.get(args[1]) is None:
            continue
        res[obj['author_name']] = obj[args[1]]
    if res == {}:
        raise ValueError("The field does not exist")
    return res


def complex_author_query(query):
    """
    author query for format author.attr:content
    :param query:
    :return:
    """
    args = query.split(':')
    function = args[1]
    base = args[0].split('.')
    attr = base[1]
    if base[0] != 'author':
        raise TypeError("This is not a author")
    function = function.split(" ")
    if len(function) == 1:
        res = match_author(function[0], attr)
    elif len(function) == 2:
        op = function[0]
        value = function[1]
        res = single_query_author(op, value, attr)
    elif len(function) == 3:
        op = function[0]
        value_left = function[1]
        value_right = function[2]
        res = logical_query_author(op, value_left, value_right, attr)
    else:
        raise TypeError("Invalid Query")
    return res


def match_author(function, attr):
    """
    author query for matching pattern
    with "" to be exact match
    :param function:
    :param attr:
    :return:
    """
    res = {}
    if "\"" not in function:
        for obj in docs_author:
            if obj.get(attr) is None:
                continue
            if function[0] in obj[attr]:
                res[obj['author_name']] = obj[attr]
    else:
        function.replace("\"", "")
        for obj in docs_author:
            if obj.get(attr) is None:
                continue
            if function == obj[attr]:
                res[obj['author_name']] = obj[attr]
    if res == {}:
        raise ValueError("The search does not exist")
    return res


def single_query_author(op, value, attr):
    """
    author query for format author.attr:Not value
    :param op:
    :param value:
    :param attr:
    :return:
    """
    res = {}
    if op.upper() != "NOT" and op != ">" and op != "<":
        raise ValueError("Invalid input")
    if op.upper() == "NOT":
        for obj in docs_author:
            if obj.get(attr) is None:
                continue
            if value not in obj[attr]:
                res[obj['author_name']] = obj[attr]
    elif op == ">":
        for obj in docs_author:
            if obj.get(attr) is None:
                continue
            if int(value) < obj[attr]:
                res[obj['author_name']] = obj[attr]
    elif op == "<":
        for obj in docs_author:
            if obj.get(attr) is None:
                continue
            if int(value) > obj[attr]:
                res[obj['author_name']] = obj[attr]
    if res == {}:
        raise ValueError("Field does not exist")
    return res


def logical_query_author(op, value_left, value_right, attr):
    """
    Author query for AND and OR operator
    :param op:
    :param value_left:
    :param value_right:
    :param attr:
    :return:
    """
    if op.upper() != "AND" and op.upper() != "OR":
        raise ValueError("Invalid input")
    try:
        res_left = match_author(value_left, attr)
    except ValueError:
        print("")
    try:
        res_right = match_author(value_right, attr)
    except ValueError:
        print("")
    if op.upper() == "AND":
        res = dict(set(res_left.items()) & set(res_right.items()))
    else:
        res = dict(list(res_left.items()) + list(res_right.items()))
    if res == {}:
        raise ValueError("Field not exist")
    return res



