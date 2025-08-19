                      #---------------------------#
                      #           mv-SUSY         #
                      #           =======         #
                      # (Tschacher & Meier, 2021) #
                      #---------------------------#

library(mvSUSY)

## set working directory
path = "~"
setwd(path)

## read in data from a flat file 
TAPx = read.csv('TAPx.txt', header=TRUE, sep=" ", na.strings=".")
TAPy = read.csv('TAPy.txt', header=TRUE, sep=" ", na.strings=".")
TAPf = read.csv('TAPf.txt', header=TRUE, sep=" ", na.strings=".")

## compute mvSUSY using 'lambda_max' method
res_x = mvsusy(TAPx, segment=10, Hz=25)
res_y = mvsusy(TAPy, segment=10, Hz=25)
res_f = mvsusy(TAPf, segment=10, Hz=25)

## plot
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

## export to flat file via data.frame and write.csv
mvSUSYlambda_TAPx = as.data.frame(res_x)
mvSUSYlambda_TAPy = as.data.frame(res_y)
mvSUSYlambda_TAPf = as.data.frame(res_f)

# Put everything in the same dataframe

write.csv(mvSUSYlambda_TAPx, paste(path, "mvSUSYlambda_TAPx.csv", sep = "/"), row.names=FALSE)
write.csv(mvSUSYlambda_TAPy, paste(path, "mvSUSYlambda_TAPy.csv", sep = "/"), row.names=FALSE)
write.csv(mvSUSYlambda_TAPf, paste(path, "mvSUSYlambda_TAPf.csv", sep = "/"), row.names=FALSE)

