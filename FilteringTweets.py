#=====================================================================================
# By: Jakob Wanger
# Description: This program will calculate the Sentimental Values of Tweets and give them
#              a happiness rating beased on what time zone (Pacific, Mountain, Central and Eastern
#              time zones.
#=====================================================================================


from sys import exit
import happy_histogram

tweetsFromEach=[0,0,0,0] #Storing total tweets for each Time Zone in Order of Pacific, Mountain, Central, Eastern
tweetWSenti= [0,0,0,0] #Storing total tweets with at Least on Sentinental Word for each Time Zone in Order of Pacific, Mountain, Central, Eastern

#--------------------Getting user input for opening a file containing the keywords----------------------------------------------------------
def gettingKeywords ():
    sentenialList=[]
    try:
        keyFileName= input("Please enter the file name where the keywords are stored: ")
        keyFile=open(keyFileName, 'r') #Trying to open file
        if keyFileName.lower()=="tweets.txt": #Making sure that if tweets file is entered in wrong position the prorgam does niot continue
            keyFile.close() #Closing file to make sure no corruption can take place
            print("File not found.")
            exit()
    except IOError: #If the file does not exist
        print("File not found.")
        exit()

    line=keyFile.readline() #Reading the first line of the file
    while line != '':
        #Adding First Element to the List
        elements=line.split(',')
        elements[1].rstrip()
        elements[1] = int (elements[1])
        #Adding Element the Word and Value in to a table
        sentenialList.append(elements)
        #Reading in the next line
        line=keyFile.readline()
    keyFile.close()
    return sentenialList #Returning the list to the main
#-----------------------------------------------------------------------------------------------------------------------

#This method will read the tweet and process it-------------------------------------------------------------------------
def getAndProcessTweetFile (keyWords):
    maxLatitude= 49.189787 #Storing the largest magnitude of the Latitude that is within the valid area
    minLatitude= 24.660845 #Storing the smallest magnitude of the Latitude that is within the valid area

    maxLongtitude= -67.444574 #Storing the largest magnitude of the Longitude that is within the valid area
    minLongtitude= -125.242264 #Storing the smallest magnitude of the Longitude that is within the valid area
    PtoMLongitude= -115.236428 #Storing the Longitude border from the Pacific Time to Mountain time region
    MtoCLongitude= -101.998892 #Storing the Longitude border from Mountain Time to Central time region
    CtoELongitude= -87.518395 #Storing the Longitude border from the Central Time to Eastern time region

    score=[0,0,0,0] #Storing score for the different time zones: Reading from left to Right: Pacific, Mountain, Central, Eastern

    try:
        tweetFileName= input("Please enter the file name where the Tweets are stored: ")
        tweetFile=open(tweetFileName, 'r') #Trying to open file
        if tweetFileName.lower()=="keywords.txt": #Making sure that if tweets file is entered in wrong position the prorgam does not continue
            tweetFile.close() #Closing file to make sure no corruption can take place
            exit()
    except IOError: #If the file does not exist
            print("File not found please try again.")
            exit()

    line=tweetFile.readline()
    while(line!= ''):
        elements=line.split(" ") #Splitting the line into individual elements on the space
        location=-1; #Stores location of where the tweet is for, for total count
        sentimentFound=-1; #Sentenial Value used to check if sentimental word is in tweet
        localScore=0; #Stores the local score the line before the finale processing is complete
        sentimentWordCount=0 #The number of sentimental words in the tweet
        #Processing Longitude and Latitude into Float variables
        latitude=elements[0].lstrip('[')
        latitude=float(latitude.rstrip(','))
        longitude=float(elements[1].rstrip(']'))

        for index in range (5,len(elements)): #Loop starting from 5th position (start of tweet) to the end of it
            strWord= str (elements[index]) #Turn the list element into a pure string =
            strWord= stripSpecial(strWord) #Call on the stripSpecial method to strip any special characters from the word
            if (latitude<=maxLatitude and latitude>=minLatitude): #If the longtitude is within the covered range
                if (longitude>=minLongtitude and longitude <= PtoMLongitude): #If the latitude is within the needed range for pacific time zone
                    location=0 #Setting Location to the Sentimental Value for Pacific Time Zone
                    if scoreCalc(strWord, keyWords)!=-1:
                        sentimentFound=0 #Setting the variable to the Sentimental Value for Pacific Time Zone
                        localScore = localScore+ scoreCalc(strWord, keyWords)
                        sentimentWordCount=sentimentWordCount+1
                elif (longitude >= PtoMLongitude and longitude <= MtoCLongitude): #If the latitude is within the needed range for Mountain time zone
                    location=1 #Setting Location to the Sentimental Value for Mountain Time Zone
                    if scoreCalc(strWord, keyWords)!=-1:
                        sentimentFound=1 #Setting the variable to the Sentimental Value for Mountian Time Zone
                        localScore = localScore+ scoreCalc(strWord, keyWords)
                        sentimentWordCount=sentimentWordCount+1
                elif (longitude >= MtoCLongitude and longitude <= CtoELongitude): #If the latitude is within the needed range for Central time zone
                    location=2 #Setting Location to the Sentimental Value for Central Time Zone
                    if scoreCalc(strWord, keyWords)!=-1:
                        sentimentFound=2 #Setting the variable to the Sentimental Value for Central Time Zone
                        localScore = localScore+ scoreCalc(strWord, keyWords)
                        sentimentWordCount=sentimentWordCount+1
                elif (longitude >= CtoELongitude and longitude <= maxLongtitude): #If the latitude is within the needed range for Eastern time zone
                    location=3 #Setting Location to the Sentimental Value for Eastern Time Zone
                    if scoreCalc(strWord, keyWords)!=-1:
                        sentimentFound=3 #Setting the variable to the Sentimental Value for Eastern Time Zone
                        localScore = localScore+ scoreCalc(strWord, keyWords)
                        sentimentWordCount=sentimentWordCount+1
                else:
                    location=-1
        line=tweetFile.readline()
        if sentimentFound!=-1: #So Long the tweet had at least one sentiment word
            tweetWSenti[sentimentFound]=tweetWSenti[sentimentFound]+1  #Set Score for Tweet
            score[location]=score[location]+(localScore/sentimentWordCount) #Add score of tweet to the total count
            tweetsFromEach[location]=tweetsFromEach[location]+1 #Adding the the total tweets to each region count
        #if location!=-1:
            #tweetsFromEach[location]=tweetsFromEach[location]+1
    tweetFile.close()
    return score
#-----------------------------------------------------------------------------------------------------------------------

def scoreCalc (word, keywords): #Used for calculating score of a words passed through the function
    score=-1 #Initzializing Varible
    for i in range(0, len(keywords)): #For loop used to comapare the contents in the file to the word from the argument
        if (word==keywords[i][0]): #If the keyword word matches the word in the tweet compute the score for the given value
            score=0
            score= score+keywords[i][1]
    return score

def stripSpecial (word): #Used to strip the special characters of the individual word passed in the argument
    word=word.replace("~","").replace("`","").replace("!","").replace("@","").replace("#","").replace("$","").replace("%","").replace("^","").replace("&","").replace("*","").replace("(","").replace(")","").replace("_","").replace("-","").replace("=","").replace("+","").replace("{","").replace("[","").replace("}","").replace("]","").replace("|","").replace(":","").replace(";","").replace("'","").replace('"',"").replace("<","").replace(",","").replace(".","").replace(">","").replace("/","").replace("?","")
    word=word.lower()
    return word

def main (): #Main Class
    keywordList=(gettingKeywords()) #Callling on the method to read the keywords file
    tweetScore= (getAndProcessTweetFile(keywordList)) #Calling method to read the tweet file and process it
    tweetPerRegion=[tweetsFromEach[0],tweetsFromEach[1],tweetsFromEach[2],tweetsFromEach[3]] #Used as a replica of tweetsFromEach, however it serves the function of preventing a divde by zero error if 0 tweets are from region

    if (tweetWSenti[0]==0): #If the region had 0 tweets to avoid error. Make the tweet from each 1. As a region
        tweetPerRegion[0]=1 #with 0 tweets by default the region will have a score of 0. Therefore, the tweet score
    if (tweetWSenti[1]==0): # 0 divided by the modified tweet count of the value for the region will result in 0
        tweetPerRegion[1]=1
    if (tweetWSenti[2]==0):
        tweetPerRegion[2]=1
    if (tweetWSenti[3]==0):
        tweetPerRegion[3]=1

    finalScore=[tweetScore[0]/tweetPerRegion[0],tweetScore[1]/tweetPerRegion[1],tweetScore[2]/tweetPerRegion[2],tweetScore[3]/tweetPerRegion[3]]
    print("The hapinness score for the Pacific Time Zone is", finalScore[0],"from", tweetsFromEach[0],"tweets")
    print("The hapinness score for the Mountain Time Zone is", finalScore[1],"from", tweetsFromEach[1],"tweets")
    print("The hapinness score for the Central Time Zone is", finalScore[2],"from", tweetsFromEach[2],"tweets")
    print("The hapinness score for the Eastern Time Zone is", finalScore[3],"from", tweetsFromEach[3],"tweets")

    happy_histogram.drawSimpleHistogram(finalScore[3], finalScore[2], finalScore[1],finalScore[0]) #Drawing the histogram
main() #Calling main
