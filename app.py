from datetime import datetime
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DB.db'
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(200), nullable=False)
    year = db.Column(db.Integer, nullable=True)
    description = db.Column(db.String(), nullable=True)
    price = db.Column(db.Float, nullable=True)
    rating = db.Column(db.Integer, nullable=True)
    is_read = db.Column(db.Boolean, nullable=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'{self.title} by {self.author}'

    def read(self):
        self.is_read = True
        # db.session.commit()
        # return redirect(url_for('index'))


@app.route('/')
def index():
    render_template('index.html')


@app.route('/search/', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_by = request.form['search_by']
        search_in = request.form['search_in']
        value = request.form['search']

        if search_by == 'title':
            if search_in == 'google':
                pass
            elif search_in == 'tzomet':
                pass
            else:
                pass
        else:  # search_by == 'author'
            if search_in == 'google':
                pass
            elif search_in == 'tzomet':
                pass
            else:
                pass


if __name__ == '__main__':
    app.run()
