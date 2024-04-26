from flask import Flask, request, jsonify
import json
import sqlite3
#Flask will allow us to create our application and handle requests. #request will allow us to add methods to routes #jsonify will encode python dictionaries into json strings
app =Flask(__name__)

def db_connection():
    conn=None
    try:
        conn= sqlite3.connect('books.sqlite')
    except sqlite3.error as e:
        print(e)
    return conn
 
@app.route('/books', methods=['GET','POST'])
#code to fetch the details of all the books.
def books():
    conn = db_connection()
    cursor =conn.cursor()
    if request.method == 'GET':
        cursor =conn.execute("SELECT * FROM book")
        books=[
            dict(id=row[0], author =row[1], language= row[2], title= row[3])
            for row in cursor.fetchall()
        ]
        if books is not None:
            return jsonify(books)

# code to add the book in the database
    if request.method == 'POST':
       new_author = request.form['author']
       new_lang = request.form['language']
       new_title= request.form['title']
       #insert query for adding the book in database
       sql= """INSERT INTO book (author,language, title) VALUEs (?,?,?)"""
       #here ? are the placeholder to pass values dynamically
       # they are also known as the parameterized query
       cursor=conn.execute(sql,(new_author,new_lang, new_title))
       conn.commit()
       return  f"Book with the id:{cursor.lastrowid} created successfully."
    
@app.route('/book/<int:id>', methods=['GET','PUT',"DELETE"])
#http://localhost:5000/book/ id_book
#operations for the single book i.e fetch only one book  
def single_book(id):
    conn =db_connection()
    cursor =conn.cursor()
    book=None
    #code to fetch only one book  from the database using its id
    if request.method == 'GET':
        cursor.execute("SELECT * FROM book where id=?",(id,))
        rows=cursor.fetchall()
        for r in rows:
            book=r
        if book is not None:
            return jsonify(book),200
        else:
            return f"Something wrong! The book with id {id} does not exist/added in the database.",404
        
    # to update the data of book
    if request.method == 'PUT':
        sql="""UPDATE book
        SET title = ?,
        author = ?,
        language = ?
        WHERE id = ?"""
        author = request.form['author']
        language = request.form['language']
        title= request.form['title']
        updated_book = {
            'id': id,
            'author':author,
            'language':language,
            'title':title
            }
        conn.execute(sql, (author,language,title,id))
        conn.commit()
        return jsonify(updated_book)
    
    #code to delete the book
    if request.method == 'DELETE':
        sql="""DELETE FROM book WHERE id=?"""
        conn.execute(sql, (id,))
        conn.commit()
        return "The book with id: {} has been deleted.".format(id),200

if __name__ == '__main__':
    app.run(debug=True)
