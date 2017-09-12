

class Book(object):
    def __init__(self, title, author_fn, author_ln, isbn10, isbn13):
        self._title = title
        self._author_fn = author_fn
        self._author_ln = author_ln
        self._isbn10 = isbn10
        self._isbn13 = isbn13
