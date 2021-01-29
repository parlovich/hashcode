import books_scn
from unittest import TestCase


class Test(TestCase):

    def test_calc_score(self):
        data = (6,
                [1, 2, 3, 6, 5, 4],
                [
                    (2, 2, [0, 1, 2, 3, 4]),
                    (3, 1, [3, 2, 5, 0])
                 ])
        results = [
            (1, [5, 2, 3]),
            (0, [0, 1, 2, 3, 4])
        ]
        expected_score = 16
        assert expected_score == books_scn.calc_score(data, results)
