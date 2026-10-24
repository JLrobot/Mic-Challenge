"""Download open drone-audio datasets that are too big for git.

    python scripts/download_data.py --list
    python scripts/download_data.py wsu_flight5 anu_ir          # small, good start (~1.1 GB + 80 MB)
    python scripts/download_data.py ddl_real --dest D:/data      # big ones only when needed

Files go to <dest>/<dataset>/ (default: ./data/external, which is git-ignored). Downloads resume if a
partial file exists. Licenses: see DATA_SOURCES.md; keep the attribution when you use the data.
"""

from __future__ import annotations

import argparse
import sys
import urllib.request
from pathlib import Path

WSU = "https://rds.westernsydney.edu.au/Centres/ICNS/2026/Jahir_Rodriguez"
WSU_F5 = f"{WSU}/dataset/test_1/Oct_11_2024/flight_5"

DATASETS: dict[str, dict] = {
    "wsu_flight5": {
        "desc": "Western Sydney UAV acoustic localization, test_1 flight 5: 4 x 6-ch WAV (24 ch, 48 kHz) + "
                "10 Hz GPS flight log + alignment params (~1.1 GB). CC BY-SA 4.0.",
        "files": [f"{WSU_F5}/device_{i}_nosync.wav" for i in range(1, 5)]
                 + [f"{WSU_F5}/Oct-11th-2024-03-49PM-Flight-Airdata.csv", f"{WSU_F5}/alignment_params.json",
                    f"{WSU}/README.md", f"{WSU}/LICENSE.txt"],
    },
    "anu_ir": {
        "desc": "ANU drone audition, measured impulse responses, 12 x .mat (~80 MB). CC BY 4.0.",
        "files": [f"https://zenodo.org/records/16197912/files/recording_S{i}.mat?download=1" for i in range(1, 13)],
    },
    "uavirbase": {
        "desc": "UaVirBASE (MUT Warsaw): fixed mic array, UAV at varied distance / height / azimuth (13.8 GB). CC BY 4.0.",
        "files": ["https://zenodo.org/records/15391924/files/Microphone_array.zip?download=1"],
    },
    "ddl_real": {
        "desc": "DDL (Surrey, MLSP 2022) real recordings with bearing / range / altitude labels (12.6 GB). CC BY 4.0.",
        "files": ["https://zenodo.org/records/6459183/files/MLSP_2022_Real_Data.zip?download=1"],
    },
    "ddl_synth": {
        "desc": "DDL synthetic set (4.6 GB). CC BY 4.0.",
        "files": ["https://zenodo.org/records/6459183/files/MLSP_2022_Synth_Data.zip?download=1"],
    },
}

HF_NOTE = ("DroneAudioSet (MIT, 42.6 GB, Hugging Face): pick a subset, e.g.\n"
           "  pip install huggingface_hub\n"
           "  huggingface-cli download ahlab-drone-project/DroneAudioSet --repo-type dataset "
           "--include \"<pattern>\" --local-dir data/external/droneaudioset\n"
           "d3set (GPL-3.0, ground array + MAVSDK telemetry): git lfs clone https://github.com/introlab/d3set "
           "(outside this repo).")


def _name(url: str) -> str:
    return url.split("?")[0].rstrip("/").split("/")[-1]


def fetch(url: str, out: Path) -> None:
    have = out.stat().st_size if out.exists() else 0
    req = urllib.request.Request(url, headers={"User-Agent": "mic-challenge-downloader"})
    if have:
        req.add_header("Range", f"bytes={have}-")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            if have and r.status != 206:
                have = 0  # server ignored the range: start over
            total = int(r.headers.get("Content-Length", 0)) + have
            mode = "ab" if have else "wb"
            done = have
            with open(out, mode) as f:
                while chunk := r.read(1 << 20):
                    f.write(chunk)
                    done += len(chunk)
                    if total:
                        print(f"\r  {out.name}: {done / 1e6:8.1f} / {total / 1e6:.1f} MB", end="", flush=True)
            print()
    except urllib.error.HTTPError as e:
        if e.code == 416:  # already complete
            print(f"  {out.name}: already complete")
            return
        raise


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("datasets", nargs="*", help="dataset keys (see --list)")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--dest", default=str(Path(__file__).resolve().parents[1] / "data" / "external"))
    a = ap.parse_args()
    if a.list or not a.datasets:
        for k, v in DATASETS.items():
            print(f"{k:12s} {v['desc']}")
        print("\n" + HF_NOTE)
        return 0
    for key in a.datasets:
        if key not in DATASETS:
            print(f"unknown dataset {key!r}; use --list", file=sys.stderr)
            return 2
        d = Path(a.dest) / key
        d.mkdir(parents=True, exist_ok=True)
        print(f"== {key} -> {d}")
        for url in DATASETS[key]["files"]:
            try:
                fetch(url, d / _name(url))
            except Exception as e:  # noqa: BLE001
                print(f"  FAILED {url}: {e}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
