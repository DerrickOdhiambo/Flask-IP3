from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
    category = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Pitch', validators=[DataRequired()])
    submit = SubmitField('Post')


class CommentForm(FlaskForm):
    text = TextAreaField('Comment')
    submit = SubmitField('Post')