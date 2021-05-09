import sys
sys.path.append("..")

from flask import request, Blueprint, jsonify, session

from mysql_connect import selectUser, insertUser
 
api_user = Blueprint("api_user", __name__)

@api_user.route("/user", methods=["GET"])
def getUser():
   try:
      if "email" in session:
         name = session["name"]
         email = session["email"]
      # name = "Andy"
      # email = "Andy@gmail.com"
         user = selectUser(name = name, email = email)
         if user:
            data = {
               "id": user["id"],
               "name": user["name"],
               "email": user["email"]
            }
            return jsonify({ "data": data })
         else:
            return jsonify({ "data": None })
   except Exception as e:
      print(e)
      return jsonify({ "error": True, "message": e })

      
@api_user.route("/user", methods=["POST"])
def postUser():
   try:
      name = request.form["name"]
      email = request.form["email"]
      password = request.form["password"]

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
      email = request.form["email"]
      password = request.form["password"]

      if not (email and password):
         return jsonify({ "error": True, "message": "登入失敗，帳號、密碼皆不得為空" })

      user = selectUser(email = email, password = password)
      if user:
         session["name"] = user["name"]
         session["email"] = user["email"]
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
      return jsonify({ "ok": True })
   except Exception as e:
      print(e)
      return jsonify({ "error": True, "message": "伺服器內部錯誤" })