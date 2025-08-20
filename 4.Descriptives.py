# -*- coding: utf-8 -*-
"""
            ----------------------------------------------------
            Capturing Eye Gaze Synchrony in a Triadic Discussion
            ----------------------------------------------------
                        DESCRIPTIVE STATISTICS
                        
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statistics
import os

# Set working directory
wd = "~"
os.chdir(wd)

# Calculate descriptive statistics
descATP = ATP.describe()
descT = descATP[['x_T', 'y_T', 'd_T', 'FaceA_T', 'FaceP_T']]
descA = descATP[['x_A', 'y_A', 'd_A', 'FaceT_A', 'FaceP_A']]
descP = descATP[['x_P', 'y_P', 'd_P', 'FaceT_P', 'FaceA_P']]

 #Generate boxplots
fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(10, 8))
sns.boxplot(x=ATP['x_T'], ax = axes[0,0])
plt.xlabel('x_T')
#plt.ylabel('Values')
#axes[0, 0].set_title('x')
sns.boxplot(x=ATP['y_T'], ax = axes[0,1])
plt.xlabel('y_T')
sns.boxplot(x=ATP['d_T'], ax = axes[0,2])
plt.xlabel('d_T')
sns.boxplot(x=ATP['x_A'], ax = axes[1,0])
plt.xlabel('x_A')
sns.boxplot(x=ATP['y_A'], ax = axes[1,1])
plt.xlabel('y_A')
sns.boxplot(x=ATP['d_A'], ax = axes[1,2])
plt.xlabel('d_A')
sns.boxplot(x=ATP['x_P'], ax = axes[2,0])
plt.xlabel('x_P')
sns.boxplot(x=ATP['y_P'], ax = axes[2,1])
plt.xlabel('y_P')
sns.boxplot(x=ATP['d_P'], ax = axes[2,2])
plt.xlabel('d_P')
#axes[1, 1].axis('off')
plt.tight_layout()
plt.show()

# View outliers 
 #detected from visual inspection inspection of the boxplots
ATP['y_T'][ATP['y_T'] > 200]
ATP['d_T'][ATP['d_T'] > 1000]

ATP['y_A'][(ATP['y_A'] < -750) | (ATP['y_A'] > 250)]
ATP['d_A'][(ATP['d_A'] < 50) | (ATP['d_A'] > 1000)].count()

ATP['y_P'][ATP['y_P'] < -700]

# Plot probability distribution
fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(10, 8))
#sns.histplot(dfT.d_T, kde=True, stat='probability')
sns.kdeplot(ATP['x_T'], label='x', fill=True, ax = axes[0,0])
plt.xlabel('x_T')
sns.kdeplot(ATP['y_T'], label='y', color='darkorange', fill=True, ax = axes[0,1])
plt.xlabel('y_T')
sns.kdeplot(ATP['d_T'], label='d', color='forestgreen', fill=True, ax = axes[0,2])
plt.xlabel('d_T')
sns.kdeplot(ATP['x_A'], label='x_A', fill=True, ax = axes[1,0])
plt.xlabel('x_A')
sns.kdeplot(ATP['y_A'], label='y_A', color='darkorange', fill=True, ax = axes[1,1])
plt.xlabel('y_A')
sns.kdeplot(ATP['d_A'], label='d_A', color='forestgreen', fill=True, ax = axes[1,2])
plt.xlabel('d_T')
sns.kdeplot(ATP['x_P'], label='x_P', fill=True, ax = axes[2,0])
plt.xlabel('x_P')
sns.kdeplot(ATP['y_P'], label='y_P', color='darkorange', fill=True, ax = axes[2,1])
plt.xlabel('y_P')
sns.kdeplot(ATP['d_P'], label='d_P', color='forestgreen', fill=True, ax = axes[2,2])
plt.xlabel('d_P')
plt.tight_layout()
plt.show()

# Mean x, y coord and marker distance when one participant looks at the other
 # T is seated with P to her right (+) and A to her left (-)
ATP[ATP['FaceA_T'] == 1].mean()[0:3] #x_T: -540.6, y_T: -295.5, d_T: 617.3
ATP[ATP['FaceP_T'] == 1].mean()[0:3] #x_T: 503.7, y_T: -310.2, d_T: 593.1
 # A is seated with T to her right (+) and P to her left (-)
ATP[ATP['FaceT_A'] == 1].mean()[5:8] #x_A: 516.8, y_A: -385.5, d_A: 645.5
ATP[ATP['FaceP_A'] == 1].mean()[5:8] #x_A: -509.1, y_A: -290.9, d_A: 587.7
 # P is seated with T to her right (+) and A to her left (-)
ATP[ATP['FaceA_P'] == 1].mean()[10:13] #x_P: 598.4, y_P: -353.6, d_P: 696.3
ATP[ATP['FaceT_P'] == 1].mean()[10:13] #x_P: -509.7, y_P: -338.1, d_P: 612.2

# Direct gaze
round(ATP['FaceA_T'].sum()/len(ATP)*100, 2) #23.78%
round(ATP['FaceP_T'].sum()/len(ATP)*100, 2) #21.26
23.78 + 21.26 #45.04
 #T gazes equally often at A and P
round(ATP['FaceT_A'].sum()/len(ATP)*100, 2) #56.53
round(ATP['FaceP_A'].sum()/len(ATP)*100, 2) #22.42
56.53 + 22.42 #78.95
 #A gazes more often at T than P 
round(ATP['FaceA_P'].sum()/len(ATP)*100, 2) #17.38
round(ATP['FaceT_P'].sum()/len(ATP)*100, 2) #46.75
17.38 + 46.75 # 64.13
 #P gazes more often at T than A
 # T gazes at A and P less often than they gaze at her
 # => T is the highest ranking member of the triad
round(statistics.mean([45.04, 78.95, 64.13]),2) #62.71
round(statistics.stdev([45.04, 78.95, 64.13]),2) #17.0

# Mutual gaze between dyads
round(ATP['mutualGaze_TA'].sum()/len(ATP)*100, 2) #13.77%
round(ATP['mutualGaze_TP'].sum()/len(ATP)*100, 2) #13.03%
round(ATP['mutualGaze_AP'].sum()/len(ATP)*100, 2) #5.61%
round(statistics.mean([13.77,13.03,5.61]),2) #10.8
round(statistics.stdev([13.77,13.03,5.61]),2) #4.51

# Joint gaze at third participant
round(ATP['jointGazeT_AP'].sum()/len(ATP)*100, 2) #33.29%
round(ATP['jointGazeA_TP'].sum()/len(ATP)*100, 2) #7.51%
round(ATP['jointGazeP_TA'].sum()/len(ATP)*100, 2) #9.08%
round(statistics.mean([33.29,7.51,9.08]),2) #16.63
round(statistics.stdev([33.29,7.51,9.08]),2) #14.45

# Joint gaze at speaker
round(ATP['jointGazeTsp_AP'].sum()/len(ATP)*100, 2) #10.56%
round(ATP['jointGazeAsp_TP'].sum()/len(ATP)*100, 2) #4.14%
round(ATP['jointGazePsp_TA'].sum()/len(ATP)*100, 2) #2.31%
sum([10.56,4.14,2.31]) #17.01

# Speaking time
round(ATP['sp_A'].sum()/len(ATP)*100, 2) #34.25%
round(ATP['sp_T'].sum()/len(ATP)*100, 2) #38.64%
round(ATP['sp_P'].sum()/len(ATP)*100, 2) #26.91%

 # LET'S PLOT THIS!
dgT = pd.DataFrame({'Direct Gaze T': ['Face A', 'Face P'],
        'Frequency (%)': [round(ATP['FaceA_T'].sum()/len(ATP)*100, 2), round(ATP['FaceP_T'].sum()/len(ATP)*100, 2)], 
        'BarColor': ['blue', 'red']})
dgA = pd.DataFrame({'Direct Gaze A': ['Face T', 'Face P'],
        'Frequency (%)': [ round(ATP['FaceT_A'].sum()/len(ATP)*100, 2), round(ATP['FaceP_A'].sum()/len(ATP)*100, 2)],
        'BarColor': ['yellow', 'red']})
dgP = pd.DataFrame({'Direct Gaze P': ['Face T', 'Face A'],
        'Frequency (%)': [ round(ATP['FaceT_P'].sum()/len(ATP)*100, 2), round(ATP['FaceA_P'].sum()/len(ATP)*100, 2)],
        'BarColor': ['yellow', 'blue']})

mg = pd.DataFrame({'Mutual Gaze': ['TA', 'TP', 'AP'],
        'Frequency (%)': [round(ATP['mutualGaze_TA'].sum()/len(ATP)*100, 2), round(ATP['mutualGaze_TP'].sum()/len(ATP)*100, 2),round(ATP['mutualGaze_AP'].sum()/len(ATP)*100, 2)], 
        'BarColor': ['green', 'darkorange', 'purple']})

jg = pd.DataFrame({'Joint Gaze': ['T', 'A', 'P'],
        'Frequency (%)': [round(ATP['jointGazeT_AP'].sum()/len(ATP)*100, 2), round(ATP['jointGazeA_TP'].sum()/len(ATP)*100, 2), round(ATP['jointGazeP_TA'].sum()/len(ATP)*100, 2)], 
        'BarColor': ['yellow', 'blue', 'red']})

jgs = pd.DataFrame({'Joint Gaze at Speaker': ['T', 'A', 'P'],
        'Frequency (%)': [round(ATP['jointGazeTsp_AP'].sum()/len(ATP)*100, 2), round(ATP['jointGazeAsp_TP'].sum()/len(ATP)*100, 2), round(ATP['jointGazePsp_TA'].sum()/len(ATP)*100, 2)], 
        'BarColor': ['yellow', 'blue', 'red']})

sp = pd.DataFrame({'Speech': ['T', 'A', 'P'],
        'Frequency (%)': [round(ATP['sp_T'].sum()/len(ATP)*100, 2), round(ATP['sp_A'].sum()/len(ATP)*100, 2), round(ATP['sp_P'].sum()/len(ATP)*100, 2)], 
        'BarColor': ['yellow', 'blue', 'red']})

# DG Summary
sns.set(style="whitegrid")
fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(8,3))
sns.barplot(x='Direct Gaze T', y='Frequency (%)', data=dgT, ci=None, palette=dgT['BarColor'], ax = axes[0])
sns.barplot(x='Direct Gaze A', y='Frequency (%)', data=dgA, ci=None, palette=dgA['BarColor'], ax = axes[1])
sns.barplot(x='Direct Gaze P', y='Frequency (%)', data=dgP, ci=None, palette=dgP['BarColor'], ax = axes[2])
plt.tight_layout()
plt.show()

# Speech Summary
sns.barplot(x='Speech', y='Frequency (%)', data=sp, ci=None, palette=jg['BarColor'])

# MG and JGS Summary
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(10,4))
sns.barplot(x='Mutual Gaze', y='Frequency (%)', data=mg, ci=None, palette=mg['BarColor'], ax = axes[0])
#sns.barplot(x='JointGaze', y='Frequency (%)', data=jg, ci=None, palette=jg['BarColor'], ax = axes[1])
sns.barplot(x='Joint Gaze at Speaker', y='Frequency (%)', data=jgs, ci=None, palette=jgs['BarColor'], ax = axes[1])
plt.tight_layout()
plt.show()

# Speech

# DG over time
fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(10,5))
sns.lineplot(x=ATP.index, y=ATP['FaceA_T'], color = 'blue', ax = axes[0])
sns.lineplot(x=ATP.index, y=ATP['FaceP_T'], color = 'red', ax = axes[1])
plt.tight_layout()
plt.show()

fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(10,5))
sns.lineplot(x=ATP.index, y=ATP['FaceT_A'], color = 'gold', ax = axes[0])
sns.lineplot(x=ATP.index, y=ATP['FaceP_A'], color = 'red', ax = axes[1])
plt.tight_layout()
plt.show()

fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(10,5))
sns.lineplot(x=ATP.index, y=ATP['FaceT_P'], color = 'gold', ax = axes[0])
sns.lineplot(x=ATP.index, y=ATP['FaceA_P'], color = 'blue', ax = axes[1])
plt.tight_layout()
plt.show()

# MG over time
fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(10, 8))
sns.lineplot(x=ATP.index, y=ATP['mutualGaze_TA'], color = 'green', ax = axes[0])
sns.lineplot(x=ATP.index, y=ATP['mutualGaze_TP'], color = 'darkorange', ax = axes[1])
sns.lineplot(x=ATP.index, y=ATP['mutualGaze_AP'], color = 'purple', ax = axes[2])
plt.tight_layout()
plt.show()

# JG over time
fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(10, 8))
sns.lineplot(x=ATP.index, y=ATP['jointGazeT_AP'], color = 'gold', ax = axes[0])
sns.lineplot(x=ATP.index, y=ATP['jointGazeA_TP'], color = 'blue', ax = axes[1])
sns.lineplot(x=ATP.index, y=ATP['jointGazeP_TA'], color = 'red', ax = axes[2])
plt.tight_layout()
plt.show()

# JGS over time
fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(10, 8))
sns.lineplot(x=ATP.index, y=ATP['jointGazeTsp_AP'], color = 'gold', ax = axes[0])
sns.lineplot(x=ATP.index, y=ATP['jointGazeAsp_TP'], color = 'blue', ax = axes[1])
sns.lineplot(x=ATP.index, y=ATP['jointGazePsp_TA'], color = 'red', ax = axes[2])
plt.tight_layout()
plt.show()

# Speech over time
fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(10, 8))
sns.lineplot(x=ATP.index, y=ATP['sp_T'], color = 'gold', ax = axes[0], )
sns.lineplot(x=ATP.index, y=ATP['sp_A'], color = 'blue', ax = axes[1])
sns.lineplot(x=ATP.index, y=ATP['sp_P'], color = 'red', ax = axes[2])
plt.tight_layout()
plt.show()

# Compute Euclidian distance between participants' gaze points
ATP = ATP.assign(d_TA = lambda x: np.sqrt((x['x_T'] + x['x_A'])**2 + (x['y_T'] - x['y_A'])**2))
round(ATP['d_TA'][ATP['d_TA'] <= 150].count()/len(ATP)*100, 2) #25.61% (-9.08% joint gaze at P = 16.53%)

ATP = ATP.assign(d_TP = lambda x: np.sqrt((x['x_T'] + x['x_P'])**2 + (x['y_T'] - x['y_P'])**2))
round(ATP['d_TP'][ATP['d_TP'] <= 150].count()/len(ATP)*100, 2) #28.86% (-7.51% joint gaze at A = 21.35%)

ATP = ATP.assign(d_AP = lambda x: np.sqrt((x['x_A'] + x['x_P'])**2 + (x['y_A'] - x['y_P'])**2))
round(ATP['d_AP'][ATP['d_AP'] <= 150].count()/len(ATP)*100, 2) #38.51% (-33.29% joint gaze at T = 5.22%)
                                                            
                                    # -> there is something more here
# Overall Pearson Correlation
#----------------------------

# Taking the values before interpolation and downsampling
 # x
TAx = pd.DataFrame({'x_T': dfT['obj_Gaze_X'], 'x_A': -dfA['obj_Gaze_X']})
TPx = pd.DataFrame({'x_T': dfT['obj_Gaze_X'], 'x_P': -dfP['obj_Gaze_X']})
APx = pd.DataFrame({'x_A': dfA['obj_Gaze_X'], 'x_P': -dfP['obj_Gaze_X']})
rTAx, pTAx = overall_Pcor(TAx, 'x_T', 'x_A', 'x-coordinate')
rTPx, pTPx = overall_Pcor(TPx, 'x_T', 'x_P', 'x-coordinate')
rAPx, pAPx = overall_Pcor(APx, 'x_A', 'x_P', 'x-coordinate')

 # y
TAy = pd.DataFrame({'y_T': dfT['obj_Gaze_Y'], 'y_A': dfA['obj_Gaze_Y']})
TPy = pd.DataFrame({'y_T': dfT['obj_Gaze_Y'], 'y_P': dfP['obj_Gaze_Y']})
APy = pd.DataFrame({'y_A': dfA['obj_Gaze_Y'], 'y_P': dfP['obj_Gaze_Y']})
rTAy, pTAy = overall_Pcor(TAy, 'y_T', 'y_A', 'y-coordinate')
rTPy, pTPy = overall_Pcor(TPy, 'y_T', 'y_P', 'y-coordinate')
rAPy, pAPy = overall_Pcor(APy, 'y_A', 'y_P', 'y-coordinate')

 # d
TAd = pd.DataFrame({'d_T': dfT['Euclidian_distances'], 'd_A': dfA['Euclidian_distances']})
TPd = pd.DataFrame({'d_T': dfT['Euclidian_distances'], 'd_P': dfP['Euclidian_distances']})
APd = pd.DataFrame({'d_A': dfA['Euclidian_distances'], 'd_P': dfP['Euclidian_distances']})
rTAd, pTAd = overall_Pcor(TAd, 'd_T', 'd_A', 'marker distance')
rTPd, pTPd = overall_Pcor(TPd, 'd_T', 'd_P', 'marker distance')
rAPd, pAPd = overall_Pcor(APd, 'd_A', 'd_P', 'marker distance')

 # Face
TAf = pd.DataFrame({'FaceA_T': dfT['AOI hit [Screenshot T.jpeg - Face A-T]'], 'FaceT_A': dfA['AOI hit [Screenshot A.jpeg - Face T-A]']})
TPf = pd.DataFrame({'FaceP_T': dfT['AOI hit [Screenshot T.jpeg - Face P-T]'], 'FaceT_P': dfP['AOI hit [Screenshot P.jpeg - Face T-P]']})
APf = pd.DataFrame({'FaceP_A': dfA['AOI hit [Screenshot A.jpeg - Face P-A]'], 'FaceA_P': dfP['AOI hit [Screenshot P.jpeg - Face A-P]']})
rTAf, pTAf = overall_Pcor(TAf, 'FaceA_T', 'FaceT_A', 'Face AOI hit', plotIt=False)
rTPf, pTPf = overall_Pcor(TPf, 'FaceP_T', 'FaceP_T', 'Face AOI hit', plotIt=False)

rAPf, pAPf = overall_Pcor(APf, 'FaceP_A', 'FaceA_P', 'Face AOI hit', plotIt=False)
