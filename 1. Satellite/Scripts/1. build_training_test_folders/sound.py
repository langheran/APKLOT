def PlayFinishedSound(L = 300):
    import numpy as np
    max_time = 3
    f1 = 220.0
    f2 = 224.0
    rate = 8000.0
    times = np.linspace(0,L,rate*L)
    signal = np.sin(2*np.pi*f1*times) + np.sin(2*np.pi*f2*times)
    return signal
    
sound_signal=PlayFinishedSound()
from IPython.display import Audio