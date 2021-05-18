import sys
sys.path.append("..")

from flask import request, Blueprint, jsonify, session

from mysql_connect import selectUser, insertUser
 
api_user = Blueprint("api_user", __name__)

@api_user.route("/user", methods=["GET"])
def getUser():
   if "user" in session:
      data = {
         "id": session["user"]["id"],
         "name": session["user"]["name"],
         "email": session["user"]["email"]
      }
      return jsonify({ "data": data })
   else:
      return jsonify({ "data": None })

@api_user.route("/user", methods=["POST"])
def postUser():
   try:
      name = request.get_json()["name"]
      email = request.get_json()["email"]
      password = request.get_json()["password"]

      if not (name and email and password):
         return jsonify({ "error": True, "message": "註冊失敗，姓名、帳號和密碼皆不得為空" })

      userVerified = selectUser(email = email)
      if userVerified:
         return jsonify({ "error": True, "message": "註冊失敗，重複的 Email 或其他原因" })

      insertUser(name = name, email = email, password = password)
      updatedUser = selectUser(email = email, password = password)
      if updatedUser:
         return jsonify({ "ok": True })
      else:
         return jsonify({ "error": True, "message": "註冊失敗，重複的 Email 或其他原因" })
   except Exception as e:
      print(e)
      return jsonify({ "error": True, "message": "伺服器內部錯誤" })

@api_user.route("/user", methods=["PATCH"])
def patchUser():
   try:
      email = request.get_json()["email"]
      password = request.get_json()["password"]

      if not (email and password):
         return jsonify({ "error": True, "message": "登入失敗，帳號、密碼皆不得為空" })

      user = selectUser(email = email, password = password)

      if user:
         session["user"] = {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"]
         }
         return jsonify({ "ok": True })
      else:
         return jsonify({ "error": True, "message": "登入失敗，帳號或密碼錯誤或其他原因" })
   except Exception as e:
      print(e)
      return jsonify({ "error": True, "message": "伺服器內部錯誤" })

@api_user.route("/user", methods=["DELETE"])
def deleteUser():
   try:
      session.clear()
      if "user" not in session:
         return jsonify({ "ok": True })
      else: 
         return jsonify({ "error": True, "message": "登出失敗" })
   except Exception as e:
      print(e)
      return jsonify({ "error": True, "message": "伺服器內部錯誤" })