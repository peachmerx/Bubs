import os

DB_URL = os.environ.get('DATABASE_URL', 'dbname=bubs')

import psycopg2
from flask import Flask, render_template, request, redirect
from models.db import sql_select
import bcrypt

app = Flask(__name__)

@app.route('/')
def index():
    results = sql_select('SELECT id, name, image_url, price FROM toys')

    product_items = []
    for row in results:
        id, name, image_url, price = row
        price = f'${price/100:.2f}'
        product_items.append([id, name, image_url, price])

    return render_template('home.html', product_items=product_items)

@app.route('/toys')
def toys():
    results = sql_select('SELECT id, name, image_url, price FROM toys')

    product_items = []
    for row in results:
        id, name, image_url, price = row
        price = f'${price/100:.2f}'
        product_items.append([id, name, image_url, price])

    return render_template('toys.html', product_items=product_items)

@app.route('/clothes')
def clothes():
    results = sql_select('SELECT id, name, image_url, price FROM clothes')

    product_items = []
    for row in results:
        id, name, image_url, price = row
        price = f'${price/100:.2f}'
        product_items.append([id, name, image_url, price])

    return render_template('clothes.html', product_items=product_items)

@app.route('/books')
def books():
    results = sql_select('SELECT id, name, image_url, price FROM books')

    product_items = []
    for row in results:
        id, name, image_url, price = row
        price = f'${price/100:.2f}'
        product_items.append([id, name, image_url, price])

    return render_template('books.html', product_items=product_items)


#LOGIN/LOGOUT
@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login_action', methods=['POST'])
def login_action():

    user_email = request.form.get('email')
    password = request.form.get('password')
    
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute('SELECT id, email, password_hash FROM users WHERE email = %s', [user_email])
    user_record = cur.fetchone()

    cur.close()
    conn.close()

    print(user_record)

    if user_record:
        if bcrypt.checkpw(password.encode(), user_record[2].encode()):
            session['user_id'] = user_record[0]
            return redirect('/profile')
    else:
        return redirect('/login')

@app.route('/add')
def create():
    return render_template('add.html')


@app.route('/add_action', methods=["POST"])
def create_action():
    # First, get user input
    name = request.form.get('name')
    price = int(request.form.get('price'))
    image = request.form.get('image_url')

    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute("INSERT INTO toys (name, price, image) VALUES (%s, %s)",
                [name, price, image])
    conn.commit()
    conn.close()

    return redirect('/toys')

@app.route('/edit_item/<id>')
def edit_item(id):

    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()

    cur.execute('SELECT id, name, price,image_url FROM toys WHERE id=%s', [id])
    id, name, price, image_url = cur.fetchone()
    print(id)

    cur.close()
    conn.close()

    return render_template('edit.html', id=id, name=name, price=price, image_url=image_url)

@app.route('/edit_action', methods=['POST'])
def edit_action():
    id = request.form.get('id')
    name = request.form.get('name')
    price = request.form.get('price')
    image_url = request.form.get('image_url')

    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    print(name, price, image_url,id)
    cur.execute('UPDATE toys SET name=%s, price=%s, image_url=%s WHERE id=%s', [name, price, image_url, id])
    conn.commit()

    cur.close()
    conn.close()

    return redirect('/toys')

@app.route('/delete/<id>', methods=['POST', 'GET'])
def delete(id):

    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()

    cur.execute('Delete from toys where id = %s', [id])
    conn.commit()

    cur.close()
    conn.close()

    return redirect('/toys')


if __name__ == '__main__':
    app.run(debug=True)