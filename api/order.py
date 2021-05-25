import sys
sys.path.append("..")

from flask import request, Blueprint, jsonify, session
from datetime import datetime
import json

from mysql_connect import insertOrder, selectOrder, selectUser
 
api_order = Blueprint("api_order", __name__)

@api_order.route("/orders", methods=["POST"])
def postOrders():
   # TBD
   try:
      if "user" in session:
         # Set Main Keys to Variables
         requestJson = request.get_json()
         orderJson = requestJson["order"]
         tripJson = orderJson["trip"]
         attractionJson = tripJson["attraction"]
         contactJson = orderJson["contact"]
         # Get information
         prime = requestJson["prime"]

         price = int(orderJson["price"])
         
         attractionId = int(attractionJson["id"])
         attractionName = attractionJson["name"]
         attractionAddress = attractionJson["address"]
         attractionImage = attractionJson["image"]
         attractionBoolean = attractionId and attractionName and attractionAddress and attractionImage

         date = tripJson["date"]
         time = tripJson["time"]
         tripBoolean = price and date and time

         contactName = contactJson["name"]
         contactEmail = contactJson["email"]
         contactPhone = contactJson["phone"]
         contactBoolean = contactName and contactEmail and contactPhone
         userId = int(session["user"]["id"])

         if not (prime and tripBoolean and attractionBoolean and contactBoolean and userId):
            return jsonify({ "error": True, "message": "訂單建立失敗，輸入不正確或其他原因" })

         insertOrder(attractionId = attractionId, date = date, time = time, price = price, userId = userId)

         # TBD
         data = {
            "number": "20210425121135",
            "payment": {
               "status": 0,
               "message": "付款成功"
            }
         }
         
         return jsonify({ "data": data })
      else:
         return jsonify({ "error": True, "message": "請先登入" })
   except Exception as e:
      print(e)
      return jsonify({ "error": True, "message": "伺服器內部錯誤" })

@api_order.route("/order/<string:number>", methods=["GET"])
def getOrder(number):
   pass
# TBD
   # try:
   #    if "user" in session:
   #       userId = int(session["user"]["id"])

   #       selectedBooking = selectBooking(userId = userId)

   #       date = datetime.strftime(selectedBooking["date"], "%Y-%m-%d")

   #       data = {
   #          "attraction": {
   #             "id": selectedBooking["id"],
   #             "name": selectedBooking["name"],
   #             "address": selectedBooking["address"],
   #             "image": json.loads(selectedBooking["images"])[0]
   #          },
   #          "date": date,
   #          "time": selectedBooking["time"],
   #          "price": selectedBooking["price"],
   #       }
   #       if data:
   #          return jsonify({ "data": data })
   #       else:
   #          return jsonify({ "data": None })
   # except Exception as e:
   #    print(e)
   #    return jsonify({ "error": True, "message": "伺服器內部錯誤" })

