# projet-fourmis
## Instructions
Use :
> pip install taichi

Execute :
[main_menu.py](./main_menu.py)

## Description du projet
Le projet a pour but de pouvoir simuler une colonie de fourmis, ou un organisme tel que le slime. Ce projet vient de notre désir de faire une simulation avec des organismes simples donnant une simulation complexe, à la suite de la publication de cette [vidéo : __Complex behaviour from Simple Rules : 3 simulations__ de Sebastian Lague](https://www.youtube.com/watch?v=kzwT3wQWAHE&t=418s)
Chaque fourmi est un automate simple, qui possède trois capteurs positionnés en arc de cercle devant elle. Ces capteurs lui permettent de lire le taux de phéromones présents sur le sol (représenté par une grille) et de se diriger dans la direction avec le taux le plus élevé. Chaque fourmi laisse une trace de phéromones derrière elle, et les phéromones s’évaporent au fil du temps.
On peut trouver dans cette [recherche](https://uwe-repository.worktribe.com/output/980579) de multiples exemples de simulations similaires.
Ce style de simulation ressemble à celle des *boids*, où plusieurs agents cohabitent dans le même environnement sans communication directe.


## Fonctionalités
Après ouverture du menu, vous avez 3 options :
- Lancer la simulation : cela permet de lancer le programme principale de simulation des fourmis
- Changer les paramètres : ouvre une nouvelle fenêtre (composée de 2 onglets) permettant de : 
    - Modifier les paramètres de la simulation (pour cela il vous faudra vérouiller les paramètres)
    - Visualiser les paramètres
    - Enregistrer les paramètres dans un CSV
    - Charger les paramètres d'un CSV
- Créer une carte : permet de créer une carte avec de la nourriture

## Algorithmie
Ce projet déploie de nombreux algorithmes complexes pour améliorer le comportement de base des fourmis, pour l'affiche et autres.
Le projet était, à la base, prévu entièrement sur tkinter. En revanche, dû à la faible vitesse d'actualisation des canvas en les adressant pixels à pixels et même la lenteur de la simulation, cette idée a étée abandonnée. Nous nous sommes mis à la recherche d'alternatives, et nous avons trouvé un projet nommé [taichi-lang](https://www.taichi-lang.org/). Ce projet, né du MIT, permet de paralléliser des calculs sur les carte graphique. Il requiert en revanche beaucoup d'apprentissage, mais permet d'obtenir plusieurs centaines d'images par seconde, à comparer avec les 17 secondes par image de la version tkinter.

## Implication

- Adam GUGLIELMINO: 35 %
- Enzo RIVIERE : 15 %
- Clémentin GRANIER : 35 %
- Louis CHARDIN : 15 %