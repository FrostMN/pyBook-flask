import sqlite3, hashlib

## All sql function in this file need to be reworked to use proper parameter substitution to prevent injection
## I currently just have it 'working' and will look at security later

def CreateDB(db_name='pyBook.db'):
    ## creates the connection to the sqlite db
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    ## String to build the db for the application
    c.execute("""
    CREATE TABLE books(
      Book_ID INTEGER PRIMARY KEY AUTOINCREMENT,
      isbn10 int,
      isbn13 int,
      title varchar(200),
      author_ln varchar(200),
      author_fn varchar(200),
      status int,
      lendee varchar(200)
      );
    """)

    ## String to build the user db
    c.execute("""
    CREATE TABLE users (
      User_ID INTEGER PRIMARY KEY AUTOINCREMENT,
      email varchar(200),
      uname varchar(200),
      admin int,
      f_name varchar(200),
      l_name varchar(200),
      salt varchar(64),
      hash varchar(64)
    );
    """)

    ## makes the user asouer
    c.execute("""
    INSERT INTO users(email, uname, admin, f_name, l_name, salt, hash)
    VALUES ('asouer@gmail.com', 'asouer', 1, 'Aaron', 'Souer', 
    'JOntEtvVYhBn2c2i4LTond7EBjRC1XmTMXxZ070H0XxJdW7zQ9keTqidhovrMkMJ', 
    'f7ef43c2d80292f702f20545fb1b4996179a71ce6eee01cfd70cc04aa9db0f95');
    
    """)

    ## makes the user guest
    c.execute("""
    INSERT INTO users(email, uname, admin, f_name, l_name, salt, hash)
    VALUES ('guest@guest.com', 'guest', 0, 'Guest', 'User', 
    'JOntEtvVYhBn2c2i4LTond7EBjRC1XmTMXxZ070H0XxJdW7zQ9keTqidhovrMkMJ', 
    'e80b5f67da290f9ce5c22cd658eeae92696354c8461288d8c1e3d143f38e0226');

    """)

    ## commits changes and closes the connection
    conn.commit()
    conn.close()


def PrintDB(db_name='pyBook.db'):
    ## prints all data from the db

    conn = sqlite3.connect('pyBook.db')
    c = conn.cursor()
    sql_res = c.execute("select * from books")

    print("+" + ("-" * 9) + "+" + ("-" * 12) + "+" + ("-" * 15) + "+" + ("-" * 42) + "+" + ("-" * 17) + "+" + ("-" * 17) + "+" + ("-" * 8) + "+" + ("-" * 22) + "+")
    print("| " + "Book_id".ljust(7) + " | " + "isbn10".ljust(10) + " | " + "isbn13".ljust(13) + " | " + "title".ljust(40) + " | " + "author_ln".ljust(15) + " | " + "author_fn".ljust(15) + " | status | " + "lendee".ljust(20) + " |")
    print("+" + ("-" * 9) + "+" + ("-" * 12) + "+" + ("-" * 15) + "+" + ("-" * 42) + "+" + ("-" * 17) + "+" + ("-" * 17) + "+" + ("-" * 8) + "+" + ("-" * 22) + "+")
    for entry in sql_res.fetchall():
        print("| " + str(entry[0]).rjust(7) + " | " + str(entry[1]).rjust(10, "0") + " | " + str(entry[2]) + " | " + str(entry[3][0:40]).ljust(40) + " | " + str(entry[4]).ljust(15) + " | " + str(entry[5]).ljust(15) + " | " + str(entry[6]).rjust(6) + " | " + str(entry[7]).ljust(20) + " |")
        print("+" + ("-" * 9) + "+" + ("-" * 12) + "+" + ("-" * 15) + "+" + ("-" * 42) + "+" + ("-" * 17) + "+" + ("-" * 17) + "+" + ("-" * 8) + "+" + ("-" * 22) + "+")

    sql_usrs_res = c.execute("select * from users")

    print()

    print("+" + ("-" * 9) + "+" + ("-" * 25) + "+" + ("-" * 17) + "+" + ("-" * 22) + "+" + ("-" * 22) + "+" + ("-" * 24) + "+" + ("-" * 24) + "+")
    print("| " + "User_ID".ljust(7) + " | " + "email".ljust(23) + " | " + "uname".ljust(15) + " | " + "f_name".ljust(20) + " | " + "l_name".ljust(20) + " | " + "salt".ljust(22) + " | " + "hash".ljust(22) + " |")
    print("+" + ("-" * 9) + "+" + ("-" * 25) + "+" + ("-" * 17) + "+" + ("-" * 22) + "+" + ("-" * 22) + "+" + ("-" * 24) + "+" + ("-" * 24) + "+")


    for entry in sql_usrs_res.fetchall():
        print("| " + str(entry[0]).rjust(7) + " | " + str(entry[1]).ljust(23) + " | " + str(entry[2]).ljust(15) + " | " + str(entry[4]).ljust(20) + " | " + str(entry[5]).ljust(20) + " | " + (str(entry[6])[:19] + "...").ljust(22) + " | " + (str(entry[7])[:19] + "...").ljust(22) + " |")
        print("+" + ("-" * 9) + "+" + ("-" * 25) + "+" + ("-" * 17) + "+" + ("-" * 22) + "+" + ("-" * 22) + "+" + ("-" * 24) + "+" + ("-" * 24) + "+")

    conn.commit()
    conn.close()


def Execute(call, db_loc="pyBook.db", params=None):
    ## exectues a sql query
    conn = sqlite3.connect(db_loc)
    c = conn.cursor()
    if params == None:
        c.execute(call)
    else:
        c.execute(call, params)
    conn.commit()
    conn.close()



def isbnExist(isbn, db_loc="pybook.db"):
    ## queries the db to determine if a book has an entry
    param = (isbn,)
    conn = sqlite3.connect(db_loc)
    c = conn.cursor()
    if len(isbn) == 13:
        c.execute('SELECT COUNT(*) FROM books WHERE isbn13=?', param)
    else:
        c.execute('SELECT COUNT(*) FROM books WHERE isbn10=?', param)
    count = c.fetchone()
    conn.commit()
    conn.close()
    if count[0] == 0:
        return False
    else:
        return True


def lendStatus(isbn, db_loc="pyBook.db"):
    param = (isbn,)
    conn = sqlite3.connect(db_loc)
    c = conn.cursor()
    # builds the correct string depending on which isbn is used
    if len(isbn) == 13:
        c.execute('SELECT status, lendee FROM books WHERE isbn13=?', param)
    else:
        c.execute('SELECT status, lendee FROM books WHERE isbn10=?', param)
    status = c.fetchone()
    conn.commit()
    conn.close()
    return status


def lendBook(isbn, lendee, db_loc="pyBook.db"):
    params = (lendee, isbn)

    # builds the correct string depending on which isbn is used
    if len(isbn) == 13:
        call = "UPDATE books SET status='1', lendee=? WHERE isbn13=?"
    else:
        call = "UPDATE books SET status='1', lendee=? WHERE isbn10=?"
    Execute(call, db_loc, params)
    ## uncomment the following line if you want to see the changes to the db after this function is called
    #PrintDB()


def returnBook(isbn, db_loc="pyBook.db"): ##
    # builds the correct string depending on which isbn is used
    params = (isbn,)
    if len(isbn) == 13:
        call = "UPDATE books SET status='0', lendee='' WHERE isbn13=?"
    else:
        call = "UPDATE books SET status='0', lendee='' WHERE isbn10=?"
    Execute(call, db_loc, params) # runs the update call to "return" the book
    ## uncomment the following line if you want to see the changes to the db after this function is called
    #PrintDB()


def Fetch(call, db_loc="pyBook.db", params=""): ## returns a line from the db will change to make more universal
    param = (params,)
    conn = sqlite3.connect(db_loc)
    c = conn.cursor()
    if not params == "":
        c.execute(call, param)
    else:
        c.execute(call)
    fetched = c.fetchone()
    conn.commit()
    conn.close()
    return fetched


def FetchAll(call, db_loc="pyBook.db", params=""): ## returns a line from the db will change to make more universal
    param = (params,)
    conn = sqlite3.connect(db_loc)
    c = conn.cursor()
    if not params == "":
        c.execute(call, param)
    else:
        c.execute(call)
    fetched = c.fetchall()
    conn.commit()
    conn.close()
    return fetched


def getBookInfo(isbn):  ## should change this to return a book object from sql call
    if len(isbn) == 13:
        call = "SELECT * FROM books WHERE isbn13=?"
    else:
        call = "SELECT * FROM books WHERE isbn10=?"
    return Fetch(call, isbn)


def addBook(book, db_loc="pyBook.db"):
    call = """
INSERT INTO books(isbn10, isbn13, title, author_ln, author_fn, status, lendee) 
VALUES( ?, ?, ?, ?, ?, 0, '');
"""
    call_params = ( book._isbn10, book._isbn13, book._title, book._author_ln, book._author_fn )
    Execute(call, db_loc, call_params)

def getLibrary(db_loc="pyBook.db"):
    #callCount = "SELECT COUNT(*) FROM books"
    #count = Fetch(callCount, db_loc)
    callLibrary = "SELECT * FROM books"
    fetched = FetchAll(callLibrary, db_loc)
    #print(fetched)
    return fetched


def deleteBook(isbn, db_loc="pyBook.db"):
    isbn = (isbn,)
    call = """
DELETE FROM books WHERE isbn10=?;
"""
    Execute(call, db_loc, isbn)


def getUser(uname, db_loc="pyBook.db"):
    call = """
SELECT COUNT(*) FROM users WHERE uname=?
    """
    return Fetch(call, db_loc, uname)[0]

def isAdmin(uname, db_loc="pyBook.db"):
    call = """
SELECT admin FROM users Where uname=?"""
    if Fetch(call, db_loc, uname)[0] == 1:
        return True
    return False


def getSalt(uname, db_loc="pyBook.db"):
    call = """
    SELECT salt FROM users WHERE uname=?
        """
    return Fetch(call, db_loc, uname)[0]


def getHash(uname, db_loc="pyBook.db"):
    call = """
    SELECT hash FROM users WHERE uname=?
        """
    return Fetch(call, db_loc, uname)[0]


