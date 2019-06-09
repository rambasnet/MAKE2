# Written by Ram Basnet
# Soft Computing: Fall 2006


import sgmllib, formatter
#import htmllib, formatter
import string, re
#import urllib, urlparse, re
#from BeautifulSoup import *
from Globals import *
from SqliteDatabase import *
from PorterStemmer import *


class ParseError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


class TextTokenizer(sgmllib.SGMLParser):
#class Parser(htmllib.HTMLParser):
    def __init__(self):
        
        f = formatter.NullFormatter()#formatter.AbstractFormatter(formatter.DumbWriter())
        #htmllib.HTMLParser.__init__(self, f)
        sgmllib.SGMLParser.__init__(self, f)
        self.SqliteDB = SqliteDatabase(Globals.DBName)
        
        self.Stemmer = PorterStemmer()
        
        #self.textData = ""
        #self.BitMap = BitMap
        #self.WordFrequency = {}
        self.splitter = re.compile(r'\W+', re.I)
        #self.splitter = re.compile(r'\s+', re.I)
        #self.badWords = re.compile(r'.*\\*\/*_*\d+.*\\*\/*_*.*', re.I)
        #self.DigitWord = re.compile(r'\b\d+\b', re.I)
        self.DigitWord = re.compile(r'[a-z]*\d+[a-z]*', re.I)
        self.AlphaNumericWord = re.compile(r'[a-z]*\W+[a-z]*', re.I)
        self.AlphabeticWord = re.compile(r'[a-z]+')
        #self.doubleSlashes = re.compile(r'\\*', re.I)
        self.BodyData = ""
        
                           
    def InitializeDocsInfo(self):
        self.BodyData = ""
        for fword in Globals.WordFrequency:
            Globals.WordFrequency[fword]['count'] = 0
            
        
    def parse(self, doc):
        self.feed(doc)
        
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
        data = self.RemovePunctuations(data)
        data = data.strip()
        if self.InTagDate:
            #if not self.DateHandled:
            self.DATE += data
            return
        
        if self.InTagMknote:
            self.MKNOTE += data
            #print "mknote = " + self.MKNOTE
            #self.MknoteHandled = True
            return
        
        if self.InTagUnknown:
            self.UNKNOWN += data
            return
        
        if self.InTagTopics:
            if len(self.TOPICS) > 0:
                self.TOPICS += "," + data
            else:
                self.TOPICS = data
            #print "Topics = %s"%(self.TOPICS)
            return
            
        if self.InTagPlaces:
            if len(self.PLACES) > 0:
                self.PLACES += ";" + data
            else:
                self.PLACES = data
            #print "Places = %s"%(self.PLACES)
            return
        
        if self.InTagPeople:
            if len(self.PEOPLE) > 0 :
                self.PEOPLE += ";" + data
            else:
                self.PEOPLE = data
                
            return
        
        if self.InTagOrgs:
            if len(self.ORGS) > 0:
                self.ORGS +=  ";" + data
            else:
                self.ORGS = data
            return
        
        if self.InTagExchanges:
            if len(self.EXCHANGES) > 0:
                self.EXCHANGES += ";" + data
            else:
                self.EXCHANGES = data
            return
        
        if self.InTagCompanies:
            if len(self.COMPANIES)  > 0:
                self.COMPANIES += ";" + data
            else:
                self.COMPANIES = data
            return
        
        if self.InTagAuthor:
            self.AUTHOR += data
            return
        
        if self.InTagDateline:
            self.DATELINE += data
                        
        elif self.InTagTitle:
            self.TITLE += data
            #self.PreprocessData(self.TITLE)
        
        elif self.InTagUnknown:
            self.UNKNOWN += data
        
        elif self.InTagBody:
            self.BodyData += data
            #print "body =" + self.BodyData
            

             
    def PreprocessData(self, data):
        data = string.lower(data)
        #print data
        myList = re.split(self.splitter, data)
        #if data <> '\n' and data <> '\r\n' and (not re.search(r'(&nbsp;)+', data)):
        #print myList
        for word in myList:
            word = word.strip()
            
            if len(word) > 2: # meaningful word must be more than 2 chars long
                #if not re.match(self.badWords, word) and word <> '': # keep only the words that start with an alphabet                
                #if not self.CheckBadCharPresent(word) and word <> '':
                #if word <> '': # and not self.NonDigitWord.match(word):
                if not self.DigitWord.match(word):
                #    return
                #if not self.AlphaNumericWord.match(word) and not self.DigitWord.match(word):
                #if self.AlphabeticWord.match(word):
                    #print newWord
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
                                Globals.WordFrequency[word] = {'id' : Globals.WordID, 'count' : 1}
  
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
            self.PreprocessData(self.TITLE)
        elif tag == tagDateline:
            self.InTagDateline = False
            
        elif tag == tagAuthor:
            self.InTagAuthor = False
        elif tag == tagUnknown:
            self.InTagUnknown = False
        elif tag == tagBody:
            self.InTagBody = False
            self.PreprocessData(self.BodyData)
        
        
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
       
       
        query = "INSERT INTO Documents (`ID`,  `ReutersTopics`, `LewisSplit`, `CgiSplit`, `Date`, `MkNote`, "
        query += "Unknown, `TextType`, `Author`, `Dateline`, `Title`, `Topics`, `Places`, `People`, "
        query += "`Orgs`, `Exchanges`, `Companies`) values ("
        query += str(docID) + ", "
        query += self.SqliteDB.SqlSQuote(self.REUTERSTOPICS) + ", "
        query += self.SqliteDB.SqlSQuote(self.LEWISSPLIT) + ", "
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
        #print query
        self.SqliteDB.ExecuteNonQuery(query)
        
        #BitMapKeys = Globals.BitMap.keys()
        #WordFreqKeys = Globals.WordFrequency.keys()
        query = "INSERT INTO BagOfWords(DocId, WordID, Frequency) values ('" + str(docID) + "', "
        for fword in Globals.WordFrequency:
            #print str(Globals.WordFrequency[fword]['count'])
            #print str(Globals.WordFrequency[fword]['id'])
            if Globals.WordFrequency[fword]['count'] > 0:
                query1 = "'" + str(Globals.WordFrequency[fword]['id']) + "' "
                query1 += ", '" + str(Globals.WordFrequency[fword]['count']) + "');"
                self.SqliteDB.ExecuteNonQuery(query + query1)
        
        self.SqliteDB.CloseConnection()
    
"""
if __name__ == "__main__":
    parser1 = ReutersParser()
    #parser1.ReadStopWords('stopwords.txt')    
    fin = open("test.txt", "r")
    data = str(fin.readlines())
    parser1.parse(data)
    parser1.close()
    fin.close()
"""
        
