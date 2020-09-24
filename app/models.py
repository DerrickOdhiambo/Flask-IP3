from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from . import db
from app import login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique = True, nullable = False)
  email = db.Column(db.String(120), unique = True, nullable = False)
  image_file = db.Column(db.String(20),nullable = False, default = 'default.jpeg')
  password = db.Column(db.String(60), nullable = False)
  posts = db.relationship('Post', backref='author', lazy=True)
  comments = db.relationship('Comments', backref='user', lazy=True)

  def get_reset_token(self, expires_sec=2000):
    s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
    return s.dumps({'user_id':self.id}).decode('utf-8')

  @staticmethod
  def verify_reset_token(token):
    s = Serializer(current_app.confiPostg['SECRET_KEY'])
    try:
      user_id = s.loads(token)['user_id']
    except:
      return None
    return User.query.get(user_id)

  def __repr__(self):
    return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
  __tablename__ = 'posts'
  
  id = db.Column(db.Integer, primary_key=True)
  category = db.Column(db.String(100), nullable = False)
  date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
  content = db.Column(db.Text, nullable = False)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
  comments = db.relationship('Comments', backref='author', lazy=True)

  def __repr__(self):
    return f"User('{self.category}', '{self.date_posted}', '{self.content}')"


class Comments(db.Model):
  __tablename__ = 'comments'
  
  id = db.Column(db.Integer, primary_key=True)
  text = db.Column(db.String(140))
  timestamp = db.Column(db.DateTime(), default=datetime.utcnow, index=True)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  posts_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

  def save_comment(self):
      db.session.add(self)
      db.session.commit()

  def __repr__(self):
    return f"User({self.text}, {self.timestamp})"
