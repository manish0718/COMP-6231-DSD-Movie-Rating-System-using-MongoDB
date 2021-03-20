from pymongo import MongoClient

# you can change userid and password to connect your own mongodb atlas cluster
testuri = "mongodb+srv://DJW:Wdj197292@sandbox.etlgv.mongodb.net/Test"
database_uri = "mongodb+srv://Dejian:Dejian@cluster0.dfnnv.mongodb.net/movies_metadata?retryWrites=true&w=majority"


def connect_to_MongoDB():
    l_count = 0
    while (l_count < 5):
        print("Attempt to connect mongodb atlas (", l_count, ") times")
        try:
            my_client = MongoClient(database_uri, connectTimeoutMS=200, retryWrites=True)
            print(my_client.stats)
            print("Notice: connected to mongodb atlas")
            print(my_client.list_database_names())
            print("Notice: connected to MovieRating Database")
            movie_rating_database = my_client["MovieRating"]
            return movie_rating_database
        except:
            l_count += 1
            print("Error: can't connect to mongodb atlas or connection timeout, please try again")


