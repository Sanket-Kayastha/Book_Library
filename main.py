from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

all_books = []

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///book_library.db"

db.init_app(app)

class Book(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=False, nullable=False)
    author: Mapped[str] = mapped_column(nullable=False)
    rating: Mapped[str] = mapped_column(nullable=False)

with app.app_context():
    db.create_all()

@app.route('/', methods=['POST','GET'])
def home():
    result = db.session.query(Book).order_by(Book.id).all()
    return render_template("index.html", book=result)


@app.route("/add", methods=['POST','GET'])
def add():

    if request.method == "POST":
        books = Book(
        title = request.form.get('name'),
        author = request.form.get("author"),
        rating = request.form.get("rating")
        )
        db.session.add(books)
        db.session.commit()
        all_books.append(books)
        return redirect(url_for('home'))

    return render_template("add.html")

@app.route("/rating", methods=["POST","GET"])
def rating():
    book_id = request.args.get('id')
    result = db.get_or_404(Book, book_id)

    if request.method == "POST":
        new_rating = request.form.get('edit_rate')
        result.rating = new_rating
        db.session.commit()

        return redirect(url_for('home'))
    
    return render_template("rating.html", book=result)

@app.route("/delete", methods=["POST", "GET"])
def delete():
    book_id = request.args.get('id')
    result = db.get_or_404(Book, book_id)

    if request.method == "POST":
        db.session.delete(result)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template("delete.html" , book = result)



if __name__ == "__main__":
    app.run(debug=True)
