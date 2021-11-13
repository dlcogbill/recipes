from flask_app import app # NEED this line
from flask import render_template,redirect,request,session
from flask_app.models.user import User # Import each model needed here!
from flask_app.models.recipe import Recipe
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route("/")
def index():
    if session.get('user_id') != None:
        # do something for logged in user
        return redirect("/dashboard")
    return render_template("logreg.html")

# Registering new user - ACTUALLY CREATES IT IN THE DATABASE
@app.route("/register", methods=["GET","POST"])
def registerUser():
    if request.method == "GET":
        return redirect("/")

    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": request.form["password"],
        "confirm": request.form["confirm"],
    }

    if not User.validate_user(data):
        return redirect('/')
    
    data["password"] = bcrypt.generate_password_hash(request.form["password"])
    session['user_id'] = User.create_one(data)
    
    return redirect("/dashboard")

# User logging in
@app.route("/login", methods=["GET","POST"])
def loginUser():
    if request.method == "GET":
        return redirect("/")
    data = {
        "email" : request.form["login_email"],
        "password": request.form["login_password"],
        }

    if not User.validate_login(data):
        return redirect('/')
    session['user_id'] = User.validate_login(data)
    return redirect("/dashboard") # never render on a post!!!

@app.route("/dashboard", methods=["GET","POST"])
def dashboard():
    if session.get('user_id') == None:
        return redirect("/")
    data = {
        "id" : session['user_id'],
        }
    user = User.get_one(data)
    session['name'] = user.first_name
    recipes = Recipe.get_all()
    return render_template("dashboard.html", recipes = recipes)

@app.route("/logout", methods=["GET","POST"])
def logoff():
    session.clear()
    return redirect("/")

@app.route("/recipes/<int:id>")
def show_recipe(id):
    if session.get('user_id') == None:
        return redirect("/")
    data = {
        "id" : id,
        }

    recipe = Recipe.get_one(data)

    return render_template("showrecipe.html", recipe = recipe)

@app.route("/recipes/new")
def add_recipe_page():
    if session.get('user_id') == None:
        return redirect("/")
    return render_template("newrecipe.html")

@app.route("/recipes/new", methods=["GET","POST"])
def add_recipe():
    if session.get('user_id') == None:
        return redirect("/")
    if request.method == "GET":
        return redirect("/")

    data = {
        "name": request.form["name"],
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "madeon": request.form["madeon"],
        "under30": request.form["under30"],
        "user_id": session["user_id"],
    }

    if not Recipe.validate_recipe(data):
        return redirect('/recipes/new')

    Recipe.create_one(data)

    return redirect("/dashboard")

@app.route("/recipes/edit/<int:id>")
def edit_recipe_page(id):
    if session.get('user_id') == None:
        return redirect("/")
    data = {
        "id": id,
    }
    
    recipe = Recipe.get_one(data)
    
    return render_template("editrecipe.html", recipe = recipe)


@app.route("/recipes/edit/<int:id>", methods=["GET","POST"])
def edit_recipe(id):
    if session.get('user_id') == None:
        return redirect("/")
    if request.method == "GET":
        return redirect("/")
    data = {
        "id": id,
        "name": request.form["name"],
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "madeon": request.form["madeon"],
        "under30": request.form["under30"],
        "user_id": session["user_id"],
    }

    if not Recipe.validate_recipe(data):
        return render_template("editrecipe.html", recipe = data)
    
    Recipe.edit_one(data) 
    return redirect("/dashboard")


@app.route("/recipes/delete/<int:id>", methods=["GET","POST"])
def delete_pastry(id):
    if session.get('user_id') == None:
        return redirect("/")
    data = {
        "id": id
    }
    Recipe.delete_one(data)
    return redirect("/dashboard")