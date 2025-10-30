# -*- coding: utf-8 -*-
"""
# ==================================================
# 2. Speaker Diarization
# ==================================================
"""

import os
import time
import pickle
import numpy as np
import pandas as pd
from pyAudioAnalysis import audioSegmentation as aS

# User parameters (edit as needed)
# -------------------------------
WD = "C:/path/to/project"     # Working directory
AUDIO_FILENAME = "voicerecording_all.wav"
N_SPEAKERS = 3                 # Expected number of speakers
PLOT_RES = 1                   # Plot result (1) or not (0)

# Define the path to the audio file
os.chdir(WD)
audio_file_path = os.path.join(WD, AUDIO_FILENAME)

# # Perform speaker segmentation
# #-----------------------------
# start = time.time()
# # Default mid_window=1.0, mid_step=0.1, short_window=0.1 
# seg_result = aS.speaker_diarization(audio_file_path, n_speakers=N_SPEAKERS, plot_res=PLOT_RES)
# end = time.time()
# print(f"This took {round((end - start) / 60, 2)} minutes") # 5.17 minutes # 2.64 min

# # Convert labels to contiguous segments and to milliseconds
# # -----------------------------------------------------
# segs, flags = aS.labels_to_segments(seg_result[0], 0.2)  #timestamps are in 0.5s
# speech_interval_msec = (segs.astype(np.int32) * 500)     # Convert to milliseconds 

# # Put the results of the speech analysis in a dataframe
# speaker_label = np.array(flags) + 1  
# speech = pd.DataFrame({
#     'speech_interval_msec': speech_interval_msec.tolist(),
#     'speaker_label': speaker_label
# })
# # Get timestamps
# segs,flags = aS.labels_to_segments(seg_result[0], 0.2) #timestamps are in 0.5s
# speech_interval_msec = segs.astype(np.int32)*500 # Convert to milliseconds

# # Put the results of the speech analysis in a dataframe
#  #-----------------------------------------------------
#   #each participant has a column indicating whether they are speaking

# speaker_label = np.array(flags) + 1
# speech = pd.DataFrame({'speech_interval_msec': speech_interval_msec.tolist(), 'speaker_label': speaker_label})
 
# # Map diarization labels to participants
# # -----------------------------------------
# # From inspecting the recording:
# #   T is speaker label 3
# #   P is speaker label 2
# #   A is speaker label 1
# speech['speech_T'] = 0
# speech.loc[speech['speaker_label'] == 3, 'speech_T'] = 1

# speech['speech_P'] = 0
# speech.loc[speech['speaker_label'] == 2, 'speech_P'] = 1

# speech['speech_A'] = 0
# speech.loc[speech['speaker_label'] == 1, 'speech_A'] = 1

# # Save speaker diarization results
# # --------------------------------------------------
# speech_csv = os.path.join(WD, "speech_segments.csv")
# speech_pkl = os.path.join(WD, "speech_segments.pkl")

# speech.to_csv(speech_csv, index=False)
# with open(speech_pkl, "wb") as f:
#     pickle.dump(speech, f)

# print(f"[SAVED] Diarization results saved as:\n  - {speech_csv}\n  - {speech_pkl}")

# Reopen diarization results to reinstate 'speech'
# --------------------------------------------------
speech_pkl = os.path.join(WD, "speech_segments.pkl")
with open(speech_pkl, "rb") as f:
    speech = pickle.load(f)

print(f"[OK] 'speech' dataframe reloaded ({len(speech)} rows)")

# Create a binary speech variable for each participant
#----------------------------------------------------------------------
def build_binary_series(df_speech: pd.DataFrame, col_name: str):
    """
    Create a per-millisecond binary series for one participant, then
    downsample by selecting every 20th sample to approximate 25 Hz.
    """
    # Initialize empty df with required columns
    out = pd.DataFrame(columns=['timestamp', col_name])

    nonsilent_parts = df_speech['speech_interval_msec'][df_speech[col_name] == 1]
    silent_parts    = df_speech['speech_interval_msec'][df_speech[col_name] == 0]

    # Non-silent (1)
    for start_ms, end_ms in nonsilent_parts:
        ts = range(start_ms, end_ms + 1)  # per-ms timestamps
        out = pd.concat(
            [out, pd.DataFrame({'timestamp': ts, col_name: [1] * len(ts)})],
            ignore_index=True
        )

    # Silent (0)
    for start_ms, end_ms in silent_parts:
        ts = range(start_ms, end_ms + 1)  # per-ms timestamps
        out = pd.concat(
            [out, pd.DataFrame({'timestamp': ts, col_name: [0] * len(ts)})],
            ignore_index=True
        )

    # Sort then downsample to ~25 Hz (every 20 ms)
    out = out.sort_values(by='timestamp').reset_index(drop=True)
    out_25hz = out.iloc[::20, :]
    return out_25hz

# Build binary time series (downsampled)
df_speechP = build_binary_series(speech, 'speech_P')
df_speechA = build_binary_series(speech, 'speech_A')
df_speechT = build_binary_series(speech, 'speech_T')

# Synchronize speech data with eye-tracking data
# -----------------------------------------------------
dfT = pd.read_csv("aruco-dist_T.csv")
dfA = pd.read_csv("aruco-dist_A.csv")
dfP = pd.read_csv("aruco-dist_P.csv")

def align_speech_to_et(df_et: pd.DataFrame, df_speech_25hz: pd.DataFrame, speech_col: str, out_csv: str):
    # Compute indices into speech timestamps using searchsorted (original logic)
    ind = []
    last_timestamp = df_speech_25hz["timestamp"].iloc[-1]
    for t2 in df_et["Recording timestamp"]:
        if t2 == 0:
            ind.append(0)
        elif 0 < t2 <= last_timestamp:
            temp_index = np.searchsorted(df_speech_25hz["timestamp"].values, t2)
            ind.append(temp_index)

    # Drop ET rows where the timestamp exceeds the max speech timestamp
    over = np.where(df_et["Recording timestamp"] > last_timestamp)[0]
    df_et = df_et.drop(over)

    # Fetch aligned speech labels
    df_et[speech_col] = df_speech_25hz[speech_col].iloc[ind].tolist()

    # Save
    df_et.to_csv(out_csv, index=False)
    print(f"[OK] Saved {out_csv} | rows: {len(df_et):,}")

# Run alignment per participant 
align_speech_to_et(dfP, df_speechP, "speech_P", "ETandSpeechP.csv")
align_speech_to_et(dfA, df_speechA, "speech_A", "ETandSpeechA.csv")
align_speech_to_et(dfT, df_speechT, "speech_T", "ETandSpeechT.csv")

