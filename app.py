
from flask import Flask, request,jsonify
from flask_mysqldb import MySQL
import json
from flask_cors import CORS
import uuid
from werkzeug.utils import secure_filename
import pyrebase
import os


#import mybase

#local upload
UPLOAD_FOLDER = "./uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

#filter mime-types
def allowed_files(filename):
    return "." in filename and filename.rsplit(".",1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "localhost"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "flask-angular"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
mysql=MySQL(app)
CORS(app)

#Configuration de mon firebase

config = {
   "apiKey": "AIzaSyAreronuS6yryuLnOgf9AKh4rNyp0Nqx9E",
    "authDomain": "flask-angular-f5d32.firebaseapp.com",
    "projectId": "flask-angular-f5d32",
    "storageBucket": "flask-angular-f5d32.appspot.com",
    "messagingSenderId": "510616657006",
    "appId": "1:510616657006:web:130fc84d80be673c535a7f",
    "measurementId": "G-GFM8MZSX8F",
    "serviceAccount":"./sow-key.json"

}

#initialiser firebase
firebase = pyrebase.initialize_app(config)

#stockage
storage = firebase.storage()

@app.route("/api/vetement", methods=["GET"])
def index():
    if request.method == "GET":
        return jsonify(data = "posts main responses")

@approute("/api/vetements", method = ["POST"])
def addvetement():
    if request.method == "POST":
        print(request.form, flush=True)

        name = request.form.get("name")
        prix = request.form.get("prix")
        photo = request.files["photo"]
        if photo and allowed_files(photo.filename):
            filename = str(uuid.uuid4())
            filename += "."
            filename += photo.filename.split(".")[1]

            #create secure name
            filename_secure = secure_filename(filename)
            #Enregistrer dans le dossier upload
            photo.save(os.path.join(app.config["UPLOAD_FOLDER"]))

            #firebase filename
            local_filename = "./uploads"
            local_filename += filename_secure

            #upload file
            storage.child(firebase_filename).put(local_filename)

            #upload fichier
            photo_image = storage.child(firebase_filename).put(local_filename)

            #avoir l'url du fichier
            photo_image = storage_child(firebase_filename).get_url(None)

            #mysql
            cur = mysql.connection.cursor()
            cur.exec(""" INSERT INTO flask-angular (nom, prix, photo) VALUES(%s, %s, %s)""",
            (name,prix,photo))

            #effacer le contenu apres refresh
            os.remove(os.path.join(app.config["UPLOAD_FOLDER"], filename_secure))
             

            return jsonify(data = "The post was created") 

if __name__ == "__main__":
    app.run(debug=True)
    


