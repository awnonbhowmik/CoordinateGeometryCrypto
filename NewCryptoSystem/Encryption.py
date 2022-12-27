import numpy as np
import numba as nb


class Encrypt:

    def __init__(self, plaintext: str, h: int, k: int, n: int) -> None:
        self.plaintext = plaintext
        self.h = h
        self.k = k
        self.n = n

    @staticmethod
    @nb.njit()
    def _ascii_conversion(plaintext: str) -> np.ndarray:
        str_characters = list(plaintext)
        str_characters = [ord(s) for s in str_characters]
        str_array = np.array(str_characters)

        return str_array

    @staticmethod
    @nb.njit()
    def _cantor_inverse(ascii_table: np.ndarray) -> np.ndarray:
        cantor_points = np.zeros(
            shape=(ascii_table.shape[0], 2), dtype=np.int64)

        for i in nb.prange(cantor_points.shape[0]):
            n = np.floor((-1 + np.sqrt(1 + 8*ascii_table[i])) / 2)
            cantor_points[i][0] = ascii_table[i] - (0.5)*n*(n+1)
            cantor_points[i][1] = n - cantor_points[i][0]

        return cantor_points

    def get_cantor_points(self):
        ascii_table = self._ascii_conversion(self.plaintext)
        cantor_points = self._cantor_inverse(ascii_table)

        return cantor_points
