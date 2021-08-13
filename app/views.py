"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
from operator import sub
from flask.wrappers import Request
import os, re
from app import app, db
from flask import render_template, request, redirect, url_for, flash, send_from_directory, abort, jsonify, g, make_response
# from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
#from datetime import datetime, timezone
import datetime
from app.models import *
# from app.forms import *
from app.jwt import *
from app.api_endpoints import *
from app.forms import *



###
# Routing for your application.
###
@app.route('/')
def home():
    return render_template('pages/home.html')

@app.route('/register')
def register_page():
    form=SignUpForm()
    return render_template('pages/register.html', form=form)


@app.route('/login')
def login_page():
    form= LoginForm()
    return render_template('pages/login_form.html', form=form)


@app.route('/createEvents')
def createEvents_page():
    form= CreateEvent()
    groups = Group.query.all()
    form.group_id.choices = ([(g.id, g.name) for g in groups])
    return render_template('pages/events_form.html', form=form)


@app.route('/createGroups')
def createGroups_page():
    form= CreateGroup()

    return render_template('pages/group_form.html', form=form)
      
@app.route('/events')
def viewAllEvents():
    return render_template('pages/view_events.html')

@app.route('/events/pending')
def viewPendingEvents():
    return render_template('pages/view_pending_events.html')

@app.route('/addMember')
def addNewMember():
    form= AddMember()
    groups = Group.query.all()
    form.group.choices = ([(g.id, g.name) for g in groups])
    return render_template('pages/add_member.html', form=form)

# FOR ADD EVENT
#  the createGroup method requires the schedule endpoint aka attachEventToGroup

# Please create all new routes and view functions above this route.
# This route is now our catch all route for our VueJS single page
# application.

# @app.route('/', defaults={'path': ''})
# @app.route('/<path:path>')
# def index(path):
#     """
#     Because we use HTML5 history mode in vue-router we need to configure our
#     web server to redirect all routes to index.html. Hence the additional route
#     "/<path:path".
#     Also we will render the initial webpage and then let VueJS take control.
#     """
#     return render_template('pages/home.html')


@app.route('/profileUploads/<filename>')
def get_profile_image(filename):
    return send_from_directory(os.path.join('..', app.config['PROFILE_UPLOAD_FOLDER']), filename)

@app.route('/eventUploads/<filename>')
def get_event_image(filename):
    return send_from_directory(os.path.join('..', app.config['EVENT_UPLOAD_FOLDER']), filename)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            )
            error_messages.append(message)

    return error_messages


###
# The functions below should be applicable to all Flask apps.
###


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8079")
