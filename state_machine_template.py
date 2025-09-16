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
    return {key:f2[f1[key]] for key in f1.keys()}

class state_machine(object):
    
    def __init__(self, transitions:dict, initial:str, accept_states:set):
       self.transitions = transitions
       self.initial = initial
       self.accept_states = set(accept_states)
       self.alphabet = set(transitions.keys())
       self.states = set(itertools.chain(*[x.items() for x in transitions.values()]))

       self.q = self.initial
  
    #Operations on machines
    def iterative_match(self,input_string:str) -> bool:
        '''Assumes that the string is a string in the alphabet.
        Returns True or False, depending on whether or not the input_string is accepted.
        '''
        if not input_string: #if input_string is empty
            return self.q in self.accept_states
        else:
            self.q = self.transitions[input_string[-1]][self.q]
            return self.iterative_match(input_string[:-1])    

    def complement(self):
        '''Returns the complement machine, that accepts the strings that the original machine does not accept'''
        return state_machine(self.initial, self.transitions, self.states - self.accept_states)

    def intersection(self,other):
        '''other is assumed to be a machine with the same alphabet.
        returns a machine that accepts when both self and other accept.
        '''
        init = (self.initial, other.initial)
        states = itertools.product(self.states, other.states)
        tr = {a : {s : (self.transitions[a][s[0], other.transitions[a][s[1]]]) for s in states} for a in self.alphabet.union(other.alphabet)}
        accept_states = set(itertools.product(self.accept_states, other.accept_states))
        return state_machine(tr, init, accept_states)
        
    def __str__(self):
        return "\n".join(["Initial state: ", str(self.initial), "Accept states: ", str(self.accept_states), "Transitions: ", str(self.transitions)])

    @classmethod
    def init_from_partial_def(cls,transitions,initial,accept_states):
        '''
        Assumes transitions is a dictionary of dictionaries. The keys of the outer dictionaries all of the letters of the alphabet.
            Each value of transitions is a dictionary, whose keys and values are (not necessarily all) of the states (strings) of the machine.
            initial is the initial state (a string).
            accept_states is a list of states that are accepted. Each state in accept state is assumed to have been mentioned in the transitions dictionary somewhere.

        See state_machines_examples_template.py for examples.
        '''
        
        return state_machine(transitions, initial, accept_states)
        
