import numpy as np
import pywt
from scipy.signal import butter, filtfilt


def highpass_filter(signal, fs, cutoff=0.1, order=2):
    """
    Remove slow baseline drift using a Butterworth high-pass filter.
    """
    nyquist = fs / 2
    normalised_cutoff = cutoff / nyquist

    b, a = butter(
        order,
        normalised_cutoff,
        btype="highpass"
    )

    return filtfilt(b, a, signal)


def polynomial_detrend(signal, order=3):
    """
    Remove a polynomial estimate of the baseline drift.
    """

    x = np.linspace(-1, 1, len(signal))

    coefficients = np.polyfit(
        x,
        signal,
        order
    )

    trend = np.polyval(
        coefficients,
        x
    )

    return signal - trend


def wavelet_detrend(
    signal,
    wavelet="db4",
    level=5
):
    """
    Remove low-frequency baseline drift using
    wavelet decomposition.

    The approximation coefficients represent
    the lowest-frequency component and are removed.
    """

    coefficients = pywt.wavedec(
        signal,
        wavelet,
        level=level
    )

    # Remove the lowest-frequency approximation
    coefficients[0] = np.zeros_like(
        coefficients[0]
    )

    corrected = pywt.waverec(
        coefficients,
        wavelet
    )

    # waverec can occasionally return one extra sample
    return corrected[:len(signal)]