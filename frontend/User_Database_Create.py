import pymongo 
  

connection_url = 'mongodb+srv://m001-student:M001MongoBasics@sandbox.punqd.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
client = pymongo.MongoClient(connection_url) 


def create_users_database():
    
    db = client.drop_database("Clients")
    
    db = client.Clients
    names = ["Manjit" , "Manish" , "Dejian" , "Avneet"]
    passwords = ["Manjit" , "Manish" , "Dejian" , "Avneet"]
    ID = [40185580,40165366,40,40168576]
    
    for i in range(len(names)):
        user = {            
            "id": ID[i],
            "Name":names[i],
            "Password":passwords[i]                     
            }
        
        db.users.insert_one(user)
        
        
    return("Finished Creating the Clients Database")



Done = create_users_database()
print(Done)