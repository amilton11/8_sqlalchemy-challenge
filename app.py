# import dependancies
from flask import Flask, jsonify
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine("sqlite:///Resources/hawaii.sqlite", echo=False)
session = Session(engine)

Base = automap_base()
Base.prepare(engine, reflect=True)

# define variables
Measurement = Base.classes.measurement
Station = Base.classes.station

# create the app
app = Flask(__name__)

# /
# home page
# list all routes
@app.route("/")
def home():
    return "/api/v1.0/precipitation <br> /api/v1.0/stations <br> /api/v1.0/tobs <br> /api/v1.0/start=YYYY-MM-DD <br> /api/v1.0/start=YYYY-MM-DD/end=YYYY-MM-DD"

# /api/v1.0/precipitation
# Convert the query results to a dictionary using date as the key and prcp as the value.
# Return the JSON representation of your dictionary.
@app.route('/api/v1.0/precipitation')
def prcp():
    data_perc = session.query(Measurement.date, Measurement.prcp).order_by(Measurement.date).all()
    return jsonify(data_perc)

# /api/v1.0/stations
# Return a JSON list of stations from the dataset.
@app.route('/api/v1.0/stations')
def station():
    data_stations = session.query(Station.station).all()
    return jsonify(data_stations)

# /api/v1.0/tobs
# Query the dates and temperature observations of the most active station for the last year of data.
# Return a JSON list of temperature observations (TOBS) for the previous year.
@app.route('/api/v1.0/tobs')
def temps():
    data_temps = session.query(Measurement.tobs).all()
    return jsonify(data_temps)

# /api/v1.0/<start> and /api/v1.0/<start>/<end>
# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.

@app.route("/api/v1.0/<start>")
def sngl_date(start):
    start_date = dt.datetime.strptime(start, "%Y-%m-%d")
    summary_stats_a = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.round(func.avg(Measurement.tobs))).filter(Measurement.date >= start_date).all()
    
    session.close()

    return jsonify(summary_stats_a)


@app.route("/api/v1.0/<start>/<end>")
def strt_end_dates(start, end):
    strt_date = dt.datetime.strptime(start, "%Y-%m-%d")
    end_date = dt.datetime.strptime(end, "%Y-%m-%d")
    summary_stats_b = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.round(func.avg(Measurement.tobs))).filter(Measurement.date.between(strt_date, end_date)).all()
    
    session.close()

    return jsonify(summary_stats_b)


# if I am being envoked by the command line
if __name__ == "__main__":
    app.run(debug=True)