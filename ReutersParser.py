# Written by Ram Basnet
# Soft Computing: Fall 2006


import sgmllib, formatter
#import htmllib, formatter
import string, re
import sys, os
#import urllib, urlparse, re
#from BeautifulSoup import *
from Globals import *
from SqliteDatabase import *
from PorterStemmer import *

tagReuters = "reuters"
tagDate = "date"
tagMknote = "mknote"
tagTopics = "topics"
tagUnknown = "unknown"
tagPlaces = "places"
tagPeople = "people"
tagOrgs = "orgs"
tagExchanges = "exchanges"
tagCompanies = "companies"
tagAuthor = "author"
tagDateline = "dateline"
tagTitle = "title"
tagBody = "body"
tagText = "text"

class ParseError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


class ReutersParser(sgmllib.SGMLParser):
#class Parser(htmllib.HTMLParser):
    def __init__(self):
        
        f = formatter.NullFormatter()#formatter.AbstractFormatter(formatter.DumbWriter())
        #htmllib.HTMLParser.__init__(self, f)
        sgmllib.SGMLParser.__init__(self, f)
        self.SqliteDB = SqliteDatabase(Globals.DBName)
        
        self.Stemmer = PorterStemmer()
        
        self.ReadStopWords('stopwords.txt')
                
        #self.textData = ""
        #self.BitMap = BitMap
        #self.WordFrequency = {}
        #self.splitter = re.compile(r'\W+', re.I)
        self.splitter = re.compile(r'\s+', re.I)
        #self.badWords = re.compile(r'.*\\*\/*_*\d+.*\\*\/*_*.*', re.I)
        self.DigitWord = re.compile(r'\b\d+\b', re.I)
        self.AlphaNumericWord = re.compile(r'\w+', re.I)
        #self.doubleSlashes = re.compile(r'\\*', re.I)
        self.tagType = ""
        self.REUTERSTOPICS = ""
        self.LEWISSPLIT = ""
        self.CGISPLIT = ""
        self.NEWID = ""
        self.DATE = ""
        self.MKNOTE = ""
        self.TOPICS = ""
        self.PLACES = ""
        self.UNKNOWN = ""
        self.AUTHOR = ""
        self.DATELINE = ""
        self.TITLE = ""
        self.TOPICS = ""
        self.PLACES = ""
        self.PEOPLE =""
        self.ORGS = ""
        self.EXCHANGES = ""
        self.COMPANIES = ""
        self.TEXTTYPE = ""
        
        self.DateHandled = False
        self.InTagDate = False
        self.MknoteHandled = False
        
        self.InTagMknote = False
        self.InTagTitle = False
        self.InTagDateline = False
        self.InTagBody = False
        self.InTagTopics = False
        self.InTagPlaces = False
        self.InTagPeople = False
        self.InTagOrgs = False
        self.InTagExchanges = False
        self.InTagCompanies = False
        self.InTagAuthor = False
        self.InTagUnknown = False
                
            
    def InitializeDocsInfo(self):
                
        self.LEWISSPLIT = ""
        self.CGISPLIT = ""
        self.NEWID = ""
        self.DATE = ""
        self.MKNOTE = ""
        #self.CATEGORYSET = ""
        self.UNKNOWN = ""
        self.AUTHOR = ""
        self.DATELINE = ""
        self.TITLE = ""
        self.REUTERSTOPICS = ""
        self.TOPICS = ""
        self.PLACES = ""
        self.PEOPLE =""
        self.ORGS = ""
        self.EXCHANGES = ""
        self.COMPANIES = ""
        self.TEXTTYPE = ""
        self.DateHandled = False
        self.MknoteHandled = False
        self.InTagTopics = False
        self.InTagPlaces = False
        self.InTagPeople = False
        self.InTagOrgs = False
        self.InTagExchanges = False
        self.InTagCompanies = False
        self.InTagMknote = False
        self.InTagTitle = False
        self.InTagDateline = False
        
        self.InTagAuthor = False
        self.InTagUnknown = False
        self.InTagBody = False
        for fword in Globals.WordFrequency:
            Globals.WordFrequency[fword]['count'] = 0
            
        
    def parse(self, doc):
        #self.textData = ""
       
        #try:
        self.feed(doc)
        #    
        #except:
        #    self.close()
        #    raise ParseError('Parser Error')
        
        #self.close()
        
    """def CheckBadCharPresent(self, word):
        for pattern in Globals.BadChars:
            if re.search(pattern, word):
                return True
          
        return False  
    """
        
    def RemovePunctuations(self, word):
        newWord = string.replace(word, "'", '')
        newWord = string.replace(newWord, '"', '')
        newWord = string.replace(newWord, '?', '')
        newWord = string.replace(newWord, '.', '')
        newWord = string.replace(newWord, ',', '')
        newWord = string.replace(newWord, ';', '')
        newWord = string.replace(newWord, ':', '')
        newWord = string.replace(newWord, '!', '')
        newWord = string.replace(newWord, '\\n', '')
        newWord = string.replace(newWord, '\\n\\r', '')
        return newWord
    
    def handle_data(self, data):
        print "asfddsa;fkljjjjjjjjj"
        data = self.RemovePunctuations(data)
        data = data.strip()
        if self.InTagDate:
            #if not self.DateHandled:
            self.DATE += data
            print "dateasdfdsf = " + data
            #   self.DateHandled = True
            return
        
        if self.InTagMknote:
            self.MKNOTE += data
            print "mknote = " + self.MKNOTE
            #self.MknoteHandled = True
            return
        
        if self.InTagUnknown:
            self.UNKNOWN += data
            return
        
        if self.InTagTopics:
            self.TOPICS += data + ","
            print "Topics = %s"%(self.TOPICS)
            return
            
        if self.InTagPlaces:
            self.PLACES += data + ","
            print "Places = %s"%(self.PLACES)
            return
        
        if self.InTagPeople:
            self.PEOPLE += data + ","
            return
        
        if self.InTagOrgs:
            self.ORGS += data + ","
            return
        
        if self.InTagExchanges:
            self.EXCHANGES += data + ","
            return
        
        if self.InTagCompanies:
            self.COMPANIES += data + ","
            return
        
        if self.InTagAuthor:
            self.AUTHOR += data
            return
        
        if self.InTagDateline:
            self.DATELINE += data
                        
        elif self.InTagTitle:
            self.TITLE += data
        
        elif self.InTagUnknown:
            self.UNKNOWN += data
        
        elif self.InTagBody:
            
            data = string.lower(data)
            
            myList = re.split(self.splitter, data)
            #if data <> '\n' and data <> '\r\n' and (not re.search(r'(&nbsp;)+', data)):
            #print myList
            for word in myList:
                word = word.strip()
                
                #if len(word) > 2: # meaningful word must be more than 2 chars long
                
                #if not re.match(self.badWords, word) and word <> '': # keep only the words that start with an alphabet                
                #if not self.CheckBadCharPresent(word) and word <> '':
                #if word <> '': # and not self.NonDigitWord.match(word):
                #if self.DigitWord.match(word):
                #    return
                if self.AlphaNumericWord.match(word):
                    #print newWord
                    if not self.DigitWord.match(word):
                        
                        if Globals.WordFrequency.has_key(word):
                            Globals.WordFrequency[word]['count'] += 1
                            #self.WordFrequency[word]['bitMapped'] = 1
                        else:
                            if word not in Globals.StopWordList:
                                word = self.Stemmer.stem(word, 0,len(word)-1) #Apply Porter Stemmer to each word
                                if Globals.WordFrequency.has_key(word):
                                    Globals.WordFrequency[word]['count'] += 1
                                
                                else:
                                    Globals.WordID += 1
                                    #print "word = %s" %word
                                    #print "id = %d " %Globals.WordFrequency[word]['id']           
                                    Globals.WordFrequency[word] = {'id' : Globals.WordID, 'count' : 1}
                                    #Globals.WordFrequency[word] = {}    
                                    #print "count = %d"%Globals.WordFrequency[word]['count']
                                    #self.WordFrequency[word]['bitMapped'] = 0
                                    
                
  
    # Overridable -- handle start tag
    def handle_starttag(self, tag, method, attrs):
        #def handle_starttag(self, <REUTER, method, attrs):
        #method(attrs)
        #pass
        #print "tag = %s: attrs = %s"%(tag, attrs)
        self.tagType = tag
        if self.tagType == tagReuters:
            for name, value in attrs:
                #print "attr name %s attr value = %s"%(name, value)
                if name == "topics":
                    self.REUTERSTOPICS = value
                if name == "lewissplit":
                    self.LEWISSPLIT = value
                if name == "cgisplit":
                    self.CGISPLIT = value
                if name == "newid":
                    self.NEWID = value
        elif self.tagType == tagText:
            for name, value in attrs:
                if name == "type":
                    self.TEXTTYPE = value
                    
        elif self.tagType ==  tagDate:
            self.InTagDate = True
        elif self.tagType == tagTopics:
            self.InTagTopics = True
        elif self.tagType == tagPlaces:
            self.InTagPlaces = True
        elif self.tagType == tagPeople:
            self.InTagPeople = True
        elif self.tagType == tagOrgs:
            self.InTagOrgs == True
        elif self.tagType == tagExchanges:
            self.InTagExchanges = True
        elif self.tagType == tagCompanies:
            self.InTagCompanies = True    
        elif self.tagType == tagMknote:
            self.InTagMknote = True
        elif self.tagType == tagTitle:
            self.InTagTitle = True
        elif self.tagType == tagDateline:
            self.InTagDateline = True
        elif self.tagType == tagAuthor:
            self.InTagAuthor = True
        elif self.tagType == tagUnknown:
            self.InTagUnknown = True
        elif self.tagType == tagBody:
            self.InTagBody = True
        
        #print "topics = " + self.TOPICS + " :: "  + "newid = " + self.NEWID
        
    
    # Overridable -- handle end tag
    def handle_endtag(self, tag, method):
        
        if tag == tagReuters:
            self.UpdateDatabase(self.NEWID)
            self.InitializeDocsInfo()
            
            #pass
        elif tag == tagTopics:
            self.InTagTopics = False
        elif tag == tagPlaces:
            self.InTagPlaces = False
        #print "tag = %s\n"%(tag)
        elif tag ==  tagDate:
            self.InTagDate = False
        elif tag == tagTopics:
            self.InTagTopics = False
        elif tag == tagPlaces:
            self.InTagPlaces = False
        elif tag == tagPeople:
            self.InTagPeople = False
        elif tag == tagOrgs:
            self.InTagOrgs == False
        elif tag == tagExchanges:
            self.InTagExchanges = False
        elif tag == tagCompanies:
            self.InTagCompanies = False    
        elif tag == tagMknote:
            self.InTagMknote = False
        elif tag == tagTitle:
            self.InTagTitle = False
        elif tag == tagDateline:
            self.InTagDateline = False
        elif tag == tagAuthor:
            self.InTagAuthor = False
        elif tag == tagUnknown:
            self.InTagUnknown = False
        elif tag == tagBody:
            self.InTagBody = False
        
        
    def start_reuters(self, tag, attrs):
        #print "start tag = %s: attrs = %s"%(tag, attrs)
        pass
        
        #self.tagType = retures
    
    def end_reuters(self, tag):
        #print "end tag = %s: "%(tag)
        pass
    
    def start_date(self, tag, attrs):
        pass
    
    def end_date(self, tag, attrs):
        pass
    
    def start_topics(self, tag, attrs):
        pass
    
    def end_topics(self, tag):
        pass
    
    def start_d(self, tag):
        pass
    
    def end_d(self, tag):
        pass
    
    def start_places(self, tag):
        pass
    
    def end_places(self, tag):
        pass
    
    def start_people(self, tag):
        pass
    def end_people(self, tag):
        pass
    
    def start_orgs(self, tag):
        pass
    def end_orgs(self, tag):
        pass
    
    def start_exchanges(self, tag):
        pass
    
    def end_exchanges(self, tag):
        pass
    
    def start_companies(self, tag):
        pass
    def end_companies(self, tag):
        pass
    
    def start_author(self, tag):
        pass
    
    def end_author(self, tag):
        pass
    
    def start_dateline(self, tag):
        pass
    def end_dateline(self, tag):
        pass
    
    def start_title(self, tag):
        pass
    def end_title(self, tag):
        pass
        
    def start_body(self, tag):
        pass
    def end_body(self, tag):
        pass
        

    def printWordFrequency(self):
        for word in Globals.WordFrequency:
            print word + "=>" + str(Globals.WordFrequency[word]['count'])
            
            
    def UpdateDatabase(self, docID):
        """
            This method is called after reading every document.
            It updates bitmap index in memory.
            It also updates the database
        """
        
                
        if not self.SqliteDB.OpenConnection():
            print 'Database Connection failed!'
            return None
       
       
        query = "INSERT INTO Documents (`ID`,  `ReutersTopics`, `CgiSplit`, `Date`, `MkNote`, "
        query += "Unknown, `TextType`, `Author`, `Dateline`, `Title`, `Topics`, `Places`, `People`, "
        query += "`Orgs`, `Exchanges`, `Companies`) values ("
        query += str(docID) + ", "
        query += self.SqliteDB.SqlSQuote(self.REUTERSTOPICS) + ", "
        query += self.SqliteDB.SqlSQuote(self.CGISPLIT) + ", "
        query += self.SqliteDB.SqlSQuote(self.DATE) + ", "
        query += self.SqliteDB.SqlSQuote(self.MKNOTE) + ","
        query += self.SqliteDB.SqlSQuote(self.UNKNOWN) + ", "
        query += self.SqliteDB.SqlSQuote(self.TEXTTYPE) + ", "
        query += self.SqliteDB.SqlSQuote(self.AUTHOR) + ", "
        query += self.SqliteDB.SqlSQuote(self.DATELINE) + ", "
        query += self.SqliteDB.SqlSQuote(self.TITLE) + ", "
        query += self.SqliteDB.SqlSQuote(self.TOPICS) + ", "
        query += self.SqliteDB.SqlSQuote(self.PLACES) + ", "
        query += self.SqliteDB.SqlSQuote(self.PEOPLE) + ", "
        query += self.SqliteDB.SqlSQuote(self.ORGS) + ", "
        query += self.SqliteDB.SqlSQuote(self.EXCHANGES) + ", "
        query += self.SqliteDB.SqlSQuote(self.COMPANIES) + ");"
        print query
        self.SqliteDB.ExecuteNonQuery(query)
        
        #BitMapKeys = Globals.BitMap.keys()
        #WordFreqKeys = Globals.WordFrequency.keys()
        query = "INSERT INTO BagOfWords(DocId, WordID, Frequency) values ('" + str(docID) + "', "
        for fword in Globals.WordFrequency:
            #print str(Globals.WordFrequency[fword]['count'])
            #print str(Globals.WordFrequency[fword]['id'])
            query1 = "'" + str(Globals.WordFrequency[fword]['id']) + "' "
            query1 += ", '" + str(Globals.WordFrequency[fword]['count']) + "');"
            print query + query1
            self.SqliteDB.ExecuteNonQuery(query + query1)
        
        self.SqliteDB.CloseConnection()
    
    
    

    def CompileBadCharsPattern(self):
        Globals.BadChars.add(re.compile(r'\W+'))
        Globals.BadChars.add(re.compile(r'_+'))
        Globals.BadChars.add(re.compile(r'~+'))
        #Globals.BadChars.add(re.compile(r'!+'))
        Globals.BadChars.add(re.compile(r'@+'))
        Globals.BadChars.add(re.compile(r'#+'))
        Globals.BadChars.add(re.compile(r'\$+'))
        Globals.BadChars.add(re.compile(r'%+'))
        Globals.BadChars.add(re.compile(r'\^+'))
        Globals.BadChars.add(re.compile(r'&+'))
        Globals.BadChars.add(re.compile(r'\*+'))
        Globals.BadChars.add(re.compile(r'\(+'))
        Globals.BadChars.add(re.compile(r'\)+'))
        Globals.BadChars.add(re.compile(r'\d+'))
        #Globals.BadChars.add(re.compile(r'-+'))
        Globals.BadChars.add(re.compile(r'\++'))
        Globals.BadChars.add(re.compile(r'\|+'))
        Globals.BadChars.add(re.compile(r'=+'))
        Globals.BadChars.add(re.compile(r'\\+'))
        Globals.BadChars.add(re.compile(r'\/+'))
        Globals.BadChars.add(re.compile(r'<+'))
        #Globals.BadChars.add(re.compile(r',+'))
        Globals.BadChars.add(re.compile(r'>+'))

                
        
    
    def ReadDirectory(self):
        sums = [1, 0] # 0 files 1 directory so far
        #InitializeKeyWordsFrequencyDictionary()
        os.path.walk(Globals.DirName, self.ReadFile, sums)
        #self.parser.close()
        fout = open(Globals.ScanStatusFile, "w")
        fout.write("Total Directories = " + str(sums[0]) + "\n")
        fout.write("Total Files = " + str(sums[1]) + "\n")
        fout.close()
        
    def ReadFile(self, sms, dirName, fileList):
        for file in fileList:
            # get full path name relative to where program is run; the
            # function os.path.join() adds the proper delimiter for the OS
            fullFileName = os.path.join(dirName, file)
            if os.path.islink(fullFileName): break
            if os.path.isfile(fullFileName):
                sms[1] += 1
                #try:
                fin = open(fullFileName, "r")
                data = str(fin.readlines())
                self.parse(data)
                print data
                fin.close()
                #except:
                #   print "Error reading file \n." + fullFileName
            else:
                sms[0] += 1
            
        return None

       
    def ReadStopWords(self, fileName):
        fin = open(fileName, 'r')
        word = fin.readline()
        while word:
            word = word[:-1]
            Globals.StopWordList.add(word)
            word = fin.readline()
        
        fin.close()
  
    
            
    def SetupReutersDB(self):
        db = SqliteDatabase(Globals.DBName)
        db.OpenConnection()
            
        #Session table
        query = """CREATE TABLE `Documents`(
            `ID` text Primary Key,
            `ReutersTopics` text,
            `CgiSplit` text,
            `Date` text,
            `MkNote` text,
            `Unknown` text,
            `TextType` text,
            `Author` text,
            `Dateline` text,
            `Title` text,
            `Topics` text,
            `Places` text,
            `People` text,
            `Orgs` text,
            `Exchanges` text,
            `Companies` text
            ); """
        db.ExecuteNonQuery(query)
        
        query = """CREATE TABLE `BagOfWords`(
            `DocID` text,
            `WordID` text,
            `Frequency` text,
            `InverseDocFrequency` text,
            Primary Key (DocID, WordID)
            ); """
        db.ExecuteNonQuery(query)
        
        query = """CREATE TABLE `Words`(
            `ID` text Primary Key,
            `Word` text
            ); """
        db.ExecuteNonQuery(query)
        
        db.CloseConnection()
        
    def WriteWrodsInDatabase(self):
        db = SqliteDatabase(Globals.DBName)
        db.OpenConnection()
        for fword in Globals.WordFrequency:
            query = "INSERT INTO Words set ID = '" + str(Globals.WordFrequency[fword]['id']) + "' "
            query += ", Word = " + db.SqlSQuote(fword) + ";"
            db.ExecuteNonQuery(query)
        db.CloseConnection()
        
        
if __name__ == '__main__':                   
    
    parser = ReutersParser()
    parser.SetupReutersDB()
    parser.ReadDirectory()
    parser.WriteWrodsInDatabase()
    
        
