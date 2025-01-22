from flask import Flask, render_template_string, render_template, jsonify, request, redirect, url_for, session, Response
from werkzeug.utils import secure_filename
import sqlite3

app = Flask(__name__)                                                                                                                  
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # Clé secrète pour les sessions

# Fonction pour vérifier si l'utilisateur est authentifié
def est_authentifie():
    return session.get('authentifie')

@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route('/lecture')
def lecture():
    if not est_authentifie():
        return redirect(url_for('authentification'))
    return "<h2>Bravo, vous êtes authentifié</h2>"

@app.route('/authentification', methods=['GET', 'POST'])
def authentification():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'password':
            session['authentifie'] = True
            return redirect(url_for('lecture'))
        else:
            return render_template('formulaire_authentification.html', error=True)
    return render_template('formulaire_authentification.html', error=False)

@app.route('/fiche_client/<int:post_id>')
def Readfiche(post_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients WHERE id = ?', (post_id,))
    data = cursor.fetchall()
    conn.close()
    return render_template('read_data.html', data=data)

@app.route('/consultation/')
def ReadBDD():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients;')
    data = cursor.fetchall()
    conn.close()
    return render_template('read_data.html', data=data)

@app.route('/enregistrer_client', methods=['GET'])
def formulaire_client():
    return render_template('formulaire.html')

USERNAME = "user"
PASSWORD = "12345"

@app.route('/fiche_nom/', methods=['GET', 'POST'])
def ReadBDD_2():
    # Vérification des identifiants dans l'en-tête HTTP
    auth = request.authorization
    if not auth or auth.username != USERNAME or auth.password != PASSWORD:
        return Response(
            "Accès refusé : Veuillez fournir un login et un mot de passe.", 
            401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'}
        )

    # Si l'utilisateur est authentifié, continuer
    nom = request.args.get('nom', '')  # Récupérer le nom passé en paramètre GET
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    if nom:
        cursor.execute('SELECT * FROM clients WHERE nom = ?', (nom,))
    else:
        cursor.execute('SELECT * FROM clients;')

    data = cursor.fetchall()
    conn.close()
    return render_template('search_data.html', data=data, nom=nom)

@app.route('/enregistrer_client', methods=['POST'])
def enregistrer_client():
    nom = request.form['nom']
    prenom = request.form['prenom']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO clients (created, nom, prenom, adresse) VALUES (?, ?, ?, ?)', 
        (1002938, nom, prenom, "ICI")
    )
    conn.commit()
    conn.close()
    return redirect('/consultation/')

if __name__ == "__main__":
    app.run(debug=True)
