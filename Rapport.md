# Rapport #

Pour ce projet, nous avons réalisé 4 stratégies sur les 5 demandées mais nous avons ajouter les budgets de déplacements de la semaine 3. En effet, nous avons eu du mal à comprendre la stratégie fictious play et comment l'implémenter dans notre code. 

Dans ce rapport, nous allons observer le comportement de nos deux parties : le Parti G et le Parti D (évidemment ce projet est garanti sans influence politique et les noms sont une coincidence...)

## Pour dresser le tableau ##

Pour se faire, nous allons tester chaque stratégie l'une contre l'autre en lançant 5 campagnes différentes durant chacune 5 jours afin de pouvoir dresser un tableau nous indiquant quelle stratégie est plus efficace que laquelle.
Cela nous permettra de savoir quelle stratégie utiliser lorsque l'on connaît celle de notre adversaire.
(Vous pouvez retrouver dans le fichier annexe.md plus de détails sur la création de notre tableau)


![tableau](https://user-images.githubusercontent.com/75998812/161092700-1b340d63-cd23-4e4f-969f-6a6070e2c564.PNG)


Sur la diagonale, nous remarquons qu'il n'y a que des égalités ce qui est logique puisque les stratégies s'affrontent elle mêmes. De plus, le tableau est symétrique sur sa diagonale.

Nous remarquons que la stratégie de Meilleure Réponse domine toutes les autres stratégies. En effet, si le parti prend cette stratégie elle est garantie de ne jamais perdre contre l'autre partie (au pire une égalité dans le cas où l'autre partie a aussi pris la meilleure réponse).

De plus, il n'y a pas d'équilibre de Nash. En effet, à chaque fois l'un des deux partis à intérêt à changer de stratégie ce qui est logique car nous sommes ici dans un jeu à somme nulle. (nous n'avons pas de situation où il y aura un couple (1,1)). 

