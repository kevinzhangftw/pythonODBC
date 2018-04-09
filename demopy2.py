#!python2
import pymssql
from datetime import datetime

def main():
    global conn
    conn = pymssql.connect(host='cypress.csil.sfu.ca', user='s_kwz', password='4YTdnH4gEGqnYJ2M', database='kwz354')
    print('Welcome to manage your flight app!')
    # appEntry()

if __name__ == "__main__":
    main()

