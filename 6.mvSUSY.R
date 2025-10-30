# ==================================================
# 6. Multivariate Surrogate Synchrony (mv-SUSY)
# ==================================================

# Load required package
# ----------------------
library(mvSUSY)

# Set working directory
# ---------------------
path <- "~"   # Change to project path as needed
setwd(path)

# Read in triadic data (exported from Python)
# -------------------------------------------
TAPx <- read.csv("TAPx.txt", header = TRUE, sep = " ", na.strings = ".")
TAPy <- read.csv("TAPy.txt", header = TRUE, sep = " ", na.strings = ".")
TAPf <- read.csv("TAPf.txt", header = TRUE, sep = " ", na.strings = ".")

# Compute mvSUSY using 'lambda_max' method
# ----------------------------------------
set.seed(1234)   
res_x = mvsusy(TAPx, segment=10, Hz=25)
res_y = mvsusy(TAPy, segment=10, Hz=25)
res_f = mvsusy(TAPf, segment=10, Hz=25)

# Print full results
# ------------------
res_x 
res_y 
res_f 

# Plot results
# ------------
x11(width=6, height=4)
plot(res_x, type="density")
x11(width=6, height=4)
plot(res_x, type="segment-wise")

x11(width=6, height=4)
plot(res_y, type="density")
x11(width=6, height=4)
plot(res_y, type="segment-wise")

x11(width=6, height=4)
plot(res_f, type="density")
x11(width=6, height=4)
plot(res_f, type="segment-wise")

# Export results
# --------------------------------------------------
mvSUSYlambda_TAPx <- as.data.frame(res_x)
mvSUSYlambda_TAPy <- as.data.frame(res_y)
mvSUSYlambda_TAPf <- as.data.frame(res_f)

write.csv(mvSUSYlambda_TAPx, file.path(path, "mvSUSYlambda_TAPx.csv"), row.names = FALSE)
write.csv(mvSUSYlambda_TAPy, file.path(path, "mvSUSYlambda_TAPy.csv"), row.names = FALSE)
write.csv(mvSUSYlambda_TAPf, file.path(path, "mvSUSYlambda_TAPf.csv"), row.names = FALSE)

cat("\n[OK] Exported mvSUSYlambda_TAPx.csv, mvSUSYlambda_TAPy.csv, mvSUSYlambda_TAPf.csv\n")

# Results summary
#----------------
mvSUSYlambda_TAPx[c(12,14,16)] <- round(mvSUSYlambda_TAPx[c(12,14,16)], 3)
mvSUSYlambda_TAPx[c(8,13,15)] <- round(mvSUSYlambda_TAPx[c(8,13,15)], 2)

mvSUSYlambda_TAPy[c(12,14,16)] <- round(mvSUSYlambda_TAPy[c(12,14,16)], 3)
mvSUSYlambda_TAPy[c(8,13,15)] <- round(mvSUSYlambda_TAPy[c(8,13,15)], 2)

mvSUSYlambda_TAPf[c(12,14,16)] <- round(mvSUSYlambda_TAPf[c(12,14,16)], 3)
mvSUSYlambda_TAPf[c(8,13,15)] <- round(mvSUSYlambda_TAPf[c(8,13,15)], 2)

mvSUSYlambda_TAPx[c(8,12,13,14,15,16)] 
#real_mean    ES t_statistic p_value statistic_nonpar p_value_nonpar
#t     49.71 0.094       -0.56   0.579            20417           0.76

mvSUSYlambda_TAPy[c(8,12,13,14,15,16)] 
# real_mean    ES t_statistic p_value statistic_nonpar p_value_nonpar
# t     45.56 0.051       -0.32    0.75            20434          0.767

mvSUSYlambda_TAPf[c(8,12,13,14,15,16)] 
# real_mean    ES t_statistic p_value statistic_nonpar p_value_nonpar
# t     29.16 0.645       -2.74   0.009            15620          0.005
