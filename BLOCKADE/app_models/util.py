from .models import Player, db
def player_exists(nickname):
    """
    Fonction qui détermine si le joueur est déjà présent dans la base de données ou non

    Préconditions:
    - 'nickname' est une chaîne de caractères représentant le pseudo d'un joueur.
    - La base de données est accessible via 'db.session'.
    - Il faut que la fonction ait accès au modèle Player

    Postconditions:
    - Retourne True si un joueur avec ce pseudo existe dans la base de données.
    - Retourne False si aucun joueur avec ce pseudo n'est trouvé.
    """

    return True if db.session.query(Player).filter_by(nickname=nickname).first() else False

def add_player(nickname): 
    """
    Fonction qui ajoute un joueur dans la base de données

    Préconditions:
    - 'nickname' doit être une chaîne de caractères qui n'existe pas encore dans la base de données.
    - La base de données est accessible via 'db.session'.
    - Il faut que la fonction ait accès au modèle Player

    Postconditions:
    - Un nouveau joueur est ajouté à la base de données.
    """
    new_player = Player(is_human = (nickname != 'IA' and nickname != 'Alice'), nickname=nickname) 
    db.session.add(new_player)  
    db.session.commit()

def id_searched_player(nickname):
    """

    Fonction qui retourne l'id d'un joueur sur base de son pseudo

    Préconditions:
    - 'nickname' doit être une chaîne de caractères représentant un pseudo existant dans la base de données.
    - La base de données est accessible via 'db.session'.
    - Il faut que la fonction ait accès au modèle Player

    Postconditions:
    - Retourne l'ID ('player_id') du joueur correspondant au pseudo.
    """
    return db.session.query(Player).filter_by(nickname=nickname).first().player_id