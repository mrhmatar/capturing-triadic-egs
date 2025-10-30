# -*- coding: utf-8 -*-
"""
# ==================================================
# 4. Descriptive Statistics
# ==================================================
                        
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statistics
import os

# Define working directory (set manually before running)
os.chdir("C:/path/to/project")  # Change as appropriate

# Read data
ATP = pd.read_csv("ATP.csv")

# Descriptive statistics for primary variables
#---------------------------------------------
descATP = ATP.describe()
descT = descATP[['x_T', 'y_T', 'd_T', 'FaceA_T', 'FaceP_T']]
descA = descATP[['x_A', 'y_A', 'd_A', 'FaceT_A', 'FaceP_A']]
descP = descATP[['x_P', 'y_P', 'd_P', 'FaceT_P', 'FaceA_P']]

 # Boxplots for spatial and distance variables
#---------------------------------------------
sns.set(style="whitegrid")
fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(10, 8))
sns.boxplot(x=ATP['x_T'], ax=axes[0, 0]); axes[0, 0].set_xlabel('x_T')
sns.boxplot(x=ATP['y_T'], ax=axes[0, 1]); axes[0, 1].set_xlabel('y_T')
sns.boxplot(x=ATP['d_T'], ax=axes[0, 2]); axes[0, 2].set_xlabel('d_T')

sns.boxplot(x=ATP['x_A'], ax=axes[1, 0]); axes[1, 0].set_xlabel('x_A')
sns.boxplot(x=ATP['y_A'], ax=axes[1, 1]); axes[1, 1].set_xlabel('y_A')
sns.boxplot(x=ATP['d_A'], ax=axes[1, 2]); axes[1, 2].set_xlabel('d_A')

sns.boxplot(x=ATP['x_P'], ax=axes[2, 0]); axes[2, 0].set_xlabel('x_P')
sns.boxplot(x=ATP['y_P'], ax=axes[2, 1]); axes[2, 1].set_xlabel('y_P')
sns.boxplot(x=ATP['d_P'], ax=axes[2, 2]); axes[2, 2].set_xlabel('d_P')

plt.tight_layout()
plt.show()

# Plot probability distribution
fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(10, 8))
sns.kdeplot(ATP['x_T'], fill=True, ax=axes[0, 0]); axes[0, 0].set_xlabel('x_T')
sns.kdeplot(ATP['y_T'], color='darkorange', fill=True, ax=axes[0, 1]); axes[0, 1].set_xlabel('y_T')
sns.kdeplot(ATP['d_T'], color='forestgreen', fill=True, ax=axes[0, 2]); axes[0, 2].set_xlabel('d_T')

sns.kdeplot(ATP['x_A'], fill=True, ax=axes[1, 0]); axes[1, 0].set_xlabel('x_A')
sns.kdeplot(ATP['y_A'], color='darkorange', fill=True, ax=axes[1, 1]); axes[1, 1].set_xlabel('y_A')
sns.kdeplot(ATP['d_A'], color='forestgreen', fill=True, ax=axes[1, 2]); axes[1, 2].set_xlabel('d_A')

sns.kdeplot(ATP['x_P'], fill=True, ax=axes[2, 0]); axes[2, 0].set_xlabel('x_P')
sns.kdeplot(ATP['y_P'], color='darkorange', fill=True, ax=axes[2, 1]); axes[2, 1].set_xlabel('y_P')
sns.kdeplot(ATP['d_P'], color='forestgreen', fill=True, ax=axes[2, 2]); axes[2, 2].set_xlabel('d_P')

plt.tight_layout()
plt.show()

# Mean gaze coordinates (x, y, distance) for face AOIs
# --------------------------------------------------
print("Mean gaze coordinates per face AOI:")
print("T->A:", ATP[ATP['FaceA_T'] == 1].mean()[0:3])
print("T->P:", ATP[ATP['FaceP_T'] == 1].mean()[0:3])
print("A->T:", ATP[ATP['FaceT_A'] == 1].mean()[5:8])
print("A->P:", ATP[ATP['FaceP_A'] == 1].mean()[5:8])
print("P->A:", ATP[ATP['FaceA_P'] == 1].mean()[10:13])
print("P->T:", ATP[ATP['FaceT_P'] == 1].mean()[10:13])

# Gaze event proportions (% of frames)
# --------------------------------------------------

# Direct gaze
dgT_A = round(ATP['FaceA_T'].sum() / len(ATP) * 100, 2)
dgT_P = round(ATP['FaceP_T'].sum() / len(ATP) * 100, 2)
dgA_T = round(ATP['FaceT_A'].sum() / len(ATP) * 100, 2)
dgA_P = round(ATP['FaceP_A'].sum() / len(ATP) * 100, 2)
dgP_A = round(ATP['FaceA_P'].sum() / len(ATP) * 100, 2)
dgP_T = round(ATP['FaceT_P'].sum() / len(ATP) * 100, 2)

print("Direct gaze frequencies (%):", dgT_A, dgT_P, dgA_T, dgA_P, dgP_A, dgP_T)
#Direct gaze frequencies (%): 23.78 21.26 56.53 22.42 17.38 46.75
mean_direct = round(statistics.mean([dgT_A + dgT_P, dgA_T + dgA_P, dgP_A + dgP_T]), 2)
sd_direct = round(statistics.stdev([dgT_A + dgT_P, dgA_T + dgA_P, dgP_A + dgP_T]), 2)
print("Mean direct gaze %:", mean_direct, "| SD:", sd_direct)
#Mean direct gaze %: 62.71 | SD: 17.0

# Mutual gaze 
mg_TA = round(ATP['mutualGaze_TA'].sum() / len(ATP) * 100, 2)
mg_TP = round(ATP['mutualGaze_TP'].sum() / len(ATP) * 100, 2)
mg_AP = round(ATP['mutualGaze_AP'].sum() / len(ATP) * 100, 2)

print(f"Mutual gaze (%): TA={mg_TA}, TP={mg_TP}, AP={mg_AP}")
#Mutual gaze (%): TA=13.77, TP=13.03, AP=5.61
mean_mg = round(statistics.mean([mg_TA, mg_TP, mg_AP]), 2)
sd_mg = round(statistics.stdev([mg_TA, mg_TP, mg_AP]), 2)
print("Mean mutual gaze %:", mean_mg, "| SD:", sd_mg)
#Mean mutual gaze %: 10.8 | SD: 4.51

# Joint gaze at speaker
jgs_T = round(ATP['jointGazeTsp_AP'].sum() / len(ATP) * 100, 2)
jgs_A = round(ATP['jointGazeAsp_TP'].sum() / len(ATP) * 100, 2)
jgs_P = round(ATP['jointGazePsp_TA'].sum() / len(ATP) * 100, 2)

print(f"Joint gaze at speaker (%): T={jgs_T}, A={jgs_A}, P={jgs_P}")
#Joint gaze at speaker (%): T=13.12, A=2.12, P=2.39
mean_jgs = round(statistics.mean([jgs_T, jgs_A, jgs_P]), 2)
sd_jgs = round(statistics.stdev([jgs_T, jgs_A, jgs_P]), 2)
print("Mean joint gaze at speaker %:", mean_jgs, "| SD:", sd_jgs)
#Mean joint gaze at speaker %: 5.88 | SD: 6.27

# Joint gaze 
jg_T = round(ATP['jointGazeT_AP'].sum() / len(ATP) * 100, 2)
jg_A = round(ATP['jointGazeA_TP'].sum() / len(ATP) * 100, 2)
jg_P = round(ATP['jointGazeP_TA'].sum() / len(ATP) * 100, 2)

print(f"Joint gaze (%): T={jg_T}, A={jg_A}, P={jg_P}")
#Joint gaze (%): T=33.19, A=7.44, P=9.09
mean_jg = round(statistics.mean([jg_T, jg_A, jg_P]), 2)
sd_jg = round(statistics.stdev([jg_T, jg_A, jg_P]), 2)
print("Mean joint gaze %:", mean_jg, "| SD:", sd_jg)
#Mean joint gaze %: 16.57 | SD: 14.41

# Speech
sp_A = round(ATP['sp_A'].sum() / len(ATP) * 100, 2)
sp_T = round(ATP['sp_T'].sum() / len(ATP) * 100, 2)
sp_P = round(ATP['sp_P'].sum() / len(ATP) * 100, 2)

print(f"Speaking time (%): T={sp_T}, A={sp_A}, P={sp_P}")
#Speaking time (%): T=38.76, A=33.69, P=27.65
mean_sp = round(statistics.mean([sp_T, sp_A, sp_P]), 2)
sd_sp = round(statistics.stdev([sp_T, sp_A, sp_P]), 2)
print("Mean speaking time %:", mean_sp, "| SD:", sd_sp)
#Mean speaking time %: 33.37 | SD: 5.56

dgT = pd.DataFrame({'Direct Gaze T': ['Face A', 'Face P'],
        'Frequency (%)': [round(ATP['FaceA_T'].sum()/len(ATP)*100, 2), round(ATP['FaceP_T'].sum()/len(ATP)*100, 2)]})
dgA = pd.DataFrame({'Direct Gaze A': ['Face T', 'Face P'],
        'Frequency (%)': [ round(ATP['FaceT_A'].sum()/len(ATP)*100, 2), round(ATP['FaceP_A'].sum()/len(ATP)*100, 2)]})
dgP = pd.DataFrame({'Direct Gaze P': ['Face T', 'Face A'],
        'Frequency (%)': [ round(ATP['FaceT_P'].sum()/len(ATP)*100, 2), round(ATP['FaceA_P'].sum()/len(ATP)*100, 2)]})

mg = pd.DataFrame({'Mutual Gaze': ['T-A', 'T-P', 'A-P'],
        'Frequency (%)': [round(ATP['mutualGaze_TA'].sum()/len(ATP)*100, 2), round(ATP['mutualGaze_TP'].sum()/len(ATP)*100, 2),round(ATP['mutualGaze_AP'].sum()/len(ATP)*100, 2)]})

jg = pd.DataFrame({'Joint Gaze': ['T', 'A', 'P'],
        'Frequency (%)': [round(ATP['jointGazeT_AP'].sum()/len(ATP)*100, 2), round(ATP['jointGazeA_TP'].sum()/len(ATP)*100, 2), round(ATP['jointGazeP_TA'].sum()/len(ATP)*100, 2)]})

jgs = pd.DataFrame({'Joint Gaze at Speaker': ['T', 'A', 'P'],
        'Frequency (%)': [round(ATP['jointGazeTsp_AP'].sum()/len(ATP)*100, 2), round(ATP['jointGazeAsp_TP'].sum()/len(ATP)*100, 2), round(ATP['jointGazePsp_TA'].sum()/len(ATP)*100, 2)]})

sp = pd.DataFrame({'Speech': ['T', 'A', 'P'],
        'Frequency (%)': [round(ATP['sp_T'].sum()/len(ATP)*100, 2), round(ATP['sp_A'].sum()/len(ATP)*100, 2), round(ATP['sp_P'].sum()/len(ATP)*100, 2)]})

# Plot summary bar charts
# --------------------------------------------------
dgT = pd.DataFrame({'Direct Gaze T': ['Face A', 'Face P'],
        'Frequency (%)': [round(ATP['FaceA_T'].sum()/len(ATP)*100, 2), round(ATP['FaceP_T'].sum()/len(ATP)*100, 2)]})
dgA = pd.DataFrame({'Direct Gaze A': ['Face T', 'Face P'],
        'Frequency (%)': [ round(ATP['FaceT_A'].sum()/len(ATP)*100, 2), round(ATP['FaceP_A'].sum()/len(ATP)*100, 2)]})
dgP = pd.DataFrame({'Direct Gaze P': ['Face T', 'Face A'],
        'Frequency (%)': [ round(ATP['FaceT_P'].sum()/len(ATP)*100, 2), round(ATP['FaceA_P'].sum()/len(ATP)*100, 2)]})

mg = pd.DataFrame({'Mutual Gaze': ['T-A', 'T-P', 'A-P'],
        'Frequency (%)': [round(ATP['mutualGaze_TA'].sum()/len(ATP)*100, 2), round(ATP['mutualGaze_TP'].sum()/len(ATP)*100, 2),round(ATP['mutualGaze_AP'].sum()/len(ATP)*100, 2)]})

jg = pd.DataFrame({'Joint Gaze': ['T', 'A', 'P'],
        'Frequency (%)': [round(ATP['jointGazeT_AP'].sum()/len(ATP)*100, 2), round(ATP['jointGazeA_TP'].sum()/len(ATP)*100, 2), round(ATP['jointGazeP_TA'].sum()/len(ATP)*100, 2)]})

jgs = pd.DataFrame({'Joint Gaze at Speaker': ['T', 'A', 'P'],
        'Frequency (%)': [round(ATP['jointGazeTsp_AP'].sum()/len(ATP)*100, 2), round(ATP['jointGazeAsp_TP'].sum()/len(ATP)*100, 2), round(ATP['jointGazePsp_TA'].sum()/len(ATP)*100, 2)]})

sp = pd.DataFrame({'Speech': ['T', 'A', 'P'],
        'Frequency (%)': [round(ATP['sp_T'].sum()/len(ATP)*100, 2), round(ATP['sp_A'].sum()/len(ATP)*100, 2), round(ATP['sp_P'].sum()/len(ATP)*100, 2)]})

# Direct Gaze 
sns.set(style="whitegrid")
fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(6,2))
sns.barplot(x='Direct Gaze T', y='Frequency (%)',  data=dgT, legend=None, palette=['lightskyblue', 'red'], ax = axes[0])
sns.barplot(x='Direct Gaze A', y='Frequency (%)', data=dgA, legend=None, palette=['yellow', 'red'], ax = axes[1])
sns.barplot(x='Direct Gaze P', y='Frequency (%)', data=dgP, legend=None, palette=['yellow', 'lightskyblue'], ax = axes[2])
plt.tight_layout()
plt.show()

# Speech 
sns.set(style="whitegrid")
fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(4,3))
sns.barplot(x='Speech', y='Frequency (%)', data=sp, legend=None, palette=['yellow', 'lightskyblue', 'red'])
plt.tight_layout()
plt.show()

# Mutual Gaze and Joint Gaze at Speaker 
sns.set(style="whitegrid")
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(8,3))
sns.barplot(x='Mutual Gaze', y='Frequency (%)', data=mg, legend=None, palette=['lawngreen', 'orange', 'mediumorchid'], ax = axes[0])
#sns.barplot(x='JointGaze', y='Frequency (%)', data=jg, legend=None, palette=['yellow', 'lightskyblue', 'red'], ax = axes[1])
sns.barplot(x='Joint Gaze at Speaker', y='Frequency (%)', data=jgs, legend=None, palette=['yellow', 'lightskyblue', 'red'], ax = axes[1])
plt.tight_layout()
plt.show()


