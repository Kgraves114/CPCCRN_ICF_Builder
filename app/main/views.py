from flask import render_template, redirect, url_for, abort, flash, Flask
from flask_login import login_required, current_user
from . import main
from .forms import EditConsentForm, EditProfileAdminForm, PostForm
from .. import db
from ..models import Permission, Role, User, Post
from ..decorators import admin_required
from flask_weasyprint import HTML, render_pdf


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('study.html', user=user)

@main.route('/user/<studyname>.pdf')
def study_pdf(studyname):
    # Make a PDF from another view
    return render_pdf(url_for('.study', studyname=current_user.studyname))

@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)

@main.route('/edit-consent', methods=['GET', 'POST'])
@login_required
def edit_consent():
    form = EditConsentForm()
    if form.validate_on_submit():
        current_user.investigator = form.investigator.data
        current_user.location = form.location.data
        current_user.background = form.background.data
        current_user.study_procedure = form.study_procedure.data
        current_user.risksbenefits = form.risksbenefits.data
        current_user.PHI = form.PHI.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Your consent has been updated.')
        return redirect(url_for('.study', studyname=current_user.studyname))
    form.investigator.data = current_user.investigator
    form.location.data = current_user.location
    form.background.data = current_user.background
    form.study_procedure.data = current_user.study_procedure
    form.risksbenefits.data = current_user.risksbenefits
    form.PHI.data = current_user.PHI
    return render_template('edit_consent.html', form=form)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.investigator = form.investigator.data
        user.location = form.location.data
        user.background = form.background.data
        user.study_procedure = form.study_procedure.data
        user.risksbenefits = form.risksbenefits.data
        user.PHI = form.PHI.data
        db.session.add(user)
        db.session.commit()
        flash('The profile has been updated.')
        return redirect(url_for('.study', studyname=user.studyname))
    form.investigator.data = user.investigator
    form.location.data = user.location
    form.background.data = user.background
    form.study_procedure.data = user.study_procedure
    form.risksbenefits.data = user.risksbenefits
    form.PHI.data = user.PHI
    return render_template('edit_consent.html', form=form, user=user)
