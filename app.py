# Set Up the Flask Weather App
# import our dependencies to our code environment.

import datetime as dt
import numpy as np
import pandas as pd

# Now let's get the dependencies we need for SQLAlchemy.
# which will help us access our data in the SQLite database.

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#Finally, add the code to import the dependencies that we need for Flask.

from flask import Flask, jsonify

#Set Up the Database engine for the Flask application
engine = create_engine("sqlite:///hawaii.sqlite")

#Now let's reflect the database into our classes.
Base = automap_base()

#Add the following code to reflect the database:
Base.prepare(engine, reflect=True)

#We'll create a variable for each of the classes so that we can reference them later
Measurement = Base.classes.measurement
Station = Base.classes.station

#Finally, create a session link from Python to our database with the following code:
session = Session(engine)

#Set Up Flask
# we need to define our app for our Flask application.
# This will create a Flask application called "app."

app = Flask(__name__)

#Create the Welcome Route
#Our first task when creating a Flask route is to define what our route will be. 
@app.route("/")

# add the routing information for each of the other routes.
# First, create a function welcome() with a return statement.
#Next, add the precipitation, stations, tobs, and temp routes

def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

#Precipitation Route
#The next route will return the precipitation data for the last year.
# CAUTION: Every time you create a new route, your code should be aligned to the left.

@app.route("/api/v1.0/precipitation")

#Next, we will create the precipitation() function.
#we want to add the line of code that calculates the date one year ago
#Next, write a query to get the date and precipitation for the previous year.
#Finally, we'll create a dictionary with the date as the key and the precipitation as the value.
#Jsonify() is a function that converts the dictionary to a JSON file. 

def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)

#Stations Route
#For this route we'll simply return a list of all the stations.
#this code should occur outside of the previous route and have no indentation.
@app.route("/api/v1.0/stations")

#we'll create a new function called stations().
#Now we need to create a query that will allow us to get all of the stations in our database. 
#then We want to start by unraveling our results into a one-dimensional array. 
#Next, we will convert our unraveled results into a list.

def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

#Monthly Temperature Route
#the goal is to return the temperature observations for the previous year.
#Next, create a function called temp_monthly()
#Now, calculate the date one year ago from the last date in the database.
#Query the primary station for all the temperature observations from the previous year.
#Finally, unravel the results into a one-dimensional array and convert that array into a list.
#we want to jsonify our temps list, and then return it.   

@app.route("/api/v1.0/tobs")

def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

#Statistics Route
#last route will be to report on the minimum, average, and maximum temperatures. 
# will have to provide both a starting and ending date. 

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

#Next, create a function called stats() to put our code in.
#We need to add parameters to our stats()function: a start parameter and an end parameter.
#With the function declared, we can now create a query to select the min max avg.
#we need to determine the starting and ending date, add an if-not statement to our code. 
#We'll need to query our database using the list that we just made.
#Then, we'll unravel the results into a one-dimensional array and convert them to a list.
#Finally, we will jsonify our results and return them.

def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)





