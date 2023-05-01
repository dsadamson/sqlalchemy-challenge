# Import the dependencies.
import numpy as np
import os
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
base = automap_base()
# reflect the tables
base.prepare(autoload_with = engine)

# Save references to each table
measurement = base.classes.measurement
station = base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    return (
        f"Welcome to the Climate App <br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start_date&gt;<br/>"
        f"/api/v1.0/&lt;start_date&gt;/&lt;end_date&gt;"
    )
#precipitation route
@app.route("/api/v1.0/precipitation")

#find most recent date and the date from 1 year ago
def precipitation():
    session = Session(engine)
    recent_date = session.query(func.max(measurement.date)).scalar()
    one_year_date = dt.datetime.strptime(recent_date, '%Y-%m-%d') - dt.timedelta(days=365)
    session.close()
    
    #query for precipitation data from the past year
    session = Session(engine)
    prcp_query = session.query(measurement.date, measurement.prcp).\
            filter(measurement.date >= one_year_date).\
            order_by(measurement.date).all()
    session.close()

    #return json object for precipitation
    prcp_dict = {}
    for date, prcp in prcp_query:
            prcp_dict[date] = prcp
    return jsonify(prcp_dict)

#stations route
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    station_query = session.query(station.station, station.name, station.latitude, station.longitude, station.elevation).all()
    session.close()

#display information about each weather station
    stations_dict = {}
    for station_result in station_query:
        station_name, name, latitude, longitude, elevation = station_result
        stations_dict[station_name] = {
            "name": name,
            "latitude": latitude,
            "longitude": longitude,
            "elevation": elevation
        }
    return jsonify(stations_dict)

#temperature route
@app.route("/api/v1.0/tobs")
def tobs():
    #find most recent date and date from 1 year before
    session = Session(engine)
    recent_date = session.query(func.max(measurement.date)).scalar()
    one_year_date = dt.datetime.strptime(recent_date, '%Y-%m-%d') - dt.timedelta(days=365)
    session.close()

    # Query temperature data for most active station and return as JSON
    session = Session(engine)
    most_active_query = session.query(measurement.station, func.count(measurement.station)).\
        group_by(measurement.station).\
        order_by(func.count(measurement.station).desc()).first()
    most_active_station = most_active_query[0]

    # find temperature at most active station for one year, until most recent date
    tobs_query = session.query(measurement.date, measurement.tobs).\
        filter(measurement.station == most_active_station).\
        filter(measurement.date >= one_year_date).\
        order_by(measurement.date).all()
    session.close()

    #append query results to list, then jsonify
    tobs_list = []
    for date, tobs in tobs_query:
        tobs_dict = {}
        tobs_dict['station'] = most_active_station
        tobs_dict['date'] = date
        tobs_dict['temperature (f)'] = tobs
        tobs_list.append(tobs_dict)
    return jsonify(tobs_list)

#start_date route
@app.route("/api/v1.0/<start_date>")
def start(start_date):
    #convert start_date to datetime object
    start_date = dt.datetime.strptime(start_date, '%Y-%m-%d').date()

    #query for max, min, and avg temp. from start_date to end of data set
    session = Session(engine)
    start_date_query = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
        filter(measurement.date >= start_date).all()
    session.close()

    # Create a dictionary for the temperature data, then jsonify
    temp_dict = {}
    temp_dict['start_date'] = start_date.isoformat()
    temp_dict['end_date'] = (session.query(func.max(measurement.date)).scalar())
    temp_dict['min_temp'] = start_date_query[0][0]
    temp_dict['max_temp'] = start_date_query[0][1]
    temp_dict['avg_temp'] = start_date_query[0][2]

    return jsonify(temp_dict)

#start_date/end_date route
@app.route("/api/v1.0/<start_date>/<end_date>")
def start_end(start_date, end_date):
    #convert start_date and end_date to datetime object
    start_date = dt.datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = dt.datetime.strptime(end_date, '%Y-%m-%d').date()
    #find min, max, and avg temp between start_date and end_date
    session = Session(engine)
    date_range_query = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
        filter(measurement.date >= start_date).\
        filter(measurement.date <= end_date)
    session.close()

    #append query results to dictionary, then jsonify
    date_range_dict = {}
    date_range_dict['start_date'] = start_date.isoformat()
    date_range_dict['end_date']=end_date.isoformat()
    date_range_dict['min_temp']=date_range_query[0][0]
    date_range_dict['max_temp']=date_range_query[0][1]
    date_range_dict['avg_temp']=date_range_query[0][2]

#run flask app
if __name__ == '__main__':
    app.run(debug=True, port=5002)