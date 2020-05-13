/*var my_elt=document.querySelector('#list_active_games');
my_elt.innerHTML+='poulet';*/

function displayGamesList(list_games){
	//console.log("function launched");

	 if (document.body) {
        var larg = (document.body.clientWidth);
        var haut = (document.body.clientHeight);
     } else {
        var larg = (window.innerWidth);
        var haut = (window.innerHeight);
     }

	document.getElementById('list_of_active_games').innerHTML="";
	var compteurLigneColonne = 0;
	var ligne = 1;
	for (const id in list_games){

        compteurLigneColonne += 1;

        if (larg>640) {
            if (compteurLigneColonne === 4) {
                compteurLigneColonne = 1;
                ligne += 1;
            }
        }

		var elt_block_game=document.createElement('div');
		elt_block_game.className="fondGrisStartMenu";
		if (larg>640) {
		    elt_block_game.style="grid-column: "+ compteurLigneColonne +"; grid-row: "+ ligne +";"
		} else {
		    elt_block_game.style="grid-column: 1; grid-row: "+ compteurLigneColonne +";"
		}

		var elt_form=document.createElement('form');
		elt_form.action="";
		elt_form.method="post";
		
		text_form="Game N°" + list_games[id]["id"] + " / Number of players : " + Object.keys(list_games[id]["players"]).length + "/" + list_games[id]["nb_players"] + " ";
		console.log(Object.keys(list_games[id]["players"]).length)
		var elt_form_text=document.createTextNode(text_form);
		elt_form.appendChild(elt_form_text);
		
		var elt_form_input=document.createElement('input');
		elt_form_input.type="submit";
		elt_form_input.value="Join game "+list_games[id]["id"];
		elt_form_input.name="submit";
		elt_form_input.className="btn btn-secondary btn-lg";
		elt_form.appendChild(elt_form_input);

		var elt_p_list_players=document.createElement('p');
		var elt_text_p_list_player=document.createTextNode("Players already signed in : ");
		elt_p_list_players.appendChild(elt_text_p_list_player);
		for (ply_id in list_games[id]["players"]){

			var elt_detail_player=document.createElement('span');
			elt_detail_player.className="text"+list_games[id]["players"][ply_id]["color"].toLowerCase();

			text_detail_player=list_games[id]["players"][ply_id]["name"] + ", " + list_games[id]["players"][ply_id]["role"] + " / ";
			var elt_text_detail_player=document.createTextNode(text_detail_player);

			elt_detail_player.appendChild(elt_text_detail_player);
			elt_p_list_players.appendChild(elt_detail_player);
		}

		elt_block_game.appendChild(elt_form);
		elt_block_game.appendChild(elt_p_list_players);
		document.getElementById('list_of_active_games').appendChild(elt_block_game);
	}
}

var testActualisationGamesList=(function(){
	var list_games={};
	return function(){
		if (document.getElementById('list_of_active_games')!=null){ //on ne rentre dans la fonction que si la liste est à l'écran
		   	//console.log(list_games);
		   	var URL = "/test_actualisation_games_list";
			var xhr = new XMLHttpRequest();
			xhr.open('POST', URL);
			var form=new FormData();
			var list_game_send_xhr=JSON.stringify(list_games);
			form.append('list_game_send_xhr',list_game_send_xhr);
			xhr.send(form);
			xhr.addEventListener("readystatechange", function () {
				if (xhr.readyState === XMLHttpRequest.DONE && (xhr.status==200 || xhr.status==0)) {
					//console.log("Response received");
					var server_response=JSON.parse(xhr.responseText);
					if (server_response["status"]=="Required"){
						//console.log("Syncronisation required");
						list_games=server_response["list_games"];
						displayGamesList(list_games);
					}
				} else if (xhr.readyState === XMLHttpRequest.DONE && xhr.status!=200 && xhr.status!=0) {
						alert("Une erreur est survenue: "+xhr.status+"/n Details: "+xhr.statusText);
				}
			})
		}
	};
})();

function displayPlayersList(list_players){
	document.getElementById('block_team_blue').innerHTML="";
	document.getElementById('block_team_red').innerHTML="";
	for (const ply_id in list_players){
		var elt_detail_player=document.createElement('div');
		elt_detail_player.id="itemJoueur";

		text_detail_player=list_players[ply_id]["name"] + ", " + list_players[ply_id]["role"].toLowerCase() + " (ID : " + list_players[ply_id]["player_id"] + ")";
		var elt_text_detail_player=document.createTextNode(text_detail_player);

		elt_detail_player.appendChild(elt_text_detail_player);
		var block_team=document.getElementById('block_team_'+list_players[ply_id]["color"].toLowerCase())
		block_team.appendChild(elt_detail_player);
	}
}

function displayPlayersListDefault(){
	if (document.getElementById('block_team_blue').firstElementChild==null){
		document.getElementById('block_team_blue').innerHTML='<div>No players yet</div>';
	}
	if (document.getElementById('block_team_red').firstElementChild==null){
		document.getElementById('block_team_red').innerHTML='<div>No players yet</div>';
	}
}

var testActualisationPlayersList=(function(){
	var list_players={};
	return function(){
		if (document.getElementById('block_team_container')!=null){ //on ne rentre dans la fonction que si la liste est à l'écran
		   	//console.log(document.getElementById('block_team_blue').firstElementChild)
		   	var URL = "/test_actualisation_players_list";
			var xhr = new XMLHttpRequest();
			xhr.open('POST', URL);
			var form=new FormData();
			var list_players_send_xhr=JSON.stringify(list_players);
			form.append('list_players_send_xhr',list_players_send_xhr);
			xhr.send(form);
			xhr.addEventListener("readystatechange", function () {
				if (xhr.readyState === XMLHttpRequest.DONE && (xhr.status==200 || xhr.status==0)) {
					//console.log("Response received");
					var server_response=JSON.parse(xhr.responseText);
					if (server_response["status"]=="Required"){
						//console.log("Syncronisation required");
						list_players=server_response["list_players"];
						displayPlayersList(list_players);
					}
					displayPlayersListDefault();
				} else if (xhr.readyState === XMLHttpRequest.DONE && xhr.status!=200 && xhr.status!=0) {
						alert("Une erreur est survenue: "+xhr.status+"/n Details: "+xhr.statusText);
				}
			})
		}
	};
})();

testActualisationGamesList();
setInterval(testActualisationGamesList,3000);

testActualisationPlayersList();
setInterval(testActualisationPlayersList,3000);




