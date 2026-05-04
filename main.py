from flask import Flask, request, redirect, url_for, render_template_string
import sqlite3
import os

app = Flask(__name__)

DATABASE = 'demo.db'

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    db = get_db()
    db.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL
        )
    ''')
    db.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')

        if name and phone:
            db = get_db()
            db.execute('INSERT INTO contacts (name, phone) VALUES (?, ?)', (name, phone))
            db.commit()

        return redirect(url_for('index'))

    db = get_db()
    contacts = db.execute('SELECT * FROM contacts').fetchall()

    return render_template_string("""
        <h1>Flask DevOps App</h1>
        <h5>Pipeline Works!</h5>

        <form method="POST">
            Name: <input name="name"><br>
            Phone: <input name="phone"><br>
            <input type="submit">
        </form>

        <ul>
        {% for c in contacts %}
            <li>{{ c['name'] }} - {{ c['phone'] }}</li>
        {% endfor %}
        </ul>
    """, contacts=contacts)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
