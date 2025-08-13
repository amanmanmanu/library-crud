from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Define Book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Book {self.title}>"

# Create tables
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def index():  # renamed from home to index
    books = Book.query.all()
    return render_template('index.html', books=books)

@app.route('/add', methods=['POST'])
def add_book():
    title = request.form['title']
    author = request.form['author']
    year = request.form['year']

    new_book = Book(title=title, author=author, year=int(year))
    db.session.add(new_book)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_book(id):
    book = Book.query.get_or_404(id)
    if request.method == 'POST':
        book.title = request.form['title']
        book.author = request.form['author']
        book.year = int(request.form['year'])
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('update.html', book=book)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
