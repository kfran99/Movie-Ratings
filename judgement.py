from flask import Flask, render_template, redirect, request, flash, session
import model
import hashlib

app = Flask(__name__)
#Passed through the session with the user so that we know it is the same user
app.secret_key = 'some_secret'
salt = " 10 Pink Unicorns = the best"

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
    global salt
     # Get login data for user from login-user form
    username = request.form.get("username")
    password = hashlib.sha1(request.form.get("password")+salt).hexdigest()

    user_list = model.session.query(model.User).filter_by(email=username, password=password).all()
    if user_list:
        session['username'] = username
        flash("User, " + session["username"] + ", authenticated.")
        id = user_list[0].id
        ratings = model.session.query(model.Rating).filter_by(user_id=id)
        return render_template("view_user.html", user=user_list[0],ratings=ratings)
    #login error
    else:
        flash("User not authenticated.")
        return render_template("login_user.html")              


@app.route("/search/movie", methods=['POST'])
def movie_search():
    #create variable to filter in like
    name = request.form.get("name")
    #query for the movie typed in the form
    movies = model.session.query(model.Movie).filter(model.Movie.name.like("%"+name+"%")).all()
    #set up a dictionary to show ratings for each movie - this will pass into the template
    ratings_dict = {}
    #get ratings for the movies
    for movie in movies:
        if movie.id not in ratings_dict:
            ratings_dict[movie.id] = []
        #gets the ratings for each movie returned
        ratings = model.session.query(model.Rating).filter_by(movie_id = movie.id).all()
        for rating in ratings:
            #ratings_dict[movie.id].append(rating.rating)
            ratings_dict[movie.id].append({"user_id": rating.user_id, "rating": rating.rating })
    if not movies:
        flash("No movies were found containing this name.")
        return render_template("movie_search.html")
    return render_template("movie_results.html", movies = movies, ratings = ratings_dict)

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

# Display a single movie record
@app.route("/movie/<id>", methods=['GET'])
def view_movie(id):
    movie = model.session.query(model.Movie).get(id)
    ratings = model.session.query(model.Rating).filter_by(user_id=id)

    # Display the movie record and update form
    return render_template("rate_movie.html", movie=movie, ratings=ratings)

# Create a new user
@app.route("/user/new", methods=['GET'])
def new_user_form():
    # Display an HTML form to create a new user
    return render_template("new_user_form.html")

@app.route("/user/new", methods=['POST'])
def new_user():
    global salt
    # Get data for user from request.form
    username = request.form.get("username")
    password = hashlib.sha1(request.form.get("password")+salt).hexdigest()
    age = request.form.get("age")
    zipcode = request.form.get("zipcode")
    user_exist = model.session.query(model.User).filter_by(email=username).all()
    #if user already exists, return to new user form
    if user_exist:
        flash("User already exists.")
        return render_template("new_user_form.html")
    # Create the user object
    user = model.User(email=username, password=password, age=age, zipcode=zipcode)
    # commit to database
    model.session.add(user)
    model.session.commit()
    session['username'] = username
    return render_template("view_user.html", user=user)

    
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