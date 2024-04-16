from flask import Flask, render_template,request,session, redirect
from pymongo import MongoClient
from dotenv import load_dotenv
import os 
#pip install pymongo
#pip install python-dotenv
app = Flask(_name_)
app.secret_key = "123456"


load_dotenv()
mongo_uri = os.environ.get("MONGO_URI")
client = MongoClient(mongo_uri)


db_name = "user"
database = client[db_name]

col_name = "login_details"
col = database[col_name]


@app.route("/hello/<name>",methods = ["GET"])
def hello(name):


 user_details = col.find({"name":name})
    # print(user_details)
 user_list = []
 for user in user_details:
   user_list.append(user)
    # print(user)
 return render_template("display.html",user_list = user_list)


@app.route("/register/page")
def login():
   return render_template("form.html")
@app.route("/register" , methods = ["POST"])
def submit():
    name = request.form.get("name")
    password = request.form.get("password")
    user_id = 1


 # session["user_id"]= str(name_of_user["user_id"])
    data = { "user_id" : user_id,"name": name , "password" : password}
    col.insert_one(data)
    # detail = col.update_many({"name": "prakash"}, {"$set" : {"password": password}})
    return "registration successful"


@app.route("/login/get" , methods = ["GET"])
def logi():
   return render_template("login.html")


@app.route("/login", methods=["POST"])
def post_login():
   name = request.form.get("name")
   password = request.form.get("password")
   name_of_user = col.find_one({"name" : name})
   if name_of_user is None:
     return "user not found"
   if password != name_of_user["password"]:
     return "password mismatch"
   session["user_id"] = name_of_user["user_id"]
   return redirect("/")


@app.route("/")
def home_page():
   if not session.get("user_id"):
     return redirect("/login/get")
   return str(session["user_id"] ) + " is user id of logined user"



@app.route("/logout")
def logout():
   session.pop("user_id")
   return "logged out"

if _name_ == "_main_":
   app.run(debug = True,port=8000)