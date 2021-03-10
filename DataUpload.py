from pymongo import MongoClient
# you can change userid and password to connect your own mongodb atlas cluster
uri="mongodb+srv://DJW:Wdj197292@sandbox.etlgv.mongodb.net/Test"

def connect_to_MongoDB():

    l_count=0
    while(l_count<5):
        print("Attempt to connect mongodb atlas (",l_count,") times")
        try:
            myclient=MongoClient(uri,connectTimeoutMS=200,retryWrites=True)
            print(myclient.stats)
            print("Notice: connected to mongodb atlas")
            return myclient
        except:
            l_count+=1
            print("Error: can't connect to mongodb atlas or connection timeout, please try again")

if __name__ == "__main__":
    client=connect_to_MongoDB()
    print(client.list_database_names())
    database=client["Test"]

