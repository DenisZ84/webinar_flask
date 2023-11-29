from . import app, db
from flask import render_template, url_for, redirect
from .models import User, Price
from .forms import MailForm


@app.route("/mail-list")
def mail_list():
    users = User.query.all()
    return render_template('users.html', **{'users': users})


@app.route("/add-mail-list", methods=['GET', 'POST'])
def add_mail_list():
    form = MailForm()
    if form.validate_on_submit():
        user = User(email=form.email.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('mail_list'))
    return render_template('add_users.html', form=form)


@app.route("/")
def index():
    fuel_prices = Price.query.all()
    return render_template('index.html', **{'fuel_prices': fuel_prices})