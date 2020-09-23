import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message   
from app import mail


def save_pic(form_picture):
  """
  function that saves the picture uploaded, gives it a rondom hex number and also resizes it
  """
  random_hex = secrets.token_hex(8)
  _, f_ext = os.path.splitext(form_picture.filename)
  picture_fn = random_hex + f_ext
  pic_path = os.path.join(current_app.root_path, 'static/images', picture_fn)

  output_size = (150, 150)
  form_picture.save(pic_path)
  i = Image.open(form_picture)
  i.thumbnail(output_size)
  i.save(pic_path)

  return picture_fn


def send_reset_email(user):
  """
  Funtion to send user an email for resetting password
  """
  token = user.get_reset_token()
  msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
  msg.body = f"""To reset your password follow the following link:
{url_for('users.reset_token', token=token, _external=True)}
If you didn't send this request please ignore the message."""
  mail.send(msg)