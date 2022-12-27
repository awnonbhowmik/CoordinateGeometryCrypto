import numpy as np
import numba as nb


class Encrypt:

    def __init__(self, plaintext: str, h1: int, k1: int, h2: int, k2: int, n: int) -> None:
        self.plaintext = plaintext
        self.h1 = h1
        self.k1 = k1
        self.h2 = h2
        self.k2 = k2
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

    @staticmethod
    @nb.njit()
    def _translate(cantor_points: np.ndarray, h1: int, k1: int, h2: int, k2: int) -> np.ndarray:
        for i in nb.prange(cantor_points.shape[0]):
            if i % 2 == 0:
                cantor_points[i][0] = cantor_points[i][0] + h1
                cantor_points[i][1] = cantor_points[i][1] + k1
            else:
                cantor_points[i][0] = cantor_points[i][0] + h2
                cantor_points[i][1] = cantor_points[i][1] + k2

        return cantor_points

    @staticmethod
    def _rotate(cantor_points: np.ndarray, n: int) -> np.ndarray:
        theta = n * np.pi / 2
        R = [[int(np.cos(theta)), int(-np.sin(theta))],
             [int(np.sin(theta)), int(np.cos(theta))]]

        for i in range(cantor_points.shape[0]):
            cantor_points[i] = np.matmul(cantor_points[i], R)

        return cantor_points

    def _encrypt(self) -> np.ndarray:
        cantor_points = self.get_cantor_points()
        cantor_points = self._translate(
            cantor_points=cantor_points, h1=self.h1, k1=self.k1, h2=self.h2, k2=self.k2)
        encrypted_points = self._rotate(cantor_points=cantor_points, n=self.n)

        return encrypted_points

    def get_encrypted_points(self) -> np.ndarray:
        encrypted_points = self._encrypt()

        return encrypted_points
