import mysql.connector
from dotenv import load_dotenv
import os
import json

load_dotenv()

def init_db():
   return mysql.connector.connect(
      host = os.getenv("SERVER_HOST"),
      port = os.getenv("SERVER_PORT"),
      user = os.getenv("SERVER_USER"),
      password = os.getenv("SERVER_PASSWORD"),
      database = os.getenv("SERVER_DATABASE"),
      charset = "utf8")

taipeiDB = init_db()

# try:
#    taipeiDB.ping(True)
# except mysql.connector.Error as err:
#    print(err)
#    taipeiDB.reconnect()

taipeiCursor = taipeiDB.cursor()

# ====================
# for /api/attraction
def selectAttractions(**kwargs):
   attractionsDataList = []
   try:
      pageStart = kwargs["page"] * 12
      pageInterval = 12 

      sql_cmd = """
               SELECT * 
               FROM attractions 
               LIMIT %s, %s
               """
      value = (pageStart, pageInterval)

      if kwargs["keyword"]:
         sql_cmd = """
               SELECT * 
               FROM attractions 
               WHERE name REGEXP %s
               LIMIT %s, %s
               """
         value = (kwargs["keyword"], pageStart, pageInterval)

      taipeiCursor.execute(sql_cmd, value)

      taipeiResults = taipeiCursor.fetchall()
      if taipeiResults:
         for taipeiResult in taipeiResults:
            attractionsData = dict(zip(taipeiCursor.column_names, taipeiResult))
            attractionsData["images"] = json.loads(attractionsData["images"])
            attractionsDataList.append(attractionsData)
         return attractionsDataList
      else:
         return None
   except Exception as e:
      print(e)
      return None

def selectAttraction(attractionId):
   try:
      sql_cmd = f"""
               SELECT *
               FROM attractions
               WHERE id = { attractionId }
               """

      taipeiCursor.execute(sql_cmd)

      taipeiResult = taipeiCursor.fetchone()

      if taipeiResult:
         attractionData = dict(zip(taipeiCursor.column_names, taipeiResult))
         attractionData["images"] = json.loads(attractionData["images"])
         return attractionData
      else:
         return None
   except Exception as e:
      print(e)
      return None
# ====================
# for /api/user
def selectUser(**kwargs):
   try:
      sql_cmd = """
               SELECT *
               FROM users
               WHERE
               """

      for key in kwargs:
        sql_cmd += f"{ key } = '{ kwargs[key] }' and "
      
      sql_cmd = sql_cmd[:-5] # 扣除掉 " and "

      taipeiCursor.execute(sql_cmd)

      taipeiResult = taipeiCursor.fetchone()

      if taipeiResult:
         userData = dict(zip(taipeiCursor.column_names, taipeiResult))
         return userData
      else:
         return None
   except Exception as e:
      print(e)
      return None

def insertUser(**kwargs):
   try:
      insertColumn = ''
      insertValue = ''

      for key in kwargs:
        insertColumn += f"{ key }, "
        insertValue += f"'{ kwargs[key] }', "

      insertColumn = insertColumn[:-2]
      insertValue = insertValue[:-2]
      
      sql_cmd = f"""
            INSERT INTO users ({ insertColumn })
            VALUES ({ insertValue })
            """

      taipeiCursor.execute(sql_cmd)

      taipeiDB.commit()

   except Exception as e:
      print(e)
# ====================
# for /api/booking
def selectBooking(**kwargs):
   # bookingsDataList = []
   try:
      sql_cmd = f"""
               SELECT a.id, a.name, a.address, a.images, b.date, b.time, b.price  
               FROM bookings b 
               JOIN attractions a ON b.attractionId = a.id 
               WHERE b.userId = {kwargs["userId"]}
               ORDER BY b.id DESC
               LIMIT 0, 1
               """

      taipeiCursor.execute(sql_cmd)

      taipeiResult = taipeiCursor.fetchone()
      if taipeiResult:
         bookingData = dict(zip(taipeiCursor.column_names, taipeiResult))
         return bookingData
      else:
         return None
   except Exception as e:
      print(e)
      return None

def insertBooking(**kwargs):
   try:
      insertColumn = ''
      insertValue = ''

      for key in kwargs:
         insertColumn += f"{ key }, "
         if type(kwargs[key]) == str:
            insertValue += f"'{ kwargs[key] }', "
         else: 
            insertValue += f"{ kwargs[key] }, "

      insertColumn = insertColumn[:-2]
      insertValue = insertValue[:-2]

      sql_cmd = f"""
            INSERT INTO bookings ({ insertColumn })
            VALUES ({ insertValue })
            """

      taipeiCursor.execute(sql_cmd)

      taipeiDB.commit()

   except Exception as e:
      print(e)

def deleteBookingData(**kwargs):
   try:
      deleteBookingId = kwargs["id"]

      sql_cmd = f"""
            DELETE FROM bookings 
            WHERE id = {deleteBookingId}
            """

      taipeiCursor.execute(sql_cmd)

      taipeiDB.commit()
   except Exception as e:
      print(e)