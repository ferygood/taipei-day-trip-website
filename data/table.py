import mysql.connector
from dotenv import load_dotenv
import os
import json

load_dotenv()

websiteDB = mysql.connector.connect(
   user = "root",
   password = "Mysql86%%%",
   database = "taipei",
   charset = "utf8"
)

webCursor = websiteDB.cursor()

webCursor.execute("""
   CREATE TABLE IF NOT EXISTS users(
      id BIGINT NOT NULL AUTO_INCREMENT, name VARCHAR(255) NOT NULL, email VARCHAR(255) NOT NULL, password VARCHAR(255) NOT NULL, 
      PRIMARY KEY (id)) charset=utf8;
   """
)

webCursor.execute("""
   CREATE TABLE IF NOT EXISTS bookings(
      id BIGINT NOT NULL AUTO_INCREMENT, attractionId INT NOT NULL, userId BIGINT NOT NULL, date DATE NOT NULL, time VARCHAR(255) NOT NULL, price INT NOT NULL, PRIMARY KEY(id)) charset=utf8;
   """
)

websiteDB.commit()