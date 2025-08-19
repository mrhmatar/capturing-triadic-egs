# -*- coding: utf-8 -*-
"""
            ----------------------------------------------------
            Capturing Eye Gaze Synchrony in a Triadic Discussion
            ----------------------------------------------------
                            DATA PREPARATION
                            
Prepares the data for future processing:
    1. Identifies and interpolates missing data, downsamples to 25 Hz
    2. Codes gaze and speech events
    3. Prepares dyadic and triadic dfs for (mv)SUSY
    
INPUTS:
    - "ETandSpeechA.csv", "ETandSpeechT.csv", and "ETandSpeechP.csv" 
    participants' merged gaze and speech data
    
OUTPUTS:
    - "TA.txt", "TP.txt","AP.txt" dyadic dataframe for SUSY
    - "TAPx.txt",  "TAPy.txt", "TAPf.txt" triadic dataframe for mvSUSY

"""
import pandas as pd
import numpy as np
from datamatrix import series as srs
import os

# Set working directory
wd = "~"
os.chdir(wd)

# Read data
dfT = pd.read_csv("ETandSpeechT.csv")
dfA = pd.read_csv("ETandSpeechA.csv")
dfP = pd.read_csv("ETandSpeechP.csv")

# Inspect for nonsensical values
dfT['Gaze point X'][(dfT['Gaze point X'] < 0)| (dfT['Gaze point X'] > 1920)].count() #32
dfT['Gaze point Y'][(dfT['Gaze point Y'] < 0) | (dfT['Gaze point Y'] > 1080)].count() #30
dfA['Gaze point X'][(dfA['Gaze point X'] < 0)| (dfA['Gaze point X'] > 1920)].count() #1
dfA['Gaze point Y'][(dfA['Gaze point Y'] < 0) | (dfA['Gaze point Y'] > 1080)].count() #3
dfP['Gaze point X'][(dfP['Gaze point X'] < 0)| (dfP['Gaze point X'] > 1920)].count() #62
dfP['Gaze point Y'][(dfP['Gaze point Y'] < 0) | (dfP['Gaze point Y'] > 1080)].count() #2

# Replace nonsensical values with NaNs
dfT.loc[(dfT['Gaze point X'] < 0)| (dfT['Gaze point X'] > 1920), ('obj_Gaze_X', 'Euclidian_distances')] = np.nan
dfT.loc[(dfT['Gaze point Y'] < 0)| (dfT['Gaze point Y'] > 1080), ('obj_Gaze_Y', 'Euclidian_distances')] = np.nan
dfA.loc[(dfA['Gaze point X'] < 0)| (dfA['Gaze point X'] > 1920), ('obj_Gaze_X', 'Euclidian_distances')] = np.nan
dfT.loc[(dfA['Gaze point Y'] < 0)| (dfA['Gaze point Y'] > 1080), ('obj_Gaze_Y', 'Euclidian_distances')] = np.nan
dfP.loc[(dfP['Gaze point X'] < 0)| (dfP['Gaze point X'] > 1920), ('obj_Gaze_X', 'Euclidian_distances')] = np.nan
dfP.loc[(dfP['Gaze point Y'] < 0)| (dfP['Gaze point Y'] > 1080), ('obj_Gaze_Y', 'Euclidian_distances')] = np.nan

# Extract relevant columns
l = min(len(dfT), len(dfA), len(dfP))
ATP = pd.DataFrame({'x_T': dfT.obj_Gaze_X.iloc[:l], 'y_T': dfT.obj_Gaze_Y.iloc[:l], 'd_T': dfT.Euclidian_distances.iloc[:l], 'FaceA_T': dfT['AOI hit [Screenshot T.jpeg - Face A-T]'].iloc[:l], 'FaceP_T': dfT['AOI hit [Screenshot T.jpeg - Face P-T]'].iloc[:l], 'sp_T': dfT['speech_T'].iloc[:l],
                    'x_A': dfA.obj_Gaze_X.iloc[:l], 'y_A': dfA.obj_Gaze_Y.iloc[:l], 'd_A': dfA.Euclidian_distances.iloc[:l], 'FaceT_A': dfA['AOI hit [Screenshot A.jpeg - Face T-A]'].iloc[:l], 'FaceP_A': dfA['AOI hit [Screenshot A.jpeg - Face P-A]'].iloc[:l], 'sp_A': dfA['speech_A'].iloc[:l],
                    'x_P': dfP.obj_Gaze_X.iloc[:l], 'y_P': dfP.obj_Gaze_Y.iloc[:l], 'd_P': dfP.Euclidian_distances.iloc[:l], 'FaceT_P': dfP['AOI hit [Screenshot P.jpeg - Face T-P]'].iloc[:l], 'FaceA_P': dfP['AOI hit [Screenshot P.jpeg - Face A-P]'].iloc[:l], 'sp_P': dfP['speech_P'].iloc[:l]})

# Count missing values
round(sum(ATP['x_T'].isna())*100/l, 2), round(sum(ATP['y_T'].isna())*100/l, 2), round(sum(ATP['d_T'].isna())*100/l, 2) 
#(15.8, 15.79, 15.94)
round(sum(ATP['x_A'].isna())*100/l, 2), round(sum(ATP['y_A'].isna())*100/l, 2), round(sum(ATP['d_A'].isna())*100/l, 2) 
#(10.74, 10.74, 10.74)
round(sum(ATP['x_P'].isna())*100/l, 2), round(sum(ATP['y_P'].isna())*100/l, 2), round(sum(ATP['d_P'].isna())*100/l, 2) 
#(11.0, 10.72, 11.01)
round(sum(ATP['FaceA_T'].isna())*100/l, 2), round(sum(ATP['FaceP_T'].isna())*100/l, 2) #(0.0, 0.0)
round(sum(ATP['FaceA_P'].isna())*100/l, 2), round(sum(ATP['FaceT_P'].isna())*100/l, 2) #(0.0, 0.0)
round(sum(ATP['FaceT_A'].isna())*100/l, 2), round(sum(ATP['FaceP_A'].isna())*100/l, 2) #(0.0, 0.0)

# Code Mutual gaze between dyads
ATP['mutualGaze_TA'] = 0
ATP['mutualGaze_TA'].loc[(ATP['FaceA_T'] == 1) & (ATP['FaceT_A'] == 1)] = 1

ATP['mutualGaze_TP'] = 0
ATP['mutualGaze_TP'].loc[(ATP['FaceP_T'] == 1) & (ATP['FaceT_P'] == 1)] = 1

ATP['mutualGaze_AP'] = 0
ATP['mutualGaze_AP'].loc[(ATP['FaceP_A'] == 1) & (ATP['FaceA_P'] == 1)] = 1

# Code when 2 participants jointly gaze at the 3rd participant when they are speaking
ATP['jointGazeP_TA'] = 0
ATP['jointGazeP_TA'].loc[(ATP['FaceP_T'] == 1) & (ATP['FaceP_A'] == 1)] = 1

ATP['jointGazeA_TP'] = 0
ATP['jointGazeA_TP'].loc[(ATP['FaceA_T'] == 1) & (ATP['FaceA_P'] == 1)] = 1

ATP['jointGazeT_AP'] = 0
ATP['jointGazeT_AP'].loc[(ATP['FaceT_A'] == 1) & (ATP['FaceT_P'] == 1)] = 1

# Code when 2 participants jointly gaze at the 3rd participant when they are speaking
ATP['jointGazePsp_TA'] = 0
ATP['jointGazePsp_TA'].loc[(ATP['FaceP_T'] == 1) & (ATP['FaceP_A'] == 1) & (ATP['sp_P'] == 1)] = 1

ATP['jointGazeAsp_TP'] = 0
ATP['jointGazeAsp_TP'].loc[(ATP['FaceA_T'] == 1) & (ATP['FaceA_P'] == 1) & (ATP['sp_A'] == 1)] = 1

ATP['jointGazeTsp_AP'] = 0
ATP['jointGazeTsp_AP'].loc[(ATP['FaceT_A'] == 1) & (ATP['FaceT_P'] == 1) & (ATP['sp_T'] == 1)] = 1

# Downsample, Interpolate, and Drop first row of NaNs
x_T = pd.Series(data=srs.downsample(ATP['x_T'].interpolate(), by=2)).dropna().reset_index(drop=True)
y_T = pd.Series(data=srs.downsample(ATP['y_T'].interpolate(), by=2)).dropna().reset_index(drop=True)
d_T = pd.Series(data=srs.downsample(ATP['d_T'].interpolate(), by=2)).dropna().reset_index(drop=True)
x_A = pd.Series(data=srs.downsample(ATP['x_A'].interpolate(), by=2)).dropna().reset_index(drop=True)
y_A = pd.Series(data=srs.downsample(ATP['y_A'].interpolate(), by=2)).dropna().reset_index(drop=True)
d_A = pd.Series(data=srs.downsample(ATP['d_A'].interpolate(), by=2)).dropna().reset_index(drop=True)
x_P = pd.Series(data=srs.downsample(ATP['x_P'].interpolate(), by=2)).dropna().reset_index(drop=True)
y_P = pd.Series(data=srs.downsample(ATP['y_P'].interpolate(), by=2)).dropna().reset_index(drop=True)
d_P = pd.Series(data=srs.downsample(ATP['d_P'].interpolate(), by=2)).dropna().reset_index(drop=True)

fATP = ATP[['FaceA_T', 'FaceT_A', 'FaceP_T', 'FaceT_P', 'FaceP_A', 'FaceA_P']]
fATP = fATP.iloc[::2, :].dropna().reset_index(drop=True)

spATP = ATP[['sp_T', 'sp_A', 'sp_P']]
spATP = spATP.iloc[::2, :].dropna().reset_index(drop=True)

TAPmg = ATP[['mutualGaze_TA', 'mutualGaze_TP', 'mutualGaze_AP']]
TAPmg = TAPmg.iloc[::2, :].dropna().reset_index(drop=True)

TAPjg = ATP[['jointGazeT_AP', 'jointGazeA_TP', 'jointGazeP_TA']]
TAPjg = TAPjg.iloc[::2, :].dropna().reset_index(drop=True)

TAPjgs = ATP[['jointGazeTsp_AP', 'jointGazeAsp_TP', 'jointGazePsp_TA']]
TAPjgs = TAPjgs.iloc[::2, :].dropna().reset_index(drop=True)

# Generate dfs
 #dyadic
TA = pd.DataFrame({'x_T': x_T, 'x_A': -x_A, 'y_T': y_T, 'y_A': y_A, 'd_T': d_T, 'd_A': d_A, 'FaceA_T': fATP.FaceA_T, 'FaceT_A': fATP.FaceT_A})
TP = pd.DataFrame({'x_T': x_T, 'x_P': -x_P, 'y_T': y_T, 'y_P': y_P, 'd_T': d_T, 'd_P': d_P, 'FaceP_T': fATP.FaceP_T, 'FaceT_P': fATP.FaceT_P})
AP = pd.DataFrame({'x_A': x_A, 'x_P': -x_P, 'y_A': y_A, 'y_P': y_P, 'd_A': d_A, 'd_P': d_P, 'FaceP_A': fATP.FaceP_A, 'FaceA_P': fATP.FaceA_P})

 #triadic
TAPx = pd.DataFrame({'x_T': x_T, 'x_A': x_A, 'x_P': x_P})
TAPy = pd.DataFrame({'y_T': y_T, 'y_A': y_A, 'y_P': y_P})
TAPd = pd.DataFrame({'d_T': d_T, 'd_A': d_A, 'd_P': d_P})

TAPf = pd.DataFrame({'FaceA_T': fATP.FaceA_T, 'FaceT_A': fATP.FaceT_A, 
                     'FaceP_T': fATP.FaceP_T, 'FaceT_P': fATP.FaceT_P,
                     'FaceP_A': fATP.FaceP_A, 'FaceA_P': fATP.FaceA_P})

# Rebuild ATP
ATP = pd.DataFrame({'x_T': x_T, 'y_T': y_T, 'd_T': d_T, 'FaceA_T': fATP.FaceA_T, 'FaceP_T': fATP.FaceP_T, 
                    'x_A': -x_A, 'y_A': y_A, 'd_A': d_A, 'FaceT_A': fATP.FaceT_A, 'FaceP_A': fATP.FaceP_A, 
                    'x_P': -x_P, 'y_P': y_P, 'd_P': d_P, 'FaceT_P': fATP.FaceT_P, 'FaceA_P': fATP.FaceA_P, 
                    'mutualGaze_TA': TAPmg.mutualGaze_TA, 'mutualGaze_TP': TAPmg.mutualGaze_TP,'mutualGaze_AP': TAPmg.mutualGaze_AP,
                    'jointGazeT_AP': TAPjg.jointGazeT_AP, 'jointGazeA_TP': TAPjg.jointGazeA_TP, 'jointGazeP_TA': TAPjg.jointGazeP_TA, 
                    'jointGazeTsp_AP': TAPjgs.jointGazeTsp_AP, 'jointGazeAsp_TP': TAPjgs.jointGazeAsp_TP, 'jointGazePsp_TA': TAPjgs.jointGazePsp_TA, 
                    'sp_T': spATP.sp_T, 'sp_A': spATP.sp_A, 'sp_P': spATP.sp_P})

# Export to txt for SUSY
TA.to_csv('TA.txt', sep=' ', index=False)
TP.to_csv('TP.txt', sep=' ', index=False)
AP.to_csv('AP.txt', sep=' ', index=False)


TAPx.to_csv('TAPx.txt', sep=' ', index=False)
TAPy.to_csv('TAPy.txt', sep=' ', index=False)
TAPd.to_csv('TAPd.txt', sep=' ', index=False)
TAPf.to_csv('TAPf.txt', sep=' ', index=False)