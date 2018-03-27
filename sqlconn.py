import pymssql


conn = pymssql.connect(host='leto.csil.sfu.ca', user='s_kwz', password='cdn289289', database='kwz354')

cur = conn.cursor()

# to validate the connection, there is no need to change the following line
cur.execute('SELECT username from dbo.helpdesk')
row = cur.fetchone()
while row:

    print (("SQL Server standard login name= %s") %  (row[0]))
    # from Python version 3: print is a function, not a statement.
    row = cur.fetchone()

conn.close()