from flask import Flask, render_template, request
from openpyxl import load_workbook
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from database import engine, Book

app = Flask(__name__)
db = scoped_session(sessionmaker(bind=engine))

@app.route('/')
def home_page():
    return render_template ('index.html')

@app.route('/form/')
def form():
    return render_template('form.html')

@app.route('/books/')
def books():
    if 'key_word' in request.args:
        key_word = request.args.get("key_word")
        session = sessionmaker(engine)()
        books = session.execute(f"""
            SELECT * FROM "Book"
            WHERE name LIKE '%{key_word}%'
                OR author LIKE '%{key_word}%'
            ;
        """)
        session.commit()
    else:
        with engine.connect() as con:
            books = con.execute("""SELECT * FROM "Book";""")

    return render_template("books_table.html", object_list=books)

    # excel = load_workbook('tales.xlsx')
    # page = excel['Лист1']

    # object_list = [[tale.value, tale.offset(column=1).value] for tale in page ['A'][1:]]
    # return render_template('books.html', object_list=object_list)
    # tales = [tale.value for tale in page['A']][1:]


    # authors = [author.value for author in page['B']][1:]

    # html = '''
    #        <a href='/books'>Книги</a>
    #        <a href='/authors/'>авторы </a>
    #        <h1> Тут будет список книг <h1>
    #        '''

    # for i in range(len(tales)):
    #     html += f'<h2>{tales[i]} - {authors[i]}<h2>' 
    
    # return html



@app.route("/authors/")
def db_authors():
    with engine.connect() as con:
        authors = con.execute('SELECT DISTINCT author FROM "Book";')

    return render_template(
        "authors_table.html", authors=authors
    )

@app.route("/db/add/", methods=["POST"])
def db_add():
    f = request.form
    book = f["book"]
    author = f["author"]
    url = f["url"]    
    
    ids = db.execute('SELECT id FROM "Book" ORDER BY id DESC;')
    max_id = ids.first().id
    c_id = max_id + 1

    db.execute(f'''
        INSERT INTO "Book" (id, name, author, image)
        VALUES ({c_id}, '{book}', '{author}', '{url}');''')
    
    db.commit()

    return "форма получена"


@app.route("/db/book/<id>/")
def db_book(id):
    obj = db.execute(f'SELECT * FROM "Book" WHERE id = {id};').first()
    return render_template("database_book.html", obj=obj)
    

@app.route("/<int:id>", methods=['GET', 'POST'])
def db_book_update(id):
    message = ''
    name = request.form.get('tale')
    author = request.form.get('author')
    image =request.form.get('image')
    if request.method == 'POST':
        db.execute(f'''
        UPDATE "Book" 
        SET 
            name='{name}',
            author='{author}',
            image='{image}'
        WHERE id={id};
        ''')
        db.commit()
        message = 'Измения сохранены и находятся на стадии обработки'

    book_obj = db.execute(f'SELECT * FROM "Book" WHERE id = {id};').first()
    return render_template("db_book_update.html", book_obj=book_obj, message=message)

@app.route('/about_us/')
def about_us():
    return render_template('about_us.html')