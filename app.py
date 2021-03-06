from flask import Flask, render_template, request
from openpyxl import load_workbook
from sqlalchemy.orm import sessionmaker
from database import engine

app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template ('index.html')

@app.route('/books/')
def books():
    # session = sessionmaker(engine)()
    # books = session.query('Book')
    # print(books)
    # session.commit()
    # return render_template('books_table.html', objects_list=books)

    excel = load_workbook('tales.xlsx')
    page = excel['Лист1']

    tales = [tale.value for tale in page['A']][1:]


    authors = [author.value for author in page['B']][1:]

    html = '''
           <a href='/books'>Книги</a>
           <a href='/authors/'>авторы </a>
           <h1> Тут будет список книг <h1>
           '''

    for i in range(len(tales)):
        html += f'<h2>{tales[i]} - {authors[i]}<h2>' 
    
    return html



@app.route('/authors/')
def authors():
    excel = load_workbook('tales.xlsx')
    page = excel['Лист1']
    authors = {author.value for author in page['B'][1:]}
    return render_template("authors.html" authors=list(authors))

@app.route('/add/', methods = ['POST'])
def add:()
    f = request.forms
    excel = load_workbook ('tales.xlsx')
    
    page = excel ['Лист1']
    l_book = len(page['A']) + 1
    excel = [f'A'{'l_book'}] = f['author']
    excel = [f'B'{'l_book'}] = f['book']
    l_author = 
    return 'форма получена'