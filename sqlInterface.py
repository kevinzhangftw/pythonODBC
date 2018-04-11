#!python3
# import pymssql
import pyodbc
from datetime import datetime

def getMaxPassengerID():
    mycursor = conn.cursor()
    mycursor.execute('select max(passenger_id) from Passenger')
    row = mycursor.fetchone()
    mycursor.close()
    # row is tuple like this (99537,), so select only first element
    return row[0]

def insertPassengerToDB(passengerTuple):
    # passenger_id = passengerTuple[0]
    # first_name = passengerTuple[1]
    # last_name = passengerTuple[2]
    # miles = passengerTuple[3]
    try:
        mycursor = conn.cursor()
        mycursor.execute('insert into Passenger values (%d, %s, %s, %d)', passengerTuple)
        conn.commit()
        return True
    except:
        print('insertion failed, passenger already exists')
        return False

def insertBooking(passenger_id, flight_code, depart_date):
    mycursor = conn.cursor()
    try:
        mycursor.execute('insert into Booking values (%s, %s, %d)', (flight_code,depart_date,passenger_id))
        conn.commit()
        return True
    except Exception as e:
        print('Insertion Failed: Possible Duplicate Insertion')
        # print("type error: " + str(e))
        return False

def insertBookingNoCommit(passenger_id, flight_code, depart_date):
    mycursor = conn.cursor()
    try:
        mycursor.execute('insert into Booking values (%s, %s, %d)', (flight_code,depart_date,passenger_id))
        # conn.commit()
        print('Booking has been successfully inserted into database')
        return True
    except:
        print('Insertion Failed: Possible Duplicate Insertion')
        return False

def createProfile():
    userInput = input('please enter your first name and last name. >> ').split()
    firstname = userInput[0]
    lastname = userInput[1]
    insertPassenger(firstname, lastname)
    appEntry()
    

def insertPassenger(firstname, lastname):
    passenger_id = getMaxPassengerID() + 1
    miles = 0
    passengerTuple = (passenger_id, firstname, lastname, miles)
    if insertPassengerToDB(passengerTuple):
        print("The profile for passenger {} {} {} was created.".format(passenger_id, firstname, lastname))
    else:
        appEntry()

def findby(flight_code, depart_date):
    mycursor = conn.cursor()
    mycursor.execute('select Passenger.passenger_id, first_name, last_name, miles from Booking, Passenger where flight_code= (%s) and depart_date=(%s) and Booking.passenger_id = Passenger.passenger_id', (flight_code, depart_date))
    row = mycursor.fetchone()
    print('==========Returning All Passengers with This Flight Instance==========')
    print('passenger_id first_name   last_name             miles')
    while row:
        print(row[0], row[1], row[2], row[3])
        row = mycursor.fetchone()
    mycursor.close()
    print('=========================================')
    print('The number of available seats for this flight instance:', findAvailableSeats(flight_code,depart_date))

def findAvailableSeats(flight_code, depart_date):
    mycursor = conn.cursor()
    mycursor.execute('select available_seats from Flight_Instance where flight_code= (%s) and depart_date=(%s)', (flight_code, depart_date))
    row = mycursor.fetchone()
    mycursor.close()
    return row[0]

def verifyFlightInstance(flight_code, depart_date):
    try:
        mycursor  = conn.cursor()
        mycursor.execute("SELECT F.flight_code, F.depart_date, F.available_seats FROM Flight_Instance F WHERE F.flight_code = %s AND F.depart_date = %s", (flight_code, depart_date))
        row = mycursor.fetchone()
        print (row[0], row[1], row[2])
        available_seats = row[2]
        mycursor.close()
        if available_seats>0:
            return True
        else:
            return False            
    except:
        return False

def verifyPassengerid(passenger_id):
    try:
        mycursor  = conn.cursor()
        mycursor.execute("SELECT first_name, last_name FROM Passenger WHERE passenger_id = %d", passenger_id)
        row = mycursor.fetchone()
        print ('Adding Booking for :', row[0], row[1])
        mycursor.close()
        return True
    except:
        return False  

def processSingleTrip(passenger_id):
    print("your chose single trip")
    inputSpec = input("specify the flight_code and depart_date. For example: JA100 2016-11-28 >> ").split()
    flight_code = inputSpec[0]
    depart_date = inputSpec[1]
    if verifyFlightInstance(flight_code, depart_date):
        print('flight instance verified, begin insertion')
        if insertBooking(passenger_id, flight_code, depart_date):
            print('Booking has been successfully added to database')
            appEntry()
        else:
            processSingleTrip(passenger_id)
    else:
        print ("Flight Instance Not found. Please try again")
        addBooking() 

def processMultiTrip(passenger_id):
    print("your chose multi trip")
    inputSpec1 = input("specify your first flight_code and depart_date. For example: JA260 2016-11-29 >> ").split()
    flight_code1 = inputSpec1[0]
    depart_date1 = inputSpec1[1]
    try:
        date1 = datetime.strptime(depart_date1,'%Y-%m-%d')
    except:
        date1 = datetime.strptime(depart_date1,'%Y/%m/%d')
    
    inputSpec2 = input("specify your second flight_code and depart_date. For example: JA260 2016-11-29 >> ").split()
    flight_code2 = inputSpec2[0]
    depart_date2 = inputSpec2[1]
    try:
        date2 = datetime.strptime(depart_date2,'%Y-%m-%d')
    except:
        date2 = datetime.strptime(depart_date2,'%Y/%m/%d')

    if depart_date1>=depart_date2:
        print('DATE ENTRY ERROR: depart_date for the second leg must be later than first depart_date')
        processMultiTrip(passenger_id)
    else:
        print('depart dates verified, checking flight instance...')
        if verifyFlightInstance(flight_code1, depart_date1) and verifyFlightInstance(flight_code2, depart_date2):
            print('both flight instances verified, begin insertion')
            try:
                insertBookingNoCommit(passenger_id, flight_code1, depart_date1)
                insertBookingNoCommit(passenger_id, flight_code2, depart_date2)
                conn.commit()
                print('Flight Instances successfully inserted')
            except:
                print('Error: Multitrip Insertion Error, Insertion rollback. check Flight_Instances')
            appEntry()
        else:
            print("Error: One or Both Flight Instances are Not found. try again")
            processMultiTrip(passenger_id)


def addBooking():
    passenger_id = input('Please enter passenger id For example: 22050 >> ')
    if verifyPassengerid(passenger_id):
        
        tripInput=input("is this a single trip or multi-city trip? enter “single” or “multi” >> ")
        if tripInput == 'single':
            processSingleTrip(passenger_id)
        elif tripInput == 'multi':
            processMultiTrip(passenger_id)
        else:
            print("wrong input!")
            addBooking()
    else:
        print('No such passenger found! please try again')
        addBooking()

def printAvailableSeats(flight_code, depart_date):
    try:
        mycursor  = conn.cursor()
        mycursor.execute("SELECT F.flight_code, F.depart_date, F.available_seats FROM Flight_Instance F WHERE F.flight_code = %s AND F.depart_date = %s", (flight_code, depart_date))
        row = mycursor.fetchone()
        print (row[0], row[1], row[2])
        available_seats = row[2]
        mycursor.close()
        if available_seats>0:
            print('number of available_seats:', available_seats)
            return True
        else:
            print('no seats available, the tickets are sold out for this flight')
            return False            
    except:
        return False



def viewPassengers():
    inputSpec = input("specify the flight_code and depart_date. For example: JA100 2016-11-28 ").split()
    flight_code = inputSpec[0]
    depart_date = inputSpec[1]
    if verifyFlightInstance(flight_code, depart_date):
        findby(flight_code, depart_date)
        appEntry()
    else:
        print('Flight_Instance not found, please try again')
        viewPassengers()

# UI
def appEntry():
    userInput = input('please select the following options: create profile, view passengers, or add booking >> ')
    if userInput == 'create profile':
        createProfile()
    elif userInput == 'view passengers':
        viewPassengers()
    elif userInput == 'add booking':
        addBooking()
    else:
        print('umm..we didnt find any matched options. you can say: create profile OR view passengers OR add booking')
        appEntry()


def main():
    global conn
    # conn = pymssql.connect(host='cypress.csil.sfu.ca', user='s_kwz', password='4YTdnH4gEGqnYJ2M', database='kwz354')
    # conn = pyodbc.connect('driver={SQL Server};server=cypress.csil.sfu.ca;uid=s_kwz;pwd=4YTdnH4gEGqnYJ2M')
    conn = pyodbc.connect('driver={SQL Server};Server=cypress.csil.sfu.ca;Trusted_Connection=yes;')
    # windows csil connection only'

    print('Welcome to manage your flight app!')
    appEntry()

if __name__ == "__main__":
    main()

