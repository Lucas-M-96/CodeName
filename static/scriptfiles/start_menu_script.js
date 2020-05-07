/*var my_elt=document.querySelector('#list_active_games');
my_elt.innerHTML+='poulet';*/

function displayGameList(list_games){
	console.log("function launched");
	document.getElementById('list_of_active_games').innerHTML="";
	for (const id in list_games){

		var elt_block_game=document.createElement('form');

		var elt_form=document.createElement('form');
		elt_form.action="";
		elt_form.method="post";
		
		text_form="Game N°" + list_games[id]["id"] + " / Number of players : " + list_games[id]["nb_players"];
		var elt_form_text=document.createTextNode(text_form);
		elt_form.appendChild(elt_form_text);
		
		var elt_form_input=document.createElement('input');
		elt_form_input.type="submit";
		elt_form_input.value="Join game "+list_games[id]["id"];
		elt_form_input.name="submit";
		elt_form_input.className="boutonStartMenu";
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




function testActualisationGameList(){
   	var URL = "/test_actualisation_start_menu";
	var xhr = new XMLHttpRequest();
	xhr.open('POST', URL);
	var form=new FormData();
	var list_game_send_xhr=JSON.stringify(list_games);
	form.append('list_game_send_xhr',list_game_send_xhr);
	xhr.send(form);
	xhr.addEventListener("readystatechange", function () {
		if (xhr.readyState === XMLHttpRequest.DONE && (xhr.status==200 || xhr.status==0)) {
			console.log("Response received");
			var server_response=JSON.parse(xhr.responseText);
			if (server_response["status"]=="Required"){
				console.log("Syncronisation required");
				list_games=server_response["data"];
				displayGameList(list_games);
			}
		} else if (xhr.readyState === XMLHttpRequest.DONE && xhr.status!=200 && xhr.status!=0) {
				alert("Une erreur est survenue: "+xhr.status+"/n Details: "+xhr.statusText);
		}
	})
}

var list_games={};
testActualisationGameList();
setInterval(testActualisationGameList,3000);