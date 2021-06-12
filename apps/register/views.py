from . import register
from flask import render_template, redirect, url_for
from apps import db
from apps.forms import RegisterForm
from apps.models import User
from werkzeug.security import generate_password_hash


@register.route('/register', methods=['GET', 'POST'])
def register():
    """Função que renderiza a tela de registro de um usuário."""
    form = RegisterForm()
    if form.validate_on_submit():
        newuser = User(
            name=form.name.data,
            email=form.email.data,
            password=generate_password_hash(form.password.data, method='pbkdf2:sha256', salt_length=8))
        db.session.add(newuser)
        db.session.commit()
        return redirect(url_for("home.index"))
    return render_template("register.html", form=form)
