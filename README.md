# STA-LTA-Detection
Seismic monitoring of earthquake-waves can be performed using the Obspy software, which requires input parameters such as trigger threshold and pre- and post-window lengths. Of course, this operation can also be carried out in MATLAB <br>
## STA/LTA Detection Principle

STA/LTA is a widely used seismic event-detection method. It compares recent signal energy with the longer-term background energy.

For a waveform sample $x_i$, the short-term average (STA) is computed over a short window:

$$
\mathrm{STA}(i)=
\frac{1}{N_{\mathrm{STA}}}
\sum_{j=i-N_{\mathrm{STA}}+1}^{i}
x_j^2
$$

where $N_{\mathrm{STA}}$ is the number of samples in the short window.

The long-term average (LTA) is calculated over a longer window:

$$
\mathrm{LTA}(i)=
\frac{1}{N_{\mathrm{LTA}}}
\sum_{j=i-N_{\mathrm{LTA}}+1}^{i}
x_j^2
$$

The STA/LTA characteristic function is then defined as:

$$
C(i)=
\frac{\mathrm{STA}(i)}{\mathrm{LTA}(i)}
$$

Before a seismic arrival, recent waveform energy is usually similar to the background energy. Therefore, the STA/LTA ratio is typically close to one:

$$
C(i) \approx 1
$$

When a seismic arrival occurs, waveform energy increases rapidly. The STA responds quickly to this increase, whereas the LTA still mainly represents the earlier background level. As a result:

$$
\mathrm{STA}(i) > \mathrm{LTA}(i)
$$

An event is declared when the characteristic function exceeds the trigger-on threshold:

$$
C(i) \geq T_{\mathrm{on}}
$$

The trigger ends when the characteristic function falls below a lower trigger-off threshold:

$$
C(i) < T_{\mathrm{off}}
$$

Using separate trigger-on and trigger-off thresholds is called **hysteresis**. It prevents repeated trigger switching when the STA/LTA ratio fluctuates near a threshold.

## Noise Test

The noisy STA/LTA example adds zero-mean Gaussian noise to the normalized waveform. The noise level is controlled relative to the waveform amplitude.

A noise level of $1.0$ represents a relatively strong noise condition, where the added noise amplitude is comparable to the normalized waveform amplitude. This provides a simple and reproducible test of STA/LTA performance under reduced signal-to-noise conditions.

As the noise level increases, the detector may produce false triggers, miss weak arrivals, or identify the event onset later than expected.

## Template Matching Principle

Template matching searches for a known waveform pattern within a longer waveform record. A short waveform segment containing a target event is selected as the template. This template is compared with all candidate segments of the same length in the continuous waveform.

The similarity between the template and a candidate segment can be evaluated using zero-mean normalized cross-correlation:

$$
R(k)=
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
}
$$

where:

- $t(j)$ is the template waveform;
- $x(k+j)$ is the candidate waveform segment starting at sample $k$;
- $L$ is the template length;
- $\bar{t}$ is the mean value of the template;
- $\bar{x}_k$ is the mean value of the candidate waveform segment.

The normalized correlation coefficient is approximately bounded by:

$$
-1 \leq R(k) \leq 1
$$

A value close to $1$ indicates that the waveform segment has a shape highly similar to the template. The best matching position is obtained by finding the maximum correlation score:

$$
k_{\mathrm{best}} = \arg\max_k R(k)
$$

Normalized correlation is generally preferred over a raw dot product because it emphasizes waveform shape instead of absolute amplitude. This makes template matching more robust when the same event has different amplitudes or when moderate noise is present.

<img width="900" height="600" alt="ce8537530e9dc2d367e1710aab6c56ef" src="https://github.com/user-attachments/assets/cb76afcb-395e-4b56-b56a-b8c8263f7bbb" /> <br>
<img width="900" height="600" alt="dc2e7d02f3b24535b854e5162cf02854" src="https://github.com/user-attachments/assets/09ad6340-5d0d-47d5-8344-67ff34b16864" /> <br>

## And we can simply use the template match method to identify the desired waveform in a noisy signal: <br>
<img width="900" height="600" alt="eb698dcc0c29e4055b2285f22025d702" src="https://github.com/user-attachments/assets/81508ab1-9c57-4d10-8f78-5d960b8bb678" /> <br>
