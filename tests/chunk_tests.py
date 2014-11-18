import unittest

import numpy

from pychedelic import chunk


class fix_channel_count_Test(unittest.TestCase):
    
    def identity_test(self):
        samples = numpy.array([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]).transpose()
        numpy.testing.assert_array_equal(chunk.fix_channel_count(samples, 2), samples)

    def up_mix_test(self):
        samples = numpy.array([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]).transpose()
        up_mixed_samples = numpy.array([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9], [5, 6, 7, 8, 9]]).transpose()
        numpy.testing.assert_array_equal(chunk.fix_channel_count(samples, 3), up_mixed_samples)

    def down_mix_test(self):
        samples = numpy.array([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]).transpose()
        down_mixed_samples = numpy.array([[0, 1, 2, 3, 4]]).transpose()
        numpy.testing.assert_array_equal(chunk.fix_channel_count(samples, 1), down_mixed_samples)


class fix_frame_count_Test(unittest.TestCase):

    def identity_test(self):
        samples = numpy.array([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]).transpose()
        numpy.testing.assert_array_equal(chunk.fix_frame_count(samples, 5, 0), samples)

    def pad_test(self):
        samples = numpy.array([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]).transpose()
        padded_samples = numpy.array([[0, 1, 2, 3, 4, 22, 22], [5, 6, 7, 8, 9, 22, 22]]).transpose()
        numpy.testing.assert_array_equal(chunk.fix_frame_count(samples, 7, 22), padded_samples)

    def crop_test(self):
        samples = numpy.array([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]).transpose()
        cropped_samples = numpy.array([[0, 1, 2], [5, 6, 7]]).transpose()
        numpy.testing.assert_array_equal(chunk.fix_frame_count(samples, 3, 0), cropped_samples)