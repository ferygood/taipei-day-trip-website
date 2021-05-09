import mysql.connector
from dotenv import load_dotenv
import os
import json

load_dotenv()

taipeiDB = mysql.connector.connect(
   host = "127.0.0.1",
   port = 3306,
   user = "root",
   password = "yaomysql86",
   database = "taipei",
   charset = "utf8"
)

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
        insertValue += f"{ kwargs[key] }, "

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
      sql_cmd = """
               SELECT attractionId, date, time, price
               FROM bookings 
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
      print(insertValue)      

      sql_cmd = f"""
            INSERT INTO bookings ({ insertColumn })
            VALUES ({ insertValue })
            """

      taipeiCursor.execute(sql_cmd)

      taipeiDB.commit()

   except Exception as e:
      print(e)

def deleteBooking(**kwargs):
   try:
      deleteBookingId = kwargs["id"]

      sql_cmd = f"""
            DELETE FROM bookings 
            WHERE attractionId = {deleteBookingId}
            """

      taipeiCursor.execute(sql_cmd)

      taipeiDB.commit()
   except Exception as e:
      print(e)