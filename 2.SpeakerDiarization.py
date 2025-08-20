# -*- coding: utf-8 -*-
"""
            ----------------------------------------------------
            Capturing Eye Gaze Synchrony in a Triadic Discussion
            ----------------------------------------------------
                            SPEAKER DIARIZATION
"""

import time
import numpy as np
import pandas as pd
from pyAudioAnalysis import audioSegmentation as aS
import os

# Set working directory
wd = "~"
os.chdir(wd)

# Define the path to the audio file
audio_file_path =  wd + "/voicerecording_all.wav"

# Perform speaker segmentation

start = time.time()
seg_result = aS.speaker_diarization(audio_file_path, n_speakers=3, plot_res=1) #default: mid_window=1.0, mid_step=0.1, short_window=0.1
end = time.time()
elapsed_time = end - start
print(f"This took {round(elapsed_time/60, 2)} minutes") # 5.17 minutes # 2.64 min

# Get timestamps
segs,flags = aS.labels_to_segments(seg_result[0], 0.2) #timestamps are in 0.5s
speech_interval_msec = segs.astype(np.int32)*500 # Convert to milliseconds

# Put the results of the speech analysis in a dataframe
 # where each participant has a column indicting whether they are speaking
 #-----------------------------------------------------------------------------
speaker_label = np.array(flags) + 1
speech = pd.DataFrame({'speech_interval_msec': speech_interval_msec.tolist(), 'speaker_label': speaker_label})
 
# From inspecting the recording: 
     #Andreja is speaker 2 -> 3 
speech['speech_A'] = 0
speech['speech_A'][speech.speaker_label == 3] = 1
     #Polona is speaker 1 -> 2
speech['speech_P'] = 0
speech['speech_P'][speech.speaker_label == 2] = 1
     #Tatjana is speaker 1 -> 2
speech['speech_T'] = 0
speech['speech_T'][speech.speaker_label == 1] = 1

# Create a DataFrame for each participant
df1 = pd.DataFrame(columns=['timestamp', 'speech_P'])
nonsilent_parts = speech['speech_interval_msec'][speech['speech_P'] == 1]
silent_parts = speech['speech_interval_msec'][speech['speech_P'] == 0]

# Populate the DataFrame with silent (0) and non-silent (1) labels
for start, end in nonsilent_parts:
    # Convert start and end times to 25 Hz timestamps
    timestamps = range(start, end + 1)
    labels = [1] * len(timestamps)  # Set label as 1 for non-silent parts
    # Append the data to the DataFrame
    df1 = pd.concat([df1, pd.DataFrame({'timestamp': timestamps, 'speech_P': labels})], ignore_index=True)

for start, end in silent_parts:
    # Convert start and end times to 25 Hz timestamps
    timestamps = range(start, end+1)
    labels = [0] * len(timestamps)  # Set label as 0 for silent parts
    # Append the data to the DataFrame
    df1 = pd.concat([df1, pd.DataFrame({'timestamp': timestamps, 'speech_P': labels})], ignore_index=True)

# Sort the DataFrame based on timestamp and downsample to 25Hz
df1 = df1.sort_values(by='timestamp').reset_index(drop=True)
df_speechP = df1.iloc[::20, :]

# A
df1 = pd.DataFrame(columns=['timestamp', 'speech_A'])
nonsilent_parts = speech['speech_interval_msec'][speech['speech_A'] == 1]
silent_parts = speech['speech_interval_msec'][speech['speech_A'] == 0]

# Populate the DataFrame with silent (0) and non-silent (1) labels
for start, end in nonsilent_parts:
    # Convert start and end times to 25 Hz timestamps
    timestamps = range(start, end + 1)
    labels = [1] * len(timestamps)  # Set label as 1 for non-silent parts
    # Append the data to the DataFrame
    df1 = pd.concat([df1, pd.DataFrame({'timestamp': timestamps, 'speech_A': labels})], ignore_index=True)

for start, end in silent_parts:
    # Convert start and end times to 25 Hz timestamps
    timestamps = range(start, end+1)
    labels = [0] * len(timestamps)  # Set label as 0 for silent parts
    # Append the data to the DataFrame
    df1 = pd.concat([df1, pd.DataFrame({'timestamp': timestamps, 'speech_A': labels})], ignore_index=True)

# Sort the DataFrame based on timestamp and downsample to 25Hz
df1 = df1.sort_values(by='timestamp').reset_index(drop=True)
df_speechA = df1.iloc[::20, :]

#T
df1 = pd.DataFrame(columns=['timestamp', 'speech_T'])
nonsilent_parts = speech['speech_interval_msec'][speech['speech_T'] == 1]
silent_parts = speech['speech_interval_msec'][speech['speech_T'] == 0]

# Populate the DataFrame with silent (0) and non-silent (1) labels
for start, end in nonsilent_parts:
    # Convert start and end times to 25 Hz timestamps
    timestamps = range(start, end + 1)
    labels = [1] * len(timestamps)  # Set label as 1 for non-silent parts
    # Append the data to the DataFrame
    df1 = pd.concat([df1, pd.DataFrame({'timestamp': timestamps, 'speech_T': labels})], ignore_index=True)

for start, end in silent_parts:
    # Convert start and end times to 25 Hz timestamps
    timestamps = range(start, end+1)
    labels = [0] * len(timestamps)  # Set label as 0 for silent parts
    # Append the data to the DataFrame
    df1 = pd.concat([df1, pd.DataFrame({'timestamp': timestamps, 'speech_T': labels})], ignore_index=True)

# Sort the DataFrame based on timestamp and downsample to 25Hz
df1 = df1.sort_values(by='timestamp').reset_index(drop=True)
df_speechT = df1.iloc[::20, :]

#speech_data = pd.merge(df_speechP, df_speechA, on="timestamp")
#speech_data =  pd.merge(speech_data, df_speechT, on="timestamp")

# Synchronize speech data with eye tracking data
#-------------------------------------------------------------------------

# Read data
dfT = pd.read_csv("aruco-dist_T.csv", index_col=0)
dfA = pd.read_csv("aruco-dist_A.csv", index_col=0)
dfP = pd.read_csv("aruco-dist_P.csv", index_col=0)

#P
# Calculate the 'ind' list using NumPy conditions and vectorized operations
ind = []
last_timestamp = df_speechP["timestamp"].iloc[-1]
for t2 in dfP["Recording timestamp"]:
    if t2 == 0:
        ind.append(0)
    elif 0 < t2 <= last_timestamp:
        temp_index = np.searchsorted(df_speechP["timestamp"], t2)
        ind.append(temp_index)

# Drop rows from df2 where "Recording timestamp" exceeds the maximum timestamp in df1
over = np.where(dfP["Recording timestamp"] > last_timestamp)[0]
dfP.drop(over, inplace=True)

 #Fetch values using indexed operations
dfP["speech_P"] = df_speechP["speech_P"].iloc[ind].tolist()
dfP.to_csv('ETandSpeechP.csv', index=False) 

#A
# Calculate the 'ind' list using NumPy conditions and vectorized operations
ind = []
last_timestamp = df_speechA["timestamp"].iloc[-1]
for t2 in dfA["Recording timestamp"]:
    if t2 == 0:
        ind.append(0)
    elif 0 < t2 <= last_timestamp:
        temp_index = np.searchsorted(df_speechA["timestamp"], t2)
        ind.append(temp_index)

# Drop rows from df2 where "Recording timestamp" exceeds the maximum timestamp in df1
over = np.where(dfA["Recording timestamp"] > last_timestamp)[0]
dfA.drop(over, inplace=True)

 #Fetch values using indexed operations
dfA["speech_A"] = df_speechA["speech_A"].iloc[ind].tolist()
dfA.to_csv('ETandSpeechA.csv', index=False) 

#T
# Calculate the 'ind' list using NumPy conditions and vectorized operations
ind = []
last_timestamp = df_speechT["timestamp"].iloc[-1]
for t2 in dfT["Recording timestamp"]:
    if t2 == 0:
        ind.append(0)
    elif 0 < t2 <= last_timestamp:
        temp_index = np.searchsorted(df_speechT["timestamp"], t2)
        ind.append(temp_index)

# Drop rows from df2 where "Recording timestamp" exceeds the maximum timestamp in df1
over = np.where(dfT["Recording timestamp"] > last_timestamp)[0]
dfT.drop(over, inplace=True)

 #Fetch values using indexed operations
dfT["speech_T"] = df_speechT["speech_T"].iloc[ind].tolist()
dfT.to_csv('ETandSpeechT.csv', index=False) 

