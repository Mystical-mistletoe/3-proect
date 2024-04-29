from flask_wtf import FlaskForm
from sqlalchemy import orm
from wtforms import StringField, TextAreaField, IntegerField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class NewsForm(FlaskForm):
    #is_private = BooleanField("Личное")
    #job = StringField('Название работы')
    team_lead = IntegerField('Участник')
    namep = StringField('ФИО персонажа')
    size = IntegerField('Возраст')
    boost = StringField('Силы/слабости')
    biograph = StringField('Биография, характер')
    is_finished = BooleanField('Живет в бункере?')
    submit = SubmitField('Применить')