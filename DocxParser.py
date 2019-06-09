import os
import shutil
import zipfile, os.path
import string

from xml.dom import minidom, Node
import CommonFunctions

#filePath = 'Cramer.docx'
#infilePath = 'testfile'
#fileData = ''

import TextParser

class DocxParser():
    def __init__(self, db, Stopwords=[], Stemmer=None, bloomFilter=None):
        self.textParser = TextParser.TextParser(db, Stopwords, Stemmer, bloomFilter)

    
    def Parse(self, docID, filePath, startTime, logFile, extractMedia = False, MediaPath=""):
        self.textData = ''
        unzip = zipfile.ZipFile(filePath)
        dataFile = ''

        for name in unzip.namelist():
            if extractMedia:
                if name.find('media') != -1:
                    imgName = name.split('/')
                    imgFile = open(os.path.join(MediaPath, imgName[2]), 'wb')
                    imgFile.write(unzip.read(name))
                    imgFile.close()

            if name == '[Content_Types].xml':
                flag = 'header'
                dataDom = minidom.parseString(unzip.read(name))
                dataFile = self.DFS(dataDom.documentElement,flag).strip('/')

        buf = unzip.read(dataFile)
        flag = 'data'
        dataDom = minidom.parseString(buf)
        self.DFS(dataDom.documentElement, flag)
        #docID, data, filePath, startTime, logFile)
        self.textParser.parse(docID, self.textData, filePath, startTime, logFile)
        #print self.textData
        
    def DFS(self, rootNode, flag):
        #global fileData

        if flag == 'header':
            for childNodes in rootNode.childNodes:
                if childNodes.nodeName == 'Override':
                    if childNodes.attributes.get('PartName').value.endswith('document.xml'):
                        return childNodes.attributes.get('PartName').value

                self.DFS(childNodes, flag)

        if flag == 'data':
            for childNodes in rootNode.childNodes:
                if childNodes.nodeType  == 3:
                    self.textData += '\n'+ childNodes.nodeValue
                self.DFS(childNodes, flag)


if __name__ == "__main__":
    import time
    import re
    stTime = time.time()
    splitter = re.compile(r'\W*')
    docParser = DocxParser(None)
    docParser.Parse(None, 'Cramer.docx', "", None, False, "")
    
            
    endTime = time.time()
    print endTime - stTime
    CommonFunctions.ConvertSecondsToDayHourMinSec(endTime-stTime)
