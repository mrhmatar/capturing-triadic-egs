# Capturing Triadic Eye Gaze Synchrony

This repository contains the data and code associated with the paper:  
**Matar, M., Heeren, A., De Raedt, R., &  Pulopulos, M.(2025). Capturing triadic eye gaze synchrony: A comparison of event-based and correlation-based approaches.**

## Contents

The repository includes four Python scripts and two R scripts implementing the full preprocessing and analysis pipeline:

### Python scripts
1. **ArucoMarkerDetection.py**  
   - Detects ArUco markers in eye-tracking scene camera videos.  
   - Synchronizes marker detection with gaze data.  
   - Computes objective gaze location indices relative to the ArUco marker.  
   **Inputs:** `scenevideo.mp4`, `Data Export ...xlsx`  
   **Outputs:** `aruco_participant.csv`, `aruco-dist_*.csv`  

2. **SpeakerDiarization.py**  
   - Performs speaker diarization on merged audio files.  
   - Synchronizes speech with gaze data.  
   **Inputs:** `voicerecording_all.wav`, `aruco-dist_*.csv`  
   **Outputs:** `ETandSpeechA.csv`, `ETandSpeechT.csv`, `ETandSpeechP.csv`  

3. **DataPreparation.py**  
   - Prepares data for synchrony analysis: interpolates missing data, downsamples to 25 Hz, codes gaze and speech events.  
   - Prepares dyadic and triadic dataframes for (mv)SUSY.  
   **Inputs:** `ETandSpeech*.csv`  
   **Outputs:** `TA.txt`, `TP.txt`, `AP.txt`, `TAPx.txt`, `TAPy.txt`, `TAPf.txt`  

4. **Descriptives.py**  
   - Generates descriptive statistics and event-based graphs.  
   **Inputs:** `ETandSpeech*.csv`  
   **Outputs:** Descriptive statistics and plots  

### R scripts
5. **SUSY.R**  
   - Applies SUSY (Synchrony analysis) to dyadic dataframes.  
   **Inputs:** `TA.txt`, `TP.txt`, `AP.txt`  
   **Outputs:** SUSY results  

6. **mvSUSY.R**  
   - Applies mvSUSY to triadic dataframes.  
   **Inputs:** `TAPx.txt`, `TAPy.txt`, `TAPf.txt`  
   **Outputs:** mvSUSY results  

---
