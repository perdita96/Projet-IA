# Projet-IA

***
Concevoir un jeu à travers une application web (Framework Flask)
Mettre en place une Intelligence Artificielle (et l’implémenter avec du Q-Learning)
***

## Technologies
- **Python** : Version 3.12
- **Flask** : Version 3.0.3
- **SQLite** : Version 3
- **SQLAlchemy**

## Installation des technologies

Pour installer les dépendances nécessaires, exécutez la commande suivante :

```bash
pip3 install -r requirements.txt
```

## Initialisation de la base de données

Avant la première utilisation du projet, il faut exécuter le script de création de la base de données :

```bash
python initDB.py
```

## Lancer le jeu

```bash
python run.py
```

## Entraînement et évaluation de l'IA

### Entraînement de l'IA

L'entraînement intensif de l'IA se fait via le script suivant :

```bash
python training.py
```
Le script entraîne l'IA sur le nombre de partie entré par l'utilisateur et fait une backup de la base de données à chaque fois que l'on met à jour l'epsilon.

### L'évaluation de l'IA 

L'évaluation de l'IA se fait en la confrontant à une IA aléatoire, via le script suivant :

```bash
python evaluate.py
```
Ce script accepte un paramètre facultatif spécifiant le nombre de parties jouées pour l'évaluation. Ce nombre doit être compris entre 50 et 10 000. Par défaut, il est fixé à 1 000.

## Collaboration
- Buret Lucien
- Desiron Anaïs
- Marchand Romain