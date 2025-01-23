# app/app.py
from flask import render_template, request, redirect, url_for
from app import app
import sqlite3

# Database connection function
def get_db_connection():
    conn = sqlite3.connect('database/inventory.db')
    conn.row_factory = sqlite3.Row
    return conn

# Route to display all products
@app.route('/')
def index():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    return render_template('index.html', products=products)

# Route to add a new product
@app.route('/add', methods=('GET', 'POST'))
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        price = request.form['price']
        conn = get_db_connection()
        conn.execute('INSERT INTO products (name, quantity, price) VALUES (?, ?, ?)', 
                     (name, quantity, price))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add_product.html')

# Route to update product details
@app.route('/update/<int:id>', methods=('GET', 'POST'))
def update_product(id):
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM products WHERE id = ?', (id,)).fetchone()
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        price = request.form['price']
        conn.execute('UPDATE products SET name = ?, quantity = ?, price = ? WHERE id = ?',
                     (name, quantity, price, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    conn.close()
    return render_template('update_product.html', product=product)

# Route to delete a product
@app.route('/delete/<int:id>')
def delete_product(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM products WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

