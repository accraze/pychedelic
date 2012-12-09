import sys, os
modpath = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(modpath)
import unittest
import numpy as np


plot_opt = False


class PychedelicTestCase(unittest.TestCase):

    def assertEqual(self, first, second):
        if isinstance(first, np.ndarray) or isinstance(second, np.ndarray):
            first = np.array(first)
            second = np.array(second)
            super(PychedelicTestCase, self).assertEqual(first.shape, second.shape)
            ma = (first == second)
            if isinstance(ma, bool):
                return self.assertTrue(ma)            
            return self.assertTrue(ma.all())
        else:
            return super(PychedelicTestCase, self).assertEqual(first, second)
