from flask import *
import mysql.connector
import json
import pandas as pd
import numpy as np


app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True

mydb = mysql.connector.connect(
	host="localhost",
	user="root",
	password="yaomysql86",
	database="taipei_travel"
)

mycursor = mydb.cursor()

# Pages
@app.route("/")
def index():
	return render_template("index.html")

@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")

@app.route("/api/attractions", methods=["GET"])
def attractions():
	page = request.args.get("page","")
	page = int(page) #輸入是字串，所以要換成數字
	keyword = request.args.get("keyword","")
	
	sql1 = "select * from main_table"
	mycursor.execute(sql1)
	result1 = mycursor.fetchall()
	df_main = pd.DataFrame(result1, columns=["id", "name", "category",
	"description", "address", "transport", "mrt", "latitude","longitude"])
	df_main["image"] = np.nan
	df_main.index += 1
	df_main = df_main.to_dict("index")

	sql2 = "select * from image_table"
	mycursor.execute(sql2)
	result2 = mycursor.fetchall()
	df_image = pd.DataFrame(result2, columns=["id", "image"])
	df_image = df_image.groupby("id").first()
	df_image = df_image.to_dict("index")

	def json_content(page, keyword=None):
		response = {"nextPage":page+1, "data":[]}
		end=0
		if page in range(0,27):
			if page==26:
				end=319
			else:
				end=12*page+12
			for i in range(12*page, end):
				if df_main[i+1]["category"] == keyword or df_main[i+1]["name"] == keyword:
					df_main[i+1]["image"] = [df_image[i+1]["image"]]
					response["data"].append(df_main[i+1])
				elif keyword=="":
					df_main[i+1]["image"] = [df_image[i+1]["image"]]
					response["data"].append(df_main[i+1])
		else:
			response = {"error": "true", "message":"page number error"}

		return response
		
	response_file = json_content(page, keyword)
	
	# 檢查 keyword 有沒有錯，有錯 data 的 value 是 empty list
	if response_file["data"] == []:
		response_file = {"error": "true", "message":"keyword error"}

	return render_template("/api/attractions.html", title="/api/attractions", jsonfile=json.dumps(response_file, ensure_ascii=False).encode("utf-8").decode())

@app.route("/api/attraction/<id>") 
def attractionid(id):
    
	aid = int(id)	
	sql1 = "select * from main_table"
	mycursor.execute(sql1)
	result1 = mycursor.fetchall()
	df_main = pd.DataFrame(result1, columns=["id", "name", "category",
	"description", "address", "transport", "mrt", "latitude","longitude"])
	df_main["image"] = np.nan
	df_main.index += 1
	df_main = df_main.to_dict("index")

	sql2 = "select * from image_table"
	mycursor.execute(sql2)
	result2 = mycursor.fetchall()
	df_image = pd.DataFrame(result2, columns=["id", "image"])
	df_image = df_image.groupby("id").first()
	df_image = df_image.to_dict("index")
	
	response = {"data":None}
	if aid in range(1,320):
		df_main[aid]["image"] = [df_image[aid]["image"]]
		response["data"] = df_main[aid]
	elif aid not in range(1,320):
		response = {"error":"true", "message":"id error"}
	
	return render_template("/api/attraction.html", title="/api/attraction", jsonfile=json.dumps(response, ensure_ascii=False).encode("utf-8").decode())


app.run(port=3000)
