import sys
sys.path.append("..")

from flask import request, Blueprint, jsonify
from mysql_connect import selectAttractions, selectAttraction
 
api_order = Blueprint("api_order", __name__)

@api_order.route("/orders", methods=["POST"])
def postOrders():
   pass

@api_order.route("/order/<string:number>", methods=["GET"])
def getOrder(number):
   pass

