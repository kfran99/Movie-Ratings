from flask import Flask, render_template, redirect, request, flash, session
import model

app = Flask(__name__)
app.secret_key = 'some_secret'

@app.route("/")
def index():
    user_list = model.session.query(model.User).limit(5).all()
    print user_list
    return render_template("user_list.html", users=user_list)

@app.route("/user/login", methods=['GET'])
def user_login_form():
    return render_template("login_user.html")

@app.route("/user/login", methods=['POST'])
def user_login():
     # Get login data for user from login-user form
    username = request.form.get("username")
    password = request.form.get("password")

    user_list = model.session.query(model.User).filter_by(email=username, password=password).all()
    if len(user_list) == 0:
        flash("User does not exist.")
        return render_template("login_user.html")
    else:
        #Note we are ignoring the case in which there are multiple users with the credentials
        flash("User authenticated.")
        session['username'] = username

        print session, session['username']
        id = user_list[0].id
        ratings = model.session.query(model.Rating).filter_by(user_id=id)    
    return render_template("view_user.html", user=user_list[0],ratings=ratings)    
    
@app.route("/search/movie", methods=['POST'])
def movie_search():
    name = request.form.get("name")
    print name
    movies = model.session.query(model.Movie).filter_by(name=name).all()
    for m in movies:
         print movies[m].name
    return "blah blah blah"

@app.route("/search/movie", methods=['GET'])
def movie_search_form():
    return render_template("movie_search.html")

# Display a single user record
@app.route("/user/<id>", methods=['GET'])
def view_user(id):
    # Display the user record and update form
    user = model.session.query(model.User).get(id)
    ratings = model.session.query(model.Rating).filter_by(user_id=id)    
    return render_template("view_user.html", user=user, ratings=ratings)

# Create a new user
@app.route("/user/new", methods=['GET'])
def new_user_form():
    # Display an HTML form to create a new user
    return render_template("new_user_form.html")

@app.route("/user/new", methods=['POST'])
def new_user():
    # Get data for user from request.form
    username = request.form.get("username")
    password = request.form.get("password")
    age = request.form.get("age")
    zipcode = request.form.get("zipcode")
    # Create the user object
    user = model.User(email=username, password=password, age=age, zipcode=zipcode)
    # commit to database
    model.session.add(user)
    model.session.commit()
    return render_template("new_user_form.html")

    
# Update an existing user
@app.route("/user/<id>", methods=['POST'])
def update_user(id):
    # Query for the user from the database

    # Check that you actually got data from the database!?

    # Get data from request.form

    # Update the user object

    # Save (hint: commit) the user to the database 

    # redirect user to movie trailers on youtube for cute cat videos
    # (flash message to the user that their update worked)
    pass












    __tablename__ = "users"
    id = Column(Integer, primary_key = True)
    email = Column(String(64), nullable=True)
    password = Column(String(64), nullable=True)
    age = Column(Integer, nullable=True)
    zipcode = Column(String(15), nullable=True)    

    

if __name__ == "__main__":
    app.run(debug = True)