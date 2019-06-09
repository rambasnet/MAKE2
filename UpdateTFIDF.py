
from Globals import *
from SqliteDatabase import *
import math


def MoveBagOfWordsToBagOfWordsNewDone():
    db = SqliteDatabase(Globals.DBName)
    db.OpenConnection()
    query = "DROP TABLE IF EXISTS `BagOfWordsNew`;"
    db.ExecuteNonQuery(query)
    
    query = """CREATE TABLE `BagOfWordsNew`(
            `DocID` numeric,
            `WordID` numeric,
            `Frequency` numeric,
            `TF` numeric,
            `IDF` numeric,
            `Temp1` numeric,
            `Temp2` numeric
            ); """
    db.ExecuteNonQuery(query)
    
    query = "select DocID, WordID, Frequency from BagOfWords;"
    #query = "select DocID, WordID, Frequency from BagOfWords;"
    rows = db.FetchAllRows(query)
    query1 = "insert into BagOfWordsNew (DocID, WordID, Frequency) values ("
    for row in rows:
   
        #print "DocID %s, Frequency = %s"%(row[0], row[1])
        query2 = "'" + row[0] + "', '" + row[1] + "', '" + row[2] +"');"  
        db.ExecuteNonQuery(query1+query2)
        
    db.CloseConnection()

def UpdateWordCount():
    db = SqliteDatabase(Globals.DBName)
    db.OpenConnection()
    query = "select DocID, Sum(Frequency) from BagOfWords group by DocID order by DocID;"
    #query = "select DocID, WordID, Frequency from BagOfWords;"
    rows = db.FetchAllRows(query)
    i = 0;
    query1 = "update Documents set WordCount = '"

    for row in rows:
        query2 = str(row[1]) + "' where ID = '" + str(row[0]) + "';"
        db.ExecuteNonQuery(query1 + query2)
        
    
    db.CloseConnection()
        
def UpdateTF():
    db = SqliteDatabase(Globals.DBName)
    db.OpenConnection()
    query = "select ID, WordCount from Documents order by ID;"
    
    rowsTotCount = db.FetchAllRows(query)
    #N = len(rowsTotCount)
    #print "N = %d"%N
    #i = 0
    
    for row in rowsTotCount:
        #db.ExecuteNonQuery(query1 + query2)
        #print row[0]
        query1 = "select DocID, WordID, Frequency from BagOfWords where DocID = '%d';"%(int(row[0]))
        #print query1
        rowsTF = db.FetchAllRows(query1)
        for rowTF in rowsTF:
            #print "%d, %d, %d"%(rowIDF[0], rowIDF[1], rowIDF[2])
            #if int(row[0]) == int(rowTF[0]):
            query2 = " update BagOfWords set TF = '%f' where DocID = '%d' and WordID = '%d';"%(float(rowTF[2])/float(row[1]), rowTF[0], rowTF[1]) 
            #print "word = %d, tf = %f"%(rowTF[1], float(rowTF[2])/float(row[1]))
            #print query2+query3
            db.ExecuteNonQuery(query2)
            #i += 1
            #break
        #break
        #if i/50000 == 1:
        
    db.CloseConnection()
    

def UpdateIDF():
    db = SqliteDatabase(Globals.DBName)
    db.OpenConnection()
        
    queryIDF = "select WordID, Count(WordID) from BagOfWords group by WordID order by WordID;"
    rowsIDF = db.FetchAllRows(queryIDF)
    #N = 21578.0
    
    for row in rowsIDF:
        #idf = math.log(float(21578)/float(row[1]), 2)
        #print "row[1] = %d" %(row[1])
        query = "update BagOfWords set IDF = '%f' where WordID = '%d'"%(math.log(21578.0/float(row[1]), 10), row[0])
        #print query
        db.ExecuteNonQuery(query)      
        #break
    
    db.CloseConnection()


if __name__ == "__main__":
    UpdateWordCount()
    print "Finished UpdateWordCount()"
    #MoveBagOfWordsToBagOfWordsNew()
    UpdateTF()
    print "Finished Update TF"
    UpdateIDF()
    print "Finished Update IDF"