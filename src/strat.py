import random
import numpy as np
import sys
import math


# Utilitaires
#Fonction d'affichage de scores
def affiche_score(finalG,finalD) :
    print("partie G : ", finalG, " VS partie D : ",finalD)
    if finalG > finalD :
        print("VICTOIRE DU PARTIE G")
    if finalG < finalD :
        print("VICTOIRE DU PARTIE D")
    if finalG == finalD :
        print("Pas de gagnant")
#Fonction pour l'affichage du menu
def menu():
    print("BIENVENU SUR LA CAMPAGNE ELECTORALE ENTRE LES PARTIES G ET D")
    jours = int(input("Sur combien de jours la campagne doit elle durer ?"))
    iteration = int(input("Avec combien d'iterations ?"))
    print("Voici les differentes stratégies possible:")
    print("1. aleatoire")
    print("2. têtu")
    print("3. stochastique expert")
    print("4. meilleure reponse")
    stratG = int(input("Quel est votre choix pour G ?"))
    
    #Si la strategie choisie n'existe pas
    if stratG not in [1,2,3,4]:
        print("ERROR: merci de choisir une strategie existante pour G.")
        stratG = int(input("Quel est votre choix pour G ?"))
    stratD = int(input("Et pour D ?"))
    if stratD not in [1,2,3,4]:
        print("ERROR: merci de choisir une strategie existante pour D.")
        stratD = int(input("Quel est votre choix pour G ?"))
    print("Voici les deux types de budget de deplacement possible:")
    print("1. Budget fixe par jour")
    print("2. Budget pour toute la campagne")
    typeBudg = int(input("Quel type de budget de deplacement souhaitez vous ?"))
    budg = int(input("Avec combien comme budget ?"))

    return jours,iteration,stratG,stratD,typeBudg,budg
#Fonction trouver l'indice de l'element elem dans la liste
def trouverIndice(elem, liste):
    for i in range(len(liste)):
        if elem == liste[i]:
            return i
    return 0


# Fonctions permettant la mise en place des differentes strategies

#Autant de militant sur chaque electeur
#exemple = (2,2,2,1,1)
def stratEqual(nbPlayers, objectifs) :
    goalPlayersTab = []
    #Nombre de militants sur un electeur
    cible = math.ceil(nbPlayers / len(objectifs))
    cpt = 0
    for i in range(len(objectifs)) :
            for j in range(cible):
                cpt += 1
                if cpt > nbPlayers :
                    return goalPlayersTab
                goalPlayersTab.append(objectifs[i])

    return goalPlayersTab

#meme stategie que stratEqual sauf qu'un electeur n'a jamais de militant
#exemple = (2,2,2,1,0)
def stratZero(nbPlayers, objectifs):
    #Nombre de militants sur un electeur
    cible = math.ceil(nbPlayers / (len(objectifs)-1))
    goalPlayersTab = []
    cpt = 0
    for i in range(len(objectifs)) :
            for j in range(cible):
                cpt += 1
                if cpt > nbPlayers :
                    return goalPlayersTab
                goalPlayersTab.append(objectifs[i])
    goalPlayersTab.append(goalPlayersTab[0])
    return goalPlayersTab

#les electeurs ont un seul militant et l'electeur restant a ce qui reste
#exemple = (3,1,1,1,1)
def stratAllOne(nbPlayers,objectifs):
    goalPlayersTab = []
    cibleOne = len(objectifs) - 1
    cpt = nbPlayers
    for i in range(nbPlayers):
        if i < cibleOne:
            goalPlayersTab.append(objectifs[i])
        else:
            goalPlayersTab.append(objectifs[-1])
    return goalPlayersTab

#les electeurs ont 3 militants et les electeurs ont ce qui restent
#exemple = (3,3,1,0,0)
def strat3Musketeers(nbPlayers,objectifs):
    goalPlayersTab = []
    cible = 3
    cpt = 0
    for i in range(nbPlayers):
        for j in range(cible):
            if cpt >= nbPlayers:
                break
            goalPlayersTab.append(objectifs[i])
            cpt += 1
    return goalPlayersTab

#Differentes strategies
#Strategie aleatoire
def stratRandom(nbPlayers, objectifs) :
    goalPlayersTab = []
    for i in range(nbPlayers) :
        val = random.randint(0,len(objectifs)-1)
        goalPlayersTab.append(objectifs[val])
    return goalPlayersTab


#Strategie tetue
def stratStubborn(choix,nbPlayers, objectifs) :
    # strategie random
    if choix == 0 :
        return stratRandom(nbPlayers, objectifs)
    #autant de militant sur chaque electeur
    if choix == 1 :
        return stratEqual(nbPlayers,objectifs)

#Strategie stochastique expert
#En focntion de la probabilite tiree, on choisit une strategie
def stratStocha(nbPlayers,objectifs):
    p = random.random()
    if p < 0.25 :
        return stratEqual(nbPlayers,objectifs)
    if p >= 0.25 and p < 0.35 :
        return stratZero(nbPlayers,objectifs)
    if p >= 0.35 and p < 0.65:
        return stratAllOne(nbPlayers,objectifs)
    else:
        return strat3Musketeers(nbPlayers,objectifs)



#Strategie meilleure reponse
#Si le partie a perdu, on ajoute un militant sur l'electeur qui a fait perdre
def stratBestAnswer(nbPlayers,objectifs,goalPlayersTab,indice,success):
    if success == 0:
        militant = random.randint(0,nbPlayers-1)
        goalPlayersTab[militant] = objectifs[indice]

    return goalPlayersTab
