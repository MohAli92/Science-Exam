from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'  # SQLite database file
db = SQLAlchemy(app)

# Define the Book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publication_year = db.Column(db.Integer)

# Create the database and tables
def add_context():
    with app.app_context():
        db.create_all()

# Initialize the database
add_context()

# Routes
@app.route('/books')
def books():
    # Fetch all books from the database
    all_books = Book.query.all()
    return render_template('books.html', books=all_books)

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        # Get book details from the form
        title = request.form['title']
        author = request.form['author']
        publication_year = request.form['publication_year']

        # Create a new Book instance
        new_book = Book(title=title, author=author, publication_year=publication_year)

        # Add the new book to the database
        db.session.add(new_book)
        db.session.commit()

        return redirect(url_for('books'))  # Redirect to the /books route after adding a book

    return render_template('add_book.html')

if __name__ == '__main__':
    app.run(debug=True)
