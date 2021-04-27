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

mycursor = mydb.cursor(buffered=True)

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
	response = {"nextpage": page+1, "data":[]}

	#1. 有給 keyword
	if keyword != None:
		val1 = "%"+keyword+"%"
		sql1 = 'select count(attract_id) from main where name like "%s" ;'%(val1)
		mycursor.execute(sql1)
		count = mycursor.fetchone()[0] #知道用 keyword 篩選後有多少筆資料
		if count > 0:
			page_list = [i for i in range(0,count,12)] # 放入 start index
			print(len(page_list))
			if page+1 > len(page_list):
				response = {"error":"true", "message":"page number error"}
			else:
				page_num = page_list[page] # 知道要第幾個 12 頁
				sql2 = "select * from main where name like '%s' limit 12 offset %s;"%(val1, page_num)
				mycursor.execute(sql2)
				result = mycursor.fetchall()
				dct={}
				for n in result:
					n = list(n)
					dct["id"] = n[0]
					dct["name"] = n[1]
					dct["category"] = n[2]
					dct["description"] = n[3]
					dct["address"] = n[4]
					dct["transpot"] = n[5]
					dct["mrt"] = n[6]
					dct["latitude"] = n[7]
					dct["longitude"] = n[8]
					sql3 = 'select img from image where attract_id = %s limit 1'%(dct["id"])
					mycursor.execute(sql3)
					dct["image"] = [mycursor.fetchone()]
					response["data"].append(dct.copy())
		elif count==0:
			response = {"error":"true", "message":"keyword not found"}

	return render_template("/api/attractions.html", title="/api/attractions", jsonfile=json.dumps(response, ensure_ascii=False).encode("utf-8").decode())

@app.route("/api/attraction/<id>") 
def attractionid(id):
	response = {"data":None}
	attract_id = int(id)
	if attract_id not in range(1,320):
		response = {"error":"true", "message":"id error"}
	else:
		sql1 = "select * from main where attract_id='%s'"%(attract_id)
		mycursor.execute(sql1)
		result1 = mycursor.fetchone()
		sql2 = "select img from image where attract_id='%s' limit 1"%(attract_id)
		mycursor.execute(sql2)
		result2 = mycursor.fetchone()
		dct = {}
		dct["id"] = result1[0]
		dct["name"] = result1[1]
		dct["category"] = result1[2]
		dct["description"] = result1[3]
		dct["address"] = result1[4]
		dct["transpot"] = result1[5]
		dct["mrt"] = result1[6]
		dct["latitude"] = result1[7]
		dct["longitude"] = result1[8]
		dct["image"] = [result2]
		response["data"] = dct
	return render_template("/api/attraction.html", title="/api/attraction", jsonfile=json.dumps(response, ensure_ascii=False).encode("utf-8").decode())

app.run(port=3000)
