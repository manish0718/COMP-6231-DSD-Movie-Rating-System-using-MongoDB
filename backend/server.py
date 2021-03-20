# server program

import datalink



def serverSetUp():
    """
    Server initialization
    """
    movie_rating_database = datalink.connect_to_MongoDB()
    print(movie_rating_database.list_collection_names())
    movie_metadata_collection = movie_rating_database["movies_metadata"]


def searchHandler(p_input_string):
    None






