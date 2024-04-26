import sqlite3
# create the connection to sqlite ,provide the path and if the path does not exist than a new one is created.
conn = sqlite3.connect('books.sqlite')
#create database tables: you need to have the idea of how your sturcturing the data .
#book object has four attribute:
# 1. id  2. author  3. language  4. title

cursor= conn.cursor()

sql_query= """ CREATE TABLE book( 
    id integer PRIMARY KEY,
    author text NOT NULL,
    language text NOT NULL,
    title text NOT NULL)"""
cursor.execute(sql_query)