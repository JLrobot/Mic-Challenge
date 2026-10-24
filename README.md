# Mic-Challenge

We have a miniDSP UMA-16 v2 microphone array (16 MEMS microphones, 4 x 4 grid) and want to use it to
locate things by sound: detect a sound source, estimate the direction it comes from (azimuth and elevation),
and track it over time.

The goal is autonomy: the acoustic direction estimate should drive a system that acts on its own, for example
a drone (real or simulated) that turns toward the detected source and flies there to take a look, without a
human in the loop.

## Plan
1. Record all 16 channels from the UMA-16 and check that every microphone works.
2. Direction of arrival (DOA) with beamforming on the live stream; show it as a heatmap over the camera image.
3. Detect and classify sources (e.g. what kind of sound it is) and track them over time.
4. Simulation: several virtual arrays with the same geometry, sources moving along known trajectories,
   to test triangulation and tracking against ground truth.
5. Closed loop: the acoustic estimate becomes a goal for an autonomous drone in simulation.

## Repository layout
- `hardware/uma16/`: array notes and microphone geometry (positions per USB channel).
- `data/uma16_real/`: real 16-channel UMA-16 recordings (with calibration) to develop against.
- `third_party/`: open-source capture / DOA / drone-sound simulation code we build on.
- `sim/models/`: MuJoCo drone models.
- `scripts/download_data.py`: fetches larger open drone-audio datasets (some with true flight trajectories).
- `DATA_SOURCES.md`: where everything comes from and under which license.

## Data and licenses
Third-party files keep their original license next to them. Large datasets are not committed; they are
downloaded with scripts.
