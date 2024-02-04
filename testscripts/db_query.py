import psycopg2
db_name='dvdrental'
db_host='ndf-db-postgress1.fyre.ibm.com'
db_user='postgres'
db_pass='dbpassw0rd'
db_port=5432
conn = psycopg2.connect(database=db_name,
                        host=db_host,
                        user=db_user,
                        password=db_pass,
                        port=db_port)
# As you can see, there are quite a few arguments you need to define in order to connect to the database. Here's a quick summary of what each of these arguments means:

# database: the name of the database that you want to connect to (you can only connect to one database with one connection object)
# host: this is probably an IP address or a URL that points to the database server (e.g., xyz.example.com)
# user: the name of the PostgreSQL user
# password: the matching password for that user
# port: the port that the PostgreSQL server uses (usually 5432 if the server is hosted locally but can be other)
# If you submitted the correct database credentials, you get a live database connection object that you can use to create a cursor object.

# A cursor object will help you execute any queries on the database and retrieve data. Here's how to create a cursor object:

cursor = conn.cursor()
# Now let's query the database using the cursor we just created:

# cursor.execute("SELECT count(*) FROM actor")
cursor.execute("SELECT * FROM actor")
# We use the execute() function and submit a query string as its argument. This query that we submitted will be run against the database. It's important to note that after the query executes, you still need to use one of the Psycopg2 functions to retrieve data rows:

# fetchone()
# fetchall()
# fetchmany()
# Let's see how each of them works!

# Example: fetchone()
# The most basic way to fetch data from your database is to use the fetchone() function. This function will return exactly one row — the first row — after executing the SQL query.

# Here's an example:
# row=cursor.fetchone()
# print(row)
# print(row[0])
# print(row[1])
# print(row[2])
# print(row[3])

# theRest=cursor.fetchall()
# print(theRest)
# print(theRest[0][1])
# print(theRest[1][1])
# print(theRest[2][2])
# print(theRest[3][2])

for actor in cursor.fetchall():
    print(actor)
    print (f'{actor[1]} {actor[2]}')

# (1, 'Budapest', 'newly-built', 'after 2011', 30, 1)
# In this example, fetchone() returns one row from the database in the form of a tuple where the order of your data in the tuple will be based on the order of the columns you specified in the query.

# Because of this, it's important to make sure you specify the order of columns properly when you create the query string so you know which data is which in the tuple.

# Example: fetchall()
# What if you need more than just one row from your database? What if you need 10, 100, 1000, or more rows? You can use the fetchall() Psycopg2 function, which works the same way as fetchone() except that it returns not just one row as a result but all of them.

# print(cursor.fetchall())
# print(cursor.fetchone())

# [(1, 'Budapest', 'newly-built', 'after 2011', 30, 1),
#  (2, 'Budapest', 'newly-built', 'after 2011', 45, 2),
#  (3, 'Budapest', 'newly-built', 'after 2011', 32, 2),
#  (4, 'Budapest', 'newly-built', 'after 2011', 48, 2),
#  (5, 'Budapest', 'newly-built', 'after 2011', 49, 2),
#  (6, 'Budapest', 'newly-built', 'after 2011', 49, 2),
#  (7, 'Budapest', 'newly-built', 'after 2011', 71, 3),
#  (8, 'Budapest', 'newly-built', 'after 2011', 50, 2),
#  (9, 'Budapest', 'newly-built', 'after 2011', 50, 2),
#  (10, 'Budapest', 'newly-built', 'after 2011', 57, 3)]
# [...]
# Notice how we get more rows back, not just one.

# Example: fetchmany()
# With fetchmany(), you have another option to retrieve multiple records from the database and have more control over the exact amount of rows retrieved.

# print(cursor.fetchmany(size=5))
# [(1, 'Budapest', 'newly-built', 'after 2011', 30, 1),
#  (2, 'Budapest', 'newly-built', 'after 2011', 45, 2),
#  (3, 'Budapest', 'newly-built', 'after 2011', 32, 2),
#  (4, 'Budapest', 'newly-built', 'after 2011', 48, 2),
#  (5, 'Budapest', 'newly-built', 'after 2011', 49, 2)]
# Here we only receive five rows because we set the size argument to 5. This function gives you more control on a code-level over how many rows to return from your database table.

# Wrapping Up
# After you're finished querying your database and using the connection object in your Python code, make sure to always close the connection using conn.close().

conn.close()