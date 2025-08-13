from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
# A simple secret for flash messages; in production set from env var
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(150), nullable=True)
    year = db.Column(db.Integer, nullable=True)
    isbn = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f"<Book {self.title}>"

# Home / list all books
@app.route("/")
def index():
    books = Book.query.order_by(Book.id.desc()).all()
    return render_template("index.html", books=books)

# Add new book (GET shows form, POST saves)
@app.route("/add", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        author = request.form.get("author", "").strip()
        year = request.form.get("year", "").strip()
        isbn = request.form.get("isbn", "").strip()

        if not title:
            flash("Title is required.", "warning")
            return redirect(url_for("add_book"))

        try:
            year_int = int(year) if year else None
        except ValueError:
            flash("Year must be a number.", "warning")
            return redirect(url_for("add_book"))

        book = Book(title=title, author=author or None, year=year_int, isbn=isbn or None)
        db.session.add(book)
        db.session.commit()
        flash("Book added successfully.", "success")
        return redirect(url_for("index"))

    return render_template("add.html")

# Edit existing book
@app.route("/edit/<int:book_id>", methods=["GET", "POST"])
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        author = request.form.get("author", "").strip()
        year = request.form.get("year", "").strip()
        isbn = request.form.get("isbn", "").strip()

        if not title:
            flash("Title is required.", "warning")
            return redirect(url_for("edit_book", book_id=book.id))

        try:
            year_int = int(year) if year else None
        except ValueError:
            flash("Year must be a number.", "warning")
            return redirect(url_for("edit_book", book_id=book.id))

        book.title = title
        book.author = author or None
        book.year = year_int
        book.isbn = isbn or None
        db.session.commit()
        flash("Book updated.", "success")
        return redirect(url_for("index"))

    return render_template("edit.html", book=book)

# Delete book
@app.route("/delete/<int:book_id>", methods=["POST"])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    flash("Book deleted.", "info")
    return redirect(url_for("index"))

# Quick create DB command
@app.cli.command("init-db")
def init_db():
    """Initialize the SQLite database."""
    db.create_all()
    print("Initialized the database.")

if __name__ == "__main__":
    # ensure DB exists locally when running directly
    db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)
