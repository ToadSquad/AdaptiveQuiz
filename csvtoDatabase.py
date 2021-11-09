import mysql.connector
import csv, random, re, os
from itertools import islice
import threading, time, json, sys


conn = mysql.connector.connect(user='root', password='root',
                              host='127.0.0.1',
                              database='mysql')
mycursor = conn.cursor()

fileName = input("FileLoc: ")
database = input("Database: ")


skipFirst = True
with open(fileName) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        if(skipFirst):
            skipFirst = False
            continue
            
        print(row)
        stringValue = 'INSERT INTO '+database+' VALUES ('
        for item in row:
            stringValue += '"'+item+'",'
        stringValue += ");"
        stringValue = stringValue.replace(",);",");")   
        print(stringValue)
        mycursor.execute(stringValue)
        conn.commit()
    

           