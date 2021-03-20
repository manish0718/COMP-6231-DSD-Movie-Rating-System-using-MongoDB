from pymongo import MongoClient
import pandas as pd

class MongoDB(object):

    def __init__(self, dBName=None, collectionName=None):

        self.dBName = dBName
        self.collectionName = collectionName

        self.client = MongoClient("mongodb+srv://manish:manish@cluster0.dfnnv.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

        self.DB = self.client[self.dBName]
        self.collection = self.DB[self.collectionName]
        print(self.client.list_database_names())



def InsertData(self, path=None):
        df = pd.read_csv(path)
        data = df.to_dict('records')

        self.collection.insert_many(data, ordered=False)
        print("All the Data has been Exported to Mongo DB Server .... ")




if __name__ == "__main__":
    mongodb = MongoDB(dBName = 'MovieRating', collectionName='ratings_small')
