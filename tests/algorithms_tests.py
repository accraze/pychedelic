import numpy as np
import pylab
import unittest
import pandas as pnd
import os
dirname = os.path.dirname(__file__)

from __init__ import PychedelicTestCase, plot_opt
from pychedelic.algorithms import *
from pychedelic.sound import Sound


class Algorithms_Test(PychedelicTestCase):

    def maxima_test(self):
        x = [0, 0.5, 1, 1.5, 2, 2.5, 3]
        y = [1, 2, 1, 2, 5, 5, 3]
        result = maxima(pnd.Series(y, index=x))
        self.assertEqual(result, [2, 5])
        self.assertEqual(result.index, [0.5, 2])

        x = [0, 0.5, 1]
        y = [2, 0, -1]
        result = maxima(pnd.Series(y, index=x))
        self.assertEqual(result, [2])
        self.assertEqual(result.index, [0])
        x = [0, 0.5, 1]
        y = [-10, -2, -1]
        result = maxima(pnd.Series(y, index=x))
        self.assertEqual(result, [-1])
        self.assertEqual(result.index, [1])
        y = [-10, -1, -1]
        result = maxima(pnd.Series(y, index=x))
        self.assertEqual(result, [-1])
        self.assertEqual(result.index, [0.5])
        y = [10, 10, -1]
        result = maxima(pnd.Series(y, index=x))
        self.assertEqual(result, [10])
        self.assertEqual(result.index, [0])

        # testing take_edges
        x = [0, 0.5, 1, 1.5, 2, 2.5, 3]
        y = [78, 5, 34, 33, 1, 4, 5]
        result = maxima(pnd.Series(y, index=x), take_edges=False)
        self.assertEqual(result, [34])
        self.assertEqual(result.index, [1])

        # testing with not ordered data
        x = [0, 0.5, 1.5, 2, 2.5, 1, 3]
        y = [78, 5, 33, 1, 4, 34, 5]
        result = maxima(pnd.Series(y, index=x), take_edges=False)
        self.assertEqual(result, [34])
        self.assertEqual(result.index, [1])

    def minima_test(self):
        x = [0, 0.5, 1, 1.5, 2, 2.5, 3]
        y = [1, 1, 2, 2, 3, 5, 3]

        result = minima(pnd.Series(y, index=x))
        self.assertEqual(result, [1, 3])
        self.assertEqual(result.index, [0, 3])

        result = minima(pnd.Series(y, index=x), take_edges=False)
        self.assertEqual(result, [1])
        self.assertEqual(result.index, [0])

    def goertzel_test(self):
        # generating test signals
        SAMPLE_RATE = 44100
        WINDOW_SIZE = 1024
        t = np.linspace(0, 1, SAMPLE_RATE)[:WINDOW_SIZE]
        sine_wave = np.sin(2*np.pi*440*t) + np.sin(2*np.pi*1020*t)
        sine_wave = sine_wave * np.hamming(WINDOW_SIZE)
        sine_wave2 = np.sin(2*np.pi*880*t) + np.sin(2*np.pi*1500*t)
        sine_wave2 = sine_wave2 * np.hamming(WINDOW_SIZE)

        # Finding the FT bins where maximums should be
        def find_bin(freq):
            bins = np.fft.fftfreq(sine_wave.size, 1.0 / SAMPLE_RATE)
            for i, b in enumerate(bins[1:]):
                if b > freq:
                    if (b - freq) < (freq - bins[i]): return b
                    else: return bins[i]

        # applying Goertzel on those signals
        freqs, results = goertzel(sine_wave, SAMPLE_RATE, (400, 500),  (900, 1100))
        result_maxs = maxima(pnd.Series(get_ft_amplitude_array(results), index=freqs), take_edges=False)
        self.assertItemsEqual([find_bin(440), find_bin(1020)], result_maxs.index)

        # applying Goertzel on those signals
        freqs, results = goertzel(sine_wave2, SAMPLE_RATE, (800, 900),  (1400, 1600))
        result_maxs = maxima(pnd.Series(get_ft_amplitude_array(results), index=freqs), take_edges=False)
        self.assertItemsEqual([find_bin(880), find_bin(1500)], result_maxs.index)

    def fft_test(self):
        # TODO
        # generating test signals
        SAMPLE_RATE = 44100
        WINDOW_SIZE = 1024
        t = np.linspace(0, 1, SAMPLE_RATE)[:WINDOW_SIZE]
        sine_wave = np.sin(2*np.pi*440*t) + np.sin(2*np.pi*1020*t)
        sine_wave = sine_wave * np.hamming(WINDOW_SIZE)
        sine_wave2 = np.sin(2*np.pi*880*t) + np.sin(2*np.pi*1500*t)
        sine_wave2 = sine_wave2 * np.hamming(WINDOW_SIZE)

        freqs, results = fft(sine_wave, SAMPLE_RATE)
        times, reconstructed = ifft(results, SAMPLE_RATE)

        freqs2, results2 = fft(sine_wave2, SAMPLE_RATE)
        times2, reconstructed2 = ifft(results2, SAMPLE_RATE)

        if plot_opt:
            pylab.subplot(3, 2, 1)
            pylab.title('(1) Sine wave 440Hz + 1020Hz')
            pylab.plot(t, sine_wave)

            pylab.subplot(3, 2, 3)
            pylab.title('(1) FFT amplitude')
            pylab.plot(freqs, get_ft_amplitude_array(results), 'o')

            pylab.subplot(3, 2, 5)
            pylab.title('(1) IFFT')
            pylab.plot(times, reconstructed)

            pylab.subplot(3, 2, 2)
            pylab.title('(2) Sine wave 880Hz + 1500Hz')
            pylab.plot(t, sine_wave2)

            pylab.subplot(3, 2, 4)
            pylab.title('(2) FFT amplitude')
            pylab.plot(freqs2, get_ft_amplitude_array(results2), 'o')

            pylab.subplot(3, 2, 6)
            pylab.title('(2) IFFT')
            pylab.plot(times2, reconstructed2)

            pylab.show()

    def paulstretch_test(self):
        # generating test signals
        SAMPLE_RATE = 44100
        SIG_SIZE = 88200

        t = np.linspace(0, 10, 10 * SAMPLE_RATE)[:SIG_SIZE]
        sig = np.hstack((
            np.sin(2*np.pi*110*t[:SIG_SIZE/2]),
            np.sin(2*np.pi*1020*t[SIG_SIZE/2:])
        ))

        stretched = paulstretch(sig, SAMPLE_RATE, 2, onset_level=1.0)
        t_stretched = np.arange(0, stretched.size) * 1.0 / SAMPLE_RATE

        raw_sound = Sound.from_file(os.path.join(dirname, 'sounds/paulstretch_test_raw.wav'))
        test_sound = Sound.from_file(os.path.join(dirname, 'sounds/paulstretch_test_stretched.wav'))
        stretched = paulstretch(raw_sound[0], SAMPLE_RATE, 8.0, windowsize_seconds=0.1, onset_level=0.5)
        stretched_sound = Sound(stretched, sample_rate=SAMPLE_RATE)
        stretched_sound.to_file('stretched.wav')

        if plot_opt:
            fig, axes = pylab.subplots(nrows=3, ncols=1)
            pylab.title('Initial signal')
            raw_sound.plot(ax=axes[0])

            pylab.title('Stretched signal')
            stretched_sound.plot(ax=axes[1])

            pylab.title('Stretched signal')
            test_sound[0].plot(ax=axes[2])
            
            pylab.show()

    def smooth_test(self):
        # TODO: test
        t = np.linspace(0, 1, 44100)
        orig_data = np.cos(2 * np.pi * t * 15)
        noisy_data = orig_data + 0.5 * (np.random.random(len(t)) - 0.5)
        noisy_data = pnd.Series(noisy_data, index=t)
        smooth_data = smooth(noisy_data, window_size=50)

        if plot_opt:
            pylab.subplot(2, 1, 1)
            pylab.title('Noisy signal')
            noisy_data.plot()

            pylab.subplot(2, 1, 2)
            pylab.title('Smooth signal')
            smooth_data.plot()
            pylab.show()

    def interleaved_test(self):
        data = np.array([[1, 2, 3], [11, 22, 33], [111, 222, 333]])
        self.assertEqual(interleaved(data), [1, 2, 3, 11, 22, 33, 111, 222, 333])
        data = np.array([[1], [11], [111], [1111]])
        self.assertEqual(interleaved(data), [1, 11, 111, 1111])
        data = np.array([1, 2, 3, 4, 5, 6])
        self.assertEqual(interleaved(data), [1, 2, 3, 4, 5, 6])

    def deinterleaved_test(self):
        data = np.array([1, 2, 3, 11, 22, 33, 111, 222, 333])
        self.assertEqual(deinterleaved(data, 3), [[1, 2, 3], [11, 22, 33], [111, 222, 333]])
        data = np.array([1, 11, 111, 1111])
        self.assertEqual(deinterleaved(data, 1), [[1], [11], [111], [1111]])
        data = np.array([1, 2, 3, 4, 5, 6])
        self.assertEqual(deinterleaved(data, 1), [[1], [2], [3], [4], [5], [6]])
        self.assertRaises(ValueError, deinterleaved, np.array([1, 2, 3, 11, 22, 33, 111, 222]), 3)

    def loop_interpolate_test(self):
        SAMPLE_RATE = 44100
        SIG_SIZE = 3000

        t = np.linspace(0, 10, 10 * SAMPLE_RATE)[:SIG_SIZE]
        sig = np.hstack((
            np.sin(2*np.pi*110*t[:SIG_SIZE/2]),
            np.sin(2*np.pi*1020*t[SIG_SIZE/2:])
        ))

        

        sig
