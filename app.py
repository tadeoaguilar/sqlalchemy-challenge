import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify
from datetime import date
import datetime as dt
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
measurement = Base.classes.measurement
station = Base.classes.station
inspector = inspect(engine)
# Save reference to the table


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
        f"/api/v1.0/tobs"
        
    )


@app.route("/api/v1.0/precipitation")
def names():
    # Create our session (link) from Python to the DB
    session = Session(engine)

   
    # Query all stations
    #dateFilter = dt.datetime(2016, date.today().month, date.today().day)

    results = session.query(measurement.date,measurement.prcp).all()
    all_stations = []
    for date, prcp in results:
        station_dict = {}
        station_dict["date"] = date
        station_dict["prcp"] = prcp
        
        all_stations.append(station_dict)
    
    session.close()

 
    return jsonify(all_stations)

if __name__ == '__main__':
    app.run(debug=True)