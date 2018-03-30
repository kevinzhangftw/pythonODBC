import pymssql


conn = pymssql.connect(host='cypress.csil.sfu.ca', user='s_kwz', password='4YTdnH4gEGqnYJ2M', database='kwz354')

mycursor = conn.cursor()
mycursor.execute('SELECT * from Passenger')
row = mycursor.fetchone()
while row:
    print(row)
    row = mycursor.fetchone()

mycursor.close()

