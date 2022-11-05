import psycopg2
from flask import Flask, render_template
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

app.run(debug=True)