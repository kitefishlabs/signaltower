import unittest
from state_machines import *

allzeros = [0 for i in range(45)]
allones = [1 for i in range(45)]
all127s = [127 for i in range(45)]
alltens = [10 for i in range(45)]


class TestStringMethods(unittest.TestCase):

    def test_init(self):
        self.assertEqual(init_grid(**{'val': 0}), allzeros)
        self.assertEqual(init_grid(**{'val': 127}), all127s)
        self.assertEqual(init_grid(), all127s)
        self.assertEqual(init_grid(**{'val': 10}), alltens)

    def test_simple(self):
        allzeros[3] = 1
        self.assertEqual(idgrid(allzeros), allzeros)
        allzeros[3] = 0
        grid = grid_allon(allzeros)
        self.assertEqual(grid_allon(grid), all127s)
        grid2 = grid_alloff(grid)
        self.assertEqual(grid2, allzeros)
        grid3 = grid_alloff(alltens)
        self.assertEqual(grid3, allzeros)
        grid4 = grid_allon(allzeros, **{'val': 10})
        self.assertEqual(grid4, alltens)

    def test_single(self):
        grid = grid_setone(allzeros, **{'i': 33, 'val': 99})
        self.assertEqual(len(grid), 45)
        for i, val in enumerate(grid):
            if i == 33:
                self.assertEqual(val, 99)
            else:
                self.assertEqual(val, 0)

    def test_add(self):
        self.assertEqual(grid_add(allzeros, **{'d': 1}), allones)
        self.assertEqual(grid_add(all127s, **{'d': 1}), all127s)
        self.assertEqual(grid_add(allzeros, **{'d': -1}), allzeros)
        self.assertEqual(grid_add(allones, **{'d': -1}), allzeros)


if __name__ == '__main__':
    unittest.main()
