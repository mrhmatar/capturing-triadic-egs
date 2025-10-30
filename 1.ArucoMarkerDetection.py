# -*- coding: utf-8 -*-
# ==================================================
# 1. ArUco Marker Detection and Gaze Translation
# ==================================================

import os
import cv2
import numpy as np
import pandas as pd
import time
import pickle

# 0. Define Working Directory
# --------------------------------------------------

# Set the main project folder that contains all videos, Tobii exports, and code.
# All outputs will be saved in the current working directory by default.
os.chdir("C:/path/to/project")
print("Working directory set to:", os.getcwd())

# The variable `video_dir` is used below to build input paths for the scene videos.
video_dir = os.getcwd()


# 1) Detect ArUco markers in Tobii scene camera video
# --------------------------------------------------
def detect_aruco_markers(
    video_path: str,
    participant_initial: str,
    out_dir: str = None,
    aruco_dict_id: int = cv2.aruco.DICT_4X4_250,
    show: bool = False,
    verbose: bool = False,
    save_video: bool = False
):
    """
    Detect ArUco markers in a Tobii scene camera video and save results.
    
    Parameters
    ----------
    video_path : str
        Path to the Tobii scene camera video (e.g., "scenevideo.mp4").
    participant_initial : str
        Short participant identifier used in output filenames (e.g., "A", "P", "T").
    out_dir : str, optional
        Directory where the outputs will be saved. Defaults to the current working directory.
    aruco_dict_id : int, optional
        OpenCV ArUco dictionary ID (default: `cv2.aruco.DICT_4X4_250`).
    show : bool, optional
        If True, displays the detection in real time.
        Press 'q' to stop visualization early.
    verbose : bool, optional
        If True, prints marker IDs and corner coordinates for each frame.
    save_video : bool, optional
        If True, saves an `.avi` video (MJPG codec, 10 fps) visualizing detected markers.

    Returns
    -------
    tuple of (str, str)
        Paths to the saved files:
        - `.csv`: contains timestamps, detected marker IDs, and corners.
        - `.pkl`: serialized dictionary with the same data (used by downstream functions).

    Outputs
    -------
    aruco_[participant].csv
    aruco_[participant].pkl
    Aruco-marker-detection_[participant].avi (if `save_video=True`)
    """
    if out_dir is None:
        out_dir = os.getcwd()

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    out_base = os.path.join(out_dir, f"aruco_{participant_initial}")
    csv_path = out_base + ".csv"
    pkl_path = out_base + ".pkl"
    video_name = os.path.join(out_dir, f"Aruco-marker-detection_{participant_initial}.avi")

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise FileNotFoundError(f"Cannot open video: {video_path}")

    marker_dict = cv2.aruco.getPredefinedDictionary(aruco_dict_id)
    param_markers = cv2.aruco.DetectorParameters()

    IDs, Corners, Timestamps = [], [], []

    # --- Setup video writer if requested ---
    result = None
    if save_video:
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        size = (frame_width, frame_height)
        result = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'MJPG'), 10, size)
        print(f"[INFO] Saving detection video as: {video_name}")

    start = time.time()
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        marker_corners, marker_IDs, _ = cv2.aruco.detectMarkers(
            gray_frame, marker_dict, parameters=param_markers
        )

        IDs.append(marker_IDs)
        Corners.append(marker_corners)
        Timestamps.append(int(cap.get(cv2.CAP_PROP_POS_MSEC)))

        if verbose:
            print(f"IDs: {marker_IDs}, Corners: {marker_corners}")

        # Draw markers
        if marker_corners:
            cv2.aruco.drawDetectedMarkers(frame, marker_corners, marker_IDs)

        # Display detection in real time
        if show:
            small_frame = cv2.resize(frame, (960, 540))
            cv2.imshow("frame", small_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Write frame to output video if enabled
        if save_video and result is not None:
            result.write(frame)

    cap.release()
    if save_video and result is not None:
        result.release()
    cv2.destroyAllWindows()

    minutes = round((time.time() - start) / 60, 2)
    print(f"[aruco] {participant_initial}: processed in {minutes} minutes")

    # Save structured data
    df = pd.DataFrame({"Timestamps": Timestamps, "aruco_IDs": IDs, "aruco_Corners": Corners})
    df.to_csv(csv_path, index=False)

    with open(pkl_path, "wb") as f:
        pickle.dump({"Timestamps": Timestamps, "aruco_IDs": IDs, "aruco_Corners": Corners}, f)

    print(f"[aruco] Saved {os.path.basename(csv_path)} (timestamps) and {os.path.basename(pkl_path)} (arrays) to {out_dir}")
    return csv_path, pkl_path


# Run ArUco marker detection for each participant
# -----------------------------------------------
detect_aruco_markers(
    video_path=os.path.join(video_dir, "20231107T115159Z(1)", "scenevideo.mp4"),
    participant_initial="A",
    show=True,
    verbose=True,
    save_video=True
)

detect_aruco_markers(
    video_path=os.path.join(video_dir, "20231107T115159Z(2)", "scenevideo.mp4"),
    participant_initial="P",
    show=True,
    verbose=True,
    save_video=True
)

detect_aruco_markers(
    video_path=os.path.join(video_dir, "20231107T115159Z(3)", "scenevideo.mp4"),
    participant_initial="T",
    show=True,
    verbose=True,
    save_video=True
)


# 2) Translate gaze coordinates relative to marker
# --------------------------------------------------
def translate_gaze_relative_to_marker(
    aruco_pkl_path: str,
    tobii_export_xlsx_path: str,
    participant_initial: str,
    out_dir: str = None,
    true_id: int = 4
):
    """
    Synchronize ArUco detections (from .pkl) with Tobii gaze data and
    reexpress gaze coordinates relative to the marker center.

    Parameters
    ----------
    aruco_pkl_path : str
        Path to aruco_[X].pkl (must include 'Timestamps', 'aruco_IDs', and 'aruco_Corners').
    tobii_export_xlsx_path : str
        Tobii Data Export .xlsx (must include 'Recording timestamp', 'Gaze point X', 'Gaze point Y').
    participant_initial : str
        Used in the output filename (e.g., "T", "A", "P").
    out_dir : str, optional
        Output directory for aruco-dist_[X].csv (defaults to the current working directory).
    true_id : int, default 4
        The known correct ArUco ID to keep.

    Returns
    -------
    str
        Path to the CSV written: aruco-dist_[participant].csv
    """
    if out_dir is None:
        out_dir = os.getcwd()

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    out_csv = os.path.join(out_dir, f"aruco-dist_{participant_initial}.csv")

    # --- Load ArUco detections directly from PKL ---
    with open(aruco_pkl_path, "rb") as f:
        aruco_data = pickle.load(f)

    ts_scene = np.array(aruco_data["Timestamps"])
    IDs = aruco_data["aruco_IDs"]
    Corners = aruco_data["aruco_Corners"]

    df2 = pd.read_excel(tobii_export_xlsx_path)
    last_timestamp = ts_scene[-1]

    idx = [
        0 if t2 == 0 else np.searchsorted(ts_scene, t2) if 0 < t2 <= last_timestamp else None
        for t2 in df2["Recording timestamp"]
    ]

    # Drop rows beyond last timestamp
    over_idx = np.where(df2["Recording timestamp"] > last_timestamp)[0]
    if len(over_idx) > 0:
        df2.drop(over_idx, inplace=True)
        df2.reset_index(drop=True, inplace=True)
        idx = [
            0 if t2 == 0 else np.searchsorted(ts_scene, t2) if 0 < t2 <= last_timestamp else None
            for t2 in df2["Recording timestamp"]
        ]

    idx_series = pd.Series(idx).fillna(0).astype(int)
    df2["aruco_IDs"] = [IDs[i] for i in idx_series]
    df2["aruco_Corners"] = [Corners[i] for i in idx_series]

    # --- Keep only the true marker ID ---
    true_ind = df2["aruco_IDs"].apply(
        lambda arr: np.where(arr == true_id)[0]
        if isinstance(arr, np.ndarray) or (hasattr(arr, "__iter__") and arr is not None)
        else np.array([])
    )

    true_corners = []
    for i, c in zip(true_ind, df2["aruco_Corners"]):
        if c is None or len(c) == 0 or len(i) == 0:
            true_corners.append(None)
        else:
            try:
                true_corners.append(np.array(c)[i])
            except Exception:
                true_corners.append(None)
    df2["true_Corners"] = true_corners

    # --- Compute marker center (X, Y) ---
    df2["aruco_Centers"] = df2["true_Corners"].apply(
        lambda x: (x[0][0][0] + x[0][0][2]) / 2 if x is not None else [np.nan, np.nan]
    )
    df2[["marker_X", "marker_Y"]] = pd.DataFrame(df2["aruco_Centers"].tolist(), index=df2.index)

    # --- Translate gaze relative to marker ---
    df2["obj_Gaze_X"] = df2["Gaze point X"] - df2["marker_X"]
    df2["obj_Gaze_Y"] = df2["marker_Y"] - df2["Gaze point Y"]
    df2["Euclidian_distances"] = np.sqrt(df2["obj_Gaze_X"]**2 + df2["obj_Gaze_Y"]**2)

    # --- Save output ---
    df2.drop(["aruco_Centers"], axis=1, inplace=True)
    df2.to_csv(out_csv, index=False)

    print(f"[DONE] Saved {os.path.basename(out_csv)} to {out_dir}")
    return out_csv


# Run gaze coordinate translation for each participant
# ----------------------------------------------------
translate_gaze_relative_to_marker(
    aruco_pkl_path="aruco_A.pkl",
    tobii_export_xlsx_path="Data Export - 20231107T115159Z(1).xlsx",
    participant_initial="A",
    true_id=4
)

translate_gaze_relative_to_marker(
    aruco_pkl_path="aruco_P.pkl",
    tobii_export_xlsx_path="Data Export - 20231107T115159Z(2).xlsx",
    participant_initial="P",
    true_id=4
)

translate_gaze_relative_to_marker(
    aruco_pkl_path="aruco_T.pkl",
    tobii_export_xlsx_path="Data Export - 20231107T115159Z(3).xlsx",
    participant_initial="T",
    true_id=4
)
