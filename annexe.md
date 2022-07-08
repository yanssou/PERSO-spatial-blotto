## Fichier montrant un peu plus en détails la création de notre tableau ##

### Aléatoire contre Aléatoire ###

Lorsque nous adoptons une stratégie aléatoire pour les deux partis, nous remarquons que nous avons une égalité parfaite entre les deux partis ce qui n'est pas surprenant car en ayant des déplacements aléatoires, les scores se stabilisent.

partiG : 1 0 0 1 0

partiD : 0 0 1 0 0

Nous mettrons donc dans notre tableau :(partiG : Random, partiD : Random)-> (0,0) 

### Aléatoire contre Têtu ###

partiG : 1 1 0 1 1 

partiD : 0 0 1 0 0

Ici, nous remarquons que la stratégie aléatoire semble plus efficace contre la stratégie têtue. Nous mettrons donc dans notre tableau : (partiG : Random, partiD : Têtu) -> (1,0)

### Aléatoire contre Stochastique Expert ###

partiG : 1 1 0 0 0
 
partiD : 0 0 1 1 0

Nous remarquons que la stratégie stochastique expert est à egalité avec la stratégie aléatoire et les scores se stabilisent avec le temps donc :

(partiG : Random, partiD : Stochastique) -> (0,0)

### Aléatoire contre Meilleure Réponse ###

partiG : 0 0 0 0 0

partiD : 1 1 1 1 1

Ici, la stratégie meilleure réponse domine complétement la stratégie aléatoire. En effet, le parti D n'a perdu aucune des campagnes ce qui est logique puisque ce dernier s'adapte à ce que le partiG a jouer :

(partiG : Random, partiD : Meilleure Réponse) -> (0,1)

### Têtu contre Têtu ###

partiG : 0 0 1 1 0

partiD : 0 1 0 0 1

Cette fois, nous remarquons une égalité entre les deux partis donc :

(partiG : Têtu, partiD : Têtu) -> (0,0)

### Têtu contre Stochastique Expert ###

partiG : 1 0 1 1 0

partiD : 0 1 0 0 1

La stratégie Têtue est meilleure que la stochastique de peu 

(partiG : Têtu, partiD : Stochastique) -> (1,0)

### Têtu contre Meilleure Réponse ###

partiG : 0 0 0 0 0

partiD : 0 1 1 1 1

Une fois de plus, la stratégie meilleure réponse est meilleure :

(partiG : Têtu, partiD : Meilleure Réponse) -> (0,1)

### Stochastique Expert contre Meilleure Réponse ###

partiG : 0 1 0 0 0

partiD : 0 0 1 1 1

La stratégie Meilleure Réponse est meilleure que Stochastique Expert :

(partiG : Stochastique, partiD : Meilleure Réponse) -> (0,1)

### Stochastique Expert contre Stochastique Expert ###

partiG : 0 1 0 1 0

partiD : 1 0 1 0 1

Ici, même si c'est le partiD qui est censé gagner, nous remarquons que les victoires se font successivement. Nous allons donc supposer qu'il y a une égalité :

(partiG : Stochastique, partiD : Stochastique) -> (0,0)

### Meilleure Réponse contre Meilleure Réponse ###

partiG : 0 0 1 0 0

partiD : 1 1 0 1 1

Ici, c'est le partiD qui gagne mais en se basant que le concept de la meilleure réponse, on en déduit que si notre campagne durerait un nombre de jours très grand, il n'y aurait pas de vainqueur car à chaque fois l'un s'adapte à l'autre. Nous allons donc mettre : 

(partiG : Meilleure Réponse, partiD : Meilleure Réponse) -> (0,0)


## Nous pouvons désormais dresser notre tableau afin d'avoir un meilleur visuel sur les stratégies et leur efficacité ##





