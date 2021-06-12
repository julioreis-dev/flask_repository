from . import login
from apps.forms import LoginForm
from apps.models import User
from apps import db
from flask import render_template, redirect, url_for, flash
from werkzeug.security import check_password_hash
from flask_login import login_user, login_required, logout_user



@login.route('/logins', methods=['GET', 'POST'])
def logins():
    """Função que renderiza a tela de login."""
    form = LoginForm()
    if form.validate_on_submit():
        email_user = form.email.data
        password = form.password.data
        currentuser = db.session.query(User).filter_by(email=email_user).first()
        if not currentuser:
            flash("Prezado usuário esse email não existe, por favor tente novamente.")
            return redirect(url_for('logins.logins'))
        if not check_password_hash(currentuser.password, password):
            flash('Password incorreto, por favor tente novamente.')
            return redirect(url_for('logins.logins'))
        else:
            login_user(currentuser)
            return redirect(url_for("coin.register_cript"))
    return render_template("login.html", form=form)


@login.route('/logout')
@login_required
def logout():
    """Função que encerra a sessão de um usuário logado."""
    logout_user()
    flash('Sessão encerrada com sucesso!!!')
    return redirect(url_for('home.index'))
