from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
import obspy
from obspy.signal.trigger import classic_sta_lta, trigger_onset
from scipy.signal import correlate

def load_normalized_trace(filename):
    """
    Read the first trace from a waveform file and normalize it to zero mean
    and unit standard deviation.

    Parameters
    ----------
    filename : str or Path
        Input waveform file.

    Returns
    -------
    obspy.Trace
        A copied and normalized ObsPy trace.
    """
    filename = Path(filename)

    if not filename.exists():
        raise FileNotFoundError(f"Waveform file not found: {filename}")

    trace = obspy.read(str(filename))[0].copy()

    signal = np.asarray(trace.data, dtype=np.float64)
    signal = signal - np.mean(signal)

    signal_std = np.std(signal)
    if signal_std == 0:
        raise ValueError("The input trace has zero standard deviation.")

    trace.data = (signal / signal_std).astype(np.float32)
    return trace

def run_sta_lta(trace, sta_seconds, lta_seconds, threshold_on, threshold_off):
    """
    Compute the classic STA/LTA characteristic function and trigger windows.

    Parameters
    ----------
    trace : obspy.Trace
        Input waveform trace.
    sta_seconds : float
        Short-term average window length in seconds.
    lta_seconds : float
        Long-term average window length in seconds.
    threshold_on : float
        Trigger-on threshold.
    threshold_off : float
        Trigger-off threshold.

    Returns
    -------
    cft : numpy.ndarray
        STA/LTA characteristic function.
    trigger_windows : numpy.ndarray
        Trigger windows in sample indices, with shape (N, 2).
    """
    sampling_rate = trace.stats.sampling_rate

    nsta = max(1, int(round(sta_seconds * sampling_rate)))
    nlta = max(1, int(round(lta_seconds * sampling_rate)))

    if nlta <= nsta:
        raise ValueError("The LTA window must be longer than the STA window.")

    if nlta >= trace.stats.npts:
        raise ValueError("The LTA window must be shorter than the trace.")

    cft = classic_sta_lta(trace.data, nsta, nlta)
    trigger_windows = trigger_onset(cft, threshold_on, threshold_off)

    return cft, trigger_windows

def add_gaussian_noise(trace, noise_level, random_seed=1):
    """
    Add zero-mean Gaussian noise to a normalized waveform.

    Parameters
    ----------
    trace : obspy.Trace
        Input waveform trace. The input trace is not modified.
    noise_level : float
        Noise standard deviation relative to the standard deviation of the
        normalized signal. For a normalized trace, noise_level=1 means the
        noise RMS is approximately equal to the signal standard deviation.
    random_seed : int
        Random seed for reproducibility.

    Returns
    -------
    obspy.Trace
        Trace with added Gaussian noise.
    """
    rng = np.random.default_rng(random_seed)

    noisy_trace = trace.copy()
    noise = rng.normal(
        loc=0.0,
        scale=noise_level * np.std(trace.data),
        size=trace.stats.npts,
    )

    noisy_trace.data = (trace.data + noise).astype(np.float32)
    return noisy_trace

def plot_sta_lta_result(
    trace,
    cft,
    trigger_windows,
    threshold_on,
    threshold_off,
    title,
):
    """
    Plot waveform, STA/LTA characteristic function, and trigger windows.

    Parameters
    ----------
    trace : obspy.Trace
        Waveform trace.
    cft : numpy.ndarray
        STA/LTA characteristic function.
    trigger_windows : numpy.ndarray
        Trigger onset and offset sample indices.
    threshold_on : float
        Trigger-on threshold.
    threshold_off : float
        Trigger-off threshold.
    title : str
        Figure title.
    """
    sampling_rate = trace.stats.sampling_rate
    time = np.arange(trace.stats.npts) / sampling_rate
    cft_time = np.arange(len(cft)) / sampling_rate

    fig, axes = plt.subplots(
        nrows=2,
        ncols=1,
        figsize=(9, 6),
        sharex=True,
        constrained_layout=True,
    )

    waveform_axis, cft_axis = axes

    waveform_axis.plot(
        time,
        trace.data,
        color="black",
        linewidth=0.6,
        label="Waveform",
    )

    cft_axis.plot(
        cft_time,
        cft,
        color="darkgreen",
        linewidth=2,
    )

    cft_axis.axhline(
        threshold_on,
        color="firebrick",
        linestyle="--",
        linewidth=1.2,
        label=f"On = {threshold_on}",
    )

    cft_axis.axhline(
        threshold_off,
        color="blue",
        linestyle="--",
        linewidth=1.2,
        label=f"Off = {threshold_off}",
    )

    for idt, (start_sample, end_sample) in enumerate(trigger_windows):
        start_time = start_sample / sampling_rate
        end_time = end_sample / sampling_rate

        label = "Detected Domain" if idt == 0 else None

        waveform_axis.axvspan(
            start_time,
            end_time,
            color="lightsalmon",
            alpha=0.20,
            label=label,
        )

        cft_axis.axvspan(
            start_time,
            end_time,
            color="lightsalmon",
            alpha=0.12,
        )

    waveform_axis.set_ylabel("Amplitude",fontsize=15)
    waveform_axis.set_title(title, fontsize=15,fontweight="bold")
    waveform_axis.set_xlabel("Time (s)", fontsize=15)
    waveform_axis.legend(loc="upper right",fontsize=12)

    cft_axis.set_xlabel("Time (s)",fontsize=15)
    cft_axis.set_ylabel("STA/LTA",fontsize=15)
    cft_axis.legend(loc="upper right",fontsize=12)

    plt.show()

def normalized_template_match(data, template):
    """
    Perform zero-mean normalized cross-correlation template matching.

    The resulting score is approximately within [-1, 1]. A value close to 1
    indicates high waveform similarity between a data segment and the template.

    Parameters
    ----------
    data : numpy.ndarray
        Full waveform in which the template is searched.
    template : numpy.ndarray
        Template waveform.

    Returns
    -------
    best_index : int
        Start sample index of the best matched segment.
    scores : numpy.ndarray
        Normalized correlation score at every valid lag.
    """
    data = np.asarray(data, dtype=np.float64)
    template = np.asarray(template, dtype=np.float64)

    if len(template) > len(data):
        raise ValueError("Template length must not exceed data length.")

    template_centered = template - np.mean(template)
    template_energy = np.sum(template_centered ** 2)

    if template_energy == 0:
        raise ValueError("The template has zero variance.")

    numerator = correlate(data, template_centered, mode="valid")

    window_length = len(template)
    cumulative_sum = np.r_[0.0, np.cumsum(data)]
    cumulative_sum_sq = np.r_[0.0, np.cumsum(data ** 2)]

    window_sum = cumulative_sum[window_length:] - cumulative_sum[:-window_length]
    window_sum_sq = (
        cumulative_sum_sq[window_length:]
        - cumulative_sum_sq[:-window_length]
    )

    window_energy = window_sum_sq - (window_sum ** 2) / window_length
    window_energy = np.maximum(window_energy, 0.0)

    denominator = np.sqrt(window_energy * template_energy)

    scores = np.zeros_like(numerator)
    valid = denominator > np.finfo(float).eps
    scores[valid] = numerator[valid] / denominator[valid]

    best_index = int(np.argmax(scores))
    return best_index, scores
