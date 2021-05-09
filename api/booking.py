import sys
sys.path.append("..")

from flask import request, Blueprint, jsonify, session, redirect, url_for
from datetime import datetime

from mysql_connect import selectBooking, insertBooking, deleteBooking, selectAttraction
 
api_booking = Blueprint("api_booking", __name__)

@api_booking.route("/booking", methods=["GET"])
def getBooking():
   try:
   # if "email" in session:
      selectedBooking = selectBooking()

      attractionId = selectedBooking["attractionId"]
      attractionData = selectAttraction(attractionId)

      attractionDataRequired = {
         "id": attractionData["id"],
         "name": attractionData["name"],
         "address": attractionData["address"],
         "image": attractionData["images"][0]
      }

      date = datetime.strftime(selectedBooking["date"], "%Y-%m-%d")

      data = {
         "attraction": attractionDataRequired,
         "date": date,
         "time": selectedBooking["time"],
         "price": selectedBooking["price"],
      }
      if data:
         return jsonify({ "data": data })
      else:
         return jsonify({ "data": None })
   except Exception as e:
      print(e)
      return jsonify({ "error": True, "message": "伺服器內部錯誤" })
      
@api_booking.route("/booking", methods=["POST"])
def postBooking():
   try:
      # if "email" in session:
      attractionId = int(request.form["id"])
      date = request.form["date"]
      time = request.form["halfDay"]
      price = int(request.form["price"])

      if not (attractionId and date and time and price):
         return jsonify({ "error": True, "message": "建立失敗，輸入不正確或其他原因" })

      insertBooking(attractionId = attractionId, date = date, time = time, price = price)
      
      return jsonify({ "ok": True })
   except Exception as e:
      print(e)
      return jsonify({ "error": True, "message": "伺服器內部錯誤" })

@api_booking.route("/booking", methods=["DELETE"])
def deleteBooking():
   try:
   # if "email" in session:
      id = 1
      deleteBooking(id = id)

      deletedBooking = selectBooking(id = id)
      if not deletedBooking:
         return jsonify({ "ok": True })
      else:
         return jsonify({ "error": True, "message": "刪除失敗" })
   except Exception as e:
      print(e)
      return jsonify({ "error": True, "message": "伺服器內部錯誤" })

