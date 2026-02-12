from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField
from wtforms.fields.simple import StringField
from wtforms.validators import InputRequired, NumberRange, Length


class RectangleForm(FlaskForm):
    length = FloatField('Length', validators=[InputRequired(), NumberRange(min=0)])
    width = FloatField('Width', validators=[InputRequired(), NumberRange(min=0)])
    area = SubmitField('Calculate Area')
    perimeter = SubmitField('Calculate Perimeter')

class WeatherReport(FlaskForm):
    city = StringField('City', validators=[InputRequired(), Length(min=2, max=100)])
    submit = SubmitField('Get Weather Report')
