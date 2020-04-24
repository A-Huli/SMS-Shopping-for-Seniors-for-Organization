from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FloatField, SubmitField
from wtforms.validators import DataRequired, Length


class AddMessagesForm(FlaskForm):
    content = StringField('Wiadomosc', validators=[Length(max=500)])
    contact_number = StringField('Numer telefonu', validators=[Length(max=12)])
    location = StringField('Lokalizacja', validators=[Length(max=100)])
    status = SelectField('Status wiadomosci', choices=[('Taken'),('Waiting for approval'),('Approved')])
    submit = SubmitField('Dodaj')


class EditMessagesForm(FlaskForm):
    content = StringField('Wiadomosc', validators=[Length(max=500)])
    contact_number = StringField('Numer telefonu', validators=[Length(max=12)])
    location = StringField('Lokalizacja', validators=[Length(max=100)])
    longtitude = FloatField('Dlugosc geograficzna')
    latitude = FloatField('Szerokosc geograficzna')
    status = SelectField('Status wiadomosci', choices=[('Taken'),('Waiting for approval'),('Approved')])
    submit = SubmitField('Zapisz')