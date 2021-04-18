from flask import Flask, request, render_template, flash
import client
from datetime import datetime, timezone

app = Flask(__name__)

app.secret_key = "key"


def fetch_db():
    conn = client.connect_with_mongoDb()
    db = conn.get_database('Clients')
    db1 = conn.get_database('MovieRating')
    return db, db1


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


@app.route('/login', methods=['GET', 'POST'])
def authentication():
    if request.method == "POST":
        username = request.form["Username"]
        password = request.form["Password"]
        if (username and password):
            l_count = 0;
            while (l_count < 5):
                print("***************************************************")
                print("Wait... Verifying Your Credentials" + "(" + str(l_count) + ")")
                print("***************************************************")
                try:
                    l_count += 1;
                    Response = ClientStub.atlas_instance(username, password)
                    if (Response == True):
                        print("***************************************************")
                        print("Successfully Loged In")
                        print("***************************************************")
                    else:
                        print("***************************************************")
                        print("Error Occurred Please Try Again")
                        print("***************************************************")
                        flash("Incorrect Credentials")
                        return render_template("login.html")
                except:
                    print("***************************************************")
                    print("Error Occurred Please Try Again")
                    print("***************************************************")
                    flash("Please Try Again")
                    return render_template("login.html")

                finally:
                    return render_template("Home.html")
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
        if name:
            l_count = 0;
            while (l_count < 5):
                print("*******************************************************")
                print("Trying to connect to the Server.........." + "(" + str(l_count) + ")")
                print("*******************************************************")
                try:
                    l_count += 1
                    print("*******************************************************")
                    print("CLIENT STUB..")
                    print(ClientStub)
                    print("*******************************************************")
                    Movie = ClientStub.getrecommend(name)
                    print("*******************************************************")
                    print("Movies from the server are:")
                    print(Movie)
                    print("*******************************************************")
                    json_movie = []
                    print("*******************************************************")
                    print("Fetching")
                    print("*******************************************************")

                    for movie in Movie:
                        queryObject = {"title": movie}
                        query = db1.movies_metadata.find_one(queryObject)
                        query.pop('_id')
                        json_movie.append(query)

                    return json_movie

                except:
                    return render_template("Home.html")
                finally:
                    return render_template("Result.html", data=json_movie[0], data1=json_movie[1], data2=json_movie[2],
                                           data3=json_movie[3], \
                                           data4=json_movie[4], data5=json_movie[5], data6=json_movie[6],
                                           data7=json_movie[7], \
                                           data8=json_movie[8], data9=json_movie[9], \
                                           MOVIE1=Movie[0], MOVIE2=Movie[1], MOVIE3=Movie[2], MOVIE4=Movie[3],
                                           MOVIE5=Movie[4], \
                                           MOVIE6=Movie[5], MOVIE7=Movie[6], MOVIE8=Movie[7], MOVIE9=Movie[8],
                                           MOVIE10=Movie[9])
        else:
            print("*******************************************************")
            print("Movie Name Not Entered By User")
            print("*******************************************************")
            flash("Please Enter The Movie Name")
            return render_template("Machine Learning.html")


@app.route("/Register", methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = request.form["Username"]
        password = request.form["Password"]
        ID = request.form["ID"]
        if username and password and ID:
            l_count = 0
            while (True):
                print("*************************************************************************")
                print("Trying To Register With The Server. Please Wait........................" + "(" + str(
                    l_count) + ")")
                print("*************************************************************************")
                try:
                    l_count += 1;
                    Response = ClientStub.register(username, password, ID)
                    if (Response == True):
                        print("*******************************************************")
                        print(username + " You Got Successfully Registered")
                        print("*******************************************************")

                except:
                    print("*******************************************************")
                    print("Something Went Wrong")
                    print("*******************************************************")
                    return render_template("SignUp.html")
                finally:
                    print("*******************************************************")
                    print(username + " You Got Successfully Registered")
                    print("*******************************************************")
                    flash("Successfully Registered")
                    return render_template("login.html")
        else:
            print("*******************************************************")
            print("Please Enter In Every Field")
            print("*******************************************************")
            flash("Please Enter In Every Field")
            return render_template("SignUp.html")


@app.route("/Insert Movie", methods=['GET', 'POST'])
def insert():
    if request.method == "POST":

        name = request.form["MovieName"]
        ID = request.form["ID"]
        user_id = request.form["User ID"]
        movie_id = request.form["Movie ID"]
        time = request.form["Time Stamp"]

        if (name and ID and user_id and movie_id and time):

            try:
                time = str(time)
                time = time.translate({ord('T'): " "})
                time = time + ":00"
                date_time_obj = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
                timestamp = date_time_obj.replace(tzinfo=timezone.utc).timestamp()
                dataToInsert = {
                    "id": str(ID),
                    "title": name,
                    "userId": str(user_id),
                    "movieId": str(movie_id),
                    "timestamp": str(int(timestamp))
                }
                print("***************************************************************")
                print("Insert The date Below.........")
                print(dataToInsert)
                print("***************************************************************")
                Response = ClientStub.insert(dataToInsert)
                if (Response == True):
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
                print("*******************************************************")
                print("Movie Information Got Successfully Inserted")
                print("*******************************************************")
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
    if request.method == "POST":

        name = request.form["MovieName"]
        ID = request.form["ID"]
        user_id = request.form["User ID"]
        movie_id = request.form["Movie ID"]
        time = request.form["Time Stamp"]

        if (name and ID and user_id and movie_id and time):

            try:
                time = str(time)
                time = time.translate({ord('T'): " "})
                time = time + ":00"
                date_time_obj = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
                timestamp = date_time_obj.replace(tzinfo=timezone.utc).timestamp()
                dataToUpdate = {
                    "id": str(ID),
                    "title": name,
                    "userId": str(user_id),
                    "movieId": str(movie_id),
                    "timestamp": str(int(timestamp))
                }
                print("***************************************************************")
                print("Updating The date Below.........")
                print(dataToUpdate)
                print("***************************************************************")
                Response = ClientStub.update(dataToUpdate)
                if (Response == True):
                    print("*******************************************************")
                    print("Movie Information Got Successfully Updated")
                    print("*******************************************************")
                else:
                    print("***************************************************************")
                    print("Movie Information Updation Was Unsuccessful On Server Side, Please Try Again")
                    print("***************************************************************")
                    flash("Movie Information Updation Was Unsuccessful On Server Side, Please Try Again")
                    return render_template("Respnse.html")

            except:
                print("***********************************************************")
                print("Something Went Wrong...... Please Try Again")
                print("***********************************************************")
                flash("Something Went Wrong...... Please Try Again")
                return render_template("Response.html")
            finally:
                print("*******************************************************")
                print("Movie Information Got Successfully Updated")
                print("*******************************************************")
                flash("Movie Information Got Successfully Updated")
                return render_template("Response.html")

        else:
            print("*******************************************************")
            print("Please Enter In Every Field")
            print("*******************************************************")
            flash("Please Enter In Every Field")
            return render_template("Response.html")


@app.route("/Delete", methods=['GET', 'POST'])
def delete():
    if request.method == "POST":
        name = request.form["MovieName"]

        if (name):
            try:
                print("***************************************************************")
                print("Deleting The Movie File from the database .........")
                print("Movie whose data to be deleted" + name)
                print("***************************************************************")
                Response = ClientStub.delete(name)
                if (Response == True):
                    print("*******************************************************")
                    print("Movie Got Successfully Deleted")
                    print("*******************************************************")
                else:
                    print("***************************************************************")
                    print("Movie Information Deleteon Was Unsuccessful On Server Side, Please Try Again")
                    print("***************************************************************")
                    flash("Movie Information Deletion Was Unsuccessful On Server Side, Please Try Again")
                    return render_template("Response.html")

            except:
                print("***********************************************************")
                print("Something Went Wrong...... Please Try Again")
                print("***********************************************************")
                flash("Something Went Wrong...... Please Try Again")
                return render_template("Response.html")
            finally:
                print("*******************************************************")
                print("Movie Got Successfully Deleted")
                print("*******************************************************")
                flash("Movie Got Successfully Deleted")
                return render_template("Response.html")

        else:
            print("*******************************************************")
            print("Please Enter In Every Field")
            print("*******************************************************")
            flash("Please Enter In Every Field")
            return render_template("Response.html")


if __name__ == '__main__':
    ClientStub = client.conncet_with_server()
    db, db1 = fetch_db()
    app.run()
