import psycopg2
from flask import Flask, render_template, request, redirect
from models.db import sql_select

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

@app.route('/clothes')
def clothes():
    results = sql_select('SELECT id, name, image_url, price FROM clothes')

    product_items = []
    for row in results:
        id, name, image_url, price = row
        price = f'${price/100:.2f}'
        product_items.append([id, name, image_url, price])

    return render_template('clothes.html', product_items=product_items)

@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login_action', methods=['POST'])
def login_action():

    user_email = request.form.get('email')
    conn = psycopg2.connect('dbname = food_truck')
    cur = conn.cursor()
    cur.execute('SELECT id, email FROM users WHERE email = %s', [user_email])

    user_record = cur.fetchone()
    print(user_record)

    cur.close()
    conn.close()

    if user_record:
        user_id, sql_result_email = user_record
        print(sql_result_email)
        print("found the user")
        print(user_id)
        return redirect('/')
    else:
        print("user not found")
        return redirect('/')

app.run(debug=True)