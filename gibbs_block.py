##########################
###Gibbs Block Sampling###
##########################

###Zhou Ye###
###12/3/2013###

import sys
from sets import Set
import random
import math
import copy
import time 

###Constant Parameters###
topic = None #topic set
alpha = None
beta = None
lam = None
burn = 1000 #burn-in time
iteration = 1100 #total iterations

###Information For Each Document###
class Document(object):
	def __init__(self, content, label):
		self.content = content
		self.length = len(content)
		self.label = label
		self.z = [None for y in range(0, len(content))]
		self.x = [None for y in range(0, len(content))]
	def __eq__(self, other):
		return (self.content, self.label)==(other.content, other.label)
	def __hash__(self):
		return(hash((tuple(self.content), self.label)))

###Information For Document Counts###
class Doc(object):
	def __init__(self, nkd, ntd):
		self.nkd = nkd
		self.ntd = ntd
	def changeValue(self, value):
		#value: value to be added; use negative value for deduction
		self.nkd += value
	def __str__(self):
		return(str(self.nkd)+","+str(self.ntd))

###Information For Word Counts###
class Word(object):
	def __init__(self, nwkg, nwk0, nwk1):
		self.nwkg = nwkg
		self.nwk0 = nwk0
		self.nwk1 = nwk1
	def changeValue(self, value, type):
		#value: value to be added; use negative value for deduction
		#type: -1 -- global; 0 -- label0; 1 -- label1
		if type==-1:
			self.nwkg += value
		elif type==0:
			self.nwk0 += value
		else:
			self.nwk1 += value
	def __str__(self):
		return(str(self.nwkg)+","++str(self.nwk0)+","+str(self.nwk1))

###Information For Total Word Counts###
class Total(object):
	def __init__(self, ntkg, ntk0, ntk1):
		self.ntkg = ntkg
		self.ntk0 = ntk0
		self.ntk1 = ntk1
	def changeValue(self, value, type):
		#value: value to be added; use negative value for deduction
		#type: -1 -- global; 0 -- label0; 1 -- label1
		if type==-1:
			self.ntkg += value
		elif type==0:
			self.ntk0 += value
		else:
			self.ntk1 += value
	def __str__(self):
		return(str(self.ntkg)+","++str(self.ntk0)+","+str(self.ntk1))

###Process Data Set And Build Vocabulary###
def process(filename):
	dataSet = []
	voc = Set()
	reader = open(filename, "r")
	data = reader.readlines()
	for line in data:
		line = line.strip()
		temp = line.split(" ")
		content = [None for y in range(0, (len(temp)-1))] #text
		label = None #class
		for i in range(0, len(temp)):
			if i==0:
				label = int(temp[0])
			else:
				content[i-1] = temp[i]
				voc.add(temp[i])
		doc = Document(content, label)
		dataSet.append(doc)
	return([dataSet, voc])

###Build Document Count Dictionary And Word Count Dictionary###
def buildDic(dataSet, voc):
	dicDoc = {}
	dicWord = {}
	dicTotal = {}
	for k in topic:
		dicTotal[k] = Total(0, 0, 0)
	for w in voc:
		for k in topic:
			dicWord[(w, k)] = Word(0, 0, 0)
	for doc in dataSet:
		for k in topic:
			dicDoc[(doc, k)] = 0
		for j in doc.z:
			dicDoc[(doc, j)] += 1
		for i in range(0, len(doc.content)):
			dicWord[(doc.content[i], doc.z[i])].nwkg += 1
			dicTotal[doc.z[i]].ntkg += 1
			if doc.label==0:
				dicWord[(doc.content[i], doc.z[i])].nwk0 += 1
				dicTotal[doc.z[i]].ntk0 += 1
			else:
				dicWord[(doc.content[i], doc.z[i])].nwk1 += 1
				dicTotal[doc.z[i]].ntk1 += 1
	return([dicDoc, dicWord, dicTotal])

def initialization(dataSet, indicator):
	#dataSet: training or testing set
	#indicator: "z" or "x"
	if indicator=="z":
		z = [[None for b in range(0, len(dataSet[a].content))] for a in range(0, len(dataSet))]
		for i in range(0, len(z)):
			for j in range(0, len(z[i])):
				z[i][j] = random.choice(topic)
		return(z)
	elif indicator=="x":
		x = [[None for b in range(0, len(dataSet[a].content))] for a in range(0, len(dataSet))]
		for i in range(0, len(x)):
			for j in range(0, len(x[i])):
				x[i][j] = random.choice(topic)
		return(x)
	else:
		print("Incorrect input arguments!")
		return(None)

def sampleZX(prob1, prob2):
	#prob1: an array of proportional probability with x = 0
	#prob2: an array of proportional probability with x = 1
	s = random.random()
	total = sum(prob1)+sum(prob2)
	for i in range(0, len(prob1)):
		if i==0:
			prob1[i] = prob1[i]/total
			if s>0 and s<=prob1[i]:
				return([topic[i], 0])
		else:
			prob1[i] = prob1[i]/total
			prob1[i] = prob1[i]+prob1[i-1]
			if s>prob1[i-1] and s<=prob1[i]:
				return([topic[i], 0])
	for i in range(0, len(prob2)):
		if i==0:
			prob2[i] = (prob2[i]+prob1[len(prob1)-1])/total
			if s>prob1[len(prob1)-1] and s<=prob2[i]:
				return([topic[i], 1])
		else:
			prob2[i] = prob2[i]/total
			prob2[i] = prob2[i]+prob2[i-1]
			if s>prob1[i-1] and s<=prob1[i]:
				return([topic[i], 1])

def assign(z, x, dataSet):
	#z: new z
	#x: new x
	#dataSet: training or testing set
	for i in range(0, len(dataSet)):
		for j in range(0, len(dataSet[i].content)):
			dataSet[i].z[j] = z[i][j]
			dataSet[i].x[j] = x[i][j]
	return(dataSet)

def expectedValue(paraSet):
	finalPara = {}
	for pair in paraSet[0]:
		mean = 0
		for i in range(0, len(paraSet)):
			mean += paraSet[i][pair]
		finalPara[pair] = mean/len(paraSet)
	return(finalPara)

def outputTheta(finalPara, trainingSet, filename):
	writer = open(filename, "w")
	for doc in trainingSet:
		line = ""
		for k in topic:
			line += str(finalPara[doc, k]).format("%.13e")+" "
		line += "\n"
		writer.write(line)
	writer.close()

def outputPhi(finalPara, voc, filename):
	writer = open(filename, "w")
	for word in voc:
		line = word+" "
		for k in topic:
			line += str(finalPara[word, k]).format("%.13e")+" "
		line += "\n"
		writer.write(line)
	writer.close()

def outputLikelihood(likelihood, filename):
	writer = open(filename, "w")
	for l in likelihood:
		writer.write(str(l).format("%.13e")+"\n")
	writer.close()

def outputTime(iterationTime, filename):
	writer = open(filename, "w")
	for t in iterationTime:
		writer.write(str(t).format("%.13e")+"\n")
	writer.close()

def outputFinal(finalOutput, filename):
	writer = open(filename, "w")
	writer.write(str(finalOutput).format("%.13e"))
	writer.close()

if __name__=="__main__":
	#set parameters and process data sets
	[trainingSet, trainingVoc] = process(sys.argv[1])
	[testingSet, testingVoc] = process(sys.argv[2])
	allVoc = list(trainingVoc.union(testingVoc)) #all vocabulary
	output = sys.argv[3]
	numTopic = int(sys.argv[4])
	topic = [m+1 for m in range(0, numTopic)]
	lam = float(sys.argv[5])
	alpha = float(sys.argv[6])
	beta = float(sys.argv[7])
	iteration = int(sys.argv[8])
	burn = int(sys.argv[9])
	print("training_size="+str(len(trainingSet))+"\n"+"testing_size="+str(len(testingSet)))
	trainingTheta = {}
	trainingPhi =  {}
	trainingPhi0 = {}
	trainingPhi1 = {}
	testingTheta = {}
	thetaSet = []
	phiSet = []
	phi0Set = []
	phi1Set = []
	trainingLikelihood = []
	testingLikelihood = []
	iterationTime = []
	print("Finish Parameter Initilization")
	#random initilization on training set
	zTrain = initialization(trainingSet, "z") #initial random z
	xTrain = initialization(trainingSet, "x") #initial random x
	trainingSet = assign(zTrain, xTrain, trainingSet)
	trainingSetCopy = copy.deepcopy(trainingSet) #do modification for z and x
	#random initilization on testing set
	zTest = initialization(testingSet, "z") #initial random z
	xTest = initialization(testingSet, "x") #initial random x
	testingSet = assign(zTest, xTest, testingSet)
	testingSetCopy = copy.deepcopy(testingSet) #do modification for z and x
	print("Finish Traning/Testing Set Initilization")
	#initialize the count information
	[trainingDicD, trainingDicW, trainingDicT] = buildDic(trainingSet, allVoc) 
	[testingDicD, testingDicW, testingDicT] = buildDic(testingSet, allVoc) #testingDicW and testingDicT are useless
	#(doc, topic) -> counts; (word, topic) -> counts; topic -> counts
	[trainingDicDCopy, trainingDicWCopy, trainingDicTCopy] = [trainingDicD.copy(), trainingDicW.copy(), trainingDicT.copy()]
	testingDicDCopy = testingDicD.copy()
	print("Finish All Count Initilization")
	#gibbs sampling procedure (exclude (d, i) thus we need -1 on any n counts on sample z)
	start = time.time()
	for t in range(0, iteration):
		print("iteration"+str(t+1))
		#sample new z and x for training
		for i in range(0, len(trainingSet)):
			doc = trainingSet[i]
			for j in range(0, len(doc.content)):
				word = doc.content[j]
				probZX1 = [None for y in range(0, numTopic)]
				probZX2 = [None for y in range(0, numTopic)]
				for k in range(0, numTopic):
					nkd = trainingDicD[(doc, topic[k])]
					ntd = doc.length-1
					if topic[k]==doc.z[j]:
						nkd -= 1
					nwkg = trainingDicW[(word, topic[k])].nwkg
					ntkg = trainingDicT[topic[k]].ntkg
					if topic[k]==doc.z[j]:
						nwkg -= 1
						ntkg -= 1
					probZX1[k] = (1-lam)*((nkd+alpha)/(ntd+alpha*numTopic))*((nwkg+beta)/(ntkg+beta*len(allVoc)))
					if doc.label==0:
						nwk0 = trainingDicW[(word, topic[k])].nwk0
						ntk0 = trainingDicT[topic[k]].ntk0
						if topic[k]==doc.z[j]:
							nwk0 -= 1
							ntk0 -= 1
						probZX2[k] = lam*((nkd+alpha)/(ntd+alpha*numTopic))*((nwk0+beta)/(ntk0+beta*len(allVoc)))
					else:
						nwk1 = trainingDicW[(word, topic[k])].nwk1
						ntk1 = trainingDicT[topic[k]].ntk1
						if topic[k]==doc.z[j]:
							nwk1 -= 1
							ntk1 -= 1
						probZX2[k] = lam*((nkd+alpha)/(ntd+alpha*numTopic))*((nwk1+beta)/(ntk1+beta*len(allVoc)))
				[zNew, xNew] = sampleZX(probZX1, probZX2)
				#update counts for training
				trainingDicDCopy[(doc, doc.z[j])] -= 1
				trainingDicDCopy[(doc, zNew)] += 1
				trainingDicWCopy[(word, doc.z[j])].changeValue(-1, -1)
				trainingDicWCopy[(word, zNew)].changeValue(1, -1)
				trainingDicTCopy[doc.z[j]].changeValue(-1, -1)
				trainingDicTCopy[zNew].changeValue(1, -1)
				if doc.label==0:
					trainingDicWCopy[(word, doc.z[j])].changeValue(-1, 0)
					trainingDicWCopy[(word, zNew)].changeValue(1, 0)
					trainingDicTCopy[doc.z[j]].changeValue(-1, 0)
					trainingDicTCopy[zNew].changeValue(1, 0)
				else:
					trainingDicWCopy[(word, doc.z[j])].changeValue(-1, 1)
					trainingDicWCopy[(word, zNew)].changeValue(1, 1)
					trainingDicTCopy[doc.z[j]].changeValue(-1, 1)
					trainingDicTCopy[zNew].changeValue(1, 1)
				#update z and x
				trainingSetCopy[i].z[j] = zNew
				trainingSetCopy[i].x[j] = xNew
		print("Finish Sampling Training Set And Updating Training Counts")
		#evaluate phi for training set
		for i in range(0, len(allVoc)):
			for j in range(0, numTopic):
				nwkg = trainingDicWCopy[(allVoc[i], topic[j])].nwkg
				ntkg = trainingDicTCopy[topic[j]].ntkg
				trainingPhi[(allVoc[i], topic[j])] = (nwkg+beta)/(ntkg+beta*len(allVoc))
				nwk0 = trainingDicWCopy[(allVoc[i], topic[j])].nwk0 
				ntk0 = trainingDicTCopy[topic[j]].ntk0
				nwk1 = trainingDicWCopy[(allVoc[i], topic[j])].nwk1
				ntk1 = trainingDicTCopy[topic[j]].ntk1
				trainingPhi0[(allVoc[i], topic[j])] = (nwk0+beta)/(ntk0+beta*len(allVoc))
				trainingPhi1[(allVoc[i], topic[j])] = (nwk1+beta)/(ntk1+beta*len(allVoc))
		print("Finish Evaluating Phi For Training Set")
		#sample new z and x for testing
		for i in range(0, len(testingSet)):
			doc = testingSet[i]
			for j in range(0, len(doc.content)):
				word = doc.content[j]
				probZX1 = [None for y in range(0, numTopic)]
				probZX2 = [None for y in range(0, numTopic)]
				for k in range(0, numTopic):
					nkd = testingDicD[(doc, topic[k])]
					ntd = doc.length-1
					if topic[k]==doc.z[j]:
						nkd -= 1
					probZX1[k] = (1-lam)*((nkd+alpha)/(ntd+alpha*numTopic))*trainingPhi[(word, topic[k])]
					if doc.label==0:
						probZX2[k] = lam*((nkd+alpha)/(ntd+alpha*numTopic))*trainingPhi0[(word, topic[k])]
					else:
						probZX2[k] = lam*((nkd+alpha)/(ntd+alpha*numTopic))*trainingPhi1[(word, topic[k])]
				[zNew, xNew] = sampleZX(probZX1, probZX2)
				#update counts
				testingDicDCopy[(doc, doc.z[j])] -= 1
				testingDicDCopy[(doc, zNew)] += 1
				#update z and x
				testingSetCopy[i].z[j] = zNew
				testingSetCopy[i].x[j] = xNew
		print("Finish Sampling Testing Set And Updating Testing Counts")
		#estimate theta for training and compute the likelihood
		trainLL = 0
		for i in range(0, len(trainingSet)):
			doc = trainingSet[i]
			for j in range(0, len(trainingSet[i].content)):
				word = doc.content[j]
				temp = 0
				for k in range(0, numTopic):
					if j==0: #update once
						nkd = trainingDicDCopy[(doc, topic[k])]
						ntd = trainingSet[i].length
						trainingTheta[(doc, topic[k])] = (nkd+alpha)/(ntd+alpha*numTopic)
					if trainingSet[i].label==0:
						temp += trainingTheta[(doc, topic[k])]*((1-lam)*trainingPhi[(word, topic[k])]+lam*trainingPhi0[(word, topic[k])])
					else:
						temp += trainingTheta[(doc, topic[k])]*((1-lam)*trainingPhi[(word, topic[k])]+lam*trainingPhi1[(word, topic[k])])
				trainLL += math.log(temp)
		trainingLikelihood.append(copy.deepcopy(trainLL))
		print("Finish Evaluating Theta And Computing Log-Likelihood For Training Set")
		#estimate theta for testing and compute the likelihood
		testLL = 0
		for i in range(0, len(testingSet)):
			doc = testingSet[i]
			for j in range(0, len(testingSet[i].content)):
				word = doc.content[j]
				temp = 0
				for k in range(0, numTopic):
					if j==0: #update once
						nkd = testingDicDCopy[(doc, topic[k])]
						ntd = testingSet[i].length
						testingTheta[(doc, topic[k])] = (nkd+alpha)/(ntd+alpha*numTopic)
					if testingSet[i].label==0:
						temp += testingTheta[(doc, topic[k])]*((1-lam)*trainingPhi[(word, topic[k])]+lam*trainingPhi0[(word, topic[k])])
					else:
						temp += testingTheta[(doc, topic[k])]*((1-lam)*trainingPhi[(word, topic[k])]+lam*trainingPhi1[(word, topic[k])])
				testLL += math.log(temp)
		testingLikelihood.append(copy.deepcopy(testLL))
		print("Finish Evaluating Theta And Computing Log-Likelihood For Testing Set")
		if t+1>burn:
			thetaSet.append(trainingTheta.copy())
			phiSet.append(trainingPhi.copy())
			phi0Set.append(trainingPhi0.copy())
			phi1Set.append(trainingPhi1.copy())
		#update sets
		trainingSet = copy.deepcopy(trainingSetCopy)
		trainingDicD = trainingDicDCopy.copy()
		trainingDicW = trainingDicWCopy.copy()
		testingSet = copy.deepcopy(testingSetCopy)
		testingDicD = testingDicDCopy.copy()
		print("Finish Updating Sets")
		iterTime = time.time()-start
		iterationTime.append(iterTime)
	#Compute Final Parameters
	finalTheta = expectedValue(thetaSet)
	finalPhi = expectedValue(phiSet)
	finalPhi0 = expectedValue(phi0Set)
	finalPhi1 = expectedValue(phi1Set)
	print("Finish Computing Expected Value Of Parameters")
	for i in range(0, len(testingSet)):
		doc = testingSet[i]
		for j in range(0, len(doc.content)):
			word = doc.content[j]
			probZX1 = [None for y in range(0, numTopic)]
			probZX2 = [None for y in range(0, numTopic)]
			for k in range(0, numTopic):
				nkd = testingDicD[(doc, topic[k])]
				ntd = doc.length-1
				if topic[k]==doc.z[j]:
					nkd -= 1
				probZX1[k] = (1-lam)*((nkd+alpha)/(ntd+alpha*numTopic))*finalPhi[(word, topic[k])]
				if doc.label==0:
					probZX2[k] = lam*((nkd+alpha)/(ntd+alpha*numTopic))*finalPhi0[(word, topic[k])]
				else:
					probZX2[k] = lam*((nkd+alpha)/(ntd+alpha*numTopic))*finalPhi1[(word, topic[k])]
			[zNew, xNew] = sampleZX(probZX1, probZX2)
			#update counts
			testingDicDCopy[(doc, doc.z[j])] -= 1
			testingDicDCopy[(doc, zNew)] += 1
			#update z and x
			testingSetCopy[i].z[j] = zNew
			testingSetCopy[i].x[j] = xNew
	print("Finish Final Sampling For Testing Set ")
	#estimate theta for testing and compute likelihood
	finalTestLL = 0
	for i in range(0, len(testingSet)):
		doc = testingSet[i]
		for j in range(0, len(testingSet[i].content)):
			word = doc.content[j]
			temp = 0
			for k in range(0, numTopic):
				if j==0: #update once
					nkd = testingDicDCopy[(testingSet[i], topic[k])]
					ntd = testingSet[i].length
					testingTheta[(doc, topic[k])] = (nkd+alpha)/(ntd+alpha*numTopic)
				if testingSet[i].label==0:
					temp += testingTheta[(doc, topic[k])]*((1-lam)*trainingPhi[(word, topic[k])]+lam*trainingPhi0[(word, topic[k])])
				else:
					temp += testingTheta[(doc, topic[k])]*((1-lam)*trainingPhi[(word, topic[k])]+lam*trainingPhi1[(word, topic[k])])
			finalTestLL += math.log(temp)
	print("Finish Final Evaluation")
	#Output
	outputTheta(finalTheta, trainingSet, output+"-theta")
	outputPhi(finalPhi, allVoc, output+"-phi")
	outputPhi(finalPhi0, allVoc, output+"-phi0")
	outputPhi(finalPhi1, allVoc, output+"-phi1")
	outputLikelihood(trainingLikelihood, output+"-trainll")
	outputLikelihood(testingLikelihood, output+"-testll")
	outputTime(iterationTime, output+"-time")
	outputFinal(finalTestLL, output+"-final")
	print("Finish Printing")
