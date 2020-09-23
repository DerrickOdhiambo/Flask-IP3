from flask import Blueprint, render_template
from app.models import Post

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
  posts = Post.query.order_by(Post.date_posted.desc()).all()
  return render_template('index.html', posts = posts)

@main.route('/category/<category>')
def post_by_category(category):
  posts = Post.query.filter_by(category=category).order_by(Post.date_posted.desc()).all()
  return render_template('post_by_category.html', posts = posts)
