# Import Flask
from flask import Flask, jsonify

# Import Dependencies
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.pool import StaticPool

################################################
# Database Setup
################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

base = automap_base()
base.prepare(engine, reflect = True)

measurement = base.classes.measurement
station = base.classes.station

################################################
# Flask Setup and Routes
################################################
app = Flask(__name__)

# Home Route
@app.route("/")
def welcome():
        return """<html>
        <h1>Hawaii Climate App (Flask API)</h1>
        <img src="https://cdn2.veltra.com/ptr/20200122204724_506709530_1209_0.jpg" alt="Hawaii"/>
        <p>Precipitation Analysis:</p>
        <ul>
        <li><a href="/api/v1.0/precipitation">/api/v1.0/precipitation</a></li>
        </ul>
        <p>Station Analysis:</p>
        <ul>
        <li><a href="/api/v1.0/stations">/api/v1.0/stations</a></li>
        </ul>
        <p>Temperature Analysis:</p>
        <ul>
        <li><a href="/api/v1.0/tobs">/api/v1.0/tobs</a></li>
        </ul>
        <p>Start Day Analysis:</p>
        <ul>
        <li><a href="/api/v1.0/2017-03-14">/api/v1.0/2017-03-14</a></li>
        </ul>
        <p>Start & End Day Analysis:</p>
        <ul>
        <li><a href="/api/v1.0/2017-03-14/2017-03-28">/api/v1.0/2017-03-14/2017-03-28</a></li>
        </ul>
        </html>
        """

# precip route
@app.route("/api/v1.0/precipitation")
def precipitation():
        session = Session(engine)
        # Calculate the date one year from the last date in data set.
        one_year_prior = dt.date(2017,8,23)-dt.timedelta(days=365)
        # Design a query to retrieve the last 12 months of precipitation data and plot the results. 
        # Starting from the most recent data point in the database. 
        # precip=prcp in csv file
        prcp_data = session.query(measurement.date, measurement.prcp).filter(measurement.date >= one_year_prior).order_by\
        (measurement.date).all()
        # Convert List of Tuples Into a Dictionary
        prcp_data_list = dict(prcp_data)
        # Return JSON Representation of Dictionary
        return jsonify(prcp_data_list)

# Station Route
@app.route("/api/v1.0/stations")
def stations():
        session = Session(engine)
        # Return a JSON List of Stations From the Dataset
        stations_all = session.query(station.station, station.name).all()
        # Convert List of Tuples Into Normal List
        station_list = list(stations_all)
        # Return JSON List of Stations from the Dataset
        return jsonify(station_list)

# TOBs Route
@app.route("/api/v1.0/tobs")
def tobs():
        session = Session(engine)
        # Query for the Dates and Temperature Observations from a Year from the Last Data Point
        one_year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
        # Design a Query to Retrieve the Last 12 Months of Precipitation Data Selecting Only the 
        # `date` and `prcp` Values
        tobs_data = session.query(measurement.date, measurement.tobs).\
                filter(measurement.date >= one_year_ago).\
                order_by(measurement.date).all()
        # Convert List of Tuples Into Normal List
        tobs_data_list = list(tobs_data)
        # Return JSON List of Temperature Observations (tobs) for the Previous Year
        return jsonify(tobs_data_list)

# Start Day Route
@app.route("/api/v1.0/<start>")
def start_day(start):
        session = Session(engine)
        start_day = session.query(measurement.date, func.min(measurement.tobs),\
        func.avg(measurement.tobs), func.max(measurement.tobs)).\
                filter(measurement.date >= start).\
                group_by(measurement.date).all()
        # Convert List of Tuples Into Normal List
        start_day_list = list(start_day)
        # Return JSON List of Min Temp, Avg Temp and Max Temp for a Given Start Range
        return jsonify(start_day_list)

# Start-End Day Route
@app.route("/api/v1.0/<start>/<end>")
def start_end_day(start, end):
        session = Session(engine)
        start_end_day = session.query(measurement.date, func.min(measurement.tobs),\
             func.avg(measurement.tobs), func.max(measurement.tobs)).\
                filter(measurement.date >= start).\
                filter(measurement.date <= end).\
                group_by(measurement.date).all()
        # Convert List of Tuples Into Normal List
        start_end_day_list = list(start_end_day)
        # Return JSON List of Min Temp, Avg Temp and Max Temp for a Given Start-End Range
        return jsonify(start_end_day_list)

# Define Main Behavior
if __name__ == '__main__':
    app.run(debug=True)


