#This file contains examples of finite state machines.
from state_machine_template import *
from functools import reduce
from numpy import identity, flip, pad
import random

def basic_example_state_machine():
    '''A first example provided about how to use init_from_partial_def
    '''
    return state_machine.init_from_partial_def({'1':{'zero':'one','one':'zero'}, '0':{'zero':'zero'}},'zero',['zero','one'])

def exercise_221():
    '''This example is provided for you. See Hopcroft and Ullman Exercise 2.2.1
    We label the states by three letters of d's (for diagonal) and a's, then L or R, depending on whether the marble exits at C or D
    For example, the state 'dad' corresponds to x_1= diagonal, ie. / , x_2=antidiagonal ie. \)'''
    transitions= {'A':{'dddL':'addL',
                       'ddaL':'adaL',
                       'dadL':'aadL',
                       'daaL':'aaaL',
                       'addL':'dadL',
                       'adaL':'daaL',
                       'aadL':'dddR',
                       'aaaL':'ddaR',
                       'dddR':'addL',
                       'ddaR':'adaL',
                       'dadR':'aadL',
                       'daaR':'aaaL',
                       'addR':'dadL',
                       'adaR':'daaL',
                       'aadR':'dddR',
                       'aaaR':'ddaR'},
                    'B':{'dddL':'daaL',
                         'ddaL':'dddR',
                         'dadL':'ddaR',
                         'daaL':'dadR',
                         'addL':'aaaL',
                         'adaL':'addR',
                         'aadL':'addR',
                         'aaaL':'aadR',
                         'dddR':'daaL',
                         'ddaR':'dddR',
                         'dadR':'ddaR',
                         'daaR':'dadR',
                         'addR':'aaaL',
                         'adaR':'addR',
                         'aadR':'addR',
                         'aaaR':'aadR'}}
    return state_machine.init_from_partial_def(transitions, 'dddL', [state for state in transitions['A'] if state[-1]=='R' ])

def implication_machine():
    '''
    Accepts if ((s1->s2)->s3)->... evaluates to True
    '''
    transitions = {
        'T':{'no_prev': 'prev_T',
             'prev_T':'prev_T',
             'prev_F':'prev_T'},
        'F':{'no_prev':'prev_F',
             'prev_T':'prev_F',
             'prev_F':'prev_T'}
    }
    return state_machine.init_from_partial_def(transitions, 'no_prev',['prev_T'])

def letter_counting_machine(multiple_dict={'0':2, '1':3}):
    '''Assumes that multiple_dict is a dictionary whose keys are the letters
    The values are positive integers.
    The machine accepts iff letter appears a multiple of multiple_dict[letter] many times.'''
    alphabet = multiple_dict.keys()

    def individual_machine(char, num) -> state_machine:
        tr = {a : identity(num, dtype=int) if a!=char else flip(identity(num, dtype=int), axis=1)+pad(array([[1,-1],[-1,1]], dtype=int), ((0, num-2),(num-2, 0))) for a in alphabet}
        return state_machine(initial=0, transitions=tr, accept_states={0}, num_states=num)

    machines = [individual_machine(u,v) for u,v in multiple_dict.items()]
    final = reduce(lambda a,b: a.intersection(b), machines)
    print(final)
    return final

def divisibility_machine(b,k):
    '''Returns a machine that accepts the strings of base-b that are divisible by k.
    Assumes b is between 2 and 10, k is between 2 and 20.
    The strings are read as usual with the most significant digit first from left-to-right, big endian style.
    '''
    pass