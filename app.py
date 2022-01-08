import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################


# Convert the query results to a dictionary using `date` as the key and `prcp` as the value. Return the JSON representation of your dictionary.
@app.route("/api/v1.0/precipitation")
def precipitationfunction():
    
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Calculate the date one year from the last date in data set.
    twelve_months_prev = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    # Perform queries to retrieve data
    datesprecpsqueryresults = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date > twelve_months_prev).all()

    session.close()    
    
    precips_dict = []
    for date, precip in datesprecpsqueryresults:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["prcp"] = precip       
        precips_dict.append(precip_dict)
    
    return jsonify(precips_dict)

# List all routes that are available.
@app.route("/")
def welcome():
    return (
        f"Welcome to my Climate App!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/[start yyyy-mm-dd]<br/>"
        f"/api/v1.0/[start yyyy-mm-dd]_[end yyyy-mm-dd]<br/>"
    )

# Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stationsfunction():
    
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Perform query to retrieve data to a tuple list
    stationsqueryresult=session.query(Station.name).order_by(Station.name).all()

    session.close()    
    
    # Convert tuple list into normal list
    stationslist = list(np.ravel(stationsqueryresult))

    # return a jsonified normal list
    return jsonify(stationslist)

# Return a JSON list of temperature observations (TOBS) for the previous year.
@app.route("/api/v1.0/tobs")
def tobsfunction():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Calculate the date one year from the last date in data set
    twelve_months_prev = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    # Query to retrieve data to a tuple list
    tobs_prev_yr_queryresult = session.query(Measurement.tobs).filter(Measurement.date > twelve_months_prev).filter(Measurement.station == "USC00519281").order_by(Measurement.date).all()
    
    session.close()    
    
    # Convert tuple list into normal list
    tobslist = list(np.ravel(tobs_prev_yr_queryresult))

    # return a jsonified normal list    
    return jsonify(tobslist)

# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start date
@app.route("/api/v1.0/<start_date>")
def start_date_summ(start_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query to retrieve summarized data
    StartTempQueryResults = session.query(func.min(Measurement.tobs).label('MinTemp'),func.max(Measurement.tobs).label('MaxTemp'),func.avg(Measurement.tobs).label('AvgTemp')).filter(Measurement.date >= start_date).all()
    
    session.close() 

    # Create a dictionary from the row data and append to a list of start_date_tobs
    start_date_tobs_list = []
    for MinTemp, AvgTemp, MaxTemp in StartTempQueryResults:
        start_date_tobs_dict = {}
        start_date_tobs_dict["MinTemp"] = MinTemp
        start_date_tobs_dict["AvgTemp"] = AvgTemp
        start_date_tobs_dict["MaxTemp"] = MaxTemp
        start_date_tobs_list.append(start_date_tobs_dict) 
    return jsonify(start_date_tobs_list)


# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for given start_end dates
@app.route("/api/v1.0/<start_date>_<end_date>") #http://127.0.0.1:5000/api/v1.0/2016-08-01/2016-08-31
def Start_end_date(start_date, end_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query to retrieve summarized data
    StartEndTempQueryResults = session.query(func.min(Measurement.tobs).label('MinTemp'),func.max(Measurement.tobs).label('MaxTemp'),func.avg(Measurement.tobs).label('AvgTemp')).\
                filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    session.close() 

    # Create dict from the row data and append to a list of start_end_date_tobs
    start_end_tobs = []
    for MinTemp, AvgTemp, MaxTemp in StartEndTempQueryResults:
        start_end_tobs_dict = {}
        start_end_tobs_dict["MinTemp"] = MinTemp
        start_end_tobs_dict["AvgTemp"] = AvgTemp
        start_end_tobs_dict["MaxTemp"] = MaxTemp
        start_end_tobs.append(start_end_tobs_dict) 
    return jsonify(start_end_tobs)

if __name__ == "__main__":
    app.run(debug=True)