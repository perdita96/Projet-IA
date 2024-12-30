from BLOCKADE.app_models.models import db, init_db 
from BLOCKADE.views import app           

if __name__ == "__main__":

    #on réinitialise la base de données de l'app dans le contexte de l'app
    with app.app_context():
        init_db()