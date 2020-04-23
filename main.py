from flask import Flask, render_template,request,redirect,url_for,session,flash
from intelligence import *
# from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.secret_key="tmp"
#app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///userus.sqlite3"
#app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False

#db=SQLAlchemy(app)

global list_games
list_games={}

@app.route("/start_menu", methods=["POST","GET"])
def start_menu():
	global list_games
	errors={}
	if request.method=="POST":

		# CREER UN JEU OU CHOISIR UN JEU A REJOINDRE
		if request.form["submit"]=="Create or join game":
			new_game_id=request.form["new_game_id"]
			session["game_id"]=new_game_id
			if new_game_id not in list_games:
				new_game_nb_players=int(request.form["new_game_nb_players"])
				new_game=Lobby(new_game_id,new_game_nb_players)
				list_games[new_game.lobby_id]=new_game
				print("New game created")
			else:
				print("Game succesfully joined")
			if "ID" in session:
				del session["ID"]
			print(list_games[new_game_id].status())
			#print(type(new_game.number_of_players))
			#session["game"]=new_game
			return redirect(url_for("start_menu"))

		# CHANGER DE JEU
		if request.form["submit"]=="Join an other game":
			del session["game_id"]
			return redirect(url_for("start_menu"))

		# AJOUTER UN NOUVEAU JOUEUR
		if request.form["submit"]=="Add player":
			#print("Sign in")
			new_player_name=request.form["new_player_name"]
			new_player_role=request.form["new_player_role"]
			new_player_color=request.form["new_player_color"]
			new_player_password=request.form["new_player_password"]
			try:
				session["ID"] = max(list_games[session["game_id"]].players.keys())+1
			except:
				session["ID"]=1
			list_games[session["game_id"]].register_player(new_player_name,Role[new_player_role],Color[new_player_color],new_player_password)
			print(list_games[session["game_id"]].status())

		# RECUPERER UN JOUEUR EXISTANT
		if request.form["submit"]=="Sign in as":
			sign_in_ID=int(request.form["sign_in_ID"])
			sign_in_password=request.form["sign_in_password"]
			if sign_in_ID in list_games[session["game_id"]].players.keys():
				if sign_in_password == list_games[session["game_id"]].players[sign_in_ID].password:
					session["ID"]=list_games[session["game_id"]].players[sign_in_ID].player_id
					return redirect(url_for("start_menu"))
				else:
					flash("Wrong password","info") # a mettre en forme correctement
			else:
				flash("No players matching with this ID","info") # a mettre en forme correctement


		# SIGN OUT JOUEUR
		if request.form["submit"]=="Sign out":
			del session["ID"]
			return redirect(url_for("start_menu"))

		# SUPPRIMER SON JOUEUR DE LA PARTIE
		if request.form["submit"]=="Delete player":
			del list_games[session["game_id"]].players[session["ID"]]
			del session["ID"]
			return redirect(url_for("start_menu"))

		# INITIALISER LA PARTIE ET AFFICHER LE PLATEAU
		if request.form["submit"]=="Start game":
			# print(len(list_games[session["game_id"]].deck))
			# Creation du jeu si ce n'est pas encore fait
			nb_red_spy=nb_red_guesser=nb_blue_spy=nb_blue_guesser=0
			errors["missing_players"]=0
			errors["role"]=[]
			del errors["role"][:]
			if len(list_games[session["game_id"]].deck)==0:
				if list_games[session["game_id"]].number_of_players == len(list_games[session["game_id"]].players):
					for ply in list_games[session["game_id"]].players.values():
						if ply.color==Color.RED and ply.role==Role.SPY:
							nb_red_spy+=1
						elif ply.color==Color.RED and ply.role==Role.GUESSER:
							nb_red_guesser+=1
						elif ply.color==Color.BLUE and ply.role==Role.SPY:
							nb_blue_spy+=1
						elif ply.color==Color.BLUE and ply.role==Role.GUESSER:
							nb_blue_guesser+=1
					if nb_red_spy != 1:
						errors["role"].append("Red spy ")
					if nb_blue_spy != 1:
						errors["role"].append("Blue spy ")
					if nb_red_guesser == 0:
						errors["role"].append("Red guesser ")
					if nb_blue_guesser == 0:
						errors["role"].append("Blue guesser ")
					if len(errors["role"])==0:
						list_games[session["game_id"]].start_game()
						print("Start game")
						return redirect(url_for("game"))
					else:
						print("Issues encoutered with following roles : ")
						print(errors["role"])
						return redirect(url_for("start_menu"))
				else:
					errors["missing_players"]=list_games[session["game_id"]].number_of_players-len(list_games[session["game_id"]].players)
					print(str(errors["missing_players"])+" players missing")
					return redirect(url_for("start_menu"))
			else:
				return redirect(url_for("game"))

	return render_template("start_menu.html",list_games=list_games,errors=errors)

@app.route("/game", methods=["POST","GET"])
def game():
	global list_games
	if request.method == "POST":
		for i in range(0,25):
			if request.form["submit"]==list_games[session["game_id"]].deck[i].text:
				flash(message,"info")
				list_games[session["game_id"]].guess(session["ID"], list_games[session["game_id"]].players[session["ID"]].color,list_games[session["game_id"]].players[session["ID"]].role, i)
			if request.form["submit"]=="passer":
				flash(message,"info")
				list_games[session["game_id"]].guess(session["ID"], list_games[session["game_id"]].players[session["ID"]].color, list_games[session["game_id"]].players[session["ID"]].role, 25)
		if request.form["submit"]=="Propose":
			flash(message,"info")
			player_proposal = request.form["word_proposal"]
			number_of_words_related = int(request.form["number-of-words"])
			list_games[session["game_id"]].propose(list_games[session["game_id"]].players[session["ID"]].color, list_games[session["game_id"]].players[session["ID"]].role, player_proposal, number_of_words_related)
	print(list_games[session["game_id"]].status())
	return render_template("game.html", list_games=list_games)

if __name__=="__main__":
	#db.create.all()
	app.run(debug=True)