from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, IntegerField, SelectField, TelField, BooleanField, PasswordField
from wtforms.validators import InputRequired, Length, Email, DataRequired, Optional, Regexp, AnyOf
from flask import current_app
import os

class FormOcorrencia(FlaskForm):

    tipomanifestChoices = ['contaminacao', 'visita', 'denuncia']

    nome = StringField('', validators=[InputRequired()])
    email = EmailField('', validators=[InputRequired(), Email(message="Endereço de email inválido.")])
    tel = TelField('', validators=[DataRequired(),Length(min=6, max=40)])
    tipomanifest = StringField(name='select-tipo-manifest', validators=[AnyOf(tipomanifestChoices)])
    cep = StringField('CEP', validators=[InputRequired(),Regexp(r'^\d{8}$', message='CEP inválido. Deve conter apenas números.')])
    rua = StringField(name='rua', validators=[InputRequired()])
    numero = IntegerField(name='numero', validators=[InputRequired()])
    bairro = StringField(name='bairro', validators=[InputRequired()])
    valorvisita = StringField(name='valorvisita', validators=[Optional()])
    valorcontaminacao = StringField(name='valorcontaminacao', validators=[Optional()])


    def __init__(self, *args, **kwargs):
            super(FormOcorrencia, self).__init__(*args, **kwargs)
            if current_app.config['TESTING'] == True:
                self.tipomanifest.data = 'visita'


class FormLogin(FlaskForm):
    email = EmailField('', validators=[InputRequired(), Email(message="Endereço de email inválido.")])
    password = PasswordField(validators=[InputRequired(), Length(8, 72, message="A senha deve ter entre 8 e 72 caracteres.")])