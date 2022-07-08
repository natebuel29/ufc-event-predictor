from flask import (
    Blueprint, current_app, flash, redirect, render_template, request, url_for,
)

invalid_event_views = Blueprint('invalid_event', __name__)


@invalid_event_views.route('/invalid-event/<date>')
def invalid_date(date):
    print(f"yoooo im in my zone im feeling it on {date}")
    return render_template('invalid_event/invalid_event.html', date=date)
