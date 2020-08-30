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
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

   
    # Query all stations
    #dateFilter = dt.datetime(2016, date.today().month, date.today().day)

    results = session.query(measurement.date,measurement.prcp).all()
    all_precep = []
    for date, prcp in results:
        station_dict = {}
        station_dict["date"] = date
        station_dict["prcp"] = prcp
        
        all_precep.append(station_dict)
    
    session.close()

 
    return jsonify(all_precep)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)


    sel =[station.name]
    results = session.query(*sel).all()    
    session.close()

    all_precep = list(np.ravel(results))
    return jsonify(all_precep)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    maxDate = session.query(func.max(measurement.date)).one()
    #Get MAx date - 1 year
    fromDate = dt.datetime.strptime(maxDate[0], '%Y-%m-%d')
    py = fromDate.year -1
    dateFilter = dt.datetime(py, fromDate.month, fromDate.day)

    mostActive =session.query(measurement.station,func.count(measurement.station)).\
    group_by(measurement.station).\
    order_by(func.count(measurement.station).desc()).all()
    station=mostActive[0][0]
    results =session.query( func.strftime("%m", measurement.date),measurement.tobs).\
        filter(measurement.station == station).\
        filter(measurement.date >= dateFilter).all()

    session.close()

    all_precep = list(np.ravel(results))
    return jsonify(all_precep)


if __name__ == '__main__':
    app.run(debug=True)


