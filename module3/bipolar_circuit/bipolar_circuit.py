import math
import sympy

class BipolarCircuit(object):
    def __add__(self, other):
        if isinstance(other, BipolarCircuit):
            return Serial(self, other)
        return NotImplemented
    
    def __or__(self, other):
        if isinstance(other, BipolarCircuit):
            return Parallel(self, other)
        return NotImplemented        
    
    
    def impedance(self, freq):
        raise Exception('The impedance method shoulb implemented for the class {self.__class__.__name___}')

class Combination(BipolarCircuit):
    def __init__(self, *args):
        for item in args:
            assert isinstance(item, BipolarCircuit)
        self.args = args

    def __repr__(self):
        all_circuits = ', '.join([repr(circ) for circ in self.args])
        return f'{self.__class__.__name__}({all_circuits})'        
        
class Serial(Combination):        
    def impedance(self, freq):
        all_child_impedance = [item.impedance(freq) for item in self.args]
        return sum(all_child_impedance)
    
class Parallel(Combination):
    def impedance(self, freq):
        all_child_admittance = [1/item.impedance(freq) for item in self.args]
        return 1/sum(all_child_admittance)

class Device(BipolarCircuit):
    def __init__(self, value):
        if isinstance(value, str):
            self.value = sympy.Symbol(value)
        else:
            self.value = value

    def __repr__(self):
        return f'{self.__class__.__name__}({self.value})'

        
class Resistor(Device):
    def impedance(self, freq):
        return self.value
    
class Capacitor(Device):
    def impedance(self, freq):
        if isinstance(self.value, sympy.Symbol):
            return 1/(sympy.I*2*sympy.pi*freq*self.value)
        else:
            return 1/(1J*2*math.pi*freq*self.value)

class Inductor(Device):        
    def impedance(self, freq):
        if isinstance(self.value, sympy.Symbol):
            return (sympy.I*2*sympy.pi*freq*self.value)
        else:
            return (1J*2*math.pi*freq*self.value)

