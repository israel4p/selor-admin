from flask_wtf import FlaskForm
from models import Domain
from wtforms import (
    StringField, SelectField, PasswordField, IntegerField,
    validators, BooleanField)


class FormUser(FlaskForm):

    name = StringField(
        'Name',
        [validators.DataRequired(), validators.Length(min=5, max=50)],
        render_kw={"placeholder": "Full Name"}
    )
    username = StringField(
        'Username',
        [validators.DataRequired(), validators.Length(min=3, max=15)],
        render_kw={"placeholder": "Username"}
    )
    domain = SelectField(
        'Domain',
        [validators.DataRequired()]
    )
    quota = IntegerField(
        'Quota',
        [validators.DataRequired()],
        render_kw={"placeholder": 'Quota in Mb'}
    )
    password = PasswordField(
        'Password',
        [validators.DataRequired(), validators.Length(min=6, max=15)],
        render_kw={"placeholder": 'Password'}
    )

    def __init__(self, *args, **kwargs):
        super(FormUser, self).__init__(*args, **kwargs)
        self.domain.choices = [
                        (c.name, c.name) for c in Domain.query.all()]


class FormEditUser(FlaskForm):
    name = StringField(
        'Name',
        [validators.DataRequired(), validators.Length(min=5, max=50)],
        render_kw={"placeholder": "Full Name"}
    )
    quota = IntegerField(
        'Quota',
        [validators.DataRequired()],
        render_kw={"placeholder": 'Quota in Mb'}
    )
    password = PasswordField(
        'Password',
        [validators.Length(max=15)],
        render_kw={"placeholder": 'Password'}
    )


class FormDomain(FlaskForm):
    company = StringField(
        'Company Name',
        [validators.DataRequired(), validators.Length(min=5, max=50)],
        render_kw={"placeholder": 'Company name'}
    )
    domain = StringField(
        'Domain',
        [validators.DataRequired(), validators.Length(min=5, max=50)],
        render_kw={"placeholder": 'Domain'}
    )


class FormLogin(FlaskForm):
    username = StringField(
        'Username',
        [validators.DataRequired(), validators.Length(min=5, max=15)],
        render_kw={"placeholder": "Username"}
    )
    password = PasswordField(
        'Password',
        [validators.DataRequired(), validators.Length(min=6, max=15)],
        render_kw={'placeholder': 'Password'}
    )
    remember = BooleanField(
        'Lembrar'
    )


class FormAdmin(FlaskForm):
    atual = PasswordField(
        'Senha Atual',
        [validators.DataRequired(), validators.Length(min=5, max=15)],
        render_kw={'placeholder': 'Senha Atual'}
    )
    nova = PasswordField(
        'Nova Senha',
        [validators.DataRequired(), validators.Length(min=5, max=15)],
        render_kw={'placeholder': 'Nova Senha'}
    )
    repetir = PasswordField(
        'Repetir Senha',
        [validators.DataRequired(), validators.Length(min=5, max=15)],
        render_kw={'placeholder': 'Repetir Senha'}
    )
