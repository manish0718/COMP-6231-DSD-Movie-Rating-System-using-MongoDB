from flask import Flask, request, render_template, flash 
import client
from datetime import datetime,timezone

app = Flask(__name__)

app.secret_key = "key"

ClientStub = client.conncet_with_server()



def fetch_db():
    conn = client.connect_with_mongoDb()
    db = conn.get_database('Clients')
    db1 = conn.get_database('MovieRating')
    return db , db1

db,db1 = fetch_db()

@app.route("/")
def login():
    return render_template("Machine Learning.html")


@app.route("/home")
def home():
    return render_template("Home.html")


@app.route("/Contact")
def contact():
    return render_template("Contact.html")


@app.route("/About")
def about():
    return render_template("About.html")


@app.route("/Search")
def ML():
    return render_template("Machine Learning.html")


@app.route("/SignUp")
def SignUp():
    return render_template("SignUp.html")


@app.route("/Insert")
def Insert():
    return render_template("Insert.html")


@app.route("/Update")
def Update():
    return render_template("Update.html")


@app.route("/Delete")
def Delete():
    return render_template("Delete.html")

@app.route("/Search-Movie")
def Search():
    return render_template("Search.html")

@app.route("/Response")
def response():
    return render_template("Response.html")


@app.route('/login', methods=['GET', 'POST'])
def authentication():
    if request.method == "POST":
        Response=False
        msg=""
        username = request.form["Username"]
        password = request.form["Password"]
        if (username and password):
            l_count=0;
            while(l_count<5):
                print("***************************************************")
                print("Wait... Verifying Your Credentials" + "(" +str(l_count) + ")")
                print("***************************************************")
                try:
                    l_count+=1;
                    Response = ClientStub.atlas_instance(username,password)
                    if (Response == True):                        
                        print("***************************************************")
                        print("Successfully Loged In")
                        print("***************************************************")       
                    else:                                               
                        print("***************************************************")
                        print("Incorrect Credentials")
                        print("***************************************************")
                        msg="Incorrect Credentials"

                except:
                    print("***************************************************")
                    print("Error Occurred Please Try Again")
                    print("***************************************************")
                    msg = "Error Occurred Please Try Again"
                                   
                finally:
                    if(Response==True):
                        return render_template("Home.html")
                    else:
                        if(msg=="Error Occurred Please Try Again"):
                            flash("Error Occurred Please Try Again")
                            return render_template("login.html")
                        else:
                            flash("Incorrect Credentials")
                            return render_template("login.html")                           
                                                    
        else:
            print("*******************************************************")
            print("Empty Credentials")
            print("*******************************************************")
            flash("Empty Credentials")
            return render_template("login.html")



@app.route("/Movie_Name", methods=['GET', 'POST'])
def fetch():
    if request.method == "POST":
        name = request.form["MovieName"]
        Response = False
        if name:
            l_count = 0;
            while (l_count < 5):
                print("*******************")
                print("Trying to connect to the Server.........." + "(" + str(l_count) + ")")
                print("*******************")
                try:
                    l_count += 1
                    print("*******************")
                    print("CLIENT STUB..")
                    print(ClientStub)
                    print("*******************")
                    Response = ClientStub.searchmovie(name)
                    if (Response == True):
                        Movie = ClientStub.getrecommend(name)
                        print("*******************")
                        print("Movies from the server are:")
                        print(Movie)
                        print("*******************")
                        json_movie = [0] * 10
                        print(json_movie)
                        print("*******************")
                        print("Fetching")
                        print("*******************")

                        # for movie in Movie:
                        #     queryObject = {"title": movie}
                        #     query = db1.movies_metadata.find_one(queryObject)
                        #     query.pop('_id')
                        #     json_movie.append(query)

                        for movie in range(len(Movie)):
                            queryObject = {"title": Movie[movie]}
                            query = db1.movies_metadata.find_one(queryObject)
                            query.pop('_id')
                            json_movie[movie] = query


                        for j in range(0, 10):
                            if not json_movie[j]:
                                json_movie[j] = "No Details"

                        diff = len(json_movie) - len(Movie)

                        for i in range(len(Movie), diff + len(Movie)):
                            Movie.append("No Movie Reccommended")

                        return json_movie
                    else:
                        print("*******************")
                        print("Movie Doesnot Exists In The Database")
                        print("*******************")
                except:
                    print("*******************")
                    print("Something Went Wrong")
                    print("*******************")
                finally:
                    if (Response == True):
                        return render_template("Result.html", data=json_movie[0], data1=json_movie[1],
                                               data2=json_movie[2], data3=json_movie[3], \
                                               data4=json_movie[4], data5=json_movie[5], data6=json_movie[6],
                                               data7=json_movie[7], \
                                               data8=json_movie[8], data9=json_movie[9], \
                                               MOVIE1=Movie[0], MOVIE2=Movie[1], MOVIE3=Movie[2], MOVIE4=Movie[3],
                                               MOVIE5=Movie[4], \
                                               MOVIE6=Movie[5], MOVIE7=Movie[6], MOVIE8=Movie[7], MOVIE9=Movie[8],
                                               MOVIE10=Movie[9])
                    else:
                        print("*******************")
                        print("Movie Doesnot Exists In The Database")
                        print("*******************")
                        flash("Movie Doesnot Exists That You Entered In The Search Bar")
                        return render_template("Response.html")


        else:
            print("*******************")
            print("Movie Name Not Entered By User")
            print("*******************")
            flash("Please Enter The Movie Name")
            return render_template("Machine Learning.html")


@app.route("/Register", methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        Response = False
        username = request.form["Username"]
        password = request.form["Password"]
        ID = request.form["ID"]
        if username and password and ID:
            l_count=0
            while(True):
                print("*************************************************************************")
                print("Trying To Register With The Server. Please Wait........................" + "(" + str(l_count) + ")")
                print("*************************************************************************")
                try:
                    l_count+=1;
                    Response = ClientStub.register(username,password,ID)
                    if(Response == True):
                        print("*******************************************************")
                        print(username + " You Got Successfully Registered")
                        print("*******************************************************")
                        
                except:
                    print("*******************************************************")
                    print("Something Went Wrong")
                    print("*******************************************************")
                finally:
                    if(Response == True):
                        flash("Successfully Registered")
                        return render_template("login.html")
                    else:
                        flash("Registration was unsuccessful Please Try Again")
                        return render_template("SignUp.html")
                        
        else:
            print("*******************************************************")
            print("Please Enter In Every Field")
            print("*******************************************************")
            flash("Please Enter In Every Field")
            return render_template("SignUp.html")
        
        
@app.route("/Insert Movie", methods=['GET', 'POST'])
def insert():
    if request.method=="POST":
        
        name = request.form["MovieName"]
        ID = request.form["ID"]
        user_id = request.form["User ID"]
        movie_id = request.form["Movie ID"]
        time = request.form["Time Stamp"]
        
        if(name and ID and user_id and movie_id and time):
            
            try:
                time = str(time)
                time=time.translate({ord('T'): " "})
                time = time +":00"
                date_time_obj = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
                timestamp = date_time_obj.replace(tzinfo=timezone.utc).timestamp()
                dataToInsert = {
                            "id": str(ID),
                            "title": str(name),
                            "userId": int(user_id),
                            "movieId": int(ID),
                            "timestamp": int(timestamp)                                   
                    }
                print("***************************************************************")
                print("Insert The date Below.........")
                print(dataToInsert)
                print("***************************************************************")
                Response=ClientStub.insert(dataToInsert)
                if(Response==True):
                    print("*******************************************************")
                    print("Movie Information Got Successfully Inserted")
                    print("*******************************************************")
                else:
                    print("***************************************************************")
                    print("Movie Information Insertion Was Unsuccessful On Server Side, Please Try Again")
                    print("***************************************************************")
                    flash("Movie Information Insertion Was Unsuccessful On Server Side, Please Try Again")
                    return render_template("Response.html")
                    
            except:
                print("***********************************************************")
                print("Something Went Wrong...... Please Try Again")
                print("***********************************************************")
                flash("Something Went Wrong...... Please Try Again")
                return render_template("Response.html")
            finally:
                flash("Movie Information Got Successfully Inserted")
                return render_template("Response.html")
                
        else:
            print("*******************************************************")
            print("Please Enter In Every Field")
            print("*******************************************************")
            flash("Please Enter In Every Field")
            return render_template("Response.html")
        
        
@app.route("/Update Movie", methods=['GET', 'POST'])
def update():
    if request.method=="POST":
        Response = False
        msg=""
        name = request.form["MovieName"]
        ID = request.form["ID"]
        user_id = request.form["User ID"]
        movie_id = request.form["Movie ID"]
        time = request.form["Time Stamp"]
        
        if(name and ID and user_id and movie_id and time):
            
            try:
                time = str(time)
                time=time.translate({ord('T'): " "})
                time = time +":00"
                date_time_obj = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
                timestamp = date_time_obj.replace(tzinfo=timezone.utc).timestamp()
                dataToUpdate = {
                            "id": str(ID),
                            "title": str(name),
                            "userId": int(user_id),
                            "movieId": int(ID),
                            "timestamp": int(timestamp)                                    
                    }
                print("***************************************************************")
                print("Updating The date Below.........")
                print(dataToUpdate)
                print("***************************************************************")
                Response = ClientStub.searchmovie(name)
                if(Response==True):
                    Response=ClientStub.update(dataToUpdate)
                    if(Response==True):
                        print("*******************************************************")
                        print("Movie Information Got Successfully Updated")
                        print("*******************************************************")
                        msg='Movie Information Got Successfully Updated'
                    else:
                        print("***************************************************************")
                        print("Movie Information Updation Was Unsuccessful On Server Side, Please Try Again")
                        print("***************************************************************")
                        msg="Movie Information Updation Was Unsuccessful On Server Side, Please Try Again"
                else:
                    print("***************************************************************")
                    print("Movie Doesnot Exists Please Enter The Correct Movie Name")
                    print("***************************************************************") 
                    msg="Movie Doesnot Exists Please Enter The Correct Movie Name"
            except:
                print("***********************************************************")
                print("Something Went Wrong...... Please Try Again")
                print("***********************************************************")
                msg="Something Went Wrong...... Please Try Again"

            finally:
                if(msg=='Movie Information Got Successfully Updated'):
                    flash("Movie Information Got Successfully Updated")
                    return render_template("Response.html")
                else:
                    if(msg=="Something Went Wrong...... Please Try Again"):
                        flash("Something Went Wrong...... Please Try Again")
                        return render_template("Response.html")
                    if(msg=="Movie Doesnot Exists Please Enter The Correct Movie Name"):
                        flash("Movie Doesnot Exists Please Enter The Correct Movie Name")
                        return render_template("Response.html")
                    if(msg=="Movie Information Updation Was Unsuccessful On Server Side, Please Try Again"):
                        flash("Movie Information Updation Was Unsuccessful On Server Side, Please Try Again")
                        return render_template("Response.html")
                    
                
        else:
            print("*******************************************************")
            print("Please Enter In Every Field")
            print("*******************************************************")
            flash("Please Enter In Every Field")
            return render_template("Response.html")
            
            
        

    
@app.route("/Delete", methods=['GET', 'POST'])
def delete():
    if request.method=="POST":
        Response = False
        Response_1 = False        
        name = request.form["MovieName"]
        movieId = request.form["Movie ID"]
        if(name):           
            try:
                dataToDelete = {
                    "title": str(name),
                    "movieId": int(movieId),                                   
                }
                print("***************************************************************")
                print("Deleting The Movie File from the database .........")
                print("Movie whose data is to be deleted is : " + name)
                print(dataToDelete)
                print("***************************************************************")
                Response = ClientStub.searchmovie(name)
                if(Response==True):
                    Response_1=ClientStub.delete(dataToDelete)
                    if(Response_1==True):
                        print("*******************************************************")
                        print("Movie Got Successfully Deleted")
                        print("*******************************************************")
                    else:
                        print("***************************************************************")
                        print("Movie Information Deletion Was Unsuccessful On Server Side, Please Try Again")
                        print("***************************************************************")
                else:
                    print("*******************************************************")
                    print("Movie Doesnot Exists In The Database")
                    print("*******************************************************")

            except:
                print("***********************************************************")
                print("Something Went Wrong...... Please Try Again")
                print("***********************************************************")
                flash("Something Went Wrong...... Please Try Again")
                return render_template("Response.html")
            finally:
                if(Response==True and Response_1==True):
                    flash("Movie Got Successfully Deleted")
                    return render_template("Response.html")
                else:
                    if(Response==True and Response_1==False):
                        flash("Movie Information Deletion Was Unsuccessful On Server Side, Please Try Again")
                        return render_template("Response.html")
                    else:
                        flash("Movie Doesnot Exists In The Database")
                        return render_template("Response.html")
                                            
        else:
            print("*******************************************************")
            print("Please Enter In Every Field")
            print("*******************************************************")
            flash("Please Enter In Every Field")
            return render_template("Response.html")    
        
        
@app.route("/SearchMovie", methods=['GET', 'POST'])
def search():
    if request.method=="POST":        
        name = request.form["MovieName"]
        
        if(name):           
            try:
                print("***************************************************************")
                print("Searching the movie " + name)
                print("***************************************************************")
                Response=ClientStub.searchmovie(name)
                json_file = []
                print("Response")
                if(Response==True):
                    print("*******************************************************")
                    print("Movie Is Present In The Database")
                    print("*******************************************************")
                    json_obj = db1.movies_metadata.find_one({"title":name}) 
                    json_file.append(json_obj)
                    print("*******************************************************")
                    return json_file
            except:
                print("***********************************************************")
                print("Something Went Wrong...... Please Try Again")
                print("***********************************************************")
                flash("Something Went Wrong...... Please Try Again")
                return render_template("Response.html")
            finally:
                print("*******************************************************")
                print("Movie Got Successfully Retrieved")
                print("*******************************************************")
                return render_template("SearchResult.html",MOVIE=json_file[0])
                
        else:
            print("*******************************************************")
            print("Please Enter In Every Field")
            print("*******************************************************")
            flash("Please Enter In Every Field")
            return render_template("Response.html")    
    


if __name__ == '__main__':

    app.run()

