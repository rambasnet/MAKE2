#-----------------------------------------------------------------------------
# Name:        SGMLParser.py
# Purpose:     
#
# Author:      Ram Basnet
#
# Created:     2008/08/07
# RCS-ID:      $Id: SGMLParser.py $
# Copyright:   (c) 2008
# Licence:     All Rights Reserved
#-----------------------------------------------------------------------------


import string, re, time
from sgmllib import SGMLParser
import formatter
import Constants
import Globals
from SqliteDatabase import *

class ParseError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


class SGMLXMLParser(SGMLParser):
    def __init__(self, db, docID, filePath, startTime, logFile, Stopwords=[], Stemmer=None):
        f = formatter.NullFormatter()#formatter.AbstractFormatter(formatter.DumbWriter())
        #htmllib.HTMLParser.__init__(self, f)
        SGMLParser.__init__(self, f)
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
        self.DocID = docID
        self.filePath = filePath.lower()
        self.startTime = startTime
        self.logFile = logFile
        #self.rawdata = ""
        #self.nomoretags = False
        self.WordDict = {}
        self.location = 0
        
    def handle_data(self, data):
        data = data.strip()
        if data:
            self.parse(data)
            #print data

    def parse(self, data):
        #self.filePath = filePath.lower()
        #self.DocID = docID
        
        phoneList = self.PhoneRE.findall(data)
        
        for numTuple in phoneList:
            if time.time() - self.startTime > 1800:
                self.logFile.write('Taking more 60 mins to parse the file...skipping and continuring to next...\n')
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
                    if self.WordDict.has_key(phone):
                        self.WordDict[phone].append(self.location)
                    else:
                        self.WordDict[phone] = [self.location]
                    
                self.location += 1
            except:
                continue
                    
        myList = data.lower().split()
        #if data <> '\n' and data <> '\r\n' and (not re.search(r'(&nbsp;)+', data)):
        #i = 0
        for word in myList:
            if time.time() - self.startTime > 1800:
                self.logFile.write('Taking more 60 mins to parse the file...skipping and continuring to next...\n')
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
        
                            if self.WordDict.has_key(word):
                                self.WordDict[word].append(self.location)
                            else:
                                self.WordDict[word] = [self.location]
                            
                        self.location += 1
                else:
                    words = self.Splitter.split(word)
                    for word in words:
                        if len(word) > 2:
                            if self.WordDict.has_key(word):
                                self.WordDict[word].append(self.location)
                            else:
                                self.WordDict[word] = [self.location]
                            
                        self.location += 1
        
            except:
                continue
            
        #self.WordDict = None
        
        #print 'WordDict size = ', len(WordDict)
            
    def handleWords(self):
        for word in self.WordDict:
            if time.time() - self.startTime > 1800:
                self.logFile.write('Taking more 60 mins to parse the file...skipping and continuring to next...\n')
                return
            
            try:
                row = self.db.FetchOneRow("SELECT ROWID FROM %s WHERE Word=%s"%(Constants.WordsTable, self.db.SqlSQuote(word)))
                wordID = 1
                if row:
                    wordID = row[0]
                    self.db.ExecuteNonQuery("UPDATE %s set Frequency = Frequency + %d where ROWID = %d"%(Constants.WordsTable, len(self.WordDict[word]), wordID))
                else:
                    stemmedWord = ""
                    if self.Stemmer:
                        stemmedWord = self.Stemmer.stem(word, 0, len(word)-1)
                        
                    query = "insert into %s (Word, StemmedWord, Frequency) values (?, ?, ?)"%(Constants.WordsTable)
                    wordID = self.db.InsertAutoRow(query, [(word, stemmedWord, len(self.WordDict[word]))])
                
                InPath = 0
                if self.filePath.find(word) >=0:
                    InPath = 1
                  
                for location in self.WordDict[word]:  
                    self.db.ExecuteNonQuery("insert into %s (DocID, WordID, Location, InPath) values (%d, %d, %d, %d)"%(Constants.WordLocation, self.DocID, wordID, location, InPath))
            except:
                pass
            
        

if __name__ == "__main__":
    import sys
    sgmlParser = SGMLXMLParser(None, 1, "filePath", time.time(), "logFile", Stopwords=[], Stemmer=None)
    fin = open(r'C:\Test\note.xml')
    sgmlParser.feed(fin.read())
    fin.close()
    

    #textParser.parse(2, HTMLParser.getText(fileName), fileName)

