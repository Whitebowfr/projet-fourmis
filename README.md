# projet-fourmis
## Instructions
Use :
> pip install taichi

Execute :
[main_menu.py](./main_menu.py)

## Description du projet
Le projet a pour but de pouvoir simuler une colonie de fourmis, ou un organisme tel que le slime. Ce projet vient de notre désir de faire une simulation avec des organismes simples donnant une simulation complexe, à la suite de la publication de cette [vidéo](https://www.youtube.com/watch?v=kzwT3wQWAHE&t=418s)
Chaque fourmi est un automate simple, qui possède trois capteurs positionnés en arc de cercle devant elle. Ces capteurs lui permettent de lire le taux de phéromones présents sur le sol (représenté par une grille) et de se diriger dans la direction avec le taux le plus élevé. Chaque fourmi laisse une trace de phéromones derrière elle, et les phéromones s’évaporent au fil du temps.
On peut trouver dans cette [recherche](https://uwe-repository.worktribe.com/output/980579) suivante de multiples exemples de simulations similaires 
Ce style de simulation ressemble à celle des boids, où plusieurs agents cohabitent dans le même environnement sans communication directe.


## Fonctionalité

Vous avez alors 3 options :
- Lancer la simulation : cela permet de lancer le programme principale de simulation des fourmis
- Changer les paramètres : ouvre une nouvelle fenêtre (composée de 2 onglets) permettant de : 
    - Modifier les paramètres de la simulation (pour cela il vous faudra vérouiller les paramètres)
    - Visualiser les paramètres
    - Enregistrer les paramètres dans un CSV
    - Charger les paramètres d'un CSV
- Créer une carte : permet de créer une carte avec de la nourriture