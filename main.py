from flask import Flask, render_template,request,redirect,url_for,session
from intelligence import *
# from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.secret_key="tmp"
#app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///userus.sqlite3"
#app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False

#db=SQLAlchemy(app)

global list_games
list_games={}

#class Game(db.Model):
#	id_game=db.Column("id", db.Integer, primary_key=True) 
#	object_game=db.Column("object_game", Lobby)
#
#	def __init__(self,my_id,my_lobby):
#		self.id_game=my_id
#		self.object_game=my_lobby

@app.route("/create_game", methods=["POST","GET"])
def create_game():
	global list_games
	if request.method=="POST":
		# INSERER UN TEST POUR VOIR SI LA PARTIE EXISTE
		new_game_id=request.form["new_game_id"]
		session["game_id"]=new_game_id
		if new_game_id not in list_games:
			new_game_nb_players=int(request.form["new_game_nb_players"])
			new_game=Lobby(new_game_id,new_game_nb_players)
			list_games[new_game.lobby_id]=new_game
			print("New game created")
		else:
			print("Game succesfully joined")
		print(list_games[new_game_id].status())
		#print(type(new_game.number_of_players))
		# session["game"]=new_game
		return redirect(url_for("add_player"))
	return render_template("create_game.html",list_games=list_games)

@app.route("/add_player", methods=["POST","GET"])
def add_player():
	global list_games
	if "game_id" not in session:
		return redirect(url_for("create_game"))
	else:
		if session["game_id"] not in list_games.keys():
			return redirect(url_for("create_game"))
		else:
			if request.method=="POST":
				new_player_name=request.form["new_player_name"]
				new_player_role=int(request.form["new_player_role"])
				new_player_color=request.form["new_player_color"]
				#new_game.players.append(Player(len(new_game.players), new_player_name, new_player_role, Color[new_player_color]))
				session["name"]=new_player_name
				session["role"]=new_player_role
				session["color"]=new_player_color
				list_games[session["game_id"]].register_player(new_player_name,new_player_role,Color[new_player_color])
				print(list_games[session["game_id"]].status())
				return redirect(url_for("add_player"))
	return render_template("add_player.html",current_game=list_games[session["game_id"]])

@app.route('/<Lobby_id>', methods=["POST","GET"])
def game(Lobby_id):
	global new_game
	new_game.start_game()
	# deck_test = ["Vol", "Chef", "Rame","Charge","Tambour","Cellule","Sol","Chemise","Solution","Chou","Mousse","Numéro","Marche","Perle","Carte","Couronne","Carrière","Portable","Lunettes","Sortie","Chaine","Botte","Corne","Mineur","Mine"]
	deck_test = new_game.deck
	if request.method == "POST":
		player_guess = request.form["guess"]
		new_game.guess(player.player_id, player.color, player.role, player_guess)
	print(new_game.status())
	return render_template("game.html", le_deck_de_mots = deck_test)

if __name__=="__main__":
	#db.create.all()
	app.run(debug=True)