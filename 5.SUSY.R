# ==================================================
# 5. Surrogate Synchrony Analysis (SUSY)
# ==================================================

# Load required package
# ---------------------
library(SUSY)
library(glue)

# Set working directory
# ---------------------
path <- "~"   # Change to your project path if needed
setwd(path)


# Read in dyadic data (exported from Python)
# ------------------------------------------
dataTA <- read.csv("TA.txt", header = TRUE, sep = " ", na.strings = ".")
dataTP <- read.csv("TP.txt", header = TRUE, sep = " ", na.strings = ".")
dataAP <- read.csv("AP.txt", header = TRUE, sep = " ", na.strings = ".")

# Compute SUSY for each dyad
# --------------------------
resTA = susy(dataTA[, 1:8], segment=30, Hz=25, maxlag=3)
resTP = susy(dataTP[, 1:8], segment=30, Hz=25, maxlag=3)
resAP = susy(dataAP[, 1:8], segment=30, Hz=25, maxlag=3)

# Print full results
# ------------------
resTA 
resTP 
resAP 

# Plot synchrony results 
# ----------------------
plot(resTA[1], type=1:5)
plot(resTA[2], type=1:5)
plot(resTA[3], type=1:5)
plot(resTA[4], type=1:5)

plot(resTP[1], type=1:5)
plot(resTP[2], type=1:5)
plot(resTP[3], type=1:5)
plot(resTP[4], type=1:5)

plot(resAP[1], type=1:5)
plot(resAP[2], type=1:5)
plot(resAP[3], type=1:5)
plot(resAP[4], type=1:5)

# Export results to csv
# ----------------------
write.csv(dfTA, file.path(path, "SUSY_TA.csv"), row.names = FALSE)
write.csv(dfTP, file.path(path, "SUSY_TP.csv"), row.names = FALSE)
write.csv(dfAP, file.path(path, "SUSY_AP.csv"), row.names = FALSE)

cat("\n[OK] Exported SUSY_TA.csv, SUSY_TP.csv, SUSY_AP.csv\n")

# Results summary
#----------------
dfTA <- as.data.frame(resTA)
dfTP <- as.data.frame(resTP)
dfAP <- as.data.frame(resAP)

glue("\n--- SUSY: ---\n 
    x: mean ES_abs = {round((dfTA[1,11]+ dfTP[1,11]+dfAP[1,11])/3,2)}; mean ES_noabs = {round((dfTA[1,23]+ dfTP[1,23]+dfAP[1,23])/3,2)}\n
    y: mean ES_abs = {round((dfTA[2,11]+ dfTP[2,11]+dfAP[2,11])/3,2)}; mean ES_noabs = {round((dfTA[2,23]+ dfTP[2,23]+dfAP[2,23])/3,2)}\n
    f: mean ES_abs = {round((dfTA[4,11]+ dfTP[4,11]+dfAP[4,11])/3,2)}; mean ES_noabs = {round((dfTA[4,23]+ dfTP[4,23]+dfAP[4,23])/3,2)}")

glue("\n--- SUSY: ---\n 
    TP: mean ES_abs_xy = {round((dfTP[1,11]+ dfTP[2,11])/2,2)}; mean ES_noabs_xy = {round((dfTP[1,23]+ dfTP[2,23])/2,2)}\n
    TA: mean ES_abs_xy = {round((dfTA[1,11]+ dfTA[2,11])/2,2)}; mean ES_noabs_xy = {round((dfTA[1,23]+ dfTA[2,23])/2,2)}\n
    AP: mean ES_abs_xy = {round((dfAP[1,11]+ dfAP[2,11])/2,2)}; mean ES_noabs_xy = {round((dfAP[1,23]+ dfAP[2,23])/2,2)}\n")

dfTA[c(4, 20)] <- round(dfTA[c(4, 20)],3)
dfTA[c(11, 23)] <- round(dfTA[c(11, 23)],2)
dfTP[c(4, 20)] <- round(dfTP[c(4, 20)],3)
dfTP[c(11, 23)] <- round(dfTP[c(11, 23)],2)
dfAP[c(4, 20)] <- round(dfAP[c(4, 20)],3)
dfAP[c(11, 23)] <- round(dfAP[c(11, 23)],2)

dfTA[c(4, 11, 20, 23)]
dfTP[c(4, 11, 20, 23)]
dfAP[c(4, 11, 20, 23)]

dfTA[c(4, 11, 20, 23)]
dfTP[c(4, 11, 20, 23)]
dfAP[c(4, 11, 20, 23)]


