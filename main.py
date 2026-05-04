from flask import Flask, request, render_template_string, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

DATABASE = "demo.db"


def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db


def init_db():
    db = get_db()
    db.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL
        );
    """)
    db.commit()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        phone = request.form.get("phone")

        if name and phone:
            db = get_db()
            db.execute(
                "INSERT INTO contacts (name, phone) VALUES (?, ?)",
                (name, phone)
            )
            db.commit()

        return redirect(url_for("index"))

    db = get_db()
    contacts = db.execute("SELECT * FROM contacts").fetchall()

    return render_template_string("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Lab 5-1 DevOps App</title>
        </head>
        <body>
            <h1>Lab 5-1 DevOps App</h1>
            <h5>Pipeline Works!</h5>

            <form method="POST" action="/">
                <label>Name:</label><br>
                <input type="text" name="name" required><br>

                <label>Phone:</label><br>
                <input type="text" name="phone" required><br><br>

                <input type="submit" value="Submit">
            </form>

            {% if contacts %}
                <table border="1">
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Phone</th>
                    </tr>
                    {% for contact in contacts %}
                    <tr>
                        <td>{{ contact["id"] }}</td>
                        <td>{{ contact["name"] }}</td>
                        <td>{{ contact["phone"] }}</td>
                    </tr>
                    {% endfor %}
                </table>
            {% else %}
                <p>No contacts found.</p>
            {% endif %}
        </body>
        </html>
    """, contacts=contacts)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    init_db()
    app.run(debug=True, host="0.0.0.0", port=port)
