from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'the string hard to guess'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
Bootstrap(app)
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)


db.create_all()


@app.route('/', methods=['GET', 'POST'])
def home():
    # edit rating
    if request.method == 'POST': # if it's POST, we need parameter 'id'
        book_id = request.args.get('id')
        new_rating = request.form['new_rating']
        edited_book = Book.query.filter_by(id=book_id).first()
        edited_book.rating = new_rating
        db.session.commit()
    # if it's GET, we don't need parameters
    all_books = Book.query.all()
    return render_template('index.html', library=all_books)


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        book = Book(title=request.form['title'],
                    author=request.form['author'],
                    rating=request.form['rating'])
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html')


@app.route("/edit/<id>")
def edit(id):
    book_to_edit = Book.query.filter_by(id=id).first()
    return render_template('edit.html', book=book_to_edit)


@app.route("/delete/<id>")
def delete(id):
    book_to_delete = Book.query.filter_by(id=id).first()
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)

