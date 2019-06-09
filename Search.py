#-----------------------------------------------------------------------------
# Name:        Searcher.py
# Purpose:     
#
# Author:      Ram B. Basnet
#
# Created:     2008/07/01
# RCS-ID:      $Id: Searcher.py $
# Copyright:   (c) 2008
# Licence:     All Rights Reserved.
# New field:   Whatever
#-----------------------------------------------------------------------------

import Constants
from SqliteDatabase import *

class Search:
    def __init__(self, dbName, Stopwords=[], searchEmails=False):
        self.dbName = dbName
        self.Stopwords = Stopwords
        self.searchEmails = searchEmails
        self.db = SqliteDatabase(dbName)
        if not self.db.OpenConnection():
            return
        
    
    def __del__(self):
        self.db.CloseConnection()

    def GetRankedDocuments(self, words):
        DocPaths = []
        rows, wordids = self.GetMatchingDocuments(words)
        if not rows or not wordids:
            return [], 0
        
        scores = self.GetScoredList(rows, wordids)
        rankedScores = [(score, DocPath) for (DocPath, score) in scores.items()]
        rankedScores.sort()
        rankedScores.reverse()
        
        """
        if totalDocs <=0:
            totalDocs = len(rankedScores)
        """
         
        for (score, DocID) in rankedScores:#[0:totalDocs]:
            #print '%f\t%s' % (score, self.GetDocPath(DocID))
            if self.searchEmails:
                DocPaths.append(self.GetEmailInfo(DocID))
                attachPath = self.GetAttachmentDocPath(DocID)
                if attachPath:
                    DocPaths.append([attachPath[0], '','','','','','',0])
            else:
                DocPaths.append(self.GetDocPath(DocID))
                
            
        #return wordids,[r[1] for r in rankedScores[0:10]]
        return DocPaths, len(rankedScores)
    
    def GetMatchingDocuments(self, words): #, offset, totalDocs):
        # Strings to build the query
        fieldList='w0.DocID'
        tableList=''  
        clauseList=''
        wordIDs=[]

        # Split the words by spaces
        wordList = words.split()  
        tableNumber = 0

        for word in wordList:
            if word in self.Stopwords:
                continue
            
            # Get the word ID
            wordRow = self.db.FetchOneRow("select rowid from %s where Word like '%s'" %(Constants.TextCatWordsTable, word+"%"))
            if wordRow:
                wordID = wordRow[0]
                wordIDs.append(wordID)
                if tableNumber > 0:
                    tableList += ','
                    clauseList += ' and '
                    clauseList += 'w%d.DocID=w%d.DocID and ' % (tableNumber-1, tableNumber)
              
                fieldList += ', w%d.Location'%(tableNumber)
                tableList += 'wordLocation w%d'%(tableNumber)
                clauseList += 'w%d.WordID = %d'%(tableNumber, wordID)
                tableNumber += 1

        # Create the query from the separate parts
        fullquery = 'select %s from %s where %s '%(fieldList, tableList, clauseList) #, totalDocs, offset)
        #print fullquery
        rows = []
        try:
            rows = self.db.FetchAllRows(fullquery)
        except:
            pass
        
        return rows, wordIDs

    def GetScoredList(self, rows, wordids):
        totalscores=dict([(row[0],0) for row in rows])

        # Put all scoring functions
        weights=[(1.0,self.LocationScore(rows)), 
                 (1.0,self.FrequencyScore(rows)),
                 (1.0,self.DistanceScore(rows))]

        for (weight, scores) in weights:
            for DocPath in totalscores:
                totalscores[DocPath] += weight*scores[DocPath]

        return totalscores

    def GetDocPath(self, id):
        return self.db.FetchOneRow("select DocPath from %s where rowid=%d"%(Constants.TextCatDocumentsTable, id))[0]


    def GetAttachmentDocPath(self, id):
        return self.db.FetchOneRow('select DocPath from %s where rowid=%d and DocType=1'%(Constants.TextCatDocumentsTable, id))
        
    def GetEmailInfo(self, id):
        #emailInfo = [self.GetDocPath()]
        return self.db.FetchOneRow("select FromID, ToID, EmailDate, Subject, Attachments, FilePath, TotalRecipients, Size from %s where DocID=?"%(Constants.EmailsTable), (id,))

    def NormalizeScores(self, scores, smallIsBetter=0):
        vsmall=0.00001 # Avoid division by zero errors
        if smallIsBetter:
            minscore=min(scores.values())
            return dict([(u,float(minscore)/max(vsmall,l)) for (u,l) in scores.items()])
        else:
            maxscore=max(scores.values())
            if maxscore==0: 
                maxscore=vsmall
            return dict([(u,float(c)/maxscore) for (u,c) in scores.items()])

    def FrequencyScore(self,rows):
        counts=dict([(row[0],0) for row in rows])
        for row in rows: 
            counts[row[0]]+=1
        return self.NormalizeScores(counts)

    def LocationScore(self, rows):
        locations=dict([(row[0],1000000) for row in rows])
        for row in rows:
            loc=sum(row[1:])
            if loc<locations[row[0]]: 
                locations[row[0]]=loc

        return self.NormalizeScores(locations, smallIsBetter=1)

    def DistanceScore(self,rows):
        # If there's only one word, everyone wins!
        if len(rows[0])<=2: 
            return dict([(row[0],1.0) for row in rows])

        # Initialize the dictionary with large values
        mindistance=dict([(row[0],1000000) for row in rows])

        for row in rows:
            dist=sum([abs(row[i]-row[i-1]) for i in range(2,len(row))])
            if dist<mindistance[row[0]]: 
                mindistance[row[0]]=dist
        return self.NormalizeScores(mindistance, smallIsBetter=1)


if __name__ == "__main__":
    search = Searcher(r'C:\Documents and Settings\Ram\Desktop\test2.tce')
    print search.GetRankedDocuments('appendix bla sfd')

