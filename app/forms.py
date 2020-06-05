from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.fields.html5 import TimeField
from wtforms.validators import DataRequired, Optional

subjects = [
    ('Bazy Danych', 'Bazy Danych'),
    ('Języki i Paradygmaty Programowania', 'Języki i Paradygmaty Programowania'),
    ('Podstawy Automatyki i Robotyki', 'Podstawy Automatyki i Robotyki'),
    ('Podstawy Techniki Mikroprocesorowej', 'Podstawy Techniki Mikroprocesorowej'),
    ('Problemy Społeczne i Zawodowe Informatyki', 'Problemy Społeczne i Zawodowe Informatyki'),
    ('Programowanie Współbieżne', 'Programowanie Współbieżne'),
    ('Systemy Operacyjne', 'Systemy Operacyjne'),
    ('Technologie Sieciowe', 'Technologie Sieciowe')]
types = [
    ('Egzamin', 'Egzamin'),
    ('Kolokwium', 'Kolokwium'),
    ('Sprawozdanie', 'Sprawozdanie'),
    ('Zadania', 'Zadania'),
    ('Inne', 'Inne')]

class SubjectForm(FlaskForm):
    subject = SelectField('Przedmiot', choices=subjects, validators=[DataRequired()])
    type = SelectField('Rodzaj zaliczenia', choices=types, validators=[DataRequired()])
    date = DateField('Data', format='%Y-%m-%d', validators=[DataRequired()])
    time = TimeField('Godzina', validators=[Optional()])
    other = StringField('Inne informacje')
    submit = SubmitField('Dodaj')