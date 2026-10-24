# Data and code sources

Everything third-party keeps its original license file next to it. Large datasets are not in git:
`python scripts/download_data.py --list`.

## In this repo
| Path | What | Source (commit) | License |
|---|---|---|---|
| `hardware/uma16/geometry/` | UMA-16 mic positions per channel (corrected + old mirrored), CSV | [acoular/acoular](https://github.com/acoular/acoular) 26.8 | BSD-3-Clause |
| `data/uma16_real/jduanen_acoustic_camera/` | **Real UMA-16 v2 recordings**: `capture_nb16.wav` (speaker at a known direction), `cal_ref.wav` + `cal.npy` (calibration); 16 ch, 48 kHz, 16 bit, 5 s each. Notebooks 15-17 (array, capture via sounddevice, calibration) and `calibrate_uma16.py` | [jduanen/Acoustic-Camera](https://github.com/jduanen/Acoustic-Camera) (f61047b) | MIT |
| `third_party/kush99_acoustic_camera/` | UMA-16 v2 live capture (`acoustic/acquisition.py`, sounddevice, device "UMA16v2", 48 kHz, 16 ch), MUSIC DOA, steering, calibration; `config/settings.py` | [Kush99-ux/multimodal_acoustic_camera](https://github.com/Kush99-ux/multimodal_acoustic_camera) (d6a4f10) | MIT |
| `third_party/DroneSynthesis2DOA/` | Drone signal synthesis, multi-array simulation, SRP-PHAT + neural DOA (geometry in yaml, a 4x4 URA can be added). Code only: the two background WAVs from Freesound were left out (license unverified) | [SOUNDS-RESEARCH/DroneSynthesis2DOA](https://github.com/SOUNDS-RESEARCH/DroneSynthesis2DOA) (da80f4a) | MIT |
| `sim/models/skydio_x2/` | MuJoCo quadcopter model | [mujoco_menagerie](https://github.com/google-deepmind/mujoco_menagerie) (f3b6013) | Apache-2.0 |
| `sim/models/bitcraze_crazyflie_2/` | MuJoCo Crazyflie model | same | MIT |

## Download with the script
| Key | Dataset | Why useful | License |
|---|---|---|---|
| `wsu_flight5` | [Western Sydney UAV acoustic localization](https://rds.westernsydney.edu.au/Centres/ICNS/2026/Jahir_Rodriguez/README.md), one flight: 24 ch, 48 kHz + **10 Hz GPS flight log** | Audio paired with true trajectory: test tracking against truth | CC BY-SA 4.0 |
| `anu_ir` | [ANU measured impulse responses](https://zenodo.org/records/16197912) | Realistic propagation for simulation | CC BY 4.0 |
| `uavirbase` | [UaVirBASE](https://zenodo.org/records/15391924): fixed array, UAV at known distance / height / azimuth | DOA accuracy vs geometry | CC BY 4.0 |
| `ddl_real`, `ddl_synth` | [DDL, MLSP 2022](https://zenodo.org/records/6459183): bearing, range, altitude labels | Detection + localization benchmark | CC BY 4.0 |
| (manual) | [DroneAudioSet](https://huggingface.co/datasets/ahlab-drone-project/DroneAudioSet) (42.6 GB, 2 x 8-ch arrays) | Large, many conditions | MIT |
| (manual) | [d3set](https://github.com/introlab/d3set): ground array + MAVSDK telemetry | Audio + telemetry | GPL-3.0 (fetch only, do not vendor) |

## Libraries (install, do not vendor)
acoular (BSD-3; live input `SoundDeviceSamplesGenerator`, moving sources `MovingPointSource` / `Trajectory`),
pyroomacoustics (MIT; DOA algorithms, no native moving sources), python-sounddevice (MIT; on Windows set
`SD_ENABLE_ASIO=1` before `import sounddevice` to use the miniDSP ASIO driver), dynamic-sound (Apache-2.0;
moving sources and moving arrays with Doppler and air absorption), ODAS (MIT; localization + tracking in C).

## Not used (and why)
- Al-Emadi DroneAudioDataset: custom license that forbids security / surveillance use.
- DREGON, SPCup 2019: academic / personal use only.
- Fraunhofer IDMT drone audio 2022: license not verified yet.
- Repos without a license file (rights unclear): rabeaifeanyi/acoustic-camera, LCAV/audioROS, DroneAudioSet-code.
- miniDSP manuals / CAD: copyrighted, link only: https://www.minidsp.com/products/usb-audio-interface/uma-16-microphone-array
