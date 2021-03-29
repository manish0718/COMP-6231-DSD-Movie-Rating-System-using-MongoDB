# server program
from bson.json_util import dumps
import datalink
import DatasetUpload



def serverSetUp():
    """
    Server initialization
    """
    movie_rating_database = datalink.connect_to_MongoDB()
    print(movie_rating_database.list_collection_names())
    movie_metadata_collection = movie_rating_database["movies_metadata"]


def searchHandler(p_input_string):
    None
    

def retrievingDetailsOfMovies(movie_title_list):
    """
    read the list of movies and return details of each movie as a document from MongoDb
    """
    mongodb = DatasetUpload.MongoDB(dBName='MoviesRating', collectionName='movies_metadata')
    for movie in movie_title_list:
        movie_doc = mongodb.collection.find({"title": movie})
        print("Retrieving document for movie: " + movie)
        for document in movie_doc:
            print(dumps(document))


if __name__ == "__main__":
    title_list = ['Toy Story', 'Jumanji', 'Grumpier Old Men', 'Father of the Bride Part II']
    retrievingDetailsOfMovies(title_list)






