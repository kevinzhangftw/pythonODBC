import pymssql

def getMaxPassengerID():
    mycursor = conn.cursor()
    mycursor.execute('select max(passenger_id) from Passenger')
    row = mycursor.fetchone()
    mycursor.close()
    # row is tuple like this (99537,), so select only first element
    return row[0]

def insertDB(passengerTuple):
    # passenger_id = passengerTuple[0]
    # first_name = passengerTuple[1]
    # last_name = passengerTuple[2]
    # miles = passengerTuple[3]
    mycursor = conn.cursor()
    mycursor.execute('insert into Passenger values (%d, %s, %s, %d)', passengerTuple)
    conn.commit()

def createProfile(firstname, lastname):
    passenger_id = getMaxPassengerID() + 1
    miles = 0
    passengerTuple = (passenger_id, firstname, lastname, miles)
    insertDB(passengerTuple)
    # i would write conditional to check insertion success or not, 
    # but pymssql does not return such Bools 
    print("The profile for passenger {} {} {} was created.".format(passenger_id, firstname, lastname))
    
def findby(flight_code, depart_date):
    print("the “passenger_id”, “first_name”, “last_name” and “miles” for all the passengers for this flight instance,")
    print("how many seats are still available for this flight instance")

def addBooking(passenger_id):
    tripInput=input("is this a single trip or multi-city trip? enter “single” or “multi”")
    if tripInput == 'single':
        print("your chose single trip")
        inputSpec = input("specify the flight_code and depart_date. For example: 12345 1990/11/03 ").split()
        flight_code = inputSpec[0]
        depart_date = inputSpec[1]
        print("fligt_code:", flight_code)
        print("depart_date:", depart_date)
    elif tripInput == 'multi':
        print("your chose multi trip")
        inputSpec1 = input("specify your first flight_code and depart_date. For example: 12345 1990/11/03 ").split()
        flight_code1 = inputSpec1[0]
        depart_date1 = inputSpec1[1]
        print("fligt_code1:", flight_code1)
        print("depart_date1:", depart_date1)

        inputSpec2 = input("specify your second flight_code and depart_date.  the “depart_date” of the second leg has to be no earlier than the “depart_date” of the first leg. For example: 12345 1990/11/03 ").split()
        flight_code2 = inputSpec2[0]
        depart_date2 = inputSpec2[1]
        print("fligt_code2:", flight_code2)
        print("depart_date2:", depart_date2)
    else:
        print("wrong input!")

# UI
def main():
    global conn
    conn = pymssql.connect(host='cypress.csil.sfu.ca', user='s_kwz', password='4YTdnH4gEGqnYJ2M', database='kwz354')
    # Tests
    # createProfile("june", "kim")
    findby(1,2)
    # addBooking(1234)



if __name__ == "__main__":
    main()

