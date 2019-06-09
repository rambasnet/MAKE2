
from Globals import *
from SqliteDatabase import *
import math

#Constants...
CatSetExchanges = "Exchanges"
CatSetOrgs = "Orgs"
CatSetPeople = "People"
CatSetPlaces = "Places"
CatSetTopics = "Topics"

SplitTypeLewisSplit = "LewisSplit"
SplitTypeCgiSplit = "CgiSplit"

SVMFileTypeTraining = "Train"
SVMFileTypeTesting = "Test"
#~~~~~~~~~~~~~~

#change the following variables accordingly...


#change to any one of the 5 cat sets
catSet = CatSetTopics
#change to lewis or cgi split
splitType = SplitTypeLewisSplit
#change to training or testing
#svmFileType = SVMFileTypeTraining 

SVMTrainFileName = "Train" + splitType + catSet + ".svm"
SVMTestFileName = "Test" + splitType + catSet + ".svm"

#slitValue can be either TRAIN OR TEST for LewisSplit
trainSplitValue = "TRAIN"
testSplitValue = "TEST"

Categories = []
WordFeaturesID = []

def LoadCategories():
    db = SqliteDatabase(Globals.DBName)
    db.OpenConnection()
    query = "select " + catSet + " from Documents order by " + catSet + ";"
    #query = "select DocID, WordID, Frequency from BagOfWords;"
    rows = db.FetchAllRows(query)
        
    for row in rows:
        cats = row[0].split(";")
        #print cats
        for cat in cats:
            if cat.strip():
                if not CheckCatExists(cat.strip()):
                    Categories.append(cat.strip())
                
    
    db.CloseConnection()
    fout = open(catSet + ".txt", "w")
    i = 1;
    for cat in Categories:
        fout.write(str(i) + " " + cat + "\n")
        i += 1
    fout.close()
    

def CheckCatExists(newCat):
    for cat in Categories:
        if cat == newCat:
            return True
    return False


def LoadWordFeatureID():
    db = SqliteDatabase(Globals.DBName)
    db.OpenConnection()
    query = "select ID from Words order by ID;"
    #query = "select DocID, WordID, Frequency from BagOfWords;"
    rows = db.FetchAllRows(query)
    for row in rows:
        WordFeaturesID.append(int(row[0]))
    #print WordFeatureID
    #for row in rows:
    
    db.CloseConnection()

def GetCategoryID(catName):
    i = 1
    for cat in Categories:
        if cat == catName:
            return i
        i += 1
    # 0 is unknown category
    return 0
    
#create bsvm file format
#output 1:value 2:value ...        
def CreateSVMFile(fileType):
    db = SqliteDatabase(Globals.DBName)
    db.OpenConnection()
    query = ""
    rowsAllDocs = None
    fileWriter = None
    if fileType == SVMFileTypeTraining:
        query = "select ID, " + catSet + " from Documents where " + splitType + " = " + db.SqlSQuote(trainSplitValue) + " order by ID;"
        rowsAllDocs = db.FetchAllRows(query)
    
        fout = open(SVMTrainFileName + ".info", "w")
        fout.write("Total Training samples: " + str(len(rowsAllDocs)) + "\n")
        fout.write("Total Features: " + str(len(WordFeaturesID)) + "\n")
        fout.close()
        fileWriter = open(SVMTrainFileName, "w")
    else:
        query = "select ID, " + catSet + " from Documents where " + splitType + " = " + db.SqlSQuote(testSplitValue) + " order by ID;"
        rowsAllDocs = db.FetchAllRows(query)
    
        fout = open(SVMTestFileName + ".info", "w")
        fout.write("Total Test samples: " + str(len(rowsAllDocs)) + "\n")
        fout.write("Total Features: " + str(len(WordFeaturesID)) + "\n")
        fout.close()
        fileWriter = open(SVMTestFileName, "w")
    
    
    #each sample document
    for row in rowsAllDocs:
        query1 = "select DocID, WordID, TF, IDF from BagOfWords where DocID = '%d' order by WordID;"%(int(row[0]))
        #handle two or more categories if any
        # the same sample will be produced for all the categories the document belongs to
        #print query1
        rowsTFIDF = db.FetchAllRows(query1)
        docCategories = row[1].split(";")
        for category in docCategories:
            if category.strip():
                #write output as first column
                fileWriter.write(str(GetCategoryID(category.strip())))
                #now write the rest of the word features in 1:tf*idf format
                for featureID in WordFeaturesID:
                    #check if each feature word is present in the sample document
                    featurePresent = False
                    for rowTFIDF in rowsTFIDF:
                        if featureID == int(rowTFIDF[1]):
                            fileWriter.write(" " + str(featureID) + ":" + str(float(rowTFIDF[2])*float(rowTFIDF[3])))
                            featurePresent = True
                            break
                    if not featurePresent:
                        fileWriter.write(" " + str(featureID) + ":" + str(0))
                #New feature
                fileWriter.write("\n")             
         
    fileWriter.close()       
    db.CloseConnection()


if __name__ == "__main__":
    LoadCategories()
    print "Finished GettingCategories()"
    LoadWordFeatureID()
    print "Finished LoadWordFeatureID()"
    CreateSVMFile(SVMFileTypeTraining)
    print "Finished CreateSVM Training File"
    CreateSVMFile(SVMFileTypeTesting)
    print "Finished CreateSVM Testing File"
    