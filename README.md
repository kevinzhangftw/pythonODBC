# pythonODBC
python DB application using pyodbc and pymssql

### on local CSIL windows Machines ONLY

to run:

### python sqlInterface.py

You will be presented with three options
create profile, view passengers, or add booking

type in your option to select that option
### create profile -> enter your first name and last name to insert in database
### view passengers -> enter flight instance to see passengers in that instance plus seats available
### add booking -> after keying passenger_id, you have to select single or multi trip

single allows you insert one valid booking
multi allows you to insert 2 valid bookings at once provided that the second depart date is later than the first one

### date format: either 2016/11/30 or 2016-11-30 is fine. But you must stay consistent to the format your choose! Date only compares to the same format
