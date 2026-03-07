from flask import Blueprint,render_template
view=Blueprint('view',__name__)
auth=Blueprint('auth',__name__)
@view.route('/',methods=["GET","POST"])
def home():
    return render_template("home.html")

@auth.route('/login',methods=["GET","POST"])
def login():
    # if form.method='POST'
    return render_template("login.html")

@auth.route('/register',methods=["GET","POST"])
def register():
    return render_template("register.html")