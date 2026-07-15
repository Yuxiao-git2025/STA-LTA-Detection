import matplotlib.pyplot as plt

from seismic_tools import (
    load_normalized_trace,
    plot_sta_lta_result,
    run_sta_lta,
)
def main():
    waveform_file = "ExampleWave.gse2"
    sta_seconds = 5.0
    lta_seconds = 10.0
    threshold_on = 1.6
    threshold_off = 0.6
    trace = load_normalized_trace(waveform_file)
    cft, trigger_windows = run_sta_lta(
        trace=trace,
        sta_seconds=sta_seconds,
        lta_seconds=lta_seconds,
        threshold_on=threshold_on,
        threshold_off=threshold_off,
    )
    print(f"Sampling rate: {trace.stats.sampling_rate:.2f} Hz")
    print(f"Number of detected triggers: {len(trigger_windows)}")

    for index, (start_sample, end_sample) in enumerate(trigger_windows, start=1):
        start_time = start_sample / trace.stats.sampling_rate
        end_time = end_sample / trace.stats.sampling_rate
        print(
            f"Event {index}: "
            f"start = {start_time:.2f} s, "
            f"end = {end_time:.2f} s, "
            f"duration = {end_time - start_time:.2f} s"
        )
    plot_sta_lta_result(
        trace=trace,
        cft=cft,
        trigger_windows=trigger_windows,
        threshold_on=threshold_on,
        threshold_off=threshold_off,
        title="Initial Waveform",
    )

if __name__ == "__main__":
    main()
