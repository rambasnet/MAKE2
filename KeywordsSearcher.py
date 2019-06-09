#-----------------------------------------------------------------------------
# Name:        KeywordsSearcher.py
# Purpose:     
#
# Author:      Ram Basnet
#
# Created:     07/06/2009
# Modified:     07/10/2009
# RCS-ID:      $Id: KeywordsSearcher.py $
# Copyright:   (c) 2008
# Licence:     All Rights Reserved
#-----------------------------------------------------------------------------

import pyPdf
import PlatformMethods
from SqliteDatabase import *

def SearchKeywords(DocID, KeywordsDict, filePath, dbFileName):
    KeywordsFrequency = {}
    
    #query = "INSERT INTO %s (DocID, WordID, Frequency, InPath) values (?, ?, ?,?)"%Constants.WordLocation 
    errorLog = open(dbFileName + ".log", 'ab')
    data = u""
    try:
        #print filePath
        parsed = False
        if KeywordsSearchCategoryList:
            if mimeType not in KeywordsSearchCategoryList:
                """
                #default list of all the mime types doesn't seem to produce the mime type for
                # MS docx document
                if mimeType == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' or extension == '.docx':
                    try:
                        DocID = db.InsertAutoRow(query, [(PlatformMethods.Encode(self.filePath),)])
                        #docID, filePath, startTime, logFile, extractMedia = False, MediaPath=""
                        docxParser.Parse(DocID, self.filePath, self.FileScanStartTime, self.fout, extractMedia = False, MediaPath="")
                        parsed = True
                    except Exception, value:
                        self.fout.write("Error in docxParser : %s Value: %s\n"%(self.filePath, value))
                        #gives junk so let's not parse it using binary
                """
                pass     

            else:
                if mimeType == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' or extension == '.docx':
                    """
                    try:
                        #docID, filePath, startTime, logFile, extractMedia = False, MediaPath=""
                        docxParser.Parse(DocID, self.filePath, self.FileScanStartTime, self.fout, extractMedia = False, MediaPath="")
                        parsed = True
                    except Exception, value:
                        #gives junk so let's not parse it using binary
                        parsed = True
                        self.fout.write("Error in docxParser : %s Value: %s\n"%(PlatformMethods.Encode(self.filePath), value))                                    
                    """
                    pass
                elif mimeType == 'application/msword':
                    try:
                        #docID, filePath, startTime, logFile, extractMedia = False, MediaPath=""
                        #docParser.Parse(DocID, self.filePath, self.FileScanStartTime, self.fout, extractMedia = False, MediaPath="")
                        fileHandler = open(filePath, 'rb')
                        fileHandler.seek(2561, 0)
                        buff = fileHandler.read()
                        fileHandler.close()
                        temp = ''
                        for index in range(0,len(buff)):
                            if buff[index] == '\x00':
                                break

                            if self.charNumRegExp.match(buff[index]):
                                #Token Words are extracted here...These words are further stemmed
                                if len(temp) > 0:
                                    #function = 1
                                    data += " " + temp
                                temp = ''
                            else:
                                temp += buff[index]
                            
                            parsed = True
                    except Exception, value:
                        #gives junk so let's not parse it using binary
                        self.fout.write("Error in DocParser : %s Value: %s\n"%(PlatformMethods.Encode(self.filePath), value))  
                    
                elif mimeType == 'application/pdf':
                    try:
                        #textParser.parse(DocID, PDFToText.GetText(self.filePath), self.filePath, self.FileScanStartTime, self.fout)
                        content = u""
                        # Load PDF into pyPDF
                        pdf = pyPdf.PdfFileReader(file(path, "rb"))
                        # Iterate pages
                        for i in range(0, pdf.getNumPages()):
                            # Extract text from page and add to content
                            content += pdf.getPage(i).extractText() + "\n"
                        # Collapse whitespace
                        data = PlatformMethods.Decode(" ".join(content.replace(u"\xa0", " ").strip().split()))
                        #return PlatformMethods.Decode(content)
                        parsed = True
                    except Exception, value:
                        self.fout.write("Error in PDFToText: %s Value: %s\n"%(PlatformMethods.Encode(self.filePath), value))

                else:
                    try:
                        #read everything else as binary file
                        fin = open(self.filePath, 'rb')
                        data = fin.read()
                        fin.close()
                        parsed = True
                    except Exception, value:
                        self.fout.write("Error in binary text : %s Value: %s\n"%(PlatformMethods.Encode(self.filePath), value))
                        parsed = True
              
        
        else:
            parsed = True
            
        if not parsed:
            try:
                fin = open(self.filePath, 'rb')
                data = fin.read()
                fin.close()
            except Exception, value:
                errorLog.write("Error in binary text : %s Value: %s\n"%(PlatformMethods.Encode(self.filePath), value))

        
    except Exception, value:
        try:
            #print "Error in Text Preprocessing: ", self.filePath, value
            errorLog.write("Error in Text Preprocessing: %s Value: %s\n"%(PlatformMethods.Encode(self.filePath), value))
        except:
            #print "Error in Text Preprocessing..."
            errorLog.write('Unknown Error in Text Preprocessing...\n')
            #continue
     
    errorLog.close()
    db = SqliteDatabase(dbFileName)
    if not db.OpenConnection():
        return
        
    for wordID in KeywordsDict:
        InPath = 0
        #KeywordsFrequency[wordID] = {'Frequency':0, 'InPath':0}
        if KeywordsDict[wordID]['re'].match(filePath):
            KeywordsFrequency[wordID]['InPath'] = 1
        frequency = len(KeywordsDict[wordID]['re'].findall(data))
        #KeywordsFrequency[wordID]['Frequency'] = len(KeywordsDict[wordID]['re'].findall(data))
        """CREATE TABLE IF NOT EXISTS %s (
            DocID INT UNSIGNED NOT NULL,
            KeywordID INT UNSIGNED NOT NULL,
            Frequency INT UNSIGNED NOT NULL,
            InPath INTEGER)
            """%(Constants.KeywordFrequencyTable)
        
        query = "insert into %s (DocID, KeywordID, Frequency, InPath) values (?,?,?,?)"
        db.ExecuteNonQuery(query, (DocID, wordID, frequency, InPath))
    
    db.CloseConnection()
    return dbFileName
        
       