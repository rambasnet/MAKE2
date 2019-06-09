#-----------------------------------------------------------------------------
# Name:        OutlookTextParser.py
# Purpose:     
#
# Author:      Ram B. Basnet
#
# Created:     2008/07/08
# RCS-ID:      $Id: OutlookTextParser.py $
# Copyright:   (c) 2008
# Licence:     All Rights Reserved.
#-----------------------------------------------------------------------------


import os.path
import string, re
from SqliteDatabase import *
import Constants
#from BeautifulSoup import *
import Globals
import EmailUtilities
import Classes
import TextParser
import PlatformMethods



class OutlookTextParser():
    def __init__(self, db, AttachmentsDict, Stopwords=[], Stemmer=None, bloomFilter=None):
        #self.filePath = filePath
        self.db = db
        self.Stemmer = Stemmer
        self.bloomFilter = bloomFilter
        self.AttachmentsDict = AttachmentsDict
        self.Stopwords = Stopwords
        self.FromRE = re.compile(r"(From:\W*)(.*)", re.I)
        self.ToRE = re.compile(r'(To:\W*)(.*)', re.I)
        self.CcRE = re.compile(r"(Cc:\W*)(.*)", re.I)
        self.BccRE = re.compile(r"(Bcc:\W*)(.*)", re.I)
        self.DateRE = re.compile(r'(Date:\W*)(.*)')
        self.SubjectRE = re.compile(r'(Subject:\W*)(.*)')
        self.AttachmentsRE = re.compile(r'(Attachments:\W*)(.*)')
        self.EmailRE = re.compile(r"[A-Z0-9._%-]+@[A-Z0-9._%-]+\.[A-Z]+", re.I)
        #self.EmailsDict = EmailsDict
        
        self.query = "insert into " + Constants.EmailsTable + "(DocID, FromID, ToID,EmailDate,Subject,Attachments,FilePath,AttachmentsPath,TotalRecipients,Size,`Group`,Label,Message) values (?,?,?,?,?,?,?,?,?,?,?,?,?)"
        #self.query1 = "insert into " + Constants.AddressBookTable + "(EmailID, FirstName, MiddleName, LastName, InBook) values (?,?,?,?,?)"
        
        #added for TC on Emails
        #self.WordCount = 0
        #self.StemmedWordCount = 0
        self.FooterLineRE = re.compile(r'[_-]{2,}')
        self.ListSepRE = re.compile(r'[~`!#$^&*()+=|\\{}\'"?><\[\],;]')
        self.Splitter = re.compile(r'\W+', re.I)
       
        self.PhoneRE = re.compile(r'([\d{3}]*)[\(\)-/\. ]*(\d{3})[\(\)-/\. ]*(\d{4})\D*')
        self.EmailRE = re.compile(r"\A[A-Z0-9._%-]+@[A-Z0-9._%-]+\.[A-Z]+", re.I)
        self.HTTPRE = re.compile(r"\A(http://)[a-z0-9_-]+\.[a-z]{2,4}\b", re.I)
        
        
    def parse(self, filePath):
        self.filePath = filePath
        self.WordsQuery = "insert into %s (Word, StemmedWord, Frequency) values (?,?,?)"%Constants.WordsTable
        
        query = "insert into %s (DocPath, DocType) values (?, ?)"%(Constants.DocumentsTable)
        self.DocID = self.db.InsertAutoRow(query, [(self.filePath, Constants.MessageDoc)])
                            
        self.fin = open(self.filePath, "rb")
        #line = self.GetLine()
        self.fromEmail = ""
        self.toEmails = []
        self.sentReceivedDate = ""
        self.subject = ""
        self.attachments = ""
        lineAfterSubject = 0
        self.NewAccounts = []
        self.Message = ""
        self.Phones = {}
        self.subjectFound = False
        
        self.location = 0

        self.sentReceivedDate = ""
        self.attachmentsPaths = ""
        filePathList = os.path.basename(self.filePath).split()
        
        if len(filePathList) >= 2:
            self.sentReceivedDate = "%s %s"%(filePathList[0], (filePathList[1].replace(".", ":")))
        else:
            print 'File found without date time: %s'%(PlatformMethods.Encode(self.filePath))
        
        self.lines = self.fin.readlines()
        headerDone = False
        endEmailLineFound = False
        
        while self.lines:
            #for line in lines:
            line = PlatformMethods.Encode(self.lines.pop(0))
            #print line
            if not line or line.startswith('X-MimeOLE:'):
                headerDone = True
                continue
            
            if self.subjectFound:
                if not line.strip():
                    if self.lines:
                        line = self.lines.pop(0)
                    else:
                        break
                        
                matched = self.AttachmentsRE.match(line)
                if matched:            
                    pass
                else:
                    if line.startswith('MIME-Version:'):
                        continue
                    else:
                        headerDone = True
                        
                        #continue
                    
            """
            #if not endEmailLineFound:
            if self.FooterLineRE.match(line):
                #endEmailLineFound = True
                if self.lines:
                    line = self.lines.pop(0).strip()
                    if not line:
                        if self.lines:
                            line = self.lines.pop(0).strip()
                            matched = self.FromRE.match(line)
                            if matched:
                                #print 'End of Email Found! Original Messages next ignored on file %s'%self.filePath
                                break
                        else:
                            break
                else:
                    break
                            
            """
                                        
            #print line
            if headerDone:
                self.Message += line
                line = line.strip()
                if line:
                    #textParser.parse(self.DocID, line, filePath)
                    self.handleLine(line.strip())
                    
                #if not endEmailLineFound:
                while self.lines:
                    line = self.lines.pop(0).strip()
                    self.Message += line
                    if self.FooterLineRE.match(line) or not line:
                        continue
                    self.handleLine(line)
                        
            else:
                #check for From: line
                line = line.strip()
                matched = self.FromRE.match(line)
                if matched:
                    fromPart = matched.group(2).strip().replace("<", '').replace(">", '').replace('"', '')
                    if fromPart:
                        #From: </O=ALBUQUERQUE PUBLIC SCHOOLS/OU=NETWORK SERVICES/CN=APS/CN=USERS/CN=ESCOBEDO_J>
                        lastCNIndex = fromPart.rfind('CN=')
                        if lastCNIndex > 0:
                            self.fromEmail = EmailUtilities.LookupEmailID(fromPart[lastCNIndex+3:])
                        else:
                            #possiblilites
                            #From: <reception@agc-nm.org>
                            #From: <Tom Savage>
                            #From: "Tom Savage" <tom@savage.com>
                            firstName, middleName, lastName, self.fromEmail = self.GetNamesAndEmailTuple(fromPart)
                            if not self.fromEmail:#look up address book to find email address
                                self.fromEmail = EmailUtilities.LookupEmailID(firstName + " " + middleName + " " + lastName)
                            
                            self.AddNewAccountToAddressBook(self.fromEmail, firstName, middleName, lastName)
                            
                    else: 
                        #self.fromEmail = EmailUtilities.LookupEmailID(matched.group(2).strip())
                        print "No From: second part: line =  ", PlatformMethods.Encode(line)
                          
                    continue
                
                #check for To: line
                matched = self.ToRE.match(line)
                if matched:
                    self.handleToCcBccSecondPart(matched)
                    continue
                
                #check for Cc: line
                matched = self.CcRE.match(line)
                if matched:
                    self.handleToCcBccSecondPart(matched)
                    continue
                
                #check for Bcc: line
                matched = self.BccRE.match(line)
                if matched:
                    self.handleToCcBccSecondPart(matched)
                    continue
                
                #check for Subject: line
                matched = self.SubjectRE.match(line)
                if matched:
                    self.subject = matched.group(2).strip()
                    self.subjectFound = True
                    continue
                  
                #check for Attachments: line
                matched = self.AttachmentsRE.match(line)
                if matched:
                    attachment = matched.group(2).strip()
                    attachList = attachment.split(',')
                    for attachment in attachList:
                        if attachment:
                            if self.attachments:
                                self.attachments += "|"
                            self.attachments += attachment
                            dateTimefileName = "%s - %s"%(self.sentReceivedDate, attachment)
                            if self.AttachmentsDict.has_key(dateTimefileName):
                                attachPath = self.AttachmentsDict[dateTimefileName]
                                #if  == attachment:
                                if self.attachmentsPaths:
                                    self.attachmentsPaths += "|"
                                self.attachmentsPaths += attachPath
                                self.attachmentsPaths += attachPath
                                self.attachmentsPaths += attachPath
                                self.attachmentsPaths += attachPath
                                self.attachmentsPaths += attachPath
                                self.attachmentsPaths += attachPath
                            else:
                                print 'No attachment file found for attachment name: %s'%(PlatformMethods.Encode(attachment))
                    continue
                    
            
        self.fin.close()
        
        if self.fromEmail:
            if not Globals.EmailsDict.has_key(self.fromEmail.lower()):
                Globals.EmailsDict[self.fromEmail.lower()] = {}
               
            manyValues = []
            
            for email in self.toEmails:
                if email:
                    if not Globals.EmailsDict.has_key(email.lower()):
                        Globals.EmailsDict[email.lower()] = {}
                    if Globals.EmailsDict[self.fromEmail.lower()].has_key(email.lower()):
                        Globals.EmailsDict[self.fromEmail.lower()][email.lower()]['Sent'] += 1
                    else:
                        Globals.EmailsDict[self.fromEmail.lower()][email.lower()] = {'Sent' : 1}
                        
                    manyValues.append((self.DocID, self.fromEmail, email, self.sentReceivedDate, self.subject, self.attachments, self.filePath, self.attachmentsPaths, len(self.toEmails), 0, 0, 'N/A', self.Message))    
                    
                    """
                    msg = Classes.EmailMessage()
                    msg.Sender = self.fromEmail
                    msg.Recipient = email
                    msg.Date = self.sentReceivedDate
                    msg.Subject = self.subject
                    msg.Attachments = self.attachments
                    msg.Size = 0
                    msg.TotalRecipients = len(self.toEmails)
                    msg.Group = 0
                    msg.filePath = self.filePath
                    msg.attachmentsPaths = self.attachmentsPaths
                    if Globals.MessageDict.has_key(self.sentReceivedDate.lower()):
                        Globals.MessageDict[self.sentReceivedDate.lower()].append(msg)
                    else:
                        Globals.MessageDict[self.sentReceivedDate.lower()] = [msg]
                    """
                    
            #if db:
            #values = tuple(self.toEmails)
            
            
            self.db.ExecuteMany(self.query, manyValues)
            #db.ExecuteMany(self.query1, self.NewAccounts)
            
            """
            print 'filePath ', filePath
            print " From: ", self.fromEmail
            print 'To: ', self.toEmails
            print " Date: ", self.sentReceivedDate, " Subject: ", self.subject, " Attachments: ", self.attachments
            print 'attach paths ', self.attachmentsPaths
            """
            #update the database for each email
        
        
        
        #add all phone numbers to database
        
        query = "insert into %s(Phone, DocID, Frequency) values (?,?,?)"%(Constants.PhonesTable)
        manyValues = []
        for key in self.Phones:
            manyValues.append((key, self.DocID, self.Phones[key]['Count']))
            
        #print manyValues
        self.db.ExecuteMany(query, manyValues)
        
        
    def AddNewAccountToAddressBook(self, email, firstName, middleName, lastName):
        if not EmailUtilities.LookupName(email):
            #self.NewAccounts.append((email, firstName, middleName, lastName, 0))
            
            newID = len(Globals.AddressBookDict) + 1
            if Globals.AddressBookDict.has_key(newID):
                newID += 1
                Globals.AddressBookDict[newID] = {'EmailID': email, 'FirstName':firstName, 'MiddleName':middleName, 'LastName':lastName, 'InBook':0}
                
                
    def GetNamesAndEmailTuple(self, secondPart):
        parts = secondPart.split()
        firstName = ""
        middleName = ""
        lastName = ""
        email = ""
        for part in parts:
            part = part.strip()
            if part == "-":
                continue
            
            
            emailFound = self.EmailRE.search(part)
            if emailFound:
                email = emailFound.group().strip()
            else:    
                if not firstName:
                    firstName = part
                elif not middleName:
                    middleName = part
                elif not lastName:
                    lastName = part
                else:
                    lastName += " " + part
            
        if not lastName:
            lastName = middleName
            middleName = ""
            
        return firstName, middleName, lastName, email
        
    
    def handleToCcBccSecondPart(self, matched):
        moreTo = False
        secondPart = matched.group(2).strip().replace("<", '').replace(">", '').replace('"', '')
        if secondPart.endswith(","):
            moreTo = True
        
        line = secondPart.strip(",")
        #print 'stripped line = ', line
        self.handleContinuousSecondPart(line)
        while moreTo:
            if self.lines:
                line = self.lines.pop(0).strip()
                if not line.endswith(","):
                    moreTo = False
                
                line = line.strip().replace("<", '').replace(">", '').replace('"', '').replace(",", '')
                #print 'stripped line = ', line
                self.handleContinuousSecondPart(line)
                
            else:
                break
            
            
    def handleContinuousSecondPart(self, secondPart):
        if secondPart:
            firstName, middleName, lastName, toEmail = self.GetNamesAndEmailTuple(secondPart)
            if toEmail:
                self.toEmails.append(toEmail)
            else:
                toEmail = EmailUtilities.LookupEmailID(firstName + " " + middleName + " " + lastName)
                self.toEmails.append(toEmail)
            self.AddNewAccountToAddressBook(toEmail, firstName, middleName, lastName)
        """
        else: 
            #self.fromEmail = EmailUtilities.LookupEmailID(matched.group(2).strip())
            print "No Second Part: second part: line =  ", secondPart
        """

                
 
    def PrintEmails(self):
        for id in Globals.EmailsDict:
            print id, " -> ", Globals.EmailsDict[id]
   
       
        
    def CheckBadCharPresent(self, word):
        for pattern in Globals.BadChars:
            if re.search(pattern, word):
                return True
          
        return False  
        
    
    def handleLine(self, line):
        data = string.lower(line)
           
        phoneList  = self.PhoneRE.findall(data)
        for numTuple in phoneList:
            phone = ""
            for num in numTuple:
                if num:
                    if phone:
                        phone += "-" + num
                    else:
                        phone += num
                        
            if phone:
                if self.Phones.has_key(phone):
                    self.Phones[phone]['Count'] += 1
                else:
                    self.Phones[phone] = {'Count':1}
                self.handleWord(phone, self.location)
                
        myList = data.split()
        #if data <> '\n' and data <> '\r\n' and (not re.search(r'(&nbsp;)+', data)):
        
        for word in myList:
            if word in self.Stopwords:
                self.location += 1
                continue
            
            if self.FooterLineRE.match(word):
                self.location += 1
                continue
            
            if self.EmailRE.match(word) or self.HTTPRE.match(word):
                words = self.ListSepRE.split(word)
                for word in words:
                    if len(word) > 2:
                        self.handleWord(word, self.location)
            else:
                words = self.Splitter.split(word)
                for word in words:
                    if len(word) > 2:
                        try:
                            self.handleWord(PlatformMethods.Encode(word), self.location)
                        except:
                            pass
                        
                    self.location += 1

        
    def handleWord(self, word, location):
        row = self.db.FetchOneRow("SELECT ROWID FROM %s WHERE Word=?"%(Constants.WordsTable), (PlatformMethods.Encode(word),))
        wordID = 1
        if row:
            wordID = row[0]
            self.db.ExecuteNonQuery("UPDATE %s set Frequency = Frequency + 1 where rowid = ?;"%(Constants.WordsTable), (wordID,))
        else:
            stemmedWord = ""
            if self.Stemmer:
                stemmedWord = self.Stemmer.stem(word, 0, len(word)-1)
                
            wordID = self.db.InsertAutoRow(self.WordsQuery, [(PlatformMethods.Encode(word), PlatformMethods.Encode(stemmedWord), 1)])
            
        InPath = 0
        if self.filePath.find(word) >=0:
            InPath = 1
            
        self.db.ExecuteNonQuery("insert into %s (DocID, WordID, Location, InPath) values (?, ?, ?, ?)"%(Constants.TextCatWordLocation), (self.DocID, wordID, location, InPath))
    
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
        for word in Globals.EmailsWordFrequency:
            print word + "=>" + str(Globals.EmailsWordFrequency[word]['count'])



if __name__ == "__main__":
    import os, sys
    
    Globals.AddressBookDict = {}
    #EmailUtilities.LoadAddressBookFromDB(Globals.AddressBookDict)
    db = SqliteDatabase('Emails.db')
    db.OpenConnection()
    EmailUtilities.SetupEmailsDB('Emails.db')
    dirName = r"..\test1"
    #sums = [0, 1] # 0 files 1 directory so far
    #try:
    #os.path.walk(dirName, ScanEmails, sums)
    #except Exception, value:
    #    print "Failed to walk directories. Error: %s"%(value)

    #for emailFile in os.listdir('..\EmailTest'):
    EmailsDict = {}
    AttachmentsDict = {}
    parser = OutlookTextParser(EmailsDict, AttachmentsDict, Stemmer=None)
    docID = 0
    wordID = 0
    stemmedWordID = 0
    for root, dirs, files in os.walk(dirName):
        for eachfile in files:
            filePath = os.path.join(root, eachfile)
            parser.parse(filePath, db, docID, wordID, stemmedWordID)
        
    """
    parser.parse('sampleEmail1.txt', db)
    parser.parse('AttachmentEmail.txt', db)
    parser.PrintEmails()
    """
    



