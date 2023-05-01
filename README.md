# Analyzing Climate Data with SQL ALchemy and Creating a Weather API with Flask

# Overview

For this project, I was asked to analyze data from 9 weather stations, using SQL Alchemy, then to use Flask to make that data available as an API. To start,
I was provided with weather measurements and data about each station in both a SQLite file and in two .csv files, available in the 'Resources' folder of this
repository. Along the way, I was able to use familiar tools like Datetime in new ways. Using Datetime specifically, to enable my API to accept specific dates and date ranges
in its URL, so users can extract data from specific points of time in which they are interested. In sum, the code I wrote will be very useful for users seeking
weather data from Hawaii over a several year span, and it can readily be improved by adding new stations and new timespans from before and after this data
was collected.

# Features

The SQL Alchemy code, featured in the Jupyter Notebook in this repository, covers many of the fundamentals of data analysis in SQL Alchemy. The code reflects
the database and finds the classes featured in the data, then saves references to each of those classes. As a result, queries can be run to find both the 
weather measurements and data about the weather stations, sorted by certain positions they hold in the data (e.g., where and when the measurements were taken).
An example is featured below:

Base = automap_base()
Base.prepare(engine, reflect=True)

#View all of the classes that automap found

for cls in Base.classes:

    print(cls.__table__.name)

#Save references to each table

Measurement = Base.classes.measurement

Station = Base.classes.station

#Perform a query to retrieve the data and precipitation scores

query1 = session.query(Measurement.date, Measurement.prcp).\

    filter(Measurement.date >= one_year_date).\
    
    order_by(Measurement.date).all()
    
This code uses the classes to locate weather measurements from their class, then filter and order them, according to a date connected in the same class.

One of the major benefits of using SQL Alchemy is that SQL data can be used to create many of the helpful visulaizations and tools available through Pandas.
For example, after getting the results of the query featured above, they can be placed into a Pandas DataFrame and then made into a number of different plots.
Moreover, helpful tools from Python -- like Datetime -- can help to further sort the data according to dates, as they did for the results of that query.

When creating the API, I followed several of the same steps, reflecting the database, finding its classes and saving them. Using flask, I generated the routes
to the types of data I was assigned to include. From there, I wrote various queries to find the data I needed -- including the most recent date, the temperature,
and the percipitation measurements -- and to sort them according to when and where they were measured. Then, for each route, I wrote a simple loop that appended
the data to an empty dictionary. Finally, I turned each dictionary into a JSON object. 

I should note, I appended each dictionary slightly differently. Studying this process, I came across several different methods of achieving the same result.
When I encountered errors using one method, I transitioned to another. In the future, I hope to edit this code to append these dictionaries in a more uniform
way.

# Instructions

To see the DataFrames and Visualizations in the Jupyter Notebook, simply copy the Notebook from Git to your local machine, then run each cell.

To go to the weather API, copy 'app.py' from Git to your local machine, then run the code. Click the link that appears in your terminal, which will open
the API in your browser. Copy and paste your desired route to append the web address displayed in your browser. 

For the start_date and start_date/end_date routes, be sure to format your desired dates as 'yyyy-mm-dd'. The SQL Alchemy queries will sort the code according
to these dates, then return statistics about weather observations that fell between them.

# Author
Daniel Adamson  
