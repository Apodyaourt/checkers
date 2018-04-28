#-*- coding: utf-8 -*-

__author__ = 'Christophe Taillan'
__email__ = 'christophe.taillan@cnes.fr'
__version__ = ''
__date__ = '28/04/2018'
__last_modified__ = '28/04/2018'

import os
import logging
import numpy as np
from neurons import Neurons
from copy import copy

logger = logging.getLogger(__name__)

class Board():
    def __init__(self):
        """
        Constructor of the Board class

        The board of the checkers game is composed in 100 tiles.
        Only 50 tiles are used : 1 of 2.
        1 refers at white pawns
        2 refers at black pawns
        """
        #: Current state of the checker board
        self.state = np.zeros(50)
        self.state[0:20] = 1 
        self.state[30:] = 2 

    def get_moves(self, color):
        """
        Return the list of all possible states from the current state
        for the white or black player
        :param color: color of the player 'white' or 'black'
        """
        if color == 'white':
            vpawn = 1
            vop = 2
        elif color == 'black':
            vpawn = 2
            vop = 1
        else:
            raise ValueError("The color must be 'white' or 'black'")

        # Check all possible moves for all pawns
        moves = []
        taken = False
        for i in range(len(self.state)):
            if self.state[i] == vpawn:
                indexes = self._get_indexes(i) 
                # If there is an opponent, the pawn must take it if able
                for j in indexes:
                    tile = i + j
                    while self.state[tile] == vop:
                        op_indexes = self._get_indexes(tile)
                        taken = True

                # If empty and any can be taken, the pawn can move to the tile
                if not taken:
                    for j in indexes:
                        if self.state[i+j] == 0:
                            move = copy(self.state)
                            move[i] = 0 
                            move[i+j] = vpawn
                            moves.append(move) 
                        
        return moves

    def _get_indexes(self, i):
        """
        Get possible neighbor tiles
        :return : indexes to move in the state vector
        """
        if i == 0:
            indexes = [5]
        elif i == 49:
            indexes = [-5]
        elif i in [1, 2, 3, 4]:
            indexes = [4, 5]
        elif i in [45, 46, 47, 48]:
            indexes = [-5, -4]
        elif i in [9, 19, 29, 39, 10, 20, 30, 40]:
            indexes = [-5, 5]
        elif i in [11, 12, 13, 14, 21, 22, 23, 24, 31, 32, 33, 34, 42, 43, 44]:
            indexes = [-6, 5, 4, 5]
        else:
            indexes = [-5, -4, 5, 6]

        return indexes

