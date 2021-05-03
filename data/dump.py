import json
import mysql.connector

with open("taipei-attractions.json") as json_file:
    data = json.load(json_file) #load json file as dictionary

df = data["result"]["results"]

# 連結 local 資料庫
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Mysqlyao86%%%",
    database="website"
)

mycursor = mydb.cursor() #啟動 cursor

"""
一個 table 包含所有的資料
"""

def imgUrl(data):
    # 將檔名jpg和png的字串篩選出來
    extension = ["jpg", "png"]
    imgList = []
    img = ""
    imgArray = data.split("http://")
    for url in imgArray:
        if any(x in url.lower() for x in extension):
            imgList.append("http://"+url)
    img = ",".join(imgList)
    return img

for res in df:
    query = "INSERT INTO main \
    (name, category, description, address, transport, mrt, latitude, longitude, images) \
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    val = (res["stitle"],res["CAT2"],res["xbody"],res["address"],res["info"],res["MRT"], 
    res["latitude"],res["longitude"], imgUrl(res["file"]))
    try:
        mycursor.execute(query, val)
        mydb.commit()
    except mysql.connector.Error as err:
        mydb.roolback() # stop mysql
        print(err)
        print("Error Code", err.errno)
        print("SQLSTATE", err.sqlstate)
        print("Message", err.msg)

mydb.close()
