from flask import reder_template
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from .. import db
from ..models import User

@auth.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name='cyyy').first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(url_for('blog.index'))
        flask('Invalid username or password.')
    return render_template('auth/login.html',form=form)


@auth.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('blog.index'))

@auth.register('/register')
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name='cyyy').first()
        if user is None:
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('blog.index'))
        flash('exist user')

    return render_template('auth/register.html',form=form)


