from state_machine_template import *

swap_machine = state_machine('a', {'c' : array([[1, 0], [0, 1]]), 's' : array([[0, 1], [1, 0]])}, {'a'}, name_to_index={'a' : 0, 'b' : 1})
swap_machine2 = state_machine.init_from_partial_def({'s' : {'a' : 'b', 'b' : 'a'}, 'c' :{'a' : 'a', 'b' : 'b'}}, 'a', 'a')

assert swap_machine.iterative_match("s")