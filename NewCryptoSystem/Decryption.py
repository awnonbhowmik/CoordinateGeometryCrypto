import numpy as np
import numba as nb

class Decrypt:

    def __init__(self, shared_key: str, encrypted_points: np.ndarray) -> None:
        self.shared_key = shared_key
        self.encrypted_points = encrypted_points
        
        self._private_parameter_extractor(self.shared_key)
    
    def _private_parameter_extractor(self) -> None:

        # This code may become too complex, think of simpler strategies

        parity_bits = self.shared_key[::2]
        pre_parameters = self.shared_key[1::2]

        parameters = []
        for parity, param in zip(parity_bits, pre_parameters):
            
            if parity == 1:
                parameters.append(int(param))
            else:
                parameters.append(int(param) * (-1))

        self.h1, self.k1, self.h2, self.k2, self.n1, self.n2 = parameters

    
    

    