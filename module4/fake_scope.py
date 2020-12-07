import numpy as np

class FakeSCPI(object):
    _record = {}
    def write(self, val):
        if ' ' in val:
            cmd, vals = val.split(' ')
            self._record[cmd] = vals
#            print('WRITE', cmd, vals)

    def ask(self, val):
        assert val[-1]=='?'
        out = self._record.get(val[:-1], '')
#        print('ASK', val,'...', out)
        return out

    ask_raw = ask

dt = 1E-4
N = 1000
array_for_test = np.sin(np.arange(N)*dt*2*np.pi*50)
yscale = .5
ymult = .5 / 2**8
yoff = 5*2**8
int_array_for_test = np.array(yoff + array_for_test/ymult, dtype=np.dtype('int16').newbyteorder('>'))
buf = int_array_for_test.data.tobytes()
#print(int_array_for_test[:10])
buf = b'#' + str(len(str(len(buf)))).encode() + str(len(buf)).encode() + buf

class FakeSCPITektronix(FakeSCPI):
    _record = {'CURVE':buf,
        'WFMO:XIN':str(dt),
        'WFMO:XZERO':'0',
        'WFMO:YMU':str(ymult),
        'WFMO:YOF':str(yoff),
        '*IDN':'TEKTRONIX,MSO3014,234234,V.34.123',
        'CH1:SCA':1}


