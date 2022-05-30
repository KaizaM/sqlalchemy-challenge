from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

#################################################
# Precipitation Route
#################################################

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all date and precitpitation
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    start_date = dt.date(2017,8,23)-dt.timedelta(days=365)
    date_range = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date >= start_date).order_by(Measurement.date).all()

    session.close()

    return jsonify(dict(date_range))

#################################################
# Stations Route
#################################################

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all Stations
    stations = ((session.query(Measurement.station,func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()))
    session.close()

    return jsonify(dict(stations))

#################################################
# Temperature Route
#################################################

@app.route("/api/v1.0/tobs")
def tabs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all date and Temperatures
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    start_date = dt.date(2017,8,23)-dt.timedelta(days=365)
    temp_range = (session.query(Measurement.date,Measurement.tobs).filter(Measurement.date >= start_date).filter(Measurement.station == 'USC00519281'))

    session.close()

    return jsonify(dict(temp_range))

#################################################
# Start Only Route
#################################################

@app.route("/api/v1.0/<start>")
def start_only(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all date and Temperatures
    temp_min = session.query(func.min(Measurement.tobs)).filter(Measurement.date >= start)
    temp_max = session.query(func.max(Measurement.tobs)).filter(Measurement.date >= start)
    temp_avg = session.query(func.avg(Measurement.tobs)).filter(Measurement.date >= start)
    
    session.close()

    final_list = [temp_min[0][0], temp_max[0][0], temp_avg[0][0]]
    return jsonify(final_list)

#################################################
# Start-End Route
#################################################
@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all date and Temperatures
    temp_min = session.query(func.min(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end)
    temp_max = session.query(func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end)
    temp_avg = session.query(func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end)
    
    session.close()

    final_list = [temp_min[0][0], temp_max[0][0], temp_avg[0][0]]
    return jsonify(final_list)

if __name__ == '__main__':
    app.run(debug=True)

