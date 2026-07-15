import numpy as np
import matplotlib.pyplot as plt

from seismic_tools import load_normalized_trace, normalized_template_match

def main():
    waveform_file = "ExampleWave.gse2"
    template_start_seconds = 32.0
    template_end_seconds = 40.0
    noise_level = 1
    random_seed = 1
    trace = load_normalized_trace(waveform_file)
    sampling_rate = trace.stats.sampling_rate

    template_trace = trace.copy()
    template_trace.trim(
        starttime=trace.stats.starttime + template_start_seconds,
        endtime=trace.stats.starttime + template_end_seconds,
    )
    template = np.asarray(template_trace.data, dtype=np.float64)
    rng = np.random.default_rng(random_seed)
    noisy_data = trace.data + rng.normal(
        loc=0.0,
        scale=noise_level * np.std(trace.data),
        size=trace.stats.npts,
    )
    best_index, scores = normalized_template_match(
        data=noisy_data,
        template=template,
    )
    best_time = best_index / sampling_rate
    template_duration = len(template) / sampling_rate
    best_score = scores[best_index]

    print(f"Template window: {template_start_seconds:.2f} to "
          f"{template_end_seconds:.2f} s")
    print(f"Best match start time: {best_time:.2f} s")
    print(f"Best match duration: {template_duration:.2f} s")
    print(f"Maximum normalized correlation: {best_score:.4f}")

    data_time = np.arange(len(noisy_data)) / sampling_rate
    template_time = np.arange(len(template)) / sampling_rate
    score_time = np.arange(len(scores)) / sampling_rate
    fig, axes = plt.subplots(
        nrows=3,
        ncols=1,
        figsize=(9, 6),
        constrained_layout=True,
    )

    template_axis, waveform_axis, score_axis = axes

    waveform_axis.plot(
        data_time,
        noisy_data,
        color="black",
        linewidth=0.6,
        label="Noisy waveform",
    )

    waveform_axis.axvspan(
        best_time,
        best_time + template_duration,
        color="lightsalmon",
        alpha=0.20,
        label="Best Fitting",
    )

    waveform_axis.set_ylabel("Amplitude",fontsize=15)
    waveform_axis.set_xlabel("Time (s)",fontsize=15)
    waveform_axis.legend(loc="upper right",fontsize=12)

    template_axis.plot(
        template_time,
        template,
        color="green",
        linewidth=1.4,
        label="Template waveform",
    )

    template_axis.set_ylabel("Amplitude",fontsize=15)
    template_axis.set_xlabel("Template time (s)",fontsize=15)
    template_axis.legend(loc="upper right",fontsize=12)
    template_axis.set_title("Template Matching Test",fontsize=18,fontweight="bold")

    score_axis.plot(
        score_time,
        scores,
        color="mediumpurple",
        linewidth=1.0,
        label="Normalized correlation",
    )

    score_axis.axvline(
        best_time,
        color="b",
        linestyle="--",
        linewidth=1.4,
        label=f"Best at = {best_time:.2f} s",
    )

    score_axis.axhline(
        0.0,
        color="gray",
        linestyle="--",
        linewidth=1.4,
    )

    score_axis.set_xlabel("Candidate start time (s)",fontsize=15)
    score_axis.set_ylabel("Correlation",fontsize=15)
    score_axis.set_ylim(-1.05, 1.05)
    score_axis.legend(loc="upper right",fontsize=12)

    plt.show()

if __name__ == "__main__":
    main()
