from . import coin
from flask import redirect, url_for, flash, render_template
from flask_login import login_required, current_user
from apps.forms import CreatePostForm, EditPostForm
from apps.models import CriptoTable
from apps import db


def repeat_field(user, coin):
    data = db.session.query(CriptoTable).filter(CriptoTable.user_id==user).filter(CriptoTable.coin==coin).first()
    return data

def all_register(number):
    data = db.session.query(CriptoTable).filter_by(user_id=number).all()
    return data



@coin.route("/cripto", methods=['GET', 'POST'])
@login_required
def register_cript():
    form = CreatePostForm()
    if form.validate_on_submit():
        result = repeat_field(current_user.id, form.data_coin.data)
        if result is None:
            new = CriptoTable(
                coin=form.data_coin.data,
                sell=form.data_sell.data,
                buy=form.data_buy.data,
                timer=form.data_timer.data,
                rt_coin=current_user)
            db.session.add(new)
            db.session.commit()
            return render_template('content.html', all_results=all_register(current_user.id))
        flash("Você já possui valores cadastrados para a referida criptomoeda.")
        return render_template("make-post.html", form=form)
    return render_template("make-post.html", form=form)

@coin.route("/about")
@login_required
def about():
    return render_template('content.html', all_results=all_register(current_user.id))


@coin.route("/api/<int:coin_id>", methods=['GET', 'POST'])
@login_required
def edit_content(coin_id):
    post=CriptoTable.query.get(coin_id)
    edit_form = EditPostForm(
        data_sell=post.sell,
        data_buy=post.buy,
        data_timer=post.timer
    )
    if edit_form.validate_on_submit():
        post.sell = edit_form.data_sell.data
        post.buy = edit_form.data_buy.data
        post.timer = edit_form.data_timer.data
        db.session.commit()
        return redirect(url_for("coin.about"))
    return render_template("post.html", post=edit_form)
