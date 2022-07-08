# -*- coding: utf-8 -*-

# Nicolas, 2021-03-05
from __future__ import absolute_import, print_function, unicode_literals

import random
import numpy as np
import sys
from itertools import chain
import math
from strat import *

import pygame

from pySpriteWorld.gameclass import Game,check_init_game_done
from pySpriteWorld.spritebuilder import SpriteBuilder
from pySpriteWorld.players import Player
from pySpriteWorld.sprite import MovingSprite
from pySpriteWorld.ontology import Ontology
import pySpriteWorld.glo

from search.grid2D import ProblemeGrid2D
from search import probleme




# ---- ---- ---- ---- ---- ----
# ---- Misc                ----
# ---- ---- ---- ---- ---- ----




# ---- ---- ---- ---- ---- ----
# ---- Main                ----
# ---- ---- ---- ---- ---- ----

game = Game()

def init(_boardname=None):
	global player,game
	name = _boardname if _boardname is not None else 'blottoMap'
	game = Game('./Cartes/' + name + '.json', SpriteBuilder)
	game.O = Ontology(True, 'SpriteSheet-32x32/tiny_spritesheet_ontology.csv')
	game.populate_sprite_names(game.O)
	game.fps = 5  # frames per second
	game.mainiteration()
	player = game.player


def main():

	#Valeurs necessaires a la creation de la campagne
	nbJours,iterations,stratG, stratD, typeBudg, budg = menu()

	init()


	#-------------------------------
	# Initialisation
	#-------------------------------

	nbLignes = game.spriteBuilder.rowsize
	nbCols = game.spriteBuilder.colsize


	players = [o for o in game.layers['joueur']]
	nbPlayers = len(players)
	print("Trouvé ", nbPlayers, " militants")


	#On localise tous les états initiaux (loc du joueur)
	#positions initiales des joueurs
	initStates = [o.get_rowcol() for o in players]
	print ("Init states:", initStates)

	#On localise tous les secteurs d'interet (les votants)
	#sur le layer ramassable
	goalStates = [o.get_rowcol() for o in game.layers['ramassable']]
	objectifs = goalStates
	print ("Goal states:", goalStates)


	#On localise tous les murs
	#Sur le layer obstacle
	wallStates = [w.get_rowcol() for w in game.layers['obstacle']]
	print ("Wall states:", wallStates)

	#Verification que les coordonnees sont legales
	def legal_position(row,col):
		#Une position legale est dans la carte et pas sur un mur
		return ((row,col) not in wallStates) and row>=0 and row<nbLignes and col>=0 and col<nbCols

	g =np.ones((nbLignes,nbCols),dtype=bool)  # par defaut la matrice comprend des True
	for w in wallStates:            # putting False for walls
		g[w]=False

	#Affectation des parties: les militants et leurs positions
	partieG = []
	partieD = []
	posPlayersG = []
	posPlayersD = []
	for p in players :
		row,col = p.get_rowcol()
		if col == 9 :
			partieG.append(p)
			posPlayersG.append(p.get_rowcol)
		else :
			partieD.append(p)
			posPlayersD.append(p.get_rowcol)


	#-------------------------------
	# Boucle principale de déplacements
	#-------------------------------

	#Variables pour le score de chaque jour
	posPlayers = initStates
	scoreParJourG = [0] * nbJours
	scoreParJourD = [0] * nbJours

	#Variables d'ajout ou non d'un militant sur un electeur pour stratBestAnswer
	ajoutG = 0
	ajoutD = 0

	for jour in range(nbJours) :

		#Modification des secteurs des electeurs pour chaque jour
		for o in game.layers['ramassable']:
			row = random.randint(0,nbLignes)
			col = random.randint(0,nbCols)
			while(not legal_position(row,col)):
				row = random.randint(0,nbLignes)
				col = random.randint(0,nbCols)
			o.set_rowcol(row,col)
		#Reattribution des nouveaux coordonnes aux variables necessaires
		goalStates = [o.get_rowcol() for o in game.layers['ramassable']]
		objectifs = goalStates

		#choix des stategies
		#Strategie aleatoire
		if stratG == 1 :
			goalPlayersTabG = stratRandom(len(partieG), objectifs)
		if stratD == 1 :
			goalPlayersTabD = stratRandom(len(partieD), objectifs)
		#Strategie tetue
		if stratG == 2 :
			goalPlayersTabG = stratStubborn(random.randint(0,1),len(partieG),objectifs)
		if stratD == 2 :
			goalPlayersTabD = stratStubborn(random.randint(0,1),len(partieD),objectifs)
		#Strategie stochastique expert
		if stratG == 3:
			goalPlayersTabG = stratStocha(len(partieG),objectifs)
		if stratD == 3 :
			goalPlayersTabD = stratStocha(len(partieD),objectifs)
		#Strategie meilleure reponse
		#Au premier jour, les electeurs sont affilies aleatoirement
		if stratG == 4 and jour == 0:
			goalPlayersTabG = stratRandom(len(partieG), objectifs)
		if stratD == 4 and jour == 0:
			goalPlayersTabD = stratRandom(len(partieD), objectifs)
		#Pour le reste de la campagne,on utilise la strategie meilleure reponse
		if stratG == 4 and jour != 0:
			goalPlayersTabG = stratBestAnswer(len(partieG),objectifs,goalPlayersTabG,indiceG,Gwin)
		if stratD == 4 and jour != 0:
			goalPlayersTabD = stratBestAnswer(len(partieD),objectifs,goalPlayersTabD,indiceD,Dwin)
		

		print("DEBUT DU JOUR ",jour+1)

		#Variables necessaires a chaque jour
		#Variables pour verifier si un militant est arrive a son electeur
		successG = [0]*(nbPlayers//2)
		successD = [0]*(nbPlayers//2)
		#Variables permettant de calculer le score d'un partie
		scoreG = [0]*len(objectifs)
		scoreD = [0]*len(objectifs)
		#Variables permettant de verifier le budget de
		#deplacement des militants par jour
		budgJourG = [0]*(nbPlayers//2)
		budgJourD = [0]*(nbPlayers//2)
		#Variables permettant de verifier le budget de
		#deplacement des militants pour toute la campagne
		budgFinalG = 0
		budgFinalD = 0
		#Variables permettant de savoir si un militant peut avancer
		bloqueG = [0]*(nbPlayers//2)
		bloqueD = [0]*(nbPlayers//2)
		#Creation de la grille de chemin pour chaque militant
		pathPlayersG = []
		pathPlayersD = []

		#Au 1er jour, on utilise les coordonnees initiales
		if jour == 0 :
			for i in range(nbPlayers//2) :
				pG = ProblemeGrid2D(initStates[i],goalPlayersTabG[i],g,'manhattan')
				pD = ProblemeGrid2D(initStates[i],goalPlayersTabD[i],g,'manhattan')
				pathPlayersG.append(probleme.astar(pG))
				pathPlayersD.append(probleme.astar(pD))
		#Sinon, on recupere les coordonneesde la fin du jour precedent
		else:
			for i in range(nbPlayers//2) :
				pG = ProblemeGrid2D(posPlayersG[i],goalPlayersTabG[i],g,'manhattan')
				pD = ProblemeGrid2D(posPlayersD[i],goalPlayersTabD[i],g,'manhattan')
				pathPlayersG.append(probleme.astar(pG))
				pathPlayersD.append(probleme.astar(pD))

		#Iterations par jour
		for i in range(iterations):
			#On fait bouger chaque joueur séquentiellement
			#On diviser le for en 2: un pour le partie G et un pour le partie D
			for j in range(nbPlayers//2) :
				#Pour le partie G
				#Si le militant n'a pas depasse son budget
				if (budgJourG[j] <= budg and typeBudg == 1) or (budgFinalG <= budg and typeBudg == 2):
					#Si le militant n'a pas atteint son objectif
					if successG[j] == 0:
						#On recupere les coordonnees du chemin a suivre
						#et on les attribue au militant
						row,col = pathPlayersG[j][i]
						print(pathPlayersG[j][i])
						posPlayersG[j]=(row,col)
						partieG[j].set_rowcol(row,col)
						print ("posG ",j," : " ,row,col)
						#On incremente les budgets de deplacement
						budgJourG[j]+=1
						budgFinalG+=1
						#Si le militant atteint son objectif
						if (row,col) == goalPlayersTabG[j]:
							print("le joueurG ",j," a atteint son but!")
							#On change la valeur du success
							#et incremente le score
							successG[j] = 1
							scoreG[trouverIndice((row,col),objectifs)] += 1
				#Si le militant a depasse son budget, on le bloque
				else:
					bloqueG[j] = 1
				#Pour le partie D
				#Si le militant n'a pas depasse son budget
				if (budgJourD[j] <= budg and typeBudg == 1) or (budgFinalD <= budg and typeBudg == 2):
					#Si le militant n'a pas atteint son objectif
					if successD[j] == 0:
						#On recupere les coordonnees du chemin a suivre
						#et on les attribue au militant
						row,col = pathPlayersD[j][i]
						print(pathPlayersD[j][i])
						posPlayersD[j]=(row,col)
						partieD[j].set_rowcol(row,col)
						print ("posD ",j," : " ,row,col)
						#On incremente les budgets de deplacement
						budgJourD[j]+=1
						budgFinalD+=1
						#Si le militant atteint son objectif
						if (row,col) == goalPlayersTabD[j]:
							#On change la valeur du success
							#et incremente le score
							print("le joueurD ",j," a atteint son but!")
							successD[j] = 1
							scoreD[trouverIndice((row,col),objectifs)] += 1
				#Si le militant a depasse son budget, on le bloque
				else:
					bloqueD[j] = 1
			#Si tous les militants des deux partis sont bloques,
			#on passe au jour suivant
			if 0 not in bloqueG and 0 not in bloqueD:
				break
			#Si tous les militants des deux parties ont atteint leur objectif,
			#on passe au jour suivant
			if 0 not in successG or 0 not in successD :
				break

			#On passe a l'iteration suivante du jeu
			game.mainiteration()

		#Calcul des scores de chaque jour
		finalG = 0
		finalD = 0
		#Variables verifiant que le partie a gagne sur l'electeur
		Gwin = 0
		Dwin = 0
		indiceG = 0
		indiceD = 0
		#On recupere le 1er electeur responsable de la perte du partie
		cpt = 0
		for i in range(len(objectifs)) :
			if scoreG[i] > scoreD[i] :
				#Si G a choisi la stratBestAnswer, il gagne
				if stratG == 4 and cpt == 0:
					Gwin = 1
				#Si D a choisi la stratBestAnswer, il perd
				if stratD == 4 and cpt == 0:
					Dwin = 0
					indiceD = i
				finalG += 1
				cpt = 1
			if scoreG[i] < scoreD[i] :
				#Si G a choisi la stratBestAnswer, il perd
				if stratG == 4 and cpt == 0:
					Gwin = 0
					indiceG = i
				#Si D a choisi la stratBestAnswer, il gagne
				if stratD == 4 and cpt == 0:
					Dwin
				finalD += 1
				cpt = 1

		#On ajoute les scores du jour au tableau
		scoreParJourG.append(finalG)
		scoreParJourD.append(finalD)

		#Affichage des resultats de la journee
		print("FIN DE LA JOURNEE !! VOICI LES SCORES : ")
		affiche_score(finalG, finalD)
	#Affichage des resultats de la campagne
	print("TUUUT TUUUUT FIN DES ELECTIONS, VOICI LE SCORE FINAL")
	affiche_score(sum(scoreParJourD), sum(scoreParJourG))








	pygame.quit()




	#-------------------------------









if __name__ == '__main__':
	main()
