import sys
sys.path.append("..")

from flask import request, Blueprint, jsonify
from mysql_connect import selectAttractions, selectAttraction
 
api_attraction = Blueprint('api_attraction', __name__)

@api_attraction.route("/attractions", methods=["GET"])
def getAttractions():
	try:
		page = int(request.args.get("page"))
		keyword = request.args.get("keyword")
		if page == None or page < 0:
			return jsonify({ "error": True, "message": "伺服器內部錯誤" })
		
		attractionsDataList = selectAttractions(page = page, keyword = keyword)

		if attractionsDataList == None or len(attractionsDataList) < 12:
			return jsonify({ "nextPage": None, "data": attractionsDataList })
		if len(attractionsDataList) == 12:
			attractionsDataListNextPage = selectAttractions(page = (page + 1), keyword = keyword)
			if attractionsDataListNextPage == None:
				return jsonify({ "nextPage": None, "data": attractionsDataList })
				
		return jsonify({ "nextPage": page + 1, "data": attractionsDataList })
	except Exception as e:
		print(e)
		return jsonify({ "error": True, "message": "伺服器內部錯誤" })

@api_attraction.route("/attraction/<int:id>", methods=["GET"])
def getAttraction(id):
	try:
		attractionData = selectAttraction(id)

		if attractionData == None:
			return jsonify({ "error": True, "message": "景點編號不正確" })	
		else:
			return jsonify({ "data": attractionData })
	except Exception as e:
		print(e)
		return jsonify({ "error": True, "message": "伺服器內部錯誤" })