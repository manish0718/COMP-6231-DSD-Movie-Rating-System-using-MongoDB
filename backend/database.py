import json

import pandas as pd
from pymongo import MongoClient
from ml import preprocessor



def _connect_mongo(db_name="MovieRating"):
    """ A util for making a connection to mongo """

    mongo_uri = "mongodb+srv://manish:manish@cluster0.dfnnv.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

    l_count = 0
    while (l_count < 5):
        print("*******************************************************")
        print("Attempt to connect mongodb atlas (", l_count, ") times")
        print("*******************************************************")
        try:
            my_client = MongoClient(mongo_uri, connectTimeoutMS=2000000, retryWrites=True)
            print("*******************************************************")
            print(my_client.stats)
            print("*******************************************************")
            print("Notice: connected to mongodb atlas")
            print("*******************************************************")
            print(my_client.list_database_names())
            print("*******************************************************")
            print("Notice: connected to MovieRating Database")
            movie_rating_database = my_client[db_name]
            return movie_rating_database
        except:
            l_count += 1
            print("******************************************************************************")
            print("Error: can't connect to mongodb atlas or connection timeout, please try again")
            print("******************************************************************************")



def get_collection(collection, no_id=True):
    """ Read from Mongo and Store into DataFrame """
    #db_name = 'MovieRating'
    # Connect to MongoDB
    client = getMongoInstance()
    db = client.get_database("MovieRating")

    # Make a query to the specific DB and Collection
    cursor = db[collection]

    # Expand the cursor and construct the DataFrame
    df = pd.DataFrame(list(cursor.find()))


    # Delete the _id
    if no_id:
        del df['_id']

    pd.options.display.max_columns = None
    pd.options.display.width = None

    return df


def update(file, collection):
    pd.options.display.max_columns = None
    pd.options.display.width = None
    db = 'MovieRating'
    # Connect to MongoDB
    db = _connect_mongo(db=db)
    collections = db[collection]

    with open(file) as f:
        file_data = json.load(f)

    collections.insert_one(file_data)
    print("Data inserted on mongodb atlas")
    
    
def insertUserData(insertData):
    # Connect to MongoDB
    client = getMongoInstance()
    db = client.get_database("MovieRating")

    movie_collection = db["movies_metadata"]
    myMoviesData = {"adult": "False","belongs_to_collection": float("NaN"),
                     "budget": float("NaN"), "genres": float("NaN"), "homepage": float("NaN"),"id": str(insertData['id']), "imdb_id": float("NaN"),
                    "original_language": float("NaN"), "original_title": float("NaN"), "overview": float("NaN"), "popularity": float("NaN"),
                    "poster_path": float("NaN"), "production_companies": float("NaN"), "production_countries": float("NaN"), "release_date": float("NaN"),
                    "revenue": float("NaN"), "runtime": float("NaN"), "spoken_languages": float("NaN"), "status": float("NaN"), "tagline": float("NaN"),"title": insertData['title'],
                    "video": "false", "vote_average": float("NaN"), "vote_count": float("NaN")}
    insertedMovieID = movie_collection.insert_one(myMoviesData)

    rating_collection = db["ratings_small"]
    myRatingsData = {"userId": insertData['userId'], "movieId": insertData['movieId'],
                     "timestamp": insertData['timestamp'], "rating": 4.5}
    insertedRatingId = rating_collection.insert_one(myRatingsData)
    

    if insertedMovieID.acknowledged and insertedRatingId.acknowledged:
        print("Data successfully inserted.")
        return True

    return False

def updateUserData(updateData):
    # Connect to MongoDB
    client = getMongoInstance()
    db = client.get_database("MovieRating")

    col1 = db["movies_metadata"]
    col2 = db["ratings_small"]

    # data for ratings
    movieID = int(updateData["movieId"])
    userId = int(updateData["userId"])
    timestamp = int(updateData["timestamp"])

    # date for moviedataset
    title = updateData["title"]
    id = str(updateData["id"])

    filter1 = { 'title': title }
    newMovieValues = {"$set": {"adult": "False","belongs_to_collection": float("NaN"),
                     "budget": float("NaN"), "genres": float("NaN"), "homepage": float("NaN"),"id": id, "imdb_id": float("NaN"),
                    "original_language": float("NaN"), "original_title": float("NaN"), "overview": float("NaN"), "popularity": float("NaN"),
                    "poster_path": float("NaN"), "production_companies": float("NaN"), "production_countries": float("NaN"), "release_date": float("NaN"),
                    "revenue": float("NaN"), "runtime": float("NaN"), "spoken_languages": float("NaN"), "status": float("NaN"), "tagline": float("NaN"),"title": title,
                    "video": "false", "vote_average": float("NaN"), "vote_count": float("NaN")}}
    filter2 = { 'userId': userId }
    newRatingValues = {"$set": {"movieId": movieID, "userId": userId, "timestamp": timestamp, "rating": 4.5}}

    x = col1.update_one(filter1, newMovieValues, upsert=True)
    y = col2.update_one(filter2, newRatingValues, upsert=True)

    if(x.acknowledged and y.acknowledged):
        print("Data successfully updated.")
        return True

    return False

def deleteUserData(data):
    client = getMongoInstance()
    db = client.get_database("MovieRating")

    col1 = db["movies_metadata"]
    col2 = db["ratings_small"]

    # data for ratings
    movieID = data["movieId"]


    # data for moviedataset
    title = data["title"]

    q1 = {"title": title}
    q2 = {"movieId": movieID}


    x = col1.delete_one(q1)

    y = col2.delete_one(q2)
    

    if (y.deleted_count > 0 and x.deleted_count > 0):
        print("Data successfully deleted.")
        return True

    return False


def getMongoInstance():
    try:
        connection_url = 'mongodb+srv://manish:manish@cluster0.dfnnv.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
        client = MongoClient(connection_url)  
    except:
        print("Connection Failed With MongoDb Cloud")
    finally:
        return client
    

def registerWithMongo(username,password,ID):
    instance = getMongoInstance()
    db = instance.Clients
    user = {
        "id": ID,
        "Name": username,
        "Password": password
    }

    db.users.insert_one(user)
    queryObject = {'Name': username, 'Password': password}
    query = db.users.find_one(queryObject)
    
    if(query):
        return True
    else:
        return False
    
    
def mongoLogin(username,password):
    client = getMongoInstance()
    db = client.get_database("Clients")
    queryObject = {'Name': username, 'Password': password}
    query = db.users.find_one(queryObject)
    if(query):
        return True
    else:
        return False
    
    
def searchMovie(p_input_movie):
    client = getMongoInstance()
    db = client.get_database("MovieRating")
    queryObject = {"title":p_input_movie}
    query = db.movies_metadata.find_one(queryObject)
    if(query):
        return True
    else:
        return False
    
    
    





    