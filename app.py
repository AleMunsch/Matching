import flask
import sqlite3

app = flask.Flask(__name__,template_folder='Views')

# connection à la bdd
connection = sqlite3.connect('bdd.db')

#creation de la table Joueur si innexistante
cursor = connection.cursor()
cursor.execute('Create table if not exists Joueur (id integer primary key, pseudo text, age interger, Jeux_1 texte, Jeux_2 texte, Jeux_3 texte)')
connection.commit()
connection.close()

@app.route('/')
def home():
    connection = sqlite3.connect('bdd.db')
    cursor = connection.cursor()
    cursor.execute('select * from Joueur')
    Joueur = cursor.fetchall()
    connection.close()
    
    list_Joueur = []
    
    for Joueur in Joueur:
        list_Joueur.append({
            "id": Joueur[0],
            "pseudo": Joueur[1],
            "age": Joueur[2],
            "Jeux_1": Joueur[3],
            "Jeux_2": Joueur[4],
            "Jeux_3": Joueur[5],
        })
    return flask.render_template('search.html', Joueur=list_Joueur)

#ajout du joueur dans la bdd
@app.route('/add', methods=['GET', 'POST'])
def add():
   if flask.request.method == 'POST':
      pseudo = flask.request.values.get('pseudo')
      age = flask.request.values.get('age')
      Jeux_1 = flask.request.values.get('Jeux_1')
      Jeux_2 = flask.request.values.get('Jeux_2')
      Jeux_3 = flask.request.values.get('Jeux_3')

      connection = sqlite3.connect('bdd.db')

      cursor = connection.cursor()
      cursor.execute('INSERT INTO Joueur (pseudo, age, Jeux_1, Jeux_2, Jeux_3) VALUES ("' + pseudo + '", "' + age + '", "' + Jeux_1 + '", "' + Jeux_2 + '", "' + Jeux_3 + '")')
      connection.commit()
      connection.close()

      return flask.redirect('/')
   else:
      return flask.render_template('add.html')

# Supprimer joueur
@app.route('/delete/<id>')
def delete(id):
   connection = sqlite3.connect('bdd.db')

   cursor = connection.cursor()
   cursor.execute('DELETE FROM Joueur WHERE id = ' + id)
   connection.commit()
   connection.close()

   return flask.redirect('/')


@app.route('/api/Joueur', methods=['GET'])
def get_Joueur():
   connection = sqlite3.connect('bdd.db')
   cursor = connection.cursor()
   cursor.execute('SELECT * FROM Joueur')
   Joueur = cursor.fetchall()
   connection.close()

   list_Joueur = []

   for Joueur in Joueur:
        list_Joueur.append({
            "id": Joueur[0],
            "pseudo": Joueur[1],
            "age": Joueur[2],
            "Jeux_1": Joueur[3],
            "Jeux_2": Joueur[4],
            "Jeux_3": Joueur[5],
        }) 

   return flask.jsonify(list_Joueur)

# ajout Joueur
@app.route('/api/Joueur', methods=['POST'])
def add_Joueur():
   if flask.request.method == 'POST':
      
      pseudo = flask.request.json['pseudo']
      age = flask.request.json['age']
      Jeux_1 = flask.request.json['Jeux_1']
      Jeux_2 = flask.request.json['Jeux_2']
      Jeux_3 = flask.request.json['Jeux_3']


      connection = sqlite3.connect('bdd.db')

      cursor = connection.cursor()
      cursor.execute('INSERT INTO Joueur (pseudo, age, Jeux_1, Jeux_2, Jeux_3) VALUES ("' + pseudo + '", "' + str(age) + '", "' + Jeux_1 + '", "' + Jeux_2 + '", "' + Jeux_3 + '")')
      connection.commit()
      connection.close()

      return flask.jsonify({
         "message": "Joueur added successfully"
      })
# Fonction de recherche de joueurs par filtres
def search_Joueur(pseudo=None, age=None, Jeux_1=None, Jeux_2=None, Jeux_3=None):
    connection = sqlite3.connect('bdd.db')
    cursor = connection.cursor()

    query = 'SELECT * FROM Joueur WHERE 1=1'

    if pseudo:
        query += f" AND pseudo LIKE '{pseudo}'"
    if age:
        query += f" AND age = {int(age)}"
        
    if Jeux_1 or Jeux_2 or Jeux_3:
        games_list = []

        if Jeux_1:
            games_list.append(Jeux_1)
        if Jeux_2:
            games_list.append(Jeux_2)
        if Jeux_3:
            games_list.append(Jeux_3)

        gamefilter = f"""({",".join(["'" + a + "'" for a in games_list])})"""

        #if Jeux_1:
        query += f" AND (Jeux_1 IN {gamefilter}"
        #if Jeux_2:
        query += f" OR Jeux_2 IN {gamefilter}"
        #if Jeux_3:
        query += f" OR Jeux_3 IN {gamefilter})"
        
    print(query)
    cursor.execute(query)

    Joueurs = cursor.fetchall()
    print(Joueurs)
    connection.close()

    list_Joueur = []

    for Joueur in Joueurs:
        list_Joueur.append({
            "id": Joueur[0],
            "pseudo": Joueur[1],
            "age": Joueur[2],
            "Jeux_1": Joueur[3],
            "Jeux_2": Joueur[4],
            "Jeux_3": Joueur[5],
        })

    return list_Joueur

# Route pour la recherche de joueurs avec filtres
@app.route('/search', methods=['POST'])
def search_Joueur_route():
    pseudo = flask.request.form.get('pseudo')
    age = flask.request.form.get('age')
    Jeux_1 = flask.request.form.get('Jeux_1')
    Jeux_2 = flask.request.form.get('Jeux_2')
    Jeux_3 = flask.request.form.get('Jeux_3')
    
    print(pseudo, age, Jeux_1, Jeux_2, Jeux_3)


    Joueur = search_Joueur(pseudo, age, Jeux_1, Jeux_2, Jeux_3)

    return flask.render_template('search_result.html', Joueurs=Joueur)


app.run(port=8888)