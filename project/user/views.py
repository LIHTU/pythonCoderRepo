# project/user/views.py


#################
#### imports ####
#################

import datetime

from flask import render_template, Blueprint, url_for, \
    redirect, flash, request, jsonify, send_from_directory, make_response
from flask.ext.login import login_user, logout_user, \
    login_required, current_user

from project.models import User, Assert, Submission
from project.email import send_email
from project.token import generate_confirmation_token, confirm_token
from project.decorators import check_confirmed
from project import db, bcrypt
from .forms import LoginForm, RegisterForm, ChangePasswordForm

from RestrictedPython import compile_restricted
from RestrictedPython.Guards import safe_builtins
from twilio.rest import TwilioRestClient
import csv
import traceback
import json
import sys
safe_builtins['type'] = type
safe_builtins['list'] = list

client = TwilioRestClient('AC0abd43e102a79cddd31560b28f042c6e', '5c6c35713fdbb13f1c0f1ebfe2090a70')



data = {}
with open('data_sets/test1.csv') as f:
    data['test1'] = [{k: v for k, v in row.items()} for row in csv.DictReader(f, skipinitialspace=True)]
with open('data_sets/test2.csv') as f:
    data['test2'] = [{k: v for k, v in row.items()} for row in csv.DictReader(f, skipinitialspace=True)]
with open('data_sets/test3.csv') as f:
    data['test3'] = [{k: v for k, v in row.items()} for row in csv.DictReader(f, skipinitialspace=True)]
with open('data_sets/test4.csv') as f:
    data['test4'] = [{k: v for k, v in row.items()} for row in csv.DictReader(f, skipinitialspace=True)]


################
#### config ####
################

user_blueprint = Blueprint('user', __name__,)


################
#### routes ####
################

@user_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        user = User(
            email=(form.email.data).lower(),
            password=form.password.data,
            confirmed=False
        )
        db.session.add(user)
        db.session.commit()

        token = generate_confirmation_token(user.email)
        confirm_url = url_for('user.confirm_email', token=token, _external=True)
        html = render_template('user/activate.html', confirm_url=confirm_url)
        subject = "Please confirm your email"
        send_email(user.email, subject, html)

        login_user(user)

        flash('A confirmation email has been sent via email.', 'success')
        return redirect(url_for("user.unconfirmed"))

    return render_template('user/register.html', form=form)


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=(form.email.data).lower()).first()
        if user and bcrypt.check_password_hash(
                user.password, request.form['password']):
            login_user(user)
            flash('Welcome.', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Invalid email and/or password.', 'danger')
            return render_template('user/login.html', form=form)
    return render_template('user/login.html', form=form)


@user_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You were logged out.', 'success')
    return redirect(url_for('user.login'))


@user_blueprint.route('/profile', methods=['GET', 'POST'])
@login_required
@check_confirmed
def profile():
    form = ChangePasswordForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=current_user.email).first()
        if user:
            user.password = bcrypt.generate_password_hash(form.password.data)
            db.session.commit()
            flash('Password successfully changed.', 'success')
            return redirect(url_for('user.profile'))
        else:
            flash('Password change was unsuccessful.', 'danger')
            return redirect(url_for('user.profile'))
    return render_template('user/profile.html', form=form)

@user_blueprint.route('/submit', methods=['GET', 'POST'])
@login_required
@check_confirmed
def submit():
    data_set = request.form['dataset']
    successes = {"vals":[]}


    submission = Submission(
        code=request.form['text'],
        data_set=data_set,
        user=current_user.email
    )
    db.session.add(submission)
    db.session.commit()

    try:
        code = compile_restricted(request.form['text'], '<string>', 'exec')
        restricted_globals = dict(__builtins__ = safe_builtins)
        exec(code) in restricted_globals
    except Exception as x:
        print("Error here")
        error = "Error when defining function:\n" + str(x)
        return jsonify({"vals":[]})
    _asserts = Assert.query.filter_by(data_set=int(data_set)).all()

    for item in _asserts:
        try:
            exec(str(item)) in restricted_globals
            successes["vals"].append(["1"])
        except AssertionError:
            successes["vals"].append(["0", "Assertion not satisfied"])
        except Exception as e:
            print(sys.exc_info()[2].tb_lineno)
            successes["vals"].append(["0", str(e)])
    return jsonify(successes)


@user_blueprint.route('/submitter', methods=['GET', 'POST'])
@login_required
@check_confirmed
def submitter():
    # removed lines here so we don't call Frankie
    return render_template('user/submitter.html')


@user_blueprint.route('/submissions.txt', methods=['GET'])
@login_required
@check_confirmed
def submissions():
    subs = Submission.query.filter_by(user=current_user.email).all()
    _subs = ""
    for sub in subs:
        _subs += "Submitted on " + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")) + "\n" +str(sub) + "\n"

    response = make_response(_subs)
    response.headers["Content-Disposition"] = "attachment; filename=submission.txt"
    return response

@user_blueprint.route('/history', methods=['GET'])
@login_required
@check_confirmed
def history():
    subs = Submission.query.filter_by(user=current_user.email).all()
    _subs = ""
    for sub in subs:
        _subs += "Submitted on " + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")) + "\n" +str(sub) + "\n"

    return _subs


@user_blueprint.route('/confirm/<token>')
@login_required
def confirm_email(token):
    if current_user.confirmed:
        flash('Account already confirmed. Please login.', 'success')
        return redirect(url_for('main.home'))
    email = confirm_token(token)
    user = User.query.filter_by(email=current_user.email).first_or_404()
    if user.email == email:
        user.confirmed = True
        user.confirmed_on = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    else:
        flash('The confirmation link is invalid or has expired.', 'danger')
    return redirect(url_for('main.home'))

@user_blueprint.route('/get_asserts/<data_set>', methods=['POST'])
@login_required
def get_asserts(data_set):
    _asserts = Assert.query.filter_by(data_set=int(data_set)).all()
    asserts = []
    for item in _asserts:
        asserts.append(str(item))
    return json.dumps(asserts)



@user_blueprint.route('/get_hint', methods=['POST'])
@login_required
@check_confirmed
def get_hint():
    data_set = request.form['dataset']
    text = request.form['text']
    hint = Assert.query.filter_by(data_set=data_set, code=text).first().get_hint()
    return hint



@user_blueprint.route('/unconfirmed')
@login_required
def unconfirmed():
    if current_user.confirmed:
        return redirect(url_for('main.home'))
    flash('Please confirm your account!', 'warning')
    return render_template('user/unconfirmed.html')


@user_blueprint.route('/resend')
@login_required
def resend_confirmation():
    token = generate_confirmation_token(current_user.email)
    confirm_url = url_for('user.confirm_email', token=token, _external=True)
    html = render_template('user/activate.html', confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_email(current_user.email, subject, html)
    flash('A new confirmation email has been sent.', 'success')
    return redirect(url_for('user.unconfirmed'))
