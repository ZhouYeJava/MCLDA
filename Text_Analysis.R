#####################
###Analytical Plot###
#####################

###Zhou Ye###
###12/05/2013###

rm(list=ls())
setwd("/Users/zhouye/Documents/Machine_Learning/Output/")
likelihoodLineNumber <- 1100

###Likelihood Gibbs And Blocked Gibbs###
trainGibbsLL <- file("./gibbs_25_0.5_0.1/collapsed-output-25-0.5-0.1.txt-trainll")
testGibbsLL <- file("./gibbs_25_0.5_0.1/collapsed-output-25-0.5-0.1.txt-testll")
open(trainGibbsLL)
trainGibbs <- vector(length=likelihoodLineNumber)
count <- 1
while (length(line <- readLines(trainGibbsLL, n=1, warn=F))>0) {
  trainGibbs[count] <- as.numeric(unlist(line))
  count <- count+1
} 
close(trainGibbsLL)
open(testGibbsLL)
testGibbs <- vector(length=likelihoodLineNumber)
count <- 1
while (length(line <- readLines(testGibbsLL, n=1, warn=F))>0) {
  testGibbs[count] <- as.numeric(unlist(line))
  count <- count+1
} 
close(testGibbsLL)
trainBlockGibbsLL <- file("./blocked_gibbs_25_0.5_0.1/blocked-collapsed-output-25-0.5-0.1.txt-trainll")
testBlockGibbsLL <- file("./blocked_gibbs_25_0.5_0.1/blocked-collapsed-output-25-0.5-0.1.txt-testll")
open(trainBlockGibbsLL)
trainBlockGibbs <- vector(length=likelihoodLineNumber)
count <- 1
while (length(line <- readLines(trainBlockGibbsLL, n=1, warn=F))>0) {
  trainBlockGibbs[count] <- as.numeric(unlist(line))
  count <- count+1
} 
close(trainBlockGibbsLL)
open(testBlockGibbsLL)
testBlockGibbs <- vector(length=likelihoodLineNumber)
count <- 1
while (length(line <- readLines(testBlockGibbsLL, n=1, warn=F))>0) {
  testBlockGibbs[count] <- as.numeric(unlist(line))
  count <- count+1
} 
close(testBlockGibbsLL)
png("likelihood.png")
plot(NA, NA, main="Likehood For Train And Test", 
     xlab="Iteration", ylab="LogLikelihood",
     xlim=c(1, likelihoodLineNumber), ylim=c(-1000000, 0))
lines(1:likelihoodLineNumber, trainGibbs, col="red", lty=1)
lines(1:likelihoodLineNumber, testGibbs, col="blue", lty=1)
lines(1:likelihoodLineNumber, trainBlockGibbs, col="red", lty=2)
lines(1:likelihoodLineNumber, testBlockGibbs, col="blue", lty=2)
text(x=500, y=trainGibbs[500]+30000, labels="gibbs_train")
text(x=500, y=testGibbs[500]+30000, labels="gibbs_test")
text(x=500, y=trainBlockGibbs[500]-30000, labels="blocked_gibbs_train")
text(x=500, y=testBlockGibbs[500]-30000, labels="blocked_gibbs_test")
dev.off()

###Likelihood Gibbs And Blocked Gibbs###
trainGibbsLL <- file("./gibbs_25_0.5_0.1/collapsed-output-25-0.5-0.1.txt-trainll")
testGibbsLL <- file("./gibbs_25_0.5_0.1/collapsed-output-25-0.5-0.1.txt-testll")
timeGibbsLL <- file("./gibbs_25_0.5_0.1/collapsed-output-25-0.5-0.1.txt-time")
open(trainGibbsLL)
trainGibbs <- vector(length=likelihoodLineNumber)
count <- 1
while (length(line <- readLines(trainGibbsLL, n=1, warn=F))>0) {
  trainGibbs[count] <- as.numeric(unlist(line))
  count <- count+1
} 
close(trainGibbsLL)
open(testGibbsLL)
testGibbs <- vector(length=likelihoodLineNumber)
count <- 1
while (length(line <- readLines(testGibbsLL, n=1, warn=F))>0) {
  testGibbs[count] <- as.numeric(unlist(line))
  count <- count+1
} 
close(testGibbsLL)
open(timeGibbsLL)
timeGibbs <- vector(length=likelihoodLineNumber)
count <- 1
while (length(line <- readLines(timeGibbsLL, n=1, warn=F))>0) {
  timeGibbs[count] <- as.numeric(unlist(line))
  count <- count+1
} 
close(timeGibbsLL)
trainBlockGibbsLL <- file("./blocked_gibbs_25_0.5_0.1/blocked-collapsed-output-25-0.5-0.1.txt-trainll")
testBlockGibbsLL <- file("./blocked_gibbs_25_0.5_0.1/blocked-collapsed-output-25-0.5-0.1.txt-testll")
timeBlockGibbsLL <- file("./blocked_gibbs_25_0.5_0.1/blocked-collapsed-output-25-0.5-0.1.txt-time")
open(trainBlockGibbsLL)
trainBlockGibbs <- vector(length=likelihoodLineNumber)
count <- 1
while (length(line <- readLines(trainBlockGibbsLL, n=1, warn=F))>0) {
  trainBlockGibbs[count] <- as.numeric(unlist(line))
  count <- count+1
} 
close(trainBlockGibbsLL)
open(testBlockGibbsLL)
testBlockGibbs <- vector(length=likelihoodLineNumber)
count <- 1
while (length(line <- readLines(testBlockGibbsLL, n=1, warn=F))>0) {
  testBlockGibbs[count] <- as.numeric(unlist(line))
  count <- count+1
} 
close(testBlockGibbsLL)
open(timeBlockGibbsLL)
timeBlockGibbs <- vector(length=likelihoodLineNumber)
count <- 1
while (length(line <- readLines(timeBlockGibbsLL, n=1, warn=F))>0) {
  timeBlockGibbs[count] <- as.numeric(unlist(line))
  count <- count+1
} 
close(timeBlockGibbsLL)
png("time.png")
plot(NA, NA, main="Time For Gibbs And Blocked Gibbs", 
     xlab="Iteration", ylab="Time(s)",
     xlim=c(1, likelihoodLineNumber), ylim=c(0, 60000))
lines(1:likelihoodLineNumber, timeGibbs, col="red", lty=1)
lines(1:likelihoodLineNumber, timeBlockGibbs, col="blue", lty=1)
text(x=500, y=timeGibbs[500], labels="gibbs_time")
text(x=500, y=timeBlockGibbs[500], labels="blocked_gibbs_time")
dev.off()
png("likelihood_time.png")
plot(NA, NA, main="Likehood VS Time For Train And Test", 
     xlab="Time(s)", ylab="LogLikelihood",
     xlim=c(0, 60000), ylim=c(-1000000, 0))
lines(timeGibbs, trainGibbs, col="red", lty=1)
lines(timeGibbs, testGibbs, col="blue", lty=1)
lines(timeBlockGibbs, trainBlockGibbs, col="red", lty=2)
lines(timeBlockGibbs, testBlockGibbs, col="blue", lty=2)
text(x=timeGibbs[500], y=trainGibbs[500]+30000, labels="gibbs_train")
text(x=timeGibbs[500], y=testGibbs[500]+30000, labels="gibbs_test")
text(x=timeBlockGibbs[500], y=trainBlockGibbs[500]-30000, labels="blocked_gibbs_train")
text(x=timeBlockGibbs[500], y=testBlockGibbs[500]-30000, labels="blocked_gibbs_test")
dev.off()

###Topic Comparison###
topic <- c(10, 20, 30, 40, 50)
topicLL <- vector(length=length(topic))
for (t in 1:length(topic)) {
  f <- file(paste(c("./topic/blocked-collapsed-output", topic[t], "0.5-0.1.txt-final"), collapse="-"))
  open(f)
  line <- readLines(f, n=1, warn=F)
  topicLL[t] <- as.numeric(unlist(line))
  close(f)
}
png("topic_comparison.png")
plot(topic, topicLL, main="Topic Comparison", xlab="Topic Number", ylab="Test Log-Likelihood", col="red")
dev.off()