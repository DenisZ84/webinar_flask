from flask_wtf import FlaskForm
from wtforms import EmailField, SubmitField
from wtforms.validators import DataRequired, Length, Email


class MailForm(FlaskForm):
    email = EmailField('Введите валидный email', 
                       validators=[DataRequired(message='Обязательное поле'),
                                   Email(),
                                   Length(1, 128)])
    submit = SubmitField('Добавить')