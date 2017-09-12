from flask import Flask, render_template, request, session, flash, redirect, url_for, abort
from secure import testPWORD
from media import Book
from fileIO import fileExists, createConfig
from apiCalls import getBook
import valid, secrets
from sqlCalls import *

from config import config as conf
from default_conf import config as dconf

if conf == "":
    print("using default conf")
    config = dconf
else:
    print("using generated conf")
    config = conf

app = Flask(__name__)

app.config.update(config)

db_path = app.root_path + "/pyBook.db"

@app.route('/')
def main():
    if not fileExists(app.root_path + "/pyBook.db"):
        return redirect(url_for('setup'))
    books = getLibrary(app.root_path + "/pyBook.db")
    print(books)
    if 'username' in session:
        creds = {'user': session['username'], 'admin': session['admin']}
    print(session)
    if "isbn" in session:
        isbn = session['isbn']
        print("isbn is set: " + isbn)
    if 'username' in session:
        if "isbn" in session:
            return render_template('index.html', dbBooks=books, creds=creds, isbnSrch=isbn)
        return render_template('index.html', dbBooks=books, creds=creds)
    else:
        return render_template('index.html', dbBooks=books)



@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if getUser(request.form['USER'], db_path) == 0:
            error = 'Invalid username or password'
        elif not testPWORD(request.form['USER'], request.form['PASSWORD'], db_path):
            error = 'Invalid username or password'
        else:
            session['logged_in'] = True
            session['username'] = request.form['USER']
            if (isAdmin(request.form['USER'], db_path)):
                print("is admin")
                session['admin'] = True
            else:
                print("not admin")
                session['admin'] = False
            flash('You were logged in')
            return redirect(url_for('main'))
    return render_template('index.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('main'))


@app.route('/lend', methods=['GET', 'POST'])
def lend():
    error = None
    if not session.get('logged_in'):
        return redirect(url_for('main'))
    else:
        if request.method == 'POST':
            print(request.form)
            lendBook(request.form['ISBN'], request.form['LENDEE'], db_path)
            return redirect(url_for('main'))
    return render_template('index.html', error=error)


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    error = None
    if not session.get('logged_in'):
        return redirect(url_for('main'))
    else:
        if request.method == 'POST':
            print(request.form)
            deleteBook(request.form['ISBN'], db_path)
            return redirect(url_for('main'))
    return render_template('index.html', error=error)


@app.route('/returned', methods=['GET', 'POST'])
def returned():
    error = None
    if not session.get('logged_in'):
        return redirect(url_for('main'))
    else:
        if request.method == 'POST':
            print(request.form)
            returnBook(request.form['ISBN'], db_path)
            return redirect(url_for('main'))
    return render_template('index.html', error=error)


@app.route('/search', methods=['GET', 'POST'])
def search():
    error = None
    if request.method == 'POST':
        raw = request.form['ISBN']
        isbn = valid.ISBN(raw)
        if(isbn):
            print(isbn + ': is a valid isbn')
            if (isbnExist(isbn, app.root_path + "/pyBook.db")):
                print('isbn exists')
                session['isbn'] = isbn;
                return redirect(url_for('main'), )
            else:
                print(isbn + ": is not in the db")
                return redirect(url_for('new_isbn'), code=307)
        else:
            print(raw + ': is not a valid isbn')
    return render_template('index.html', error=error)

@app.route('/setup')
def setup():
    if not session.get('logged_in'):
        return redirect(url_for('main'))
    else:
        return render_template('setup.html')

@app.route('/create', methods=['GET', 'POST'])
def create():
    if not session.get('logged_in'):
        return redirect(url_for('main'))
    else:
        if request.method == 'POST':
            if conf == "":

                flask_secret_key = secrets.token_hex(32)
                api_url = "http://isbndb.com/api/v2/json/{{KEY}}/book/"
                api_key = request.form['API_KEY']

                configString = """config = {'API_URL': '{{api_url}}', 'API_KEY': '{{api_key}}', 'SECRET_KEY': '{{secret}}', 'USERNAME': 'testing', 'PASSWORD': '123Testing'}"""

                configString = configString.replace('{{api_url}}', api_url)
                configString = configString.replace('{{api_key}}', api_key)
                configString = configString.replace('{{secret}}', flask_secret_key)

                print(configString)

                print(app.root_path)

                createConfig(configString, app.root_path + "/config.py")

                CreateDB(app.root_path + "/pyBook.db")
                return redirect(url_for('main'))
            return redirect(url_for('main'))
        return redirect(url_for('main'))


@app.route('/new', methods=['GET', 'POST'])
def new_isbn():
    if not session.get('logged_in'):
        return redirect(url_for('main'))
    else:
        if request.method == 'POST':
            print('in /new')
            print(request.form)
            try:
                print("in try")
                print(getBook(request.form['ISBN']))
                newBook = getBook(request.form['ISBN'])
            except:
                return redirect(url_for('edit'), code=307)
            print(newBook)
            if newBook._author_fn == "":
                return redirect(url_for('edit'), code=307)
            return render_template('new.html', newBook=newBook)
        return render_template('new.html')


@app.route('/add', methods=['GET', 'POST'])
def add_isbn():
    if not session.get('logged_in'):
        return redirect(url_for('main'))
    else:
        if request.method == 'POST':
            addBook(getBook(request.form['ISBN']), app.root_path + "/pyBook.db")
        return redirect(url_for('main'))
    return redirect(url_for('main'))


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    if not session.get('logged_in'):
        return redirect(url_for('main'))
    else:
        print (getBook(request.form['ISBN']))
        newBook = getBook(request.form['ISBN'])
        return render_template('edit.html', newBook=newBook)


@app.route('/make', methods=['GET', 'POST'])
def make():
    if not session.get('logged_in'):
        return redirect(url_for('main'))
    else:
        if request.method == 'POST':
            newBook = Book(str(request.form['TITLE']).strip(), str(request.form['FNAME']).strip(), str(request.form['LNAME']).strip(), str(request.form['ISBN10']).strip(), str(request.form['ISBN13']).strip() )
            addBook(newBook, app.root_path + "/pyBook.db")
            print(request.form)
            return redirect(url_for('main'))
        return render_template('edit.html')


if __name__ == '__main__':
    app.run()

