import pymysql.cursors
import csv
# Connect to the database
connection = pymysql.connect(host='172.18.0.1',
                             user='hd',
                             password='Qwerty@123',
                             database='anime',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

# connection = pymysql.connect(host='192.168.56.102',
#                              user='hadoop2',
#                              password='Qwerty@123',
#                              database='anime',
#                              charset='utf8mb4',
#                              cursorclass=pymysql.cursors.DictCursor)
 
def insert(Name, Type, Episode, Rating, Average, Review):
    
    with connection.cursor() as cursor:
        # Create a new record
        sql = "INSERT INTO `ADBdetails` (`Name`, `Type`, `Episode`, `Rating`, `Average`, `Review`) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (Name, Type, Episode, Rating, Average, Review))
    connection.commit()

from hdfs import InsecureClient

client = InsecureClient('http://localhost:9870', user='aj')

with client.read('/user/aj/ADB.csv', encoding='utf-8') as reader:
# with open('data/ADB.csv',encoding='utf-8') as reader:
  
  
  csvFile = csv.reader(reader)
 
  next(csvFile)
 
  Name = ''
  Type = ''
  Episode = 0
  Rating  = 0
  Average = 0
  Review =0
  Airdate = 0
  Enddate = 0

 
 
 
  for lines in csvFile:
       
        Name = lines[0]
        if lines[1] != '-':
            Type = str(lines[1])
        else:
            Type = None
 
        try:
            Episode = int(lines[2])
        except:
            Episode= None
 
        try:
            Rating = float(lines[3].split("(")[0])
        except:
            Rating = None
       
        try:
            Average = float(lines[4].split("(")[0])
        except:
            Average = None
       
        try:
            Review = float(lines[5].split("(")[0])
        except:
            Review = None


        insert(Name,Type,Episode,Rating,Average,Review)