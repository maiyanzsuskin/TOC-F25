'''
This file contains a template for the first homework assignment for Theory of Computation Fall 2025, Tulane University
'''
from collections import defaultdict
import copy
import itertools
import networkx as nx
import matplotlib.pyplot as plt
import time
from itertools import product, chain

def compose(f1,f2):
    '''Assumes that f1 and f2 are dictionaries that represent functions.
    Returns a dictionary whose keys are those of f1 and that represents the composition of f1 and f2.'''
    return {key:f2[f1[key]] for key in f1.keys()}


class state_machine(object):
    
    def __init__(self, Q, q0, delta:dict, sigma:set, accept_states:dict):
        '''Q is the states, q0 is the inital state, delta is the transition function, sigma is the alphabet
        delta := dict[letters: dict[states, states]]
        accept states = {q:True if q is an accept state else q:False for q in Q}'''
        assert q0 in Q, "q0 not in Q!"
        assert all([d in sigma for d in delta.keys()]), "Key in delta not in sigma!"
        self.Q = Q
        self.q = q0
        self.sigma = sigma
        self.delta = delta
        
        #TODO: Initialize in any way you see fit.
       
    #Operations on machines
    def iterative_match(self,input_string:str) -> bool:
        '''Assumes that the string is a string in the alphabet.
        Returns True or False, depending on whether or not the input_string is accepted.
        '''
        if not input_string: #if input_string is empty
            return self.accept_states[self.q] #True only if an accept state currently
        else: 
            self.q = self.delta[input_string[0]][self.q]
            return self.iterative_match(input_string[1:])

    def complement(self):
        '''Returns the complement machine, that accepts the strings that the original machine does not accept'''
        return state_machine(self.Q, self.q0, self.delta, self.sigma, {q : not self.accept_states[q] for q in self.Q})

    def intersection(self,other):
        '''other is assumed to be a machine with the same alphabet.
        returns a machine that accepts when both self and other accept.'''
        alphabet = product(self.sigma, other.sigma)
        delta = {a : {(u,v) : (self.delta[a][u], other.delta[a][v]) for u,v in product(self.Q, other.Q)} for a in alphabet}
        accept_states = {(u,v) : u and v for u,v in product(self.Q, other.Q)}
        return state_machine(product(self.Q, other.Q), (self.q0, other.q0), delta=delta, sigma=alphabet, accept_states=accept_states)
    
    def union(self, other):
        return self.complement().intersection(other.complement()).complement()
    
    @classmethod
    def init_from_partial_def(cls,transitions,initial,accept_states):
        '''
        Assumes transitions is a dictionary of dictionaries. The keys of the outer dictionaries all of the letters of the alphabet.
            Each value of transitions is a dictionary, whose keys and values are (not necessarily all) of the states (strings) of the machine.
            initial is the initial state (a string).
            accept_states is a list of states that are accepted. Each state in accept state is assumed to have been mentioned in the transitions dictionary somewhere.

        See state_machines_examples_template.py for examples.
        '''
        states = set(chain([x.keys() for x in transitions.values()]))
        
        return state_machine(states, initial, transitions, transitions.keys(), {q : q in accept_states for q in states})   
