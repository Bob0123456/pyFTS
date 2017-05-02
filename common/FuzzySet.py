import numpy as np
from pyFTS import *
from pyFTS.common import Membership


class FuzzySet:
    """
    Fuzzy Set
    """
    def __init__(self, name, mf, parameters, centroid):
        """
        Create a Fuzzy Set 
        :param name: fuzzy set name
        :param mf: membership function
        :param parameters: parameters of the membership function
        :param centroid: fuzzy set center of mass
        """
        self.name = name
        self.mf = mf
        self.parameters = parameters
        self.centroid = centroid
        if self.mf == Membership.trimf:
            self.lower = min(parameters)
            self.upper = max(parameters)
        elif self.mf == Membership.gaussmf:
            self.lower = parameters[0] - parameters[1]*3
            self.upper = parameters[0] + parameters[1]*3

    def membership(self, x):
        """
        Calculate the membership value of a given input
        :param x: input value 
        :return: membership value of x at this fuzzy set
        """
        return self.mf(x, self.parameters)

    def __str__(self):
        return self.name + ": " + str(self.mf.__name__) + "(" + str(self.parameters) + ")"


def fuzzyInstance(inst, fuzzySets):
    """
    Calculate the membership values for a data point given fuzzy sets
    :param inst: data point
    :param fuzzySets: list of fuzzy sets
    :return: array of membership values
    """
    mv = np.array([fs.membership(inst) for fs in fuzzySets])
    return mv


def fuzzyInstances(data, fuzzySets):
    """
    Calculate the membership values for a data point given fuzzy sets
    :param inst: data point
    :param fuzzySets: list of fuzzy sets
    :return: array of membership values
    """
    ret = []
    for inst in data:
        mv = np.array([fs.membership(inst) for fs in fuzzySets])
        ret.append(mv)
    return ret


def getMaxMembershipFuzzySet(inst, fuzzySets):
    """
    Fuzzify a data point, returning the fuzzy set with maximum membership value
    :param inst: data point
    :param fuzzySets: list of fuzzy sets 
    :return: fuzzy set with maximum membership
    """
    mv = fuzzyInstance(inst, fuzzySets)
    return fuzzySets[np.argwhere(mv == max(mv))[0, 0]]

def getMaxMembershipFuzzySetIndex(inst, fuzzySets):
    """
    Fuzzify a data point, returning the fuzzy set with maximum membership value
    :param inst: data point
    :param fuzzySets: list of fuzzy sets 
    :return: fuzzy set with maximum membership
    """
    mv = fuzzyInstance(inst, fuzzySets)
    return np.argwhere(mv == max(mv))[0, 0]


def fuzzySeries(data, fuzzySets):
    fts = []
    for item in data:
        fts.append(getMaxMembershipFuzzySet(item, fuzzySets))
    return fts
