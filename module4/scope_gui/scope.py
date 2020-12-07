import numpy as np

class SCPI(object):
    def __init__(self, instr):
        self._instr = instr

    def scpi_ask(self, cmd):
        cmd = cmd if cmd.endswith('?') else cmd + '?'
        return self._instr.ask(cmd)

    def scpi_write(self, cmd, *args):
        """ Execute a SCPI command

        for example :
        inst.scpi_write('FREQ', 1234)
        """
        arg_str = ','.join(str(elm) for elm in args)
        self._instr.write(cmd + ' ' + arg_str)

    def scpi_ask_for_float(self, cmd):
        """Ask an convert to float"""
        out = self.scpi_ask(cmd)
        try : 
            return float(out)
        except ValueError:
            raise Exception(f'Cannot convert {out!r} to float')
        
class TektronixScope(SCPI):
    def get_idn(self):
        return tuple(self.scpi_ask('*IDN?').split(','))
    
    idn = property(get_idn)
    
    def get_channel_scale(self, channel_number):
        # CH1:SCA?
        cmd = f"CH{channel_number}:SCA?"
        return self.scpi_ask_for_float(cmd)
    
    def set_channel_scale(self, channel_number, value):
        # CH1:SCA xx
        cmd = f"CH{channel_number}:SCA"
        self.scpi_write(cmd, value)
        
    @property
    def channel1_scale(self):
        return self.get_channel_scale(1)
    
    @channel1_scale.setter
    def channel1_scale(self, value):
        self.set_channel_scale(1, value)
        
    @property
    def vertical_offset(self):
        return self.scpi_ask_for_float('WFMO:YOF')

    @property
    def vertical_multiplication_factor(self):
        return self.scpi_ask_for_float('WFMO:YMU')

    @property
    def horizontal_increment(self):
        return self.scpi_ask_for_float('WFMO:XIN')

    @property
    def horizontal_zero(self):
        return self.scpi_ask_for_float('WFMO:XZERO')
    
    def get_waveform(self):
        data = self._instr.ask_raw('CURVE?')
        header_length = int(data[1:2])
        header = data[2:2+header_length]
        array_size = int(header)
        data = data[2 + header_length:2 + header_length + array_size ]
        data =  np.frombuffer(data, dtype=np.dtype('int16').newbyteorder('>'))        
        horizontal_axis = np.arange(len(data))*self.horizontal_increment + self.horizontal_zero
        return horizontal_axis, (data-self.vertical_offset)*self.vertical_multiplication_factor
        
