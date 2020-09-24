from flask import Blueprint, render_template,url_for,flash, redirect, request, abort
from flask_login import current_user, login_required
from app import db
from app.models import Post, Comments
from app.posts.forms import PostForm, CommentForm

posts = Blueprint('posts', __name__)


@posts.route('/post/new', methods={'GET','POST'})
@login_required
def new_post():
  form = PostForm()
  if form.validate_on_submit():
    post = Post(category = form.category.data, content = form.content.data, author = current_user)
    db.session.add(post)
    db.session.commit()
    flash('Your pitch has been created!', 'success')
    return redirect(url_for('main.home'))
  return render_template('new_post.html', title = 'New Pitch', form = form, legend='New Pitch')


@posts.route('/post/<int:post_id>')
def post(post_id):
  post = Post.query.get(post_id)
  return render_template('post.html', title = post.category, post = post)


@posts.route('/post/<int:post_id>/update', methods=['GET','POST'])
@login_required
def update_post(post_id):
  post = Post.query.get(post_id)
  if post.author != current_user:
    abort(403)
  form = PostForm()
  if form.validate_on_submit():
    post.category = form.category.data
    post.content = form.content.data
    db.session.commit()
    flash('Your pitch has been updated!', 'success')
    return redirect(url_for('posts.post', post_id=post.id))
  elif request.method == 'GET':
    form.category.data = post.category
    form.content.data = post.content
  return render_template('new_post.html', title='Update Pitch', form=form, legend='Update Pitch')


@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
  post = Post.query.get(post_id)
  if post.author != current_user:
    abort(403)
  db.session.delete(post)
  db.session.commit()
  flash('Your post has been deleted!', 'success')
  return redirect(url_for('main.home'))


@posts.route('/post/<int:post_id>/comment', methods=['GET','POST'])
@login_required
def comment_post(post_id):
  post = Post.query.get(post_id)
  form = CommentForm()
  comments = Comments(text=form.text.data)
  if request.method == 'POST':
    db.session.add(post)
    db.session.commit()
    flash('Your comment has been posted!', 'success')
    return redirect(url_for('posts.post', post_id=post.id))
  return render_template('comment.html', title='Comments', post=post, form=form, comments=comments)
