#-----------------------------------------------------------------------------
# Name:        TextParser.py
# Purpose:     
#
# Author:      Ram Basnet
#
# Created:     2008/06/30
# RCS-ID:      $Id: TextParser.py $
# Copyright:   (c) 2008
# Licence:     All Rights Reserved
#-----------------------------------------------------------------------------


import string, re, time
import Constants
import Globals
import PlatformMethods
from SqliteDatabase import *

class ParseError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


class TextParser():
    def __init__(self, db, Stopwords=[], Stemmer=None, bloomFilter=None):
        #self.FileName = FileName
        self.db = db
        self.Stopwords = Stopwords
        #self.WordCount = 0
        #self.StemmedWordCount = 0
        #self.FooterLineRE = re.compile(r'[_-]{2,}')
        self.AlphaNumeric = re.compile(r'[a-zA-Z]+|[0-9]+', re.I)
        self.ListSepRE = re.compile(r'[~`!#$^&*()+=|\\{}\'"?><\[\],;]')
        self.Splitter = re.compile(r'\W*')
        #self.EmailRE = re.compile(r"\A[A-Z0-9._%-]+@[A-Z0-9._%-]+\.[A-Z]+", re.I)
        #self.HTTPRE = re.compile(r"\A(http://)[a-z0-9_-]+\.[a-z]{2,4}\b", re.I)
        self.Stemmer = Stemmer
        
        self.PhoneRE = re.compile(r'([\d{3}]*)[\(\)-/\. ]*(\d{3})[\(\)-/\. ]*(\d{4})\D*')
        self.EmailRE = re.compile(r"\A[A-Z0-9._%-]+@[A-Z0-9._%-]+\.[A-Z]+", re.I)
        self.HTTPRE = re.compile(r"\A(http://)[a-z0-9_-]+\.[a-z]{2,4}\b", re.I)
        self.bloomFilter = bloomFilter
        

    def parse(self, docID, data, filePath, startTime, logFile):
        self.filePath = filePath.lower()
        self.DocID = docID
        
        phoneList = self.PhoneRE.findall(data)
        location = 0
        WordDict = {}
        
        for numTuple in phoneList:
            if time.time() - startTime > 1800:
                logFile.write('%s :Excedeed 30 mins. Skipping!\n'%PlatformMethods.Encode(self.filePath))
                return
            
            try:
                phone = ""
                for num in numTuple:
                    if num:
                        if phone:
                            phone += "-" + num
                        else:
                            phone += num
                            
                if phone:
                    if WordDict.has_key(phone):
                        WordDict[phone].append(location)
                    else:
                        WordDict[phone] = [location]
                    
                location += 1
            except:
                continue
                    
        myList = data.lower().split()
        #if data <> '\n' and data <> '\r\n' and (not re.search(r'(&nbsp;)+', data)):
        i = 0
        for word in myList:
            if time.time() - startTime > 1800:
                logFile.write('%s :Excedeed 30 mins. Skipping!\n'%PlatformMethods.Encode(self.filePath))
                return
            
            try:
                if not self.AlphaNumeric.match(word):
                    continue

                if word in self.Stopwords:
                    continue
                
                if self.EmailRE.match(word) or self.HTTPRE.match(word):
                    words = self.ListSepRE.split(word)
                    for word in words:
                        if len(word) > 2:
                            """
                            try:
                                self.handleWord(word, i)
                            except:
                                pass
                            """
                            if WordDict.has_key(word):
                                WordDict[word].append(i)
                            else:
                                WordDict[word] = [i]
                            
                        i += 1
                else:
                    words = self.Splitter.split(word)
                    for word in words:
                        if len(word) > 2:
                            if WordDict.has_key(word):
                                WordDict[word].append(i)
                            else:
                                WordDict[word] = [i]
                            
                        i += 1
            
     
            except:
                continue
            
        self.handleWords(WordDict, logFile, startTime)
        WordDict = None
        
        #print 'WordDict size = ', len(WordDict)
            
    def handleWords(self, WordDict, logFile, startTime):
        wordID = 1
        for word in WordDict:
            if time.time() - startTime > 1800:
                logFile.write('%s :Excedeed 30 mins. Skipping!\n'%PlatformMethods.Encode(self.filePath))
                return
            
            try:
                found = False
                """
                if self.bloomFilter:
                    if word in self.bloomFilter: #take care of rare false positive given by bloom-filter
                        row = self.db.FetchOneRow("SELECT ROWID FROM %s WHERE Word=?"%(Constants.WordsTable), (PlatformMethods.Encode(word),))
                        if row:
                            wordID = row[0]
                            self.db.ExecuteNonQuery("UPDATE %s set Frequency = Frequency + %d where ROWID = %d"%(Constants.WordsTable, len(WordDict[word]), wordID))
                            found = True
                """
                #else:
                row = self.db.FetchOneRow("SELECT ROWID FROM %s WHERE Word=?"%(Constants.WordsTable), (PlatformMethods.Encode(word),))
                if row:
                    wordID = row[0]
                    self.db.ExecuteNonQuery("UPDATE %s set Frequency = Frequency + %d where ROWID = %d"%(Constants.WordsTable, len(WordDict[word]), wordID))
                    #found = True
                    
                else:
                    """
                    if not found: 
                        if bloomFilter: 
                            self.bloomFilter.add(word)
                    """
                    stemmedWord = ""
                    if self.Stemmer:
                        stemmedWord = self.Stemmer.stem(word, 0, len(word)-1)
                        
                    query = "insert into %s (Word, StemmedWord, Frequency) values (?, ?, ?)"%(Constants.WordsTable)
                    wordID = self.db.InsertAutoRow(query, [(PlatformMethods.Encode(word), PlatformMethods.Encode(stemmedWord), len(WordDict[word]))])
                
                InPath = 0
                if self.filePath.find(word) >=0:
                    InPath = 1
                  
                for location in WordDict[word]:  
                    self.db.ExecuteNonQuery("insert into %s (DocID, WordID, Location, InPath) values (%d, %d, %d, %d)"%(Constants.WordLocation, self.DocID, wordID, location, InPath))
                    
            except:
                continue
            
        
    def handleWord(self, word, location):
        row = self.db.FetchOneRow("SELECT ROWID FROM %s WHERE Word=%s"%(Constants.WordsTable, self.db.SqlSQuote(word)))
        wordID = 1
        if row:
            wordID = row[0]
            self.db.ExecuteNonQuery("UPDATE %s set Frequency = Frequency + 1 where ROWID = %d"%(Constants.WordsTable, wordID))
        else:
            stemmedWord = ""
            if self.Stemmer:
                stemmedWord = self.Stemmer.stem(word, 0, len(word)-1)
                
            query = "insert into %s (Word, StemmedWord, Frequency) values (?, ?, ?)"%(Constants.WordsTable)
            wordID = self.db.InsertAutoRow(query, [(word, stemmedWord, 1)])
            
        InPath = 0
        if self.filePath.find(word) >=0:
            InPath = 1
            
        self.db.ExecuteNonQuery("insert into %s (DocID, WordID, Location, InPath) values (%d, %d, %d, %d)"%(Constants.WordLocation, self.DocID, wordID, location, InPath))
        


if __name__ == "__main__":
    """
    import sys
    import HTMLParser
    db = SqliteDatabase('test.db')
    if not db.OpenConnection():
        sys.exit(0)

    textParser = TextParser(db)
    fileName = r'C:\Documents and Settings\Ram\Desktop\Analysis\SummitVsIBMData\eFiles\session001\pricing_proposals\sap\ecommerce\su0133354^isa_erp.ppt'
    print HTMLParser.getText(fileName)

    #textParser.parse(2, HTMLParser.getText(fileName), fileName)
    """
    import os.path
    import time
    import re
    import MSOfficeToText
    import CommonFunctions
    stTime = time.time()
    splitter = re.compile(r'\W*')
    docFileName = r'C:\Test\Assignment.rtf'
    data = MSOfficeToText.WordToText(docFileName)
    
    for word in splitter.split(data):
        try:
            print word
        except:
            print 'error'
            
    endTime = time.time()
    print endTime - stTime
    CommonFunctions.ConvertSecondsToDayHourMinSec(endTime-stTime)
