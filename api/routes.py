from flask import *
import mysql.connector
import os

mydb = ""
if os.getenv("SERVER_HOST"):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Mysqlyao86%%%",
        database="website"
    )
else:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="yaomysql86",
        database="website"
    )

cursor = mydb.cursor(buffered=True)

#將api獨立寫然後用 blueprint 做連結

api = Blueprint("api", __name__, url_prefix="/api")

@api.route("/attraction/<attractionid>", methods=["GET"])
def getAttraction(attractionid):
    # 讓用戶可以用景點 id 做搜尋
    try:
        query = "SELECT * FROM main WHERE id = %s;"
        cursor.execute(query, (attractionid,))

        #如果有資料
        if cursor.rowcount > 0:
            result = cursor.fetchone()

            response = {
                "data":{
                    "id":result[0],
                    "name":result[1],
                    "category":result[2],
                    "description":result[3],
                    "address":result[4],
                    "transport":result[5],
                    "mrt":result[6],
                    "latitude":float(result[7]),
                    "longitude":float(result[8]),
                    "images": result[9].split(',') #load 全部照片但是要去掉不是 jpg 開頭
                }
            }
            return jsonify(response), 200
        else:
            response = {
                "error": True,
                "message": "景點編號不存在"
            }
            return jsonify(response), 400
    
    except mysql.connector.Error as err:
        print("Error Code:", err.errno)
        print("Message", err.msg)
        response = {
            "error":True,
            "message":"伺服器內部錯誤"
        }
        return jsonify(response), 500

@api.route("/attractions", methods=["GET"])
def getAttractions():
    #讓使用者可以用頁碼和關鍵字做搜尋
    pageNum = 0
    nextPageNum = 0

    #檢查有無輸入頁碼和關鍵字
    if "page" in request.args:
        page = request.args.get('page')
        pageNum = int(page)*12 #一頁12筆資料
    if "keyword" in request.args:
        keyword = request.args.get('keyword')
    else:
        keyword = None #沒有關鍵字就照順序顯示
    
    try:
        if keyword:
            query = """
                SELECT * FROM
                (SELECT t.*, (@row_number:=@row_number + 1) AS num
                FROM main t
                JOIN ( SELECT @row_number := 0) r
                WHERE name Like %s) temp
                WHERE num > %s LIMIT 13;"""
            cursor.execute(query, ("%"+keyword+"%", pageNum,),)
        else:
            query = "SELECT * FROM main WHERE id > %s LIMIT 13;"
            cursor.execute(query, (pageNum,))
    
        #檢查有無正確 query 到資料
        if cursor.rowcount > 0:
            results = cursor.fetchall()

            #如果回傳資料超過12筆 （設計上一頁最多顯示 12筆)
            if cursor.rowcount > 12:
                nextPageNum = int(pageNum/12 + 1)
            else:
                nextPageNum = None
            
            #response
            i = 0
            df = []
            for row in results:
                    if i < 12 :
                        responseTemp = { 'id': int(row[0]) ,
                            "name": row[1] ,
                            "category": row[2] ,
                            "description": row[3] ,
                            "address": row[4] ,
                            "transport": row[5] ,
                            "mrt": row[6] ,
                            "latitude": float(row[7]) ,
                            "longitude": float(row[8]) ,
                            "images": row[9].split(',')
                        }
                        df.append(responseTemp)
                    i += 1
            response = {
                "nextPage":nextPageNum,
                "data":df
            }
            return jsonify(response), 200

        else:
            response = {
                "nextPage":None,
                "data":[]
            }
            return jsonify(response), 400

    except mysql.connector.Error as err:
        print("Error Code:", err.errno)
        print("Message", err.msg)
        response = {
            "error":True,
            "message":"伺服器內部錯誤"
        }
        return jsonify(response), 500
