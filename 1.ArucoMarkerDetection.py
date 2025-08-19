# -*- coding: utf-8 -*-
"""
                ----------------------------------------------------
                Capturing Eye Gaze Synchrony in a Triadic Discussion
                ----------------------------------------------------
                            ARUCO MARKER DETECTION

1. Detects ArUco marker (ID and Corners) in eye tracking scene camera video.
2. Synchronizes ArUco detection data (i.e., scene camera video frame rate) with gaze data (i.e., eye tracker sampling rate).
3. Computes objective gaze location indices relative to ArUco marker (i.e., relatable across video frames).

INPUTS:
- Eye tracker scene camera video 'scenevideo.mp4' in Tobii Glasses 3 SD card folder "20231107T115159Z(3)"
- Eye tracking data file for 1 participant ('Data Export 20231107T115159Z(3).xlsx' in Tobii Pro Lab)

*Eye tracking videos were not shared to protect participants' privacy

OUTPUTS:
- ArUcO marker detection file 'aruco_participant.csv'
- Eye tracking data file with objective gaze location indices e.g., 'aruco-dist_T.csv'

"""

import cv2
import numpy as np
import pandas as pd
import time
import os

# Set working directory
wd = "~"
os.chdir(wd)

marker_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)
param_markers =  cv2.aruco.DetectorParameters()

# Get data from video
#--------------------

# Video input setup
videoPath = "20231107T115159Z(3)/scenevideo.mp4"
video_capture = cv2.VideoCapture(videoPath)
video_capture.get(cv2.CAP_PROP_FPS)
start = time.time()

IDs = []
Corners = []
Timestamps = []

cap = video_capture
while True:
    ret, frame = cap.read()
    if not ret:
        break
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    marker_corners, marker_IDs, reject = cv2.aruco.detectMarkers(gray_frame, marker_dict, parameters = param_markers)
    
    # Record IDs and Corners for detected markers + print them in the console
    IDs.append(marker_IDs)
    Corners.append(marker_corners)
    Timestamps.append(int(cap.get(cv2.CAP_PROP_POS_MSEC)))
    print(f"IDs: {marker_IDs}, Corners: {marker_corners}")
    
    # Draw rectangles around identified markers and display their ID and the coordinates of the top right corner
    if marker_corners:
        for ids, corners in zip(marker_IDs, marker_corners):
            cv2.polylines(frame, [corners.astype(np.int32)], True, (0, 255, 255), 4, cv2.LINE_AA)
            corners = corners.reshape(4, 2)
            corners = corners.astype(np.int32)
            top_right = corners[0].ravel()
            cv2.putText(frame, f"id: {ids[0]}", top_right, cv2.FONT_HERSHEY_PLAIN, 1.3, (200, 100, 0), 2, cv2.LINE_AA)   
    cv2.imshow("frame", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()
end = time.time()
print(f"This took {round((end-start)/60, 2)} minutes") # ~ 10 min
 
# Save everything into a dataframe 
markers = {"aruco_IDs": IDs, "aruco_Corners": Corners, "Timestamps": Timestamps}
df1 = pd.DataFrame(markers)
df1.to_csv("aruco_T.csv", index = False)
# ^ this is only to inspect the data for false detections. Don't read from it.
df1.shape

# Synchronize scene camera video frame rate with eye tracker sampling rate (ChatGPT's code, takes seconds !)
#-------------------------------------------------------------------------

# Read into the eye tracking data file
df2 = pd.read_excel("Data Export - 20231107T115159Z(3).xlsx")
df2.shape
df2.columns

# Calculate the 'ind' list using NumPy conditions and vectorized operations
ind = []
last_timestamp = df1["Timestamps"].iloc[-1]
for t2 in df2["Recording timestamp"]:
    if t2 == 0:
        ind.append(0)
    elif 0 < t2 <= last_timestamp:
        temp_index = np.searchsorted(df1["Timestamps"], t2)
        ind.append(temp_index)

# Drop rows from df2 where "Recording timestamp" exceeds the maximum timestamp in df1
over = np.where(df2["Recording timestamp"] > last_timestamp)[0]
df2.drop(over, inplace=True)

 #Fetch values using indexed operations instead of iteration
df2["aruco_IDs"] = df1["aruco_IDs"].iloc[ind].tolist()
df2["aruco_Corners"] = df1["aruco_Corners"].iloc[ind].tolist()

# False detection correction
#---------------------------

# Find the index of the correctly detected marker in each row
true_ID = 4
true_ind = df2["aruco_IDs"].apply(lambda x: np.where(x == true_ID)[0])

# Take marker corners for the correctly detected marker only
true_corners = []
for i, c in zip(true_ind, df2["aruco_Corners"]):
    if len(c) > 0 and i is not None:
        true_corners.append(np.array(c)[i])
    else:
        true_corners.append(None)
df2["true_Corners"] = true_corners

# Compute objective gaze coordinates & Euclidian distance from marker
#--------------------------------------------------------------------

# Get coordinates of ArUco marker center
df2["aruco_Centers"] = df2["true_Corners"].apply(lambda x: (x[0][0][0]+x[0][0][2])/2 if x is not None else [np.nan, np.nan])
df2[['marker_X','marker_Y']] = pd.DataFrame(df2.aruco_Centers.tolist(), index= df2.index)

# Compute objective gaze coordinates relative to marker center
df2 = df2.assign(obj_Gaze_X = lambda x : (x['Gaze point X'] - x['marker_X']))
df2 = df2.assign(obj_Gaze_Y = lambda x : (x['marker_Y'] - x['Gaze point Y'])) #take the opposite so that y>0 is up and y<0 is down

# Compute Euclidian distance between gaze focus and aruco marker center
df2 = df2.assign(Euclidian_distances = lambda x: np.sqrt(x['obj_Gaze_X']**2 + x['obj_Gaze_Y']**2))

# Clean data and save output into a csv file
#-------------------------------------------

# Clean up a little
df2["true_Corners"] = df2["true_Corners"].apply(lambda x : x[0][0] if x is not None else np.nan)
df2 = df2.drop(["aruco_Centers"], axis = 1)

# Take a look at the data and save it as a csv file
df2
df2.columns
df2.to_csv('aruco-dist_T.csv', index=False) 
