/*var my_elt=document.querySelector('#list_active_games');
my_elt.innerHTML+='poulet';*/

	function display_game_list(){
		console.log('display')
		var elt_html=document.getElementById('list_active_games');
		elt_html.innerHTML+='<p>Selection OK</p>';
		//var list_games={{list_games_java|tojson}};
		elt_html.innerHTML='';
		for (const id in list_games){
			elt_html.innerHTML+='<p>Game N°: '+list_games[id]["id"]+' - Number of players: '+list_games[id]["nb"]+'<p>';
		}
	}
	
	display_game_list();