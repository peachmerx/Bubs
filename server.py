import os

DB_URL = os.environ.get('DATABASE_URL', 'dbname=bubs')

import psycopg2
from flask import Flask, render_template, request, redirect, session
from models.db import sql_select
import bcrypt

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY")

@app.route('/')
def index():

    return render_template('home.html')

@app.route('/toys')
def toys():
    results = sql_select('SELECT * FROM toys')

    product_items = []
    for row in results:
        id, brand, name, image_url, price = row
        price = f'${price/100:.2f}'
        product_items.append([id, brand, name, image_url, price])

    return render_template('toys.html', product_items=product_items)

# @app.route('/clothes')
# def clothes():
#     results = sql_select('SELECT id, brand, name, image_url, price FROM clothes')

#     product_items = []
#     for row in results:
#         id, brand, name, image_url, price = row
#         price = f'${price/100:.2f}'
#         product_items.append([id, brand, name, image_url, price])

#     return render_template('clothes.html', product_items=product_items)

# @app.route('/books')
# def books():
#     results = sql_select('SELECT id, name, image_url, price FROM books')

#     product_items = []
#     for row in results:
#         id, name, image_url, price = row
#         price = f'${price/100:.2f}'
#         product_items.append([id, name, image_url, price])

#     return render_template('books.html', product_items=product_items)


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
            return redirect('/')
    else:
        return redirect('/login')

@app.route('/add')
def create():
    return render_template('add.html')


@app.route('/add_action', methods=["POST"])
def create_action():
    # First, get user input
    brand = request.form.get('brand')
    name = request.form.get('name')
    price = int(request.form.get('price'))
    image_url = request.form.get('image_url')

    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute("INSERT INTO toys (brand, name, price, image_url) VALUES (%s, %s, %s, %s)",
                [brand, name, price, image_url])
    conn.commit()
    conn.close()

    return redirect('/toys')

@app.route('/edit/<id>')
def edit(id):

    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()

    cur.execute('SELECT id, brand, name, price,image_url FROM toys WHERE id=%s', [id])
    id, brand, name, price, image_url = cur.fetchone()
    print(id)

    cur.close()
    conn.close()

    return render_template('edit.html', id=id, brand=brand, name=name, price=price, image_url=image_url)

@app.route('/edit_action', methods=['POST'])
def edit_action():
    id = request.form.get('id')
    brand = request.form.get('brand')
    name = request.form.get('name')
    price = request.form.get('price')
    image_url = request.form.get('image_url')

    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    print(brand, name, price, image_url,id)
    cur.execute('UPDATE toys SET brand=%s, name=%s, price=%s, image_url=%s WHERE id=%s', [brand, name, price, image_url, id])
    conn.commit()

    cur.close()
    conn.close()

    return redirect('/toys')

@app.route('/delete/<item_id>')
def delete(item_id):

    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()

    cur.execute('SELECT id, name, price,image_url FROM toys WHERE id=%s', [item_id])
    id, name, price, image_url = cur.fetchone()

    cur.close()
    conn.close()

    return render_template('delete.html', item_id=item_id, id=id, name=name, price=price, image_url=image_url)

@app.route('/delete_action', methods=['POST', 'GET'])
def delete_action(item_id):

    item_id = request.form.get('item_id')

    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()

    cur.execute('Delete from toys where id = %s', [item_id])
    conn.commit()

    cur.close()
    conn.close()

    return redirect('/toys')


if __name__ == '__main__':
    app.run(debug=True)