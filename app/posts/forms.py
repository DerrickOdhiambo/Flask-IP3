from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
    category = SelectField(u'Categories', choices=[('Career', 'Career'), ('PickUp_Lines', 'PickUp_Lines'), ('Slogans', 'Slogans'), ('Product', 'Product')])
    content = TextAreaField('Pitch', validators=[DataRequired()])
    submit = SubmitField('Post')


class CommentForm(FlaskForm):
    text = TextAreaField('Comment')
    submit = SubmitField('Post')


