import model
import csv

def load_users(session):
    # use u.user
    with open('./seed_data/u.user', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            values = row[0].split("|")
            print int(values[0]), int(values[1]), values[4]
            user = model.User(id=int(values[0]), email='none', password="none",  age=int(values[1]), zipcode=values[4])
            session.add(user)
        session.commit()
      
def load_movies(session):
    # use u.item
    with open('./seed_data/u.item', 'rb') as f:
        reader = csv.reader(f)
    #     class Movie(Base):
    # __tablename__ = "movies"
    # id = Column(Integer, primary_key = True)
    # name = Column(String(64))
    # released_at = Column(DateTime(timezone=False), nullable=True)
    # imdb_url = Column(String(128), nullable=True)

        for row in reader:
            values = ','.join(row)
            values = values.split('|')
            print values[2]

           
            movie = model.Movie(id=int(values[0]), name=values[1], released_at=values[2], imdb_url=values[4])
            session.add(movie)
        session.commit()    

def load_ratings(session):
    # use u.data
    with open('./seed_data/u.data', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            values = row[0].split( )
            rating = model.Rating(movie_id=int(values[1]), user_id=int(values[0]), rating=int(values[2]))
            session.add(rating)
            print values
        session.commit()    
        
     #  Open hard-coded csv file (u.user)
   #  Get a line a time, parse somehow,
   # we get a row that looks like 942|48|F|librarian|78209
   # open  session add row 
   #  create statements like:
   #  c.password = "somethingmoresecure"
   #  charles = User(email="charles@hackbrightacademy.com", password="notsecure",
   # age=25, zipcode="94103")
   #   session.add
   #   session.commit
   #   close file
   #   done
    pass

def main(session):
    # You'll call each of the load_* functions with the session as an argument
    #load_users(session)
    #load_ratings(session)
    load_movies(session)
    pass

if __name__ == "__main__":
    s= model.connect()
    main(s)
