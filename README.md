# STA-LTA-Detection
Seismic monitoring of earthquake-waves can be performed using the Obspy software, which requires input parameters such as trigger threshold and pre- and post-window lengths. Of course, this operation can also be carried out in MATLAB <br>
<img width="900" height="600" alt="ce8537530e9dc2d367e1710aab6c56ef" src="https://github.com/user-attachments/assets/cb76afcb-395e-4b56-b56a-b8c8263f7bbb" /> <br>
<img width="900" height="600" alt="dc2e7d02f3b24535b854e5162cf02854" src="https://github.com/user-attachments/assets/09ad6340-5d0d-47d5-8344-67ff34b16864" /> <br>

## And we can simply use the template match method to identify the desired waveform in a noisy signal: <br>
<img width="900" height="600" alt="eb698dcc0c29e4055b2285f22025d702" src="https://github.com/user-attachments/assets/81508ab1-9c57-4d10-8f78-5d960b8bb678" /> <br>


# Seismic Detection and Template Matching

This project provides three simple seismic signal-processing examples based on an ObsPy waveform file:

- **STA/LTA detection on a clean waveform**
- **STA/LTA detection after adding Gaussian noise**
- **Template matching in a noisy waveform**

The purpose is to compare an energy-based event detector with a waveform-similarity-based detection method.

## Requirements

Install the required Python packages:

```bash
pip install obspy numpy scipy matplotlib
```

The waveform file `ExampleWave.gse2` should be placed in the project directory.

## Workflow

Run the following scripts independently:

```bash
python main_sta_lta_clean.py
python main_sta_lta_noisy.py
python main_template_matching.py
```

Each script prints the main detection result in the terminal and displays a figure showing the waveform and corresponding detection output.

## STA/LTA Detection Principle

STA/LTA is a widely used seismic event-detection method. It compares the recent signal energy with the longer-term background energy.

For a waveform \(x_i\), the short-term average (STA) is computed over a short window:

\[
\mathrm{STA}(i)
=
\frac{1}{N_{\mathrm{STA}}}
\sum_{j=i-N_{\mathrm{STA}}+1}^{i}
x_j^2,
\]

where \(N_{\mathrm{STA}}\) is the number of samples in the short window.

The long-term average (LTA) is calculated over a longer window:

\[
\mathrm{LTA}(i)
=
\frac{1}{N_{\mathrm{LTA}}}
\sum_{j=i-N_{\mathrm{LTA}}+1}^{i}
x_j^2.
\]

The STA/LTA characteristic function is then defined as:

\[
C(i)
=
\frac{\mathrm{STA}(i)}{\mathrm{LTA}(i)}.
\]

Before a seismic arrival, the recent signal energy is usually similar to the background energy, so:

\[
C(i)\approx1.
\]

When an earthquake arrival occurs, waveform energy increases rapidly. The STA responds quickly to this change, while the LTA still represents the previous background level. Therefore, the ratio increases:

\[
\mathrm{STA}(i)>\mathrm{LTA}(i),
\qquad
C(i)>1.
\]

An event is declared when the STA/LTA ratio exceeds a trigger-on threshold:

\[
C(i)\geq T_{\mathrm{on}}.
\]

The trigger ends when the ratio falls below a lower trigger-off threshold:

\[
C(i)<T_{\mathrm{off}}.
\]

Using separate on and off thresholds is called **hysteresis**. It prevents repeated switching when the STA/LTA ratio fluctuates near a single threshold.

In this project, the default values are:

\[
T_{\mathrm{on}}=1.5,
\qquad
T_{\mathrm{off}}=0.5.
\]

The short-term and long-term windows are set to 5 s and 10 s, respectively. These values can be adjusted according to the expected event duration, waveform sampling rate, signal frequency content, and background noise level.

## Noise Test

The noisy STA/LTA example adds zero-mean Gaussian noise to the normalized waveform. The noise level is controlled by its standard deviation relative to the waveform standard deviation.

A noise level of \(1.0\) means that the noise standard deviation is approximately equal to the standard deviation of the normalized waveform. This provides a reproducible and interpretable test of detector performance under reduced signal-to-noise conditions.

Increasing noise may produce false triggers, hide weak arrivals, or shift trigger onset times. In practical applications, STA/LTA parameters should therefore be tuned using representative noise conditions.

## Template Matching Principle

Template matching searches for a known waveform pattern within a longer waveform record. A short waveform segment containing a target event is selected as the template. The template is then compared with all possible waveform segments of the same length in the continuous data.

This project uses zero-mean normalized cross-correlation:

\[
R(k)
=
\frac{
\sum_{j=0}^{L-1}
\left[x(k+j)-\bar{x}_k\right]
\left[t(j)-\bar{t}\right]
}{
\sqrt{
\sum_{j=0}^{L-1}
\left[x(k+j)-\bar{x}_k\right]^2
}
\sqrt{
\sum_{j=0}^{L-1}
\left[t(j)-\bar{t}\right]^2
}
}.
\]

Here:

- \(t(j)\) is the template waveform;
- \(x(k+j)\) is the candidate waveform segment starting at sample \(k\);
- \(L\) is the template length;
- \(\bar{t}\) and \(\bar{x}_k\) are the mean values of the template and candidate segment.

The correlation coefficient is approximately bounded by:

\[
-1\leq R(k)\leq1.
\]

A score close to \(1\) indicates that the candidate segment has a waveform shape very similar to the template. The best match is determined by:

\[
k_{\mathrm{best}}=\arg\max_k R(k).
\]

Normalized correlation is preferred over a raw dot product because it focuses on waveform shape rather than absolute amplitude. This makes template matching more robust when the waveform amplitude changes or noise is present.
