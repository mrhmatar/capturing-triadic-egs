---

# Capturing Triadic Eye Gaze Synchrony

---

This repository contains the data and code associated with the paper:
**Matar, M., Heeren, A., De Raedt, R., & Pulopulos, M. (2025). Capturing eye gaze synchrony in a triadic interaction: A proof-of-concept study.**

---

## Overview

This repository provides a complete, reproducible pipeline for capturing and analyzing **eye gaze synchrony (eGS)** during **triadic interactions**.
It integrates ArUco marker–based gaze translation, speaker diarization, multimodal synchronization, and (multi)variate synchrony analysis.

All scripts are designed to be run within a single **project folder** that contains the relevant video, audio, Tobii exports, and code files.
Each step produces intermediate outputs (`.csv`, `.pkl`, `.txt`) to facilitate independent execution and modular debugging.

---

## Contents

The repository includes **four Python scripts** and **two R scripts** implementing the full preprocessing and analysis pipeline.

---

### Python scripts

#### 1. ArucoMarkerDetection.py

* Detects ArUco markers in Tobii scene camera videos.
* Saves results both as `.csv` (for quick inspection) and `.pkl` (for downstream processing).
* Optionally generates a visualization video (`.avi`) showing detected markers frame by frame.
* Synchronizes Tobii gaze data with ArUco marker detections and translates gaze coordinates relative to the marker center (reading directly from the `.pkl` file).

**Inputs:**
`scenevideo.mp4`, `Data Export ...xlsx`

**Intermediates:**

* `aruco_[participant].csv`
* `aruco_[participant].pkl`
* `marker-detection_[participant].avi` *(optional visualization)*

**Outputs:**
`aruco-dist_[participant].csv`

---

#### 2. SpeakerDiarization.py

* Performs speaker diarization on merged triadic audio files.
* Saves results both as `.csv` and `.pkl` so they can be reloaded without re-running diarization.
* Aligns the resulting speech timelines with the corresponding eye-tracking data.

**Inputs:**
`voicerecording_all.wav`, `aruco-dist_[participant].csv`

**Intermediates:**

* `speech_segments.csv`
* `speech_segments.pkl`

**Outputs:**
`ETandSpeechA.csv`, `ETandSpeechT.csv`, `ETandSpeechP.csv`

---

#### 3. DataPreparation.py

* Prepares synchronized eye-tracking and speech data for synchrony analysis.
* Handles missing data, downsampling to 25 Hz, and event coding (mutual gaze, joint gaze, speech).
* Exports dyadic and triadic matrices required for SUSY and mv-SUSY.
* Generates an intermediate combined file (`ATP.csv`) for descriptive analyses.

**Inputs:**
`ETandSpeechA.csv`, `ETandSpeechT.csv`, `ETandSpeechP.csv`

**Outputs:**

* `ATP.csv`
* `TA.txt`, `TP.txt`, `AP.txt`
* `TAPx.txt`, `TAPy.txt`, `TAPd.txt`, `TAPf.txt`

---

#### 4. Descriptives.py

* Generates descriptive statistics and visual summaries of gaze and speech events.
* Includes spatial distributions, direct/mutual/joint gaze frequencies, and speaking time proportions.

**Inputs:**
`ATP.csv`

**Outputs:**
Summary tables and plots

---

### R scripts

#### 5. SUSY.R

* Applies **SUSY (Surrogate Synchrony Analysis)** to dyadic matrices (x, y, and face AOI hit variables).
* Computes synchrony metrics, plots results, and exports effect-size summaries.

**Inputs:**
`TA.txt`, `TP.txt`, `AP.txt`

**Outputs:**
`SUSY_TA.csv`, `SUSY_TP.csv`, `SUSY_AP.csv`

---

#### 6. mvSUSY.R

* Applies **multivariate SUSY (mv-SUSY)** to triadic matrices.
* Estimates group-level synchrony using the `lambda_max` method.
* Exports detailed results for each modality.

**Inputs:**
`TAPx.txt`, `TAPy.txt`, `TAPf.txt`

**Outputs:**
`mvSUSYlambda_TAPx.csv`, `mvSUSYlambda_TAPy.csv`, `mvSUSYlambda_TAPf.csv`

---

## Please cite this work as

If you use this repository, please cite it as follows:

**APA citation**

Matar, M. (2025). *Capturing triadic eye gaze synchrony* [Computer software]. GitHub.
Available at: [https://github.com/mrhmatar/capturing-triadic-egs](https://github.com/mrhmatar/capturing-triadic-egs)

**BibTeX citation**

```bibtex
@software{matar2025capturingegs,
  author    = {Matar, M.},
  title     = {Capturing triadic eye gaze synchrony},
  year      = {2025},
  publisher = {GitHub},
  url       = {https://github.com/mrhmatar/capturing-triadic-egs},
  version   = {1.0.0}
}
```
---
## Version Notes

This is the **first public release** of the *Capturing Triadic Eye Gaze Synchrony* pipeline.  
Previous development versions were maintained privately during internal testing and validation.

---
