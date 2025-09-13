'''
This file contains a template for the first homework assignment for Theory of Computation Fall 2025, Tulane University
'''
from collections import defaultdict
import copy
import itertools
import networkx as nx
import matplotlib.pyplot as plt
import time
from functools import reduce
from numpy import linalg

def compose(f1,f2):
    '''Assumes that f1 and f2 are dictionaries that represent functions.
    Returns a dictionary whose keys are those of f1 and that represents the composition of f1 and f2.'''
    return {key:f2[f1[key]] for key in f1.keys()}


class state_machine(object):
    
    def __init__(self, initial, transitions:dict, accept_states:set, **kwargs):
        '''self.name_to_index represents a mapping from strings naming each states to indices of self.v, not technically necessary but is helpful for clarity. 
        self.accept_vector is a vector s.t. accept_vector dot v != 0 only if the machine is currently in an accept state
        transitions is a dict from letters of the alphabet to matrices'''

        self.name_to_index = kwargs.get("name_to_index")
        self.index_to_name = kwargs.get("index_to_name")

        if self.name_to_index is None and self.index_to_name is not None: self.name_to_index = {v:u for u,v in self.index_to_name.items()}
        if self.name_to_index is not None and self.index_to_name is None: self.index_to_name = {v:u for u,v in self.name_to_index.items()}

        self.states = kwargs.get("states")
        if self.states is None: self.states = set(self.name_to_index.keys())

        self.alphabet = kwargs.get("alphabet")
        if self.alphabet is None: self.alphabet = set(transitions.keys())
        
        self.accept_states = accept_states
        self.transitions = transitions
        
        if type(initial) == int:
            self.v0 = initial
            self.initial = self.index_to_name[initial]
        elif type(initial) == str:
            self.v0 = self.name_to_index[initial]
            self.initial = initial
        else:
            raise TypeError("Bad type was passed to initial, must be either int or str")
        
        if type(accept_states[0]) == str:
            self.accept_vector = [1 if x in accept_states else 0 for x in range(len(self.alphabet))]
        elif type(accept_states[0]) == int:
            self.accept_vector = [1 if x in accept_states else 0 for x in range(len(self.alphabet))] #Use accept_vector dot v to see if the machine accepts
            
        self.v = [1 if x==self.v0 else 0 for x in range(len(self.alphabet))]
        
    #Operations on machines
    def iterative_match(self,input_string:str) -> bool:
        '''Assumes that the string is a string in the alphabet.
        Returns True or False, depending on whether or not the input_string is accepted.
        '''
        
        if not input_string: #if input_string is empty
            return False if linalg.dot(self.accept_vector, self.v) == 0 else True #True only if an accept state currently
        else: 
            self.v @= reduce(lambda x, y: x @ y, input_string)
            return False if linalg.dot(self.accept_vector, self.v) == 0 else True

    def complement(self):
        '''Returns the complement machine, that accepts the strings that the original machine does not accept'''
        return state_machine(self.initial, self.transitions, self.states - self.accept_states, self.name_to_index)

    def intersection(self,other):
        '''other is assumed to be a machine with the same alphabet.
        returns a machine that accepts when both self and other accept.
        
        To avoid hash issues, use the convention that the str a,b represents the tuple (a,b). 
        You can quickly recover from this using the split func'''
        assert self.alphabet == other.alphabet
        initial = self.initial + "," + other.initial
        states = itertools.product(self.states, other.states)
        accept_states = set([u+","+v for u,v in itertools.product(self.accept_states, other.accept_states)])
        
        transitions = {a : linalg.tensordot(self.transitions[a], other.transitions[a]) for a in self.alphabet}

        return state_machine(initial, transitions, accept_states, states=states) #whatever dude
        

    
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
