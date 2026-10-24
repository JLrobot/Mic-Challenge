# Mic-Challenge

We have a miniDSP UMA-16 v2 microphone array (16 MEMS microphones, 4 x 4 grid) and want to use it to
locate things by sound: detect a sound source, estimate the direction it comes from (azimuth and elevation),
and track it over time.

The goal is autonomy: the acoustic direction estimate should drive a system that acts on its own, for example
a drone (real or simulated) that turns toward the detected source and flies there to take a look, without a
human in the loop.

## Problem overview
Scenario: defending a base in Ukraine at night. Approaching enemy movement (e.g. vehicles 2-3 km away)
cannot be seen in the dark. Ground-based acoustic sensors (UMA-16 arrays) hear it and give the direction
it comes from. A drone is then sent there automatically to look.

The catch: GNSS is jammed. A drone that navigates only with vision + GNSS drifts strongly once GNSS is gone,
so it does not reliably reach the place the sound came from.

Our idea: use the ground array as an extra navigation sensor for the drone. One array gives no global
position, only a direction (azimuth and elevation) to a sound source, and that includes our own drone.
We fuse these bearings with the drone's visual-inertial estimate in place of GNSS:
- bearing array -> target: where the drone has to go;
- bearing array -> drone (plus the drone's barometric altitude): bounds the drift of the drone's own estimate.
Result: an autonomous flight to the sound source that stays on track without GNSS.

Open questions we want to answer: how far the array can hear vehicles and our own drone, how accurate the
bearings are, and how much the bearing updates reduce the drift compared with vision only.

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
