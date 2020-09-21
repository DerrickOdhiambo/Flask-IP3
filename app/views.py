import os
import secrets
from PIL import Image
from flask import render_template, flash, redirect, url_for, request
from app import app, db, bcrypt
from app.form import RegistrationForm, LoginForm, AccountUpdateForm
from app.models import User,Post
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
def home():
  return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('home'))
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    if user and bcrypt.check_password_hash(user.password, form.password.data):
      login_user(user, remember=form.remember.data)
      next_page = request.args.get('next')
      return redirect(next_page) if next_page else redirect(url_for('home'))
    else:
      flash('Login unsuccessful. Check email or password!', 'danger')
  return render_template('login.html', title = 'Login', form = form )

@app.route('/register', methods = ['GET', 'POST'])
def register():
  if current_user.is_authenticated:
    return redirect(url_for('home'))
  form = RegistrationForm()
  if form.validate_on_submit():
    hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    user = User(username = form.username.data, email = form.email.data, password = hashed_password)
    db.session.add(user)
    db.session.commit()
    flash(f'Account for was created successfully! You can now log into your account!','success') 
    return redirect(url_for('login'))
  return render_template('register.html', title = 'Register', form = form)


@app.route('/logout')
def logout():
  logout_user()
  return redirect(url_for('home'))


def save_pic(form_picture):
  """
  function that saves the picture uploaded, gives it a rondom hex number and also resizes it
  """
  random_hex = secrets.token_hex(8)
  _, f_ext = os.path.splitext(form_picture.filename)
  picture_fn = random_hex + f_ext
  pic_path = os.path.join(app.root_path, 'static/images', picture_fn)

  output_size = (150, 150)
  form_picture.save(pic_path)
  i = Image.open(form_picture)
  i.thumbnail(output_size)
  i.save(pic_path)

  return picture_fn

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
  form = AccountUpdateForm()
  if form.validate_on_submit():
    if form.picture.data:
        picture_file = save_pic(form.picture.data)
        current_user.image_file = picture_file
    current_user.username = form.username.data
    current_user.email = form.email.data
    db.session.commit()
    flash('Your account has been updated!', 'success')
    return redirect(url_for('account'))
  elif request.method == 'GET':
    form.username.data = current_user.username
    form.email.data = current_user.email
  image_file = url_for('static', filename='images/' + current_user.image_file)
  return render_template('account.html', title = 'Account', image_file=image_file, form=form)