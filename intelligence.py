#!/usr/bin/env python
import enum
import random

table_de_carte = ["Vol", "Chef", "Rame","Charge","Tambour","Cellule","Sol","Chemise","Solution","Chou","Mousse","Numéro","Marche","Perle","Carte","Couronne","Carrière","Portable","Lunettes","Sortie","Chaine","Botte","Corne","Mineur","Mine","Entrée","Bretelle","Poste","Banane","Phare","Don","Pendule","Fin","Pompe","Australie","Napoléon","Tube","Lit","Avocat","Physique","Ampoule","Patron","Confinement","Titre","Cartouche","Cuisine","Trait","Air","Prise","Uniforme","Page","Clé","Somme","Club","Cabinet","Coupe","Timbre","Vaisseau","Tuile","Couteau","Toile","Couverture","Menu","Bureau","Religieuse","But","Radio","Cadre","Essence","Cafard","Arc","Canne","Passe","Canon","Plat","Mémoire","Manège","Ligne","Membre","Opération","Planche","Carreau","Louche","Russie","Vin","Barre","Atout","Bon","Liquide","Orange","Course","Boite","Raie","Bombe","Plateau","Poele","Partie","Baie","Pensée","Boulet","Poire","Bouton","Bougie","Coq","Espagne","Col","Ordre","Campagne","Jet","Queue","Foyer","Grèce","Tokyo","Eponge","Note","Critique","Vague","Cycle","Farce","Droit","Vase","Eclair","Balance","Ensemble","Voile","Prêt","Rayon","Glace","Ferme","Gorge","Feuille","Grain","Ronde","Grenade","Brique","Grue","Enceinte","Guide","Banc","Bete","Iris","Lentille","Asile","Peste","Fort","Gel","Garde","Remise","Sardine","Europe","Hollywood","Palais","Bande","Vision","Piece","Paille","Facteur","Majeur","Sens","Pile","Espace","Plan","Bar","Court","Fer","Fuite","Formule","New-York","Alpes","Londres","Ninja","Plante","Marque","Talon","Commerce","Rouleau","Front","Lettre","Marron","Siège","Recette","Etude","Kiwi","Palme","Langue","Meuble","Figure","Carton","Moule","Quartier","Bourse","Volume","Charme","Rome","Révolution","Fraise","Manche","Base","Pêche","Asterix","Lumière","Camember","Français","Rat","Pôle","Appareil","Tableau","Argent","Nœud","Blé","Code","Pied","Journal","Tour","Champ","Café","Tête","Classe","Trou","Cinéma","Flûte","Amour","Dragon","Aile","Araignée","Noir","Courant","Mouche","Place","Baguette","Afrique","Lien","Point","Citrouille","Baleine","Dinosaure","Roulette","Ange","Scène","Temple","Coton","Vampire","Canard","Amérique","Molière","Canada","Luxe","Cirque","Millionaire","Chevalier","Crochet","Machine","Bouchon","Table","Etoile","Himalaya","Paris","Chance","Roi","Ceinture","Piano","Soldat","Ballon","Lion","Papier","Banque","Pomme","Plume","Espion","Droite","Cœur","Pingouin","Héros","Cheval","Vent","Chien","Robe","Noel","Casino","Bateau","Pouce","Mort","Bûche","Microscope","Pirate","Satellite","Kangourou","Jungle","Hôtel","Pigeon","Angleterre","Or","Herbe","Temps","Restaurant","Requin","Château","Parachute","Balle","Laser","Terre","Filet","Colle","Schtroumpf","Allemagne","Tennis","Oiseau","Chausson","Pyramide","Fou","Nuit","Echelle","Hiver","Vie","Géant","Bouteille","Reine","Science","Visage","Jour","Main","Miel","Serpent","Marin","Forêt","Lait","Ecole","Gauche","Règle","Chapeau","Centre","Zéro","Cochon","Verre","Anneau","Souris","Aiguille","Sept","Chocolat","Robot","Eau","Bœuf","Docteur","Voiture","Guerre","Opéra","Génie","Cercle","Chat","Danse","Police","Atlantique","Egalité","Chine","Champagne","Coronavirus","Bière","Princesse","Fantome","Jumelles","Alien","Sorcière","Licorne","Poison","Trésor","Maladie","Bâton","Sirène","Mars","Esprit","Nain","Mode","Jeu","Histoire","Hôpital","Chasse","Egypte","Resistance","Corde","Rouge","Poisson","Livre","Branche","Œil","Maîtresse","Œuf","Lune","Moustache","Magie","Avion","Indien","Berlin","Vert","Plage","Rose","Pilote","Neige","Pétrole","Bouche","Soleil","Poulet"]

# TODO
# problèmes suivants relevés:
#

class Color(enum.IntEnum):
    """Represent a team color
    """
    RED = 1
    BLUE = 2
    DARK = 3
    NEUTRAL = 4


class TurnType(enum.Enum):
    """Represent a type of turn, either 'guess' or 'play'"""
    GUESS = enum.auto()
    PROPOSAL = enum.auto()
    GAME_OVER = enum.auto()


class Card:

    def __init__(self, t, c):
        # sanity checks
        if not isinstance(c, Color):
            raise TypeError('Given color is not of type Color:', c)

        self.text = t
        self.color = c

    def __str__(self):
        """Return text"""
        return ";".join([str(self.text), str(self.color)])


class Player:
    """Represent a player"""

    def __init__(self, player_id, name, r, c):
        # attributes forever
        if not isinstance(c, Color):
            raise TypeError('Given color is not of type Color:', c)

        self.name = name
        self.color = c
        self.role = r
        self.player_id = player_id

    def __str__(self):
        """Return id, name"""
        if self.role==1:
            role_name="spy"
        else:

            role_name="guesser"
        return ";".join([str(self.player_id), self.name, role_name, self.color.name])


class Lobby:
    """Represent a table and a running game.
    Should be able to:
    * launch a game -> fn __init__(number_of_players)
    * return a complete game status -> fn status()
    * register a player -> fn register(player)
    """

    def __init__(self, lobby_id, number_of_players):
        """Create a new game instance"""
        # attributes for keeping track of the current game
        self.players = []
        self.redCards = []
        self.blueCards = []
        self.neutralCards = []
        self.guesses = []
        self.number_of_players = number_of_players
        self.lobby_id = lobby_id


        # these values are set in the prepare_gameturn f'n
        # here, we set the default
        self.choix_premiere_equipe = random.randint(1,2)
        if self.choix_premiere_equipe == 1:
            self.current_team_color = Color.RED
        else:
            self.current_team_color = Color.BLUE

        # 0: game not started
        self.current_turn_type = None
        self.current_role = None
        self.current_number_proposal = None
        self.blue_rest = 0
        self.red_rest = 0
        self.blue_guesses_left = None
        self.red_guesses_left = None
        self.blue_wins = 0
        self.red_wins = 0
        self.red_players = 0
        self.blue_players = 0
        self.number_of_guesses = []

        # attributes for keeping track of the current gameturn
        self.current_guesse = None
        self.current_wins = []

        # full deck: will be created at beginning of each gameturn
        self.deck = []
        self.cards_order = random.sample(range(0, len(table_de_carte)), len(table_de_carte))
        # when all players join, a gameturn must be prepared and the game can start

    def generate_new_round(self):
        self.guesses[:] = []
        self.current_turn_type = None
        self.current_role = None
        self.current_number_proposal = None
        self.blue_rest = 0
        self.red_rest = 0
        self.blue_guesses_left = None
        self.red_guesses_left = None
        self.start_game()

    def generate_new_deck(self):
        """Generate a new full deck"""
        self.redCards[:] = []
        self.blueCards[:] = []
        self.neutralCards[:] = []
        self.deck[:] = []
        # shuffle deck at the beginning of gameturn

        if self.current_team_color == Color.RED:
            self.redCards = random.sample(range(0, 25), 25)
            self.killerCard = self.redCards.pop()
            for i in range(0,8):
                self.blueCards.append(self.redCards.pop())
            for i in range(0,7):
                self.neutralCards.append(self.redCards.pop())
        elif self.current_team_color == Color.BLUE:
            self.blueCards = random.sample(range(0, 25), 25)
            self.killerCard = self.blueCards.pop()
            for i in range(0,8):
                self.redCards.append(self.blueCards.pop())
            for i in range(0,7):
                self.neutralCards.append(self.blueCards.pop())

        # TODO to take random cards from a library
        # TODO to take different cards for the same game
        for value in range(0, 25):
            for i in range(0,len(self.redCards)):
                if value == self.redCards[i]:
                    self.deck.append(Card(table_de_carte[self.cards_order.pop()], Color.RED))
            for j in range(0,len(self.blueCards)):
                if value == self.blueCards[j]:
                    self.deck.append(Card(table_de_carte[self.cards_order.pop()], Color.BLUE))
            if value == self.killerCard :
                self.deck.append(Card(table_de_carte[self.cards_order.pop()], Color.DARK))
            for k in range(0,len(self.neutralCards)):
                if value == self.neutralCards[k]:
                    self.deck.append(Card(table_de_carte[self.cards_order.pop()], Color.NEUTRAL))

        self.blue_guesses_left = len(self.blueCards)
        self.red_guesses_left = len(self.redCards)

    def set_next_team_color(self):
        next_team_color = self.current_team_color
        if next_team_color == Color.RED:
            self.current_team_color = Color.BLUE
        if next_team_color == Color.BLUE:
            self.current_team_color = Color.RED

    def set_next_role(self):
        next_role = self.current_role
        if next_role == 1:
            self.current_role = 2
        if next_role == 2:
            self.current_role = 1

    def register_player(self, name, r, c):
        """Create a new player"""
        current_id = len(self.players)
        # if all players already joined
        if current_id == self.number_of_players:
            raise RuntimeError('A player is trying to join a full lobby. His name: ', name)
        # else append a new Player instance to the list of players
        # the name argument is the chosen username
        else:
            assert current_id >= 0 and current_id < self.number_of_players
            self.players.append(Player(current_id, name, r, c))


    def update_current_wins(self):
        """Update the current_wins array at the end of a turn"""
        print("team red has {} game win(s) / team blue has {} game win(s)".format(self.red_wins,self.blue_wins))

    def prepare_gameturn(self):
        """Shuffle deck, draw all cards for beginning of gameturn"""

        # shuffle deck at the beginning of gameturn
        self.generate_new_deck()
        self.current_turn_type = TurnType.PROPOSAL
        self.current_role = 1
        self.current_number_proposal = 0
        self.current_guesse = 0
        self.red_players = 0
        self.blue_players = 0
        self.number_of_guesses[:] = []
        for player in self.players:
            if player.color == Color.RED:
                self.red_players += 1
            if player.color == Color.BLUE:
                self.blue_players += 1

    def close_game(self):
        """Close a gameturn, applies life losses"""
        self.current_turn_type = TurnType.GAME_OVER

    def guess(self, player_id, team_color, team_role, given_guess):
        """Assign a guess to a player, if it's his turn"""
        if self.current_turn_type != TurnType.GUESS:
            print('It is not a guess round.')
        # is this team the current team
        elif team_color != self.current_team_color:
            print("It is not this team turn!")
        elif team_role != self.current_role:
            print("you don't have this role!")
        else:
            # if not, this is a valid guess
            out_of_guess = 0
            self.number_of_guesses.append(given_guess)

            if team_color == Color.RED:
                if len(self.number_of_guesses) < (self.red_players - 1):
                    print("il manque la supposition de certaines personnes")
                    out_of_guess = 3
                else:
                    for i in range(0, len(self.number_of_guesses)-1):
                        if self.number_of_guesses[i] != self.number_of_guesses[i+1]:
                            print("tous les joueurs n'ont pas les mêmes suppositions, celles-ci sont réinitialisées")
                            out_of_guess = 4
                    if out_of_guess == 4:
                        self.number_of_guesses[:] = []
            else:
                if len(self.number_of_guesses) < (self.blue_players - 1):
                    print("il manque la supposition de certaines personnes")
                    out_of_guess = 3
                else:
                    for i in range(0, len(self.number_of_guesses)-1):
                        if self.number_of_guesses[i] != self.number_of_guesses[i+1]:
                            print("tous les joueurs n'ont pas les mêmes suppositions, celles-ci sont réinitialisées")
                            out_of_guess = 4
                    if out_of_guess == 4:
                        self.number_of_guesses[:] = []

            if out_of_guess == 0:
                self.number_of_guesses[:]= []
                for i in range(0, len(self.guesses)):
                    if self.guesses[i] == given_guess:
                        out_of_guess = 2
                if out_of_guess == 0:
                    if given_guess < 25 and given_guess >= 0 :
                        self.guesses.append(given_guess)
                        card = self.deck[given_guess]
                        if card.color == team_color:
                            self.current_guesse += 1
                            if team_color == Color.RED:
                                self.red_guesses_left -= 1
                            if team_color == Color.BLUE:
                                self.blue_guesses_left -= 1
                            if self.red_guesses_left == 0:
                                self.red_wins += 1
                                self.update_current_wins()
                                self.close_game()
                            if self.blue_guesses_left == 0:
                                self.blue_wins += 1
                                self.update_current_wins()
                                self.close_game()
                        elif card.color == Color.DARK:
                            if team_color == Color.RED:
                                self.blue_wins += 1
                            if team_color == Color.BLUE:
                                self.red_wins += 1
                            out_of_guess = 1
                            self.update_current_wins()
                            self.close_game()
                        elif card.color == Color.NEUTRAL:
                            if team_color == Color.RED:
                                if self.current_guesse == self.current_number_proposal:
                                    self.red_rest += 1
                                else:
                                    self.red_rest += (self.current_number_proposal - self.current_guesse)
                            if team_color == Color.BLUE:
                                if self.current_guesse == self.current_number_proposal:
                                    self.blue_rest += 1
                                else:
                                    self.blue_rest += (self.current_number_proposal - self.current_guesse)
                            out_of_guess = 1
                            self.set_next_team_color()
                            self.set_next_role()
                            self.current_turn_type = TurnType.PROPOSAL
                        else:
                            if team_color == Color.RED:
                                self.blue_guesses_left -= 1
                                if self.current_guesse == self.current_number_proposal:
                                    self.red_rest += 1
                                else:
                                    self.red_rest += (self.current_number_proposal - self.current_guesse)
                            if team_color == Color.BLUE:
                                self.red_guesses_left -= 1
                                if self.current_guesse == self.current_number_proposal:
                                    self.blue_rest += 1
                                else:
                                    self.blue_rest += (self.current_number_proposal - self.current_guesse)
                            out_of_guess = 1
                            if self.red_guesses_left == 0:
                                self.red_wins += 1
                                self.update_current_wins()
                                self.close_game()
                            elif self.blue_guesses_left == 0:
                                self.blue_wins += 1
                                self.update_current_wins()
                                self.close_game()
                            else:
                                self.set_next_team_color()
                                self.set_next_role()
                                self.current_turn_type = TurnType.PROPOSAL
                    elif given_guess == 25:
                        out_of_guess = 1
                        if self.current_guesse == self.current_number_proposal:
                            if team_color == Color.RED:
                                self.red_rest += 1
                            if team_color == Color.BLUE:
                                self.blue_rest += 1
                        else :
                            if team_color == Color.RED:
                                self.red_rest += (self.current_number_proposal - self.current_guesse)
                            if team_color == Color.BLUE:
                                self.blue_rest += (self.current_number_proposal - self.current_guesse)
                        self.set_next_team_color()
                        self.set_next_role()
                        self.current_turn_type = TurnType.PROPOSAL

                    if self.current_guesse == self.current_number_proposal and out_of_guess != 1 and self.red_guesses_left != 0 and self.blue_guesses_left != 0 :
                        if team_color == Color.RED:
                            if self.red_rest == 0:
                                self.set_next_team_color()
                                self.set_next_role()
                                self.current_turn_type = TurnType.PROPOSAL
                            else :
                                self.red_rest -= 1
                        if team_color == Color.BLUE:
                            if self.blue_rest == 0:
                                self.set_next_team_color()
                                self.set_next_role()
                                self.current_turn_type = TurnType.PROPOSAL
                            else :
                                self.blue_rest -= 1
                    elif self.current_guesse > self.current_number_proposal:
                        self.set_next_team_color()
                        self.set_next_role()
                        self.current_turn_type = TurnType.PROPOSAL
                else:
                    print("ce mot a déjà été révélé")

    def propose(self, team_color, player_role, given_proposal, number):
        """Assign a proposal to the rest of the team, if it's his turn"""
        if self.current_turn_type != TurnType.PROPOSAL:
            print('It is not a proposal round.')
        # is this team the current team
        elif team_color != self.current_team_color:
            print("It is not this team turn!")
        elif player_role != self.current_role:
            print("you don't have this role!")
        # if not, this is a valid proposal
        else:
            print(given_proposal + "en" + str(number))

            self.current_number_proposal = number
            self.current_guesse = 0
            self.set_next_role()
            self.current_turn_type = TurnType.GUESS


    def start_game(self):
        """Start the game, set all necessary attributes"""

        # is the game ready
        if self.number_of_players != len(self.players):
            raise RuntimeError('Not all players have joined. Current player count:', len(self.players))

        # the game can start!
        self.prepare_gameturn()

    def status(self):
        """Return detailed status of game"""
        return {
            'game_board': [str(card) for card in self.deck],
            'players': [str(player) for player in self.players],
            'current_team_color': self.current_team_color,
            'current_turn_type': self.current_turn_type,
            'red wins : ' : self.red_wins,
            'blue wins : ': self.blue_wins,
            'red left guesses : ': self.red_guesses_left,
            'blue left guesses : ': self.blue_guesses_left,
            'red rest': self.red_rest,
            'blue rest': self.blue_rest,
        }


if __name__ == "__main__":
    # mock game for testing
    newgame = Lobby(1, 5)
    newgame.register_player('spyrouge0', 1, Color.RED)
    newgame.register_player('guessrouge1', 2, Color.RED)
    newgame.register_player('guessrouge2', 2, Color.RED)
    newgame.register_player('spybleu3', 1, Color.BLUE)
    newgame.register_player('guessbleu4', 2, Color.BLUE)
    newgame.start_game()
    while True:
        current_team_color = newgame.current_team_color
        current_role = newgame.current_role
        print("\n", newgame.status(), "\n")
        print("\nCurrent team:")
        print(str(current_team_color))
        if newgame.current_turn_type == TurnType.GUESS:
            numerojoueur = int(input('ID joueur: '))
            joueur = newgame.players[numerojoueur]
            # newgame.guess(current_team_color, current_role, int(input('Guess: ')))
            newgame.guess(joueur.player_id, joueur.color, joueur.role, int(input('Guess: ')))
            print(newgame.status())
        elif newgame.current_turn_type == TurnType.PROPOSAL:
            newgame.propose(current_team_color, current_role, str(input('proposal: ')), int(input('number: ')))
            print(newgame.status())
        else:
            print("Current turn type: {}".format(newgame.current_turn_type))
            newround = input('new game ? 1 for yes 2 for no')
            if newround == '1':
                newgame.generate_new_round()
            else:
                print(newgame.status())
                break
