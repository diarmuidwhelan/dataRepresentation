import mysql.connector 
mydb = mysql.connector.connect(   host="localhost",   user="root",   password="pwd" ) 
mycursor = mydb.cursor() 
mycursor.execute("CREATE DATABASE datarepresentation")
