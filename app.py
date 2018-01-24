"""contains backend logic for the web app"""
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# set up database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/blog'

db = SQLAlchemy(app)


class Blogpost(db.Model):
    """Creates model for blogposts in the database"""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    subtitle = db.Column(db.String(100))
    author = db.Column(db.String(50))
    date_posted = db.Column(db.DateTime)
    content = db.Column(db.Text)

@app.route('/')
def index():
    """displays the home page and shows our blog posts"""
    # queries the db for all blog posts and displays the most recent first
    posts = Blogpost.query.order_by(Blogpost.date_posted.desc()).all()

    return render_template('index.html', posts=posts)

@app.route('/about')
def about():
    """renders the about page"""
    return render_template('about.html')

@app.route('/post/<int:post_id>')
def post(post_id):
    """displays a particular post based on its id"""
    post = Blogpost.query.filter_by(id=post_id).one()

    return render_template('post.html', post=post)

@app.route('/add')
def add():
    """renders the page that allows you to add posts"""
    return render_template('add.html')

@app.route('/addpost', methods=['POST'])
def addpost():
    """adds the blog post to the database"""
    title = request.form['title']
    subtitle = request.form['subtitle']
    author = request.form['author']
    content = request.form['content']

    new_post = Blogpost(title=title, subtitle=subtitle, author=author, content=content,
                        date_posted=datetime.now())

    db.session.add(new_post)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/delpost/<int:post_id>')
def delpost(post_id):
    """deletes the blog post in the database"""
    delete_post = Blogpost.query.get(post_id)

    db.session.delete(delete_post)
    db.session.commit()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
