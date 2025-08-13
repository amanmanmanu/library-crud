from flask import Flask, render_template, request, redirect, url_for
import db

app = Flask(__name__)

@app.route("/")
def index():
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    conn.close()
    return render_template("book.html", books=books)

@app.route("/add", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        year = request.form["year"]

        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO books (title, author, year) VALUES (?, ?, ?)", (title, author, year))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    return render_template("addbook.html")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_book(id):
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE id = ?", (id,))
    book = cursor.fetchone()

    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        year = request.form["year"]
        cursor.execute("UPDATE books SET title=?, author=?, year=? WHERE id=?", (title, author, year, id))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))

    conn.close()
    return render_template("editbook.html", book=book)

@app.route("/delete/<int:id>")
def delete_book(id):
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
