import flask
import jwt
#Créer des jetons JWT
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
#Utiliser des pages html
from flask import render_template
from flask import redirect, url_for, make_response
#Utiliser Flask et récupérer les variables d'un formulaire
from flask import Flask, request

import json
#Connexion à la base de données
import mysql.connector
from datetime import datetime, timedelta
import time
#Bcrypt
import bcrypt


app = Flask(__name__)
app.secret_key = "secretLocal"
jwt_secret_key = "secretJwt"

def generate_jwt(username):
    #Generation de token
    payload = {
        'username': username,
        'exp': datetime.now() + timedelta(minutes=30)
    }
    token = jwt.encode(payload, jwt_secret_key, algorithm='HS256')
    return token
    #renvoi le token

#Connection à la base de données
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="bubu3000",
    database="pythonProject"
)


@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/traitement',methods = ['GET','POST'])
def traitement():
    #On récupère les variables rentrés par l'utiilsateur
    login = request.form['login']
    password = bytes(request.form['password'].encode('utf-8'))


    #La ligne suivante permet de tester l'output
    #print_salt = salt.decode('utf-8')

    # Si l'utilisateur a bien rentré un login, on va chercher le mot de passe
    if len(login) >= 1:
        sql_check = "SELECT * FROM pythonProject_students where login = '%s' " % login
        mycursor = mydb.cursor()
        mycursor.execute(sql_check)
        check = mycursor.fetchall()
        # si la requête de vérification est vide, l'utilisateur n'existe pas
        if len(check) == 0:
            return "Accès refusé."

        #On récupère le salt dans le tableau où le login est égal à login
        sql_salt = "SELECT salt from pythonProject_students where login = '%s' " % login
        mycursor = mydb.cursor()
        mycursor.execute(sql_salt)
        salt = mycursor.fetchall()
        #On le transforme en type bytes pour qu'il puisse être utilisé par la suite
        salt = bytes(salt[0][0].encode("utf-8"))

        # Génération du mdp haché à partir de celui rentré par l'utilisateur + du salt qu'on a trouvé dans sa table
        typed_password = bcrypt.hashpw(password, salt)

        #On récupère le mot de passe hashé dans la DB
        sql_password = "SELECT hashed from pythonProject_students where login = '%s' " % login
        mycursor = mydb.cursor()
        mycursor.execute(sql_password)
        real_password = mycursor.fetchall()
        real_password = bytes(real_password[0][0].encode("utf-8"))


        # Si le mot de passe obtenu correspond au mot de passe tapé puis haché, alors on affiche le formulaire 2
        if real_password == typed_password:
            # Si mot de passe vérifié, alors je génère mon JWT
            jwt_token = generate_jwt(login)
            # Je prepare ma réponse avec une redirection
            response = make_response(redirect(url_for('protected')))
            # Dans ma réponse je mettrais a jour les cookis
            response.set_cookie('jwt', jwt_token)
            response.set_cookie('pythonProject', "coucou")
            return response
            #return render_template('resultats.html', login=login)
        # Si le mot de passe obtenu ne correspond pas, on refuse l'accès
        else:
            return "Accès refusé."


    else:
        return "Merci de taper un login !"

@app.route('/protected')
def protected():
    try:
        #Je récupère le token
        token = request.cookies.get('jwt')
        payload = jwt.decode(token, jwt_secret_key, algorithms=['HS256'])
        username = payload['username']

        now = datetime.now()
        # SI ON SE TROUVE ACTUELLEMENT DANS UNE SESSION OUVERTE
        #Chercher la date de la dernière session
        sql_last_session_date = "SELECT date, closing_hour FROM pythonProject_sessions ORDER BY session_id DESC LIMIT 1"
        mycursor = mydb.cursor(dictionnary = True)
        parametersAsTUple = (date_session, heure_fermeture)
        mycursor.execute(sql_last_session_date,parametersAsTUple)
        sessions_info = mycursor.fetchone()
        last_session_date_raw = sessions_info.get("date")
        last_session_date_str = str(last_session_date_raw[0][0])
        last_session_date = datetime.strptime(last_session_date_str, '%Y-%m-%d').date()

        #Chercher la date actuelle :
        current_date = now.strftime('%Y-%m-%d')
        current_date = datetime.strptime(current_date, '%Y-%m-%d').date()
        mycursor.close()

        if last_session_date == current_date :
            mycursor = mydb.cursor()
            #Il faut maintenant chercher l'heure de fermeture de la dernière session
            last_closing_hour_raw = sessions_info['closing_hour']
            last_closing_hour_str = str(last_closing_hour_raw[0][0])
            #On transforme le résultat en datetime
            last_closing_hour = datetime.strptime(last_closing_hour_str, '%H:%M:%S')

            #Et chercher l'heure actuelle
            current_hour_str = now.strftime('%H:%M:%S')
            #On transforme également le résultat en datetime
            current_hour = datetime.strptime(current_hour_str, '%H:%M:%S')

            #puis on compare les 2 :
            if last_closing_hour > current_hour:
                print("succès comparaison d'heures")
            else:
                print("échec comparaison d'heures")

        else:
            current_date = str(current_date)
            last_session_date = str(last_session_date)
            return last_session_date





    except jwt.ExpiredSignatureError:
        response = make_response(redirect(url_for('login')))
        return response
    except jwt.InvalidTokenError:
        response = make_response(redirect(url_for('login')))
        return response

        current_time = list(datetime.datetime.now())
        if last_session > current_time:
            return render_template("formulaire.html")
        else:
            return render_template("non_accessible.html")

@app.route('/formulaire',methods = ['GET','POST'])
def formulaire():
    #On récupère le token
    token = request.cookies.get('jwt')
    payload = jwt.decode(token, jwt_secret_key, algorithms=['HS256'])
    username = payload['username']

    if request.method == 'POST':
        avancement = request.form['avancement']
        difficulte = request.form['difficulte']
        progression = request.form['progression']
    else:
        return render_template("login.html")


    #Déterminer dans quelle session on se trouve en comparant l'heure actuelle avec les heures contenues en BD dans Sessions
    #En déduire l'id de session dans laquelle on est

    #Récupérer l'id de l'étudiant

    #Insérer dans
    #sql = "INSERT INTO pythonProject_surveyResults VALUES"difficulté, avancement, progression, id_étudiant, id_session




if __name__ == "__main__":
    app.run(debug=True)