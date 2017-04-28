import sys
import HAC
import MOS
import AdjScore
import operator
import collections
from textblob import TextBlob

#Get the filename as command line argument
filename = sys.argv[1]

#reviewTitle is the list containing title of all reviews
reviewTitle = []

#reviewContent is the list containing all reviews
reviewContent = []

#Extract review title and content from the file
with open(filename) as f:
	review = []
	for line in f:
		if line[:3] == "[t]":							#Incase the line starts with [t], then its the title of review
			if review:
				reviewContent.append(review)
				review = []
			reviewTitle.append(line.split("[t]")[1].rstrip("\r\n"))
		else:	
			if "##" in line:								#Each line in review starts with '##'
				x = line.split("##")
				for i in range(1, len(x)):			#x[0] is the feature given the file.Its been ignored here as its not a part of the review
					review.append(x[i].rstrip("\r\n"))
			else:
				continue
	reviewContent.append(review)

#The HAC algorithm to extract features and adjectives in the review
featureList, adjDict = HAC.findFeatures(reviewContent)

#Get adjective scores for each adjective
adjScores = AdjScore.getScore(adjDict)

#MOS algorithm to get feature score and review score
posRevIndex, negRevIndex, avgFeatScore = MOS.rankFeatures(adjScores, featureList, reviewTitle, reviewContent)