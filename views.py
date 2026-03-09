from flask import Blueprint,render_template, request,session,redirect,url_for
from new import Helper
from werkzeug.security import check_password_hash
view=Blueprint('view',__name__)
auth=Blueprint('auth',__name__)
helper = Helper()
@view.route('/',methods=["GET","POST"])
def home():
    return render_template("home.html")

@auth.route('/login',methods=["GET","POST"])
def login():
    if request.method=="POST":
        username=request.form.get("username")
        password=request.form.get("password")

        user_id=helper.Auth(username,password)
        if user_id:
            session["user_id"]=user_id
            session["username"]=username
            return redirect(url_for("view.home"))
        else:
            return render_template("login.html",error="Invalid username or password")
    return render_template("login.html")

@auth.route('/register',methods=["GET","POST"])
def register():
    if request.method=="POST":
        username=request.form.get("username")
        email=request.form.get("email")
        password=request.form.get("password")
        result=helper.insert_user(username,email,password)
        if result==2:
            return render_template("register.html",error="Username or email already exists")
        elif result==False:
            return render_template("register.html",error="Registration failed. Please try again.")
        else:
            return redirect(url_for("auth.login"))
    return render_template("register.html")

@view.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("view.login"))
# @view.route('/Add-Expense',methods=["GET","POST"])

