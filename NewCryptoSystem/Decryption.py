import numpy as np
import numba as nb


class Decrypt:

    def __init__(self, shared_key: str, encrypted_points: np.ndarray) -> None:
        self.shared_key = shared_key
        self.encrypted_points = encrypted_points

        self._private_parameter_extractor()

    def _private_parameter_extractor(self) -> None:

        key_list = list(self.shared_key)

        digit_bit_indices = []

        current_digit_bit_index = 1

        digit_bit_indices.append(current_digit_bit_index)

        current_digit_bit_value = int(key_list[current_digit_bit_index])

        while True:

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

        parameters = []

        parity = 0

        for index, skip in zip(digit_bit_indices, digit_bit_values):
            param_start = index + 1
            param_end = index + skip + 1

            param = key_list[param_start:param_end]
            param = "".join(param)
            param = int(param)

            if parity_bit_values[parity] == 1:
                parameters.append(param)
            else:
                param = param * (-1)
                parameters.append(param)

            parity = parity + 1

        self.h1, self.k1, self.h2, self.k2, self.n1, self.n2 = parameters

    @staticmethod
    @nb.njit()
    def _translate(cantor_points: np.ndarray, h1: int, k1: int, h2: int, k2: int) -> np.ndarray:
        for i in nb.prange(cantor_points.shape[0]):
            if i % 2 == 0:
                cantor_points[i][0] = cantor_points[i][0] - h1
                cantor_points[i][1] = cantor_points[i][1] - k1
            else:
                cantor_points[i][0] = cantor_points[i][0] - h2
                cantor_points[i][1] = cantor_points[i][1] - k2

        return cantor_points

    @staticmethod
    def _rotate(cantor_points: np.ndarray, n1: int, n2: int) -> np.ndarray:
        theta_1 = n1 * np.pi / 2
        R1 = [[int(np.cos(theta_1)), int(-np.sin(theta_1))],
              [int(np.sin(theta_1)), int(np.cos(theta_1))]]

        R1_I = np.linalg.inv(R1)

        theta_2 = n2 * np.pi / 2
        R2 = [[int(np.cos(theta_2)), int(-np.sin(theta_2))],
              [int(np.sin(theta_2)), int(np.cos(theta_2))]]

        R2_I = np.linalg.inv(R2)
        for i in range(cantor_points.shape[0]):
            if i % 2 == 0:
                cantor_points[i] = np.matmul(cantor_points[i], R1_I)
            else:
                cantor_points[i] = np.matmul(cantor_points[i], R2_I)

        return cantor_points

    @staticmethod
    @nb.njit()
    def _cantor_function(cantor_points: np.ndarray) -> np.ndarray:
        ascii_values = np.zeros(cantor_points.shape[0], dtype=np.int64)

        for index, value in enumerate(cantor_points):
            ascii_values[index] = (
                0.5) * (value[0] + value[1]) * (value[0] + value[1] + 1) + value[1]

        return ascii_values

    def decrypt(self):
        cantor_points = self._rotate(
            cantor_points=self.encrypted_points, n1=self.n1, n2=self.n2)

        cantor_points = self._translate(
            cantor_points=self.encrypted_points, h1=self.h1, k1=self.k1, h2=self.h2, k2=self.k2)

        ascii_values = self._cantor_function(cantor_points=cantor_points)

        ascii_values = list(ascii_values)

        ascii_values = [chr(x) for x in ascii_values]

        plaintext = "".join(ascii_values)

        return plaintext
