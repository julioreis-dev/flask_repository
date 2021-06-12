from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField
from wtforms.validators import DataRequired, Email, Length

coins = ['Bitcoin', 'Chainlink', 'XRP', 'Litecoin', 'WiBX', 'Chiliz', 'Ethereum', 'Dogecoin', 'Cardano']
timer = [5, 10, 15, 20, 25, 30]


class RegisterForm(FlaskForm):
    """
    Classe que cria o formulário de registro de usuários
    """
    name = StringField('Nome do usuário', validators=[DataRequired()])
    email = StringField(label='Email', validators=[DataRequired(), Email(message='This field requires a valid email '
                                                                                 'address')])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=8, message='The password must '
                                                                                                 'contain at least 8'
                                                                                                 ' character')])
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    """
    Classe que cria o formulário de login de usuário
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired(),
                                         Length(min=8, message='Your password have at least 8 character')])
    submit = SubmitField("Submit Login")


class CreatePostForm(FlaskForm):
    """
    Classe que cria o formulário de registro dos critérios de compra e venda dos ativos configurados pelos
    usuários
    """
    data_coin = SelectField("Escolha a sua criptomoeda", choices=coins, validators=[DataRequired()])
    data_sell = StringField("Valor de venda", validators=[DataRequired()], default=0.0)
    data_buy = StringField("Valor de compra", validators=[DataRequired()], default=0.0)
    data_timer = SelectField("Timer de alerta", choices=timer, validators=[DataRequired()])
    submit = SubmitField("Submit")


class EditPostForm(FlaskForm):
    """
    Classe que cria o formulário de edição dos critérios de compra e venda de ativos
    """
    data_sell = StringField("Valor de venda", validators=[DataRequired()])
    data_buy = StringField("Valor de compra", validators=[DataRequired()])
    data_timer = SelectField("Timer de alerta", choices=timer, validators=[DataRequired()])
    submit = SubmitField("Submit")
