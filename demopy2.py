#!python2
import pymssql
from datetime import datetime

# UI
def appEntry():
    userInput = input('please select the following options: create profile, view passengers, or add booking >> ')
    if userInput == 'create profile':
        print('createProfile()')
    elif userInput == 'view passengers':
        print('viewPassengers()')
    elif userInput == 'add booking':
        print('addBooking()')
    else:
        print('umm..we didnt find any matched options. you can say: create profile OR view passengers OR add booking')
        appEntry()

def main():
    global conn
    conn = pymssql.connect(host='cypress.csil.sfu.ca', user='s_kwz', password='4YTdnH4gEGqnYJ2M', database='kwz354')
    print('Welcome to manage your flight app!')
    appEntry()

if __name__ == "__main__":
    main()

