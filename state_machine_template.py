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
from numpy import linalg, array, dot

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
        if self.states is None and self.name_to_index is not None: 
            self.states = set(self.name_to_index.keys())

        self.num_states = kwargs.get("num_states")
        if self.num_states is None and self.states is not None:
            self.num_states = len(self.states)
        
        if self.num_states is None and self.states is None:
            raise ValueError("Need to specify either number of states or set of state names")

        self.alphabet = kwargs.get("alphabet")
        if self.alphabet is None: self.alphabet = set(transitions.keys())
        
        self.accept_states = accept_states
        self.transitions = transitions
        
        if type(initial) == int and self.index_to_name is not None:
            self.v0 = initial
            self.initial = self.index_to_name[initial]
        elif type(initial) == str and self.name_to_index is not None:
            self.v0 = self.name_to_index[initial]
            self.initial = initial
        elif self.index_to_name is None and self.name_to_index is None and type(initial) == int:
            self.v0 = initial
        else:
            raise TypeError("Must specify some kind of mapping between named states and indices or else not name states")
        
        self.v = array([1 if x==self.v0 else 0 for x in range(self.num_states)])

        if all([type(x)==str for x in accept_states]):
            self.accept_vector = array([1 if self.index_to_name[x] in self.accept_states else 0 for x in range(self.num_states)])
        elif all([type(x)==int for x in accept_states]):
            self.accept_vector = array([1 if x in self.accept_states else 0 for x in range(self.num_states)]) #Use accept_vector dot v to see if the machine accepts

    #Operations on machines
    def iterative_match(self,input_string:str) -> bool:
        '''Assumes that the string is a string in the alphabet.
        Returns True or False, depending on whether or not the input_string is accepted.
        '''
        
        if not input_string: #if input_string is empty
            return False if dot(self.accept_vector, self.v) == 0 else True #True only if an accept state currently
        else: 
            self.v = self.v @ reduce(lambda x, y: x @ y, [self.transitions[a] for a in input_string])
            return False if dot(self.accept_vector, self.v) == 0 else True

    def complement(self):
        '''Returns the complement machine, that accepts the strings that the original machine does not accept'''
        return state_machine(self.initial, self.transitions, self.states - self.accept_states, num_states = self.num_states, name_to_index=self.name_to_index)

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
        
        states = set(itertools.chain(*[d.keys() for d in transitions.values()]))

        isCompletelySpecified = all(
                [set(d.keys())==states for d in transitions.values()]
            )
        
        if not isCompletelySpecified:
            assert "implied garbage state, this string is super long to prevent name collisions" not in states, "Are we serious rn"
            states.add("implied garbage state, this string is super long to prevent name collisions")

        name_to_index = {s : idx for idx, s in enumerate(states)}
        index_to_name = {v : u for u,v in name_to_index.items()}
        alphabet = transitions.keys()

        def make_transition_matrix(letter):
            transition_d = transitions[letter]
            
            matrix = [[1 if i==name_to_index[transition_d[index_to_name[idx]]] else 0 for i in range(len(states))] for idx in range(len(states))]
            
            if not isCompletelySpecified:
                impl_garbage_idx = name_to_index["implied garbage state, this string is super long to prevent name collisions"]
                impl_garbage_row = [1 if idx==impl_garbage_idx else 0 for idx in range(len(states))]
                for idx, row in enumerate(matrix):
                    if all([ele==0 for ele in row]):
                        matrix[idx] = impl_garbage_row

            return array(matrix)

        m_transitions = {a : make_transition_matrix(a) for a in alphabet}

        return state_machine(initial, m_transitions, set(accept_states), alphabet=alphabet, states=states, name_to_index=name_to_index)
        
