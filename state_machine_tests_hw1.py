from unittest import TestCase
import numpy as np
from state_machine_examples_template import *
import unittest
from gradescope_utils.autograder_utils.decorators import weight, number

class CreateTests(TestCase):
    @weight(5)
    @number('1')
    def test_complement(self):
        machine= exercise_221()
        complement_machine =machine.complement()
        for test_input in itertools.product(['A','B'],repeat = 5):
            machine.iterative_match(test_input) == (not complement_machine.iterative_match(test_input))
    @weight(5)
    @number('2')
    def test_letter_counting_machine(self):
        machine1 = letter_counting_machine({'0':2, '1':3})
        def theoretical_result(test_input):
            return len([x for x in test_input if x=='0'])%2==0 and len([x for x in test_input if x =='1']) %3==0
        for test_input in itertools.product(['0','1'], repeat = 5):
            assert machine1.iterative_match(test_input) == theoretical_result(test_input)
    @weight(5)
    @number('3')
    def test_intersection(self):
        machine1 = letter_counting_machine({'0':2, '1':3})
        machine2 = letter_counting_machine({'0':3,'1':4})
        machine3 = machine1.intersection(machine2)
        for test_input in itertools.product(['0','1'],repeat = 6):
            assert machine3.iterative_match(test_input) == (machine1.iterative_match(test_input) and machine2.iterative_match(test_input))
    @weight(5)
    @number('4')
    def test_divisibility_machine(self):
        
        for b in range(2,11):
            for k in range(2,20):
                for test_num in range(100):
                    M=divisibility_machine(b,k)
                    assert M.iterative_match(np.base_repr(test_num, b)) == (test_num %k==0)

    @weight(5)
    @number('5')
    def test_implication_machines(self):
        pass

unittest.main()