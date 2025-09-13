from state_machine_template import *

swap_machine = state_machine('a', {'c' : array([[0,1],[1,0]])}, {'b'}, name_to_index={'a':0,'b':1})
const_reject_machine = state_machine('x', {'c' : array([[1,0],[0,1]])}, {'y'}, name_to_index={'x':0,'y':1})
const_accept_machine = state_machine('u', {'c' : array([[1,0],[0,1]])}, {'u'}, name_to_index={'u':0,'v':1})

swapT = swap_machine.intersection(const_accept_machine)
swapF = swap_machine.intersection(const_reject_machine)

assert swapT.iterative_match('ccc')
assert not swapF.iterative_match('ccc')