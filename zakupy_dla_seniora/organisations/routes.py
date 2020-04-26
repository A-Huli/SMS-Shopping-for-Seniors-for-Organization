from flask import Blueprint, render_template, redirect, abort, url_for, request
from flask_login import current_user
from flask_babel import _

from zakupy_dla_seniora.auth.functions import superuser_role_required, employee_role_required
from zakupy_dla_seniora.organisations.forms import AddOrganisationForm, EditOrganisationForm
from zakupy_dla_seniora.organisations.models import Organisations


organisations = Blueprint('organisations', __name__, url_prefix='/<lang_code>')


@organisations.route('/organisation')
@organisations.route('/organisation/<org_id>')
def organisation(org_id=None):
    org = Organisations.get_by_id(org_id).to_dict_view_organisation()
    if not org:
        abort(404)
    name = org.pop('Name')
    employees = org.pop('Employees')
    volunteers = org.pop('Volunteers')
    return render_template('organisations/view_organisation.jinja2', org=org, name=name, employees=employees,
                           volunteers=volunteers)


@organisations.route('/organisations', methods=['GET'])
@superuser_role_required
def get_all_organisations():
    orgs = Organisations.query.all()
    orgs = [org.to_dict_view_all_organisations() for org in orgs]
    if 'msg' in request.args:
        return render_template('organisations/all_organisations.jinja2', organisations=orgs, columns=orgs[0].keys(),
                               msg=request.args['msg'])
    return render_template('organisations/all_organisations.jinja2', organisations=orgs, columns=orgs[0].keys())


@organisations.route('/organisation/delete/<org_id>')
@superuser_role_required
def delete_organisation(org_id):
    org = Organisations.get_by_id(org_id)
    msg = f"{_('Organisation')} {org.name} {_('has been deleted')}."
    org.delete()
    return redirect(url_for('organisations.get_all_organisations', msg=msg))


@organisations.route('/organisation/add', methods=['GET', 'POST'])
@superuser_role_required
def add_organisation():
    form = AddOrganisationForm()
    if request.method == 'POST' and form.validate_on_submit():
        if not Organisations.get_by_name(form.name.data):
            org = Organisations(**form.to_dict(), added_by=current_user.id)
            org.save()
            msg = f"{_('Organisation')} {org.name} {_('has been successfully added')}."
            return redirect(url_for('organisations.add_organisation', msg=msg))
        else:
            msg = f"{_('Name')} {form.name.data} {_('is already taken.')}."
            return render_template('organisations/add_organisation.jinja2', form=form,
                                   msg=msg)
    if 'msg' not in request.args:
        return render_template('organisations/add_organisation.jinja2', form=form)
    return render_template('organisations/add_organisation.jinja2', form=form,
                           msg=request.args['msg'], success=True)


@organisations.route('/organisation/edit/', methods=['GET', 'POST'])
@organisations.route('/organisation/edit/<org_id>', methods=['GET', 'POST'])
@employee_role_required
def edit_organisation(org_id=None):
    org = Organisations.get_by_id(org_id)
    if not org:
        abort(404)
    form = EditOrganisationForm(obj=org)
    if request.method == 'POST' and form.validate_on_submit():
        org.edit(**form.to_dict())
        org.save()
        return redirect(url_for('organisations.edit_organisation', org_id=org_id,
                                msg=_('Changes were successfully saved.')))
    if 'msg' not in request.args:
        return render_template('organisations/edit_organisation.jinja2', organisation=org, form=form)
    return render_template('organisations/edit_organisation.jinja2', organisation=org, form=form,
                           msg=request.args['msg'], success=True)
