from time import time
import os
import re
import operator

import TextParser


class DocParser():
    def __init__(self, db, Stopwords=[], Stemmer=None, bloomFilter=None):
        self.textParser = TextParser.TextParser(db, Stopwords, Stemmer, bloomFilter=bloomFilter)
        self.charNumRegExp = re.compile('\W', re.IGNORECASE)
    
    def Parse(self, docID, filePath, startTime, logFile, extractMedia = False, MediaPath=""):
        self.textData = ''
        
        fileHandler = open(filePath, 'rb')
        fileHandler.seek(2561, 0)
        buff = fileHandler.read()
        fileHandler.close()
        temp = ''
        textData = ""
        for index in range(0,len(buff)):
            if buff[index] == '\x00':
                break

            if self.charNumRegExp.match(buff[index]):
                #Token Words are extracted here...These words are further stemmed
                if len(temp) > 0:
                    function = 1
                    textData += " " + temp
                temp = ''
            else:
                temp = temp + buff[index]
                
        self.textParser.parse(docID, textData, filePath, startTime, logFile)

if __name__ == "__main__":
    start_time = time()    
    docFile = 'test.doc'
    docParser(docFile)
    print "Time Elapsed: %f" % (time()-start_time)
