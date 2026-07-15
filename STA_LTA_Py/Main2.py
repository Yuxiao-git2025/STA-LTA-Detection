from seismic_tools import (
    add_gaussian_noise,
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
    noise_level = 1.0
    random_seed = 1
    clean_trace = load_normalized_trace(waveform_file)
    noisy_trace = add_gaussian_noise(
        trace=clean_trace,
        noise_level=noise_level,
        random_seed=random_seed,
    )

    cft, trigger_windows = run_sta_lta(
        trace=noisy_trace,
        sta_seconds=sta_seconds,
        lta_seconds=lta_seconds,
        threshold_on=threshold_on,
        threshold_off=threshold_off,
    )
    print(f"Noise level: {noise_level:.2f}")
    print(f"Number of detected triggers: {len(trigger_windows)}")

    for index, (start_sample, end_sample) in enumerate(trigger_windows, start=1):
        start_time = start_sample / noisy_trace.stats.sampling_rate
        end_time = end_sample / noisy_trace.stats.sampling_rate
        print(
            f"Trigger {index}: "
            f"start = {start_time:.2f} s, "
            f"end = {end_time:.2f} s, "
            f"duration = {end_time - start_time:.2f} s"
        )
    plot_sta_lta_result(
        trace=noisy_trace,
        cft=cft,
        trigger_windows=trigger_windows,
        threshold_on=threshold_on,
        threshold_off=threshold_off,
        title=f"Noisy Waveform "
              f"(Noise Level = {noise_level:.1f})",
    )

if __name__ == "__main__":
    main()
