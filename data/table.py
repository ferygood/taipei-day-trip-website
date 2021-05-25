import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

websiteDB = mysql.connector.connect(
   host = os.getenv("SERVER_HOST"),
   port = os.getenv("SERVER_PORT"),
   user = os.getenv("SERVER_USER"),
   password = os.getenv("SERVER_PASSWORD"),
   database = os.getenv("SERVER_DATABASE"),
   charset = "utf8"
)

webCursor = websiteDB.cursor()

webCursor.execute("""
   CREATE TABLE IF NOT EXISTS users(
      id BIGINT NOT NULL AUTO_INCREMENT,
      name VARCHAR(255) NOT NULL, 
      email VARCHAR(255) NOT NULL, 
      password VARCHAR(255) NOT NULL, 
      PRIMARY KEY (id)) charset=utf8;
   """
)

webCursor.execute("""
   CREATE TABLE IF NOT EXISTS bookings(
      id BIGINT NOT NULL AUTO_INCREMENT, 
      attractionId INT NOT NULL, 
      userId BIGINT NOT NULL, 
      date DATE NOT NULL, 
      time VARCHAR(255) NOT NULL, 
      price INT NOT NULL, 
      PRIMARY KEY(id)) charset=utf8;
   """
)

# webCursor.execute("""
#    CREATE TABLE IF NOT EXISTS orders(
#       id BIGINT NOT NULL AUTO_INCREMENT, 
#       number VARCHAR(255) NOT NULL,
#       prime VARCHAR(255) NOT NULL,
#       price INT NOT NULL, 
#       attractionId INT NOT NULL, 
#       userId BIGINT NOT NULL, 
#       date DATE NOT NULL, 
#       time VARCHAR(255) NOT NULL, 
#       phone VARCHAR(255) NOT NULL,
#       status INT NOT NULL,
#       PRIMARY KEY(id)) charset=utf8;
#    """
# )

websiteDB.commit()