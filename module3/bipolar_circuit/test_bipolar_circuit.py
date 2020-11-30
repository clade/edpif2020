import unittest
import math
import sympy
from sympy import Symbol

from bipolar_circuit import Resistor, Capacitor, Inductor, Serial, Parallel

class TestBipolarCircuit(unittest.TestCase):
    def test_resistor(self):
        R1 = Resistor(10)
        self.assertEqual(repr(R1), "Resistor(10)")
        self.assertEqual(R1.impedance(10), 10)

    def test_capacitor(self):
        C1 = Capacitor(1)
        self.assertEqual(C1.impedance(10), 1/(10*math.pi*2J))

    def test_parallel(self):
        R1 = Resistor(1)
        R2 = Resistor(10)        
        R = R1|R2
        self.assertTrue(isinstance(R, Parallel))
        self.assertEqual(R.impedance(10), 1/(1/10 + 1))

class TestBipolarCircuitSympy(unittest.TestCase):
    def test_capacitor(self):
        C1 = Capacitor(Symbol('C1'))
        omega = Symbol('omega')
        self.assertEqual(C1.impedance(freq=omega/(2*sympy.pi)), 1/sympy.I/omega/Symbol('C1'))

    def test_init(self):
        C1 = Capacitor('C1')
        self.assertEqual(C1.value, Symbol('C1'))
#R1 = Resistor(1)
#R2 = Resistor(10)
#R3 = Resistor(10)


#assert repr(R1)== "Resistor(1)"

#assert R1.impedance(10)==1

#assert (R1+R2).impedance(10)==11
#assert (R3|R2).impedance(10)==5


