from flask import ( Blueprint, flash, redirect, render_template, request, url_for, jsonify)

from uhcarmel.auth import login_required
from uhcarmel.db import get_db, Location

bp = Blueprint('locations', __name__,url_prefix='/uhcarmel/locations')

@bp.route('/')
def index():
    db = get_db()
    locations = db.query(Location).all()
    return render_template('locations/index.html', locations=locations)

@bp.route('/JSON')
def get_all_locations_json():
    db = get_db()
    locations = db.query(Location).all()
    return jsonify(locations= [l.serialize for l in locations])

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        name = request.form['name']
        altitude = request.form['altitude']
        longitude = request.form['longitude']
        error = None

        if not name or not altitude or not longitude:
            error = 'Missing data'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            new_location = Location(name=name, altitude=altitude, longitude=longitude)
            db.add(new_location)
            db.commit()
            return redirect(url_for('locations.index'))

    return render_template('locations/create.html')


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    db = get_db()
    location = db.query(Location).filter_by(id=id).one()

    if request.method == 'POST':
        name = request.form['name']
        altitude = request.form['altitude']
        longitude = request.form['longitude']
        error = None

        if not name or not altitude or not longitude:
            error = 'Missing data'

        if error is not None:
            flash(error)
        else:
            location.name = name
            location.altitude = altitude
            location.longitude = longitude
            db.add(location)
            db.commit()
            return redirect(url_for('locations.index'))

    return render_template('locations/update.html', location=location)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    db = get_db()
    location = db.query(Location).filter_by(id=id).one()
    db.delete(location)
    db.commit()
    return redirect(url_for('locations.index'))