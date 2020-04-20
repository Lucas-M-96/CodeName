from flask import Flask, render_template,request,redirect,url_for,session
from intelligence import *
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.secret_key="tmp"
#app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///userus.sqlite3"
#app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False

#db=SQLAlchemy(app)

global new_game

#class Game(db.Model):
#	id_game=db.Column("id", db.Integer, primary_key=True) 
#	object_game=db.Column("object_game", Lobby)
#
#	def __init__(self,my_id,my_lobby):
#		self.id_game=my_id
#		self.object_game=my_lobby

@app.route("/create_game", methods=["POST","GET"])
def create_game():
	if request.method=="POST":
		# INSERER UN TEST POUR VOIR SI LA PARTIE EXISTE
		global new_game
		new_game_id=request.form["new_game_id"]
		new_game_nb_players=int(request.form["new_game_nb_players"])
		new_game=Lobby(new_game_id,new_game_nb_players)
		print(new_game.status())
		print(type(new_game.number_of_players))
		# session["game"]=new_game
		return redirect(url_for("add_player"))
	return render_template("create_game.html")

@app.route("/add_player", methods=["POST","GET"])
def add_player():
	if request.method=="POST":
		global new_game
		new_player_name=request.form["new_player_name"]
		new_player_role=request.form["new_player_role"]
		new_player_color=request.form["new_player_color"]
		#new_game.players.append(Player(len(new_game.players), new_player_name, new_player_role, Color[new_player_color]))
		new_game.register_player(new_player_name,new_player_role,Color[new_player_color])
		print(new_game.status())
		return redirect(url_for("add_player"))
	return render_template("add_player.html")

if __name__=="__main__":
	#db.create.all()
	app.run(debug=True)