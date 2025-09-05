'''
This file contains a template for the first homework assignment for Theory of Computation Fall 2025, Tulane University
'''
from collections import defaultdict
import copy
import itertools
import networkx as nx
import matplotlib.pyplot as plt
import time

def compose(f1,f2):
    '''Assumes that f1 and f2 are dictionaries that represent functions.
    Returns a dictionary whose keys are those of f1 and that represents the composition of f1 and f2.'''
    return {key:f2[f1[key]] for key in f1}


class state_machine(object):
    
    def __init__(self,args):
        #TODO: Initialize in any way you see fit.
        pass
    #Operations on machines
    def iterative_match(self,input_string):
        '''Assumes that the string is a string in the alphabet.
        Returns True or False, depending on whether or not the input_string is accepted.
        '''
        pass
    def complement(self):
        '''Returns the complement machine, that accepts the strings that the original machine does not accept'''
        pass

    def intersection(self,other):
        '''other is assumed to be a machine with the same alphabet.
        returns a machine that accepts when both self and other accept.'''
        pass
    
    @classmethod
    def init_from_partial_def(cls,transitions,initial,accept_states):
        '''
        Assumes transitions is a dictionary of dictionaries. The keys of the outer dictionaries all of the letters of the alphabet.
            Each value of transitions is a dictionary, whose keys and values are (not necessarily all) of the states (strings) of the machine.
            initial is the initial state (a string).
            accept_states is a list of states that are accepted. Each state in accept state is assumed to have been mentioned in the transitions dictionary somewhere.

        See state_machines_examples_template.py for examples.
        '''
        pass    
