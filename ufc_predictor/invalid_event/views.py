from flask import (
    Blueprint, current_app, flash, redirect, render_template, request, url_for,
)

invalid_event_views = Blueprint('invalid_event', __name__)


@invalid_event_views.route('/invalid-event/<date>')
def invalid_date(date):
    return render_template('invalid_event/no_event.html', date=date)
