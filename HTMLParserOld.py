# Written by Ram Basnet


#import sgmllib, formatter
import htmllib, formatter
import string, re

#from BeautifulSoup import *
import Globals

class ParseError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


class HTMLParser(htmllib.HTMLParser):
    def __init__(self, Stemmer=None):
        #sgmllib.SGMLParser.__init__(self)
        f = formatter.NullFormatter()#formatter.AbstractFormatter(formatter.DumbWriter())
        htmllib.HTMLParser.__init__(self, f)
        #self.textData = ""
        #self.BitMap = BitMap
        #self.WordFrequency = {}
        self.WordCount = 0
        self.StemmedWordCount = 0
        self.FooterLineRE = re.compile(r'[_-]{2,}')
        self.ListSepRE = re.compile(r'[~`!#$^&*()+=|\\{}\'"?><\[\],;]')
        self.Splitter = re.compile(r'\W+', re.I)
        self.EmailRE = re.compile(r"\A[A-Z0-9._%-]+@[A-Z0-9._%-]+\.[A-Z]+", re.I)
        self.HTTPRE = re.compile(r"\A(http://)[a-z0-9_-]+\.[a-z]{2,4}\b", re.I)
        self.Stemmer = Stemmer
        self.PhoneRE = re.compile(r"[1]*[- .(]*[0-9]*[- \.)]*[A-Z0-9]{3,3}[- .]+[A-Z0-9]{4,4}\b", re.I)
        #self.PunctuationMarks
        #self.splitter = re.compile(r' ')
        #self.badWords = re.compile(r'.*\\*\/*_*\d+.*\\*\/*_*.*', re.I)
        
    def parse(self, doc, wordID, stemmedWordID):
        #self.textData = ""
        #Globals.WordFrequency = {}
        self.WordCount = 0
        self.StemmedWordCount = 0
        self.WordID = wordID
        self.StemmedWordID = stemmedWordID
        
        try:
            self.feed(doc)
            
        except:
            self.close()
            raise ParseError('Parser Error')
        
        self.close()
        
    def CheckBadCharPresent(self, word):
        for pattern in Globals.BadChars:
            if re.search(pattern, word):
                return True
          
        return False  
        
    def RemovePunctuations(self, word):
        newWord = string.replace(word, "'", '')
        newWord = string.replace(newWord, '"', '')
        newWord = string.replace(newWord, '?', '')
        newWord = string.replace(newWord, '.', '')
        newWord = string.replace(newWord, ',', '')
        newWord = string.replace(newWord, ';', '')
        newWord = string.replace(newWord, ':', '')
        newWord = string.replace(newWord, "\\", "")
        newWord = string.replace(newWord, "/", "")
        newWord = string.replace(newWord, "-", "")
        newWord = string.replace(newWord, "_", "")
        newWord = string.replace(newWord, "!", "")
        newWord = string.replace(newWord, "@", "")
        
        return newWord
    
    def handle_data(self, data):
        data = string.lower(data)
        myList = data.split()
        #if data <> '\n' and data <> '\r\n' and (not re.search(r'(&nbsp;)+', data)):
        for word in myList:
            if self.FooterLineRE.match(word):
                continue
            if self.EmailRE.match(word) or self.HTTPRE.match(word) or self.PhoneRE.match(word):
                words = self.ListSepRE.split(word)
                for word in words:
                    if word:
                        self.handleWord(word)
            else:
                words = self.Splitter.split(word)
                for word in words:
                    if word:
                        self.handleWord(word)
   
   
    def handleWord(self, word):
        if Globals.WordFrequency.has_key(word):
            Globals.WordFrequency[word]['count'] += 1
            self.WordCount += 1
        else:
            if word not in Globals.Stopwords:
                self.WordCount += 1
                self.WordID += 1
                Globals.WordFrequency[word] = {'id': self.WordID, 'count' : 1}
        
        if not self.Stemmer:
            return
        #print 'stemmer'

        if Globals.StemmedWordFrequency.has_key(word):
            Globals.StemmedWordFrequency[word]['count'] += 1
            self.StemmedWordCount += 1
        else:
            if len(word) < 2:
                return
            if word not in Globals.Stopwords:
                #if len(word) <=2:
                #    return
                word = self.Stemmer.stem(word, 0,len(word)-1) #Apply Porter Stemmer to each word
                if Globals.StemmedWordFrequency.has_key(word):
                    Globals.StemmedWordFrequency[word]['count'] += 1
                    self.StemmedWordCount += 1
                else:
                    self.StemmedWordCount += 1
                    self.StemmedWordID += 1
                    Globals.StemmedWordFrequency[word] = {'id' : self.StemmedWordID, 'count' : 1}
    
    def ResetCounters(self):
        self.WordCount = 0
        self.StemmedWordCount = 0
        
    def GetWordCount(self):
        return self.WordCount
    
    def GetStemmedWordCount(self):
        return self.StemmedWordCount

    def GetWordID(self):
        return self.WordID

    def GetStemmedWordID(self):
        return self.StemmedWordID
        
    def printWordFrequency(self):
        for word in Globals.WordFrequency:
            print word + "=>" + str(Globals.WordFrequency[word]['count'])


if __name__ == "__main__":
    data = open('APSShortEmails.txt', 'r').read()    
    parser1 = HTMLParser()
    #parser1.ReadStopWords('stopwords.txt')    
    parser1.parse(data)
    print parser1.GetWordCount()
    #print "docID = %d"%parser1.DocID
    data = open('..\APSCaseDesktop1\Final\Final.txt', 'r').read()    
    #parser1.ReadStopWords('stopwords.txt')    
    parser1.parse(data) 
    #data = open('ShortEmails.txt', 'r').read()    
    #parser1.ReadStopWords('stopwords.txt')    
    #parser1.parse(data) 
    #print parser1.GetWordCount()
    #print "docID = %d"%parser1.DocID
    parser1.close()

    #stripper.ReadStopWords('stopwords.txt')
    #stripper.WriteStopWords()
    parser1.printWordFrequency()




