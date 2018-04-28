#-*- coding: utf-8 -*-

__author__ = 'Christophe Taillan'
__email__ = 'christophe.taillan@cnes.fr'
__version__ = ''
__date__ = '28/02/2018'
__last_modified__ = '28/04/2018'

import os
import logging
import numpy as np
from neurons import Neurons
from random import uniform

logger = logging.getLogger(__name__)

class Player():
    def __init__(self):
        """
        Constructor of the Player class

        A player is compose in his neural network (brain) and rank. 
        """
        #: Rank of the checker player
        self.rank = 0

        #: Brain of the player
        self.neurons = Neurons()

    def evaluate(self, moves):
        """
        Calculate the score of all possible moves
        :param moves: list of possible moves
        """
        max_score = -1000
        for move in moves:
            score = self.neurons.evaluate(move)
            if score > max_score:
                max_score = score
                best_move = move
        return best_move

