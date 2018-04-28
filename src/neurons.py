#-*- coding: utf-8 -*-

__author__ = 'Christophe Taillan'
__email__ = 'christophe.taillan@cnes.fr'
__version__ = ''
__date__ = '29/02/2018'
__last_modified__ = '28/04/2018'

import logging
import numpy as np

logger = logging.getLogger(__name__)

def sigmoid (x): return 1./(1 + np.exp(-x))

class Neurons():
    def __init__(self, nHidden = 64):
        """
        Constructor of the Neurons class

        Represents the "brains" of the checker player
        The neural network is composed with 3 layers :
          - nInputs input neurons
          - n hidden neurons
          - 1 output neuron
        """
        self.nHidden = nHidden
        self.nInputs = 32
        self.outputLayerSize = 1
        self.Wh = np.random.uniform(-1., 1., size=(self.nInputs, nHidden))
        self.hBias = np.random.random_integers(-10, 10, nHidden)
        self.Wz = np.random.uniform(-1., 1., size=(nHidden, self.outputLayerSize))
        self.zBias = np.random.random_integers(-10, 10, self.outputLayerSize)

    def evaluate(self, X):
        """
        Calculate values 
        :param X: vector of nInputs dimension
        :return: score of played move
        """
        H = sigmoid(np.dot(X, self.Wh) + self.hBias)
        Z = sigmoid(np.dot(H, self.Wz) + self.zBias)
        return Z

