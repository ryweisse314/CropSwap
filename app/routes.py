# app/routes.py

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.forms import RegistrationForm, LoginForm, ListingForm
from app.models import User, Produce, Listing
from flask import Blueprint

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, zipcode=form.zipcode.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created! You can now log in.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        flash('Invalid email or password.', 'danger')
    return render_template('login.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/dashboard')
@login_required
def dashboard():
    have_listings = Listing.query.filter_by(user_id=current_user.id, type='have').all()
    want_listings = Listing.query.filter_by(user_id=current_user.id, type='want').all()
    return render_template('dashboard.html', have_listings=have_listings, want_listings=want_listings)

@bp.route('/add_listing', methods=['GET', 'POST'])
@login_required
def add_listing():
    form = ListingForm()
    form.produce.choices = [(p.id, p.name) for p in Produce.query.order_by('name')]
    if form.validate_on_submit():
        listing = Listing(user_id=current_user.id, produce_id=form.produce.data, type=form.listing_type.data)
        db.session.add(listing)
        db.session.commit()
        flash('Listing added!', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template('add_listing.html', form=form)

@bp.route('/matches')
@login_required
def matches():
    matches = []
    user_wants = Listing.query.filter_by(user_id=current_user.id, type='want').all()
    user_haves = Listing.query.filter_by(user_id=current_user.id, type='have').all()
    zipcode = current_user.zipcode

    for want in user_wants:
        potential_havers = Listing.query.filter_by(produce_id=want.produce_id, type='have').all()
        for match in potential_havers:
            if match.owner.zipcode != zipcode:
                continue
            matches.append(("You want", want.produce.name, "Matched with", match.owner.username))

    for have in user_haves:
        potential_wanters = Listing.query.filter_by(produce_id=have.produce_id, type='want').all()
        for match in potential_wanters:
            if match.owner.zipcode != zipcode:
                continue
            matches.append(("You have", have.produce.name, "Matched with", match.owner.username))

    return render_template('matches.html', matches=matches)
