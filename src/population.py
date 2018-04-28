#-*- coding: utf-8 -*-

__author__ = 'Christophe Taillan'
__email__ = 'christophe.taillan@cnes.fr'
__version__ = ''
__date__ = '28/02/2018'
__last_modified__ = '28/04/2018'

import os
import logging
from random import sample, uniform, gauss
from player import Player
from copy import copy
from statistics import median
import numpy as np

logger = logging.getLogger(__name__)


class Population:
    def __init__(self, nIndiv = 100):
        """
        Constructor of the Population class
        """
        if nIndiv%4 != 0:
            raise Exception("Number of indiv must be an integer of 4")
        self.nIndiv = nIndiv
        self.players = []
        for i in range(nIndiv):
            self.players.append(Player())
        self.scores = []

        self.cut_ratio = 0.5

    def simulate(self):
        """
        Calculate the trajectories
        """
        for player in self.players:
            #player.calculate_trajectories(xTarget, yTarget)
            player.calculate_trajectory(0.0, 0.1, xTarget, yTarget)
            self.scores.append(player.score)

    def select(self):
        """
        Select the best players
        """
        winners = []
        for i in range(int(self.nIndiv/2)):
            challengers = sample(self.players, 2)
            self.players.remove(challengers[0])
            self.players.remove(challengers[1])

            sum_scores = challengers[0].score + challengers[1].score
            prob0 = challengers[0].score / sum_scores
            prob1 = challengers[1].score / sum_scores
            al = uniform(0.,1.)
            if al < prob0 :
                winners.append(challengers[1])
            else:
                winners.append(challengers[0])

        self.players = winners

    def reproduce(self):
        """
        Take DNA from two parents to create two children
        """
        # Init lists
        list_children = []
        list_parents = copy(self.players)

        for i in range(int(self.nIndiv / 4)):
            # Choose two parents
            len(list_parents)
            parents = sample(list_parents, 2)
            list_parents.remove(parents[0])
            list_parents.remove(parents[1])
            parents[0].neurons.linearize()
            parents[1].neurons.linearize()
            # Linearize DNA
            dna_p0 = parents[0].neurons.dna
            dna_p1 = parents[1].neurons.dna
            nGenes = len(dna_p0)

            # Create 2 children
            child0 = Player()
            child1 = Player()
            child0.neurons.linearize()
            child1.neurons.linearize()
            
            # Barycenter method
            for i in range(len(dna_p0)):
                alpha = uniform(-0.5, 1.5)
                child0.neurons.dna[i] = alpha * dna_p0[i] + (1 - alpha) * dna_p1[i]
                child1.neurons.dna[i] = alpha * dna_p1[i] + (1 - alpha) * dna_p0[i]

            child0.neurons.delinearize()
            child1.neurons.delinearize()
            list_children.append(child0)
            list_children.append(child1)

        self.players = self.players + list_children

    def mutate(self, ratio=0.01):
        """
        Randomly mutate one gene to insure diversity
        """
        nMut = int(ratio * self.nIndiv)
        iMut = sample(range(self.nIndiv), nMut)
        for i in iMut:
            self.players[i].neurons.linearize()
            iDNA = sample(range(len(self.players[i].neurons.dna)), 1)
            self.players[i].neurons.dna[iDNA[0]] = self.players[i].neurons.dna[iDNA[0]] + gauss(self.players[i].neurons.dna[iDNA[0]], 2.)
            self.players[i].neurons.delinearize()

    def find_better(self):
        """
        Find the better player in the population
        :return : better player
        """
        betterPlayer = self.players[0]
        for player in self.players:
            if player.score < betterPlayer.score:
                betterPlayer = player
        return betterPlayer 

    def find_worst(self):
        """
        Find the worst player in the population
        :return : worst player
        """
        worstPlayer = self.players[0]
        for player in self.players:
            if player.score > worstPlayer.score:
                worstPlayer = player
        return worstPlayer 



