def createProfile(firstname, lastname):
    largestPassenger_id = 1234 #SELECT MAX(passenger_id) FROM Passenger
    passenger_id = largestPassenger_id + 1
    miles = 0
    # INSERT ON Passenger first_name last_name passenger_id miles
    print("The profile for passenger {} {} {} was created.".format(passenger_id, firstname, lastname))

# Test
createProfile("kai", "z")

