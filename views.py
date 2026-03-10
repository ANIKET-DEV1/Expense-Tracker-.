from flask import Blueprint,render_template, request,session,redirect,url_for
from .new import Helper
from datetime import datetime,date
from werkzeug.security import check_password_hash
from .verify import operation
view=Blueprint('view',__name__)
auth=Blueprint('auth',__name__)
helper = Helper()
opera=operation()
@view.route('/',methods=["GET","POST"])
def home():
    return render_template("home.html")

@auth.route('/login',methods=["GET","POST"])
def login():
    error=None
    if request.method=="POST":
        username=request.form.get("username")
        password=request.form.get("password")

        user_id=helper.Auth(username,password)
        if user_id:
            session["user_id"]=user_id
            session["username"]=username
            return redirect(url_for("view.home"))
        else:
            error="Invalid username or password"
    return render_template("login.html", error=error)

@auth.route('/register',methods=["GET","POST"])
def register():
    error=None
    if request.method=="POST":
        username=request.form.get("username")
        email=request.form.get("email")
        password=request.form.get("password")
        comfirmpassword=request.form.get("Cpassword")
        
        if password != comfirmpassword:
            error="Passwords doesn't match"
            return render_template("register.html",error=error)
        result=helper.insert_user(username,email,password)
        if result==2:
           error="Username or email already exists"
        elif result==False:
            error="Registration failed. Please try again."
        else:
            return redirect(url_for("auth.login"))
    return render_template("register.html",error=error)

@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("auth.login"))

@view.route('/Add-Expense',methods=["GET","POST"])
def add_expenses():
    if "user_id" in session:
        raw=helper.Category_exist(session["user_id"])
        categories=[c[0] for c in raw]
        if request.method=="POST":
            amount=request.form.get("amount").strip()
            description=request.form.get("description")
            category=request.form.get("category").capitalize().strip()
            date=request.form.get("expenseDate")
            result = opera.verify_expense_deatils(session["user_id"], description, amount, date, category)
            error_msg = None
            if result == 2:
                error_msg = "Invalid amount. Please enter a positive number."
            elif result == 3:
                error_msg = "Description cannot be empty."
            elif result == 4:
                error_msg = "Invalid date. Please enter a valid date in the format YYYY-MM-DD."
            elif result == 5:
                error_msg = "Database error. Please try again later."
            elif result == 6:
                error_msg = "Category does not exist. Please select a valid category."
            else:
                    return redirect(url_for("view.home"))
            if error_msg:
                return render_template("add_expense.html", categories=categories, error=error_msg)
        return render_template("add_expense.html", categories=categories)
        

