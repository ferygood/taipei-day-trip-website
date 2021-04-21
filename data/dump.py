import json
import mysql.connector

with open("taipei-attractions.json") as json_file:
    data = json.load(json_file) #load json file as dictionary

df = data["result"]["results"]

# 連結 local 資料庫
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="yaomysql86",
    database="taipei_travel"
)

mycursor = mydb.cursor() #啟動 cursor

"""
有兩個 table: main_table (id, name, address)
             image_table (id, img_url)
"""

for n in range(0, len(df)):
    spot_id = df[n]["_id"]
    spot_name = df[n]["stitle"]
    spot_address = df[n]["address"]
    spot_img = df[n]["file"]
    #因為景點網址的開頭都是 http 所以我們用 http:// 分
    urls = spot_img.split("http://")[1:]
    http_urls = ["http://"+url for url in urls] #把 http 補回去
    
    #將資料放到資料庫內
    sql1 = "insert into main_table (id, name, address) values (%s, %s, %s)"
    val1 = (spot_id, spot_name, spot_address)
    mycursor.execute(sql1, val1)

    sql2 = "insert into image_table (id, img) values (%s, %s)"
    for url in http_urls:
        val2 = (spot_id, url)
        mycursor.execute(sql2, val2)
    mydb.commit()



#mycursor.execute("show tables;")
#result = mycursor.fetchall()


