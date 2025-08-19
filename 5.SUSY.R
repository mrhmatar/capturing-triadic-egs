                        #---------------------------#
                        #           SUSY            #
                        #           ====            #
                        # (Tschacher & Meier, 2019) #
                        #---------------------------#

## load packages
library(SUSY)

## set working directory
path = "~"
setwd(path)

## read in data from a flat file
dataTA = read.csv('TA.txt', header=TRUE, sep=" ", na.strings=".")
dataTP = read.csv('TP.txt', header=TRUE, sep=" ", na.strings=".")
dataAP = read.csv('AP.txt', header=TRUE, sep=" ", na.strings=".")
  
## compute SUSY for columns 1-2, 3-4, 5-6
resTA = susy(dataTA[, 1:8], segment=30, Hz=25, maxlag=3)
resTP = susy(dataTP[, 1:8], segment=30, Hz=25, maxlag=3)
resAP = susy(dataAP[, 1:8], segment=30, Hz=25, maxlag=3)

## print all SUSY computations
resTA
resTP
resAP

## subset (and print) susy object to single results
resTA[1]
resTA[2]
resTA[3]

## plot SUSY computations, plot type 1, 2, 3, 4, 5
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

## export to flat file via data.frame and write.csv
dfTA = as.data.frame(resTA)
write.csv(dfTA, paste(path, "SUSY_TA.csv", sep = "/"), row.names=FALSE)

dfTP = as.data.frame(resTP)
write.csv(dfTP, paste(path, "SUSY_TP.csv", sep = "/"), row.names=FALSE)

dfAP = as.data.frame(resAP)
write.csv(dfAP, paste(path, "SUSY_AP.csv", sep = "/"), row.names=FALSE)

