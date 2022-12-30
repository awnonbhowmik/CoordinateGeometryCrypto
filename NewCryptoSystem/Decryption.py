import numpy as np
import numba as nb


class Decrypt:

    def __init__(self, shared_key: str, encrypted_points: np.ndarray) -> None:
        self.shared_key = shared_key
        self.encrypted_points = encrypted_points

        self._private_parameter_extractor(self.shared_key)

    def _private_parameter_extractor(self) -> None:

        key_list = list(self.shared_key)

        digit_bit_indices = []

        current_digit_bit_index = 1

        digit_bit_indices.append(current_digit_bit_index)

        current_digit_bit_value = int(key_list[current_digit_bit_index])

        while True:

            print(digit_bit_indices)

            try:
                current_digit_bit_index = current_digit_bit_index + current_digit_bit_value + 2

                current_digit_bit_value = int(
                    key_list[current_digit_bit_index])

                digit_bit_indices.append(current_digit_bit_index)
            except:
                break

        parity_bit_indices = [x-1 for x in digit_bit_indices]

        parity_bit_values = [int(key_list[x]) for x in parity_bit_indices]

        digit_bit_values = [int(key_list[x]) for x in digit_bit_indices]

        parameter = []

        parity = 0

        for index, skip in zip(digit_bit_indices, digit_bit_values):
            param_start = index + 1
            param_end = index + skip + 1

            param = key_list[param_start:param_end]
            print(param)
            param = "".join(param)
            param = int(param)

            if parity_bit_values[parity] == 1:
                parameter.append(param)
            else:
                param = param * (-1)
                parameter.append(param)

            parity = parity + 1

        self.h1, self.k1, self.h2, self.k2, self.n1, self.n2 = parameter
