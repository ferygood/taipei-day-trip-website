from flask import *
from api.routes import api
import os

app=Flask(
	__name__,
	static_folder="static",
	static_url_path="/static"
	)

app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config["JSON_SORT_KEYS"]=False #讓 jsonify 不要按照字母順序，要按照自己設計順序

# Pages
@app.route("/")
def index():
	return render_template("index.html")

@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")

@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")

app.register_blueprint(api)

# 條件式可同時在本地端和 EC2 上做測試
if os.getenv("HOME")=="/home/ec2-user":
	app.run(port=3000, host="0.0.0.0")
else:
	app.run(port=3000)
