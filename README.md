## Description

Le modèle Wa-Tor simule un écosystème aquatique simplifié où :
- Les **poissons** se déplacent aléatoirement et se reproduisent périodiquement
- Les **requins** chassent les poissons, consomment de l'énergie et meurent de faim s'ils ne mangent pas

L'environnement est une grille toroïdale (les bords sont connectés), permettant aux créatures de se déplacer continuellement dans toutes les directions.

## Dépendances

```
numpy
tkinter
matplotlib
```


Installation :

```bash
git clone git@github.com:NICHIKU/Wa-Tor.git
```

```bash
pip install numpy
```

```bash
pip install numpy
```

```bash
pip install PLT
```

##  Utilisation

Exécuter le fichier main.py, Entrez vos paramètres, 
Une fois cela fait et que l'interface s'ouvre,
Cliquez sur Ouvrir JSON et allez dans le dossier output du projet qui vient de se créer et sélectionnez votre simulation,
Une fois cela fait cliquer sur play.

```bash
cd mon-dossier
python3 main.py
```

##  Paramètres recommandés

Dans le fichier main.py situé dans le dossier src

```python
world = wator_planet(width=60, height=60, perc_fish=0.5, perc_shark=0.05)
```

width et height : Taille de la grille de la simulation
perc_fish et perc_shark : pourcentage de shark et de fish dans la grille lors de l'initialisation (1 étant 100%)

## Caractéristiques 
- **Reproduction** : les poissons et les requins se reproduisent à intervalles réguliers
- **Énergie** : niveau d'énergie des requins qui diminuent à chaque mouvement
- **Faim** : les requins meurt si l'énergie atteint 0
- **Chasse** : les requins peuvent manger des poissons pour regagner de l'énergie

## Mécanismes de simulation

#### Mouvement des poissons
1. Cherche une case vide adjacente
2. Si disponible, se déplace aléatoirement
4. Sinon, laisse une case vide

#### Mouvement des requins
1. Cherche un poisson adjacent en priorité
2. Si trouvé, mange le poisson et se déplace à sa position
3. Sinon, se déplace vers une case vide
4. Perd 1 point d'énergie à chaque mouvement




## Contributions

- Souhaïb : Interface graphique et liaison avec la simulation
- Edilene : Version retravaillé et approfondi de la simulation ainsi que création des UML
- Ethan : Squelette de base (class fish et shark) avec version béta de la simulation et exportation json



