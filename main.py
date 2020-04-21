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

@app.route("/create_game", methods=["POST","GET"])
def create_game():
	global list_games
	if "name" in session:
		print("Session already opened : Game ID = "+session["game_id"]+" Name = "+session["name"])
	if request.method=="POST":
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
				if request.form["submit"]=="Sign in":
					print("Sign in")
					new_player_name=request.form["new_player_name"]
					new_player_role=int(request.form["new_player_role"])
					new_player_color=request.form["new_player_color"]
					session["name"]=new_player_name
					session["role"]=new_player_role
					session["color"]=new_player_color
					list_games[session["game_id"]].register_player(new_player_name,new_player_role,Color[new_player_color])
					print(list_games[session["game_id"]].status())
					return redirect(url_for("add_player"))
				if request.form["submit"]=="Start game":
					print("Start game")
					return redirect(url_for("game"))
	return render_template("add_player.html",current_game=list_games[session["game_id"]])


@app.route("/game", methods=["POST","GET"])
def game():
	global list_games
	list_games[session["game_id"]].start_game()
	# deck_test = ["Vol", "Chef", "Rame","Charge","Tambour","Cellule","Sol","Chemise","Solution","Chou","Mousse","Numéro","Marche","Perle","Carte","Couronne","Carrière","Portable","Lunettes","Sortie","Chaine","Botte","Corne","Mineur","Mine"]
	deck_test = list_games[session["game_id"]].deck
	if request.method == "POST":
		player_guess = request.form["guess"]
		list_games[session["game_id"]].guess(player.player_id, player.color, player.role, player_guess)
	print(list_games[session["game_id"]].status())
	return render_template("game.html", le_deck_de_mots = deck_test)

if __name__=="__main__":
	#db.create.all()
	app.run(debug=True)