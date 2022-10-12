This code grabs the CSV files in folder 'Bottom_Temperature', gets the
sensor values, pre-computes lat and lon (it is a fixed grid) and writes
all this info altogether with the year's day number (from filename)
in a database called 'bt.db', more precisely inside a table called 'BT'.

You can test it by opening main.py. 

main_write() creates the database with the behavior previously described. It
contains a call to main_erase() to start from scratch a database so it does
not contain duplicates in multiple calls to main_write() are done while
testing.

main_read() allows to query the database. There is a extremely simple example
inside this function as well as a comment indicating the value it should give as answer.

