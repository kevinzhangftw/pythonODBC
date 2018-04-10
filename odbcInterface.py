import pyodbc

conn = pyodbc.connect('driver={SQL Server};server=cypress.csil.sfu.ca;uid=s_kwz;pwd=4YTdnH4gEGqnYJ2M')
#  ^^^ 2 values must be change for your own program.

#  Since the CSIL SQL Server has configured a default database for each user, there is no need to specify it (<username>354)

cur = conn.cursor()

# to validate the connection, there is no need to change the following line
cur.execute('SELECT username from dbo.helpdesk')
row = cur.fetchone()
while row:
    print ('SQL Server standard login name = ' + row[0])
    row = cur.fetchone()

conn.close()
