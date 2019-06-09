# Written by Ram Basnet

import os.path
import string, re
from SqliteDatabase import *
import Constants
#from BeautifulSoup import *
import Globals
import EmailUtilities
import Classes

class ParseError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


class OutlookTextParser():
    def __init__(self, EmailsDict, AttachmentsDict, Stemmer=None):
        #self.filePath = filePath
        #db = db
        self.AttachmentsDict = AttachmentsDict
        
        self.FromNameOnlyRE = re.compile(r"\A(From:\W*)([A-Z\.\- _0-9]+)([ >]*)", re.I)
        self.FromEmailOnlyRE = re.compile(r"\A(From:\W*)([A-Z0-9\._%\-]+@[A-Z0-9\._%\-]+\.[A-Z]+)*([ >]*)", re.I)
        #self.FromRE = re.compile(r"\A(From:\W*)([A-Z.\- _0-9]+)*(<)*([A-Z0-9._%-]+@*[A-Z0-9._%-]+\.[A-Z]+)*(>)*", re.I)
        self.FromNameAndEmailRE = re.compile(r"\A(From:\W*)([A-Z\.\- _0-9]+)([ <]+)([A-Z0-9\._%\-]+@[A-Z0-9\._%\-]+\.[A-Z]+)*([ >]+)", re.I)
        
        self.ToNameOnlyRE = re.compile(r"\A(To:\W*)([A-Z\.\- _0-9]+)([ >]*)([ ,;]*)", re.I)
        self.ToEmailOnlyRE = re.compile(r"\A(To:\W*)([A-Z0-9\._%\-]+@[A-Z0-9\._%\-]+\.[A-Z]+)*([ >]*)([ ,;]*)", re.I)
        self.ToNameAndEmail1RE = re.compile(r"\A(To:\W*)([A-Z\.\- _0-9]+)([ <]+)([A-Z0-9\._%\-]+@[A-Z0-9\._%\-]+\.[A-Z]+)*([ >]+)([ ,;]*)", re.I)
        #self.ToRE = re.compile(r"\A(To:\W*)(['A-Z.\- @%0-9_]+)*(<)*([A-Z0-9._%-]+@*[A-Z0-9._%-]+\.[A-Z]+)*(>)*([,;])*", re.I)
        
        #self.RestToRE = re.compile(r"([ \t])*(['A-Z.\- @%0-9]+)*(<)*([A-Z0-9._%-]+@*[A-Z0-9._%-]+\.[A-Z]+)*(>)*", re.I)
        self.RestToNameOnlyRE = re.compile(r"([ \t]*)('[A-Z\.\- _0-9]+)([ >]*)([ ,;]*)", re.I)
        self.RestToEmailOnlyRE = re.compile(r"([ \t]*)([A-Z0-9\._%\-]+@[A-Z0-9\._%\-]+\.[A-Z]+)*([ >]*)([ ,;]*)", re.I)
        self.RestToNameAndEmail1RE = re.compile(r"([ \t]*)([A-Z\.\- _0-9]+)([ <]+)([A-Z0-9\._%\-]+@[A-Z0-9\._%\-]+\.[A-Z]+)*([ >]+)([ ,;]*)", re.I)
        self.CcRE = re.compile(r"\A(Cc:\W*)(['A-Z.\- @%0-9]+)(<)*([A-Z0-9._%-]+@*[A-Z0-9._%-]+\.[A-Z]+)*(>)*([,;])*", re.I)
        self.BccRE = re.compile(r"\A(Bcc:\W*)(['A-Z.\- @%0-9]+)*(<)*([A-Z0-9._%-]+@*[A-Z0-9._%-]+\.[A-Z]+)*(>)*([,;])*", re.I)
        self.DateRE = re.compile(r'\A(Date:*\W*)(.+)')
        self.SubjectRE = re.compile(r'\A(Subject:\W*)(.*)')
        self.AttachmentsRE = re.compile(r'\A(Attachments:\W*)(.*)')
        #self.FooterLineRE = re.compile(r'[_-]{2,}')
        #self.ListSepRE = re.compile(r'[~`!#$^&*()+=|\\{}\'"?><\[\],;]')
        #self.Splitter = re.compile(r'\W+', re.I)
        self.EmailRE = re.compile(r"[A-Z0-9._%-]+@[A-Z0-9._%-]+\.[A-Z]+", re.I)
        self.EmailsDict = EmailsDict
        self.query = "insert into " + Constants.EmailsTable + "(DocID, FromID,ToID,EmailDate,Subject,Attachments,FilePath,AttachmentsPath,TotalRecipients,Size,`Group`,Label,Message) values (?,?,?,?,?,?,?,?,?,?,?,?,?)"
        self.query1 = "insert into " + Constants.AddressBookTable + "(EmailID, FirstName, MiddleName, LastName, InBook) values (?,?,?,?,?)"
        
        #added for TC on Emails
        self.WordCount = 0
        self.StemmedWordCount = 0
        self.FooterLineRE = re.compile(r'[_-]{2,}')
        self.ListSepRE = re.compile(r'[~`!#$^&*()+=|\\{}\'"?><\[\],;]')
        self.Splitter = re.compile(r'\W+', re.I)
        self.EmailRE = re.compile(r"\A[A-Z0-9._%-]+@[A-Z0-9._%-]+\.[A-Z]+", re.I)
        self.HTTPRE = re.compile(r"\A(http://)[a-z0-9_-]+\.[a-z]{2,4}\b", re.I)
        self.Stemmer = Stemmer
        self.PhoneRE = re.compile(r"[1]*[- .(]*[0-9]*[- \.)]*[A-Z0-9]{3,3}[- .]+[A-Z0-9]{4,4}\b", re.I)
        self.PhonePattern = re.compile(r'(\d{3})\D*(\d{3})\D*(\d{4})\D*(\d*)$') #call search with the pattern
        
        
    def parse(self, filePath, db, docID, wordID, stemmedWordID):
        
        self.DocID = docID
        self.WordID = wordID
        self.StemmedWordID = stemmedWordID
        self.WordCount = 0
        self.StemmedWordCount = 0
        
        self.fin = open(filePath, "r")
        line = self.GetLine()
        self.fromEmail = ""
        self.toEmails = []
        self.sentReceivedDate = ""
        self.subject = ""
        self.attachments = ""
        lineAfterSubject = 0
        self.NewAccounts = []
        self.Message = ""
        self.Phones = {}
        
        
        self.sentReceivedDate = ""
        self.attachmentsPaths = ""
        filePathList = os.path.basename(filePath).split()
        
        if len(filePathList) >= 2:
            self.sentReceivedDate = "%s %s"%(filePathList[0], (filePathList[1].replace(".", ":")))
        else:
            print 'File found without date time: %s'%filePath
        
        while line:
            
            line = line.strip()
            self.handleLine(line)
            #print line
            #if lineAfterSubject > 3:
            #    break
            #print line
            #self.FromRE = re.compile(r"\A(From: )([A-Z.\- _0-9]+)(<)*([A-Z0-9._%-]+@[A-Z0-9._%-]+\.[A-Z]+)*(>)*", re.I)
            if line.startswith('From:'):
                lastCNIndex = line.rfind('CN=')
                if lastCNIndex > 0:
                    self.fromEmail = EmailUtilities.LookupEmailID(line.strip()[lastCNIndex+3:-1])
                else:
                    
                    matched = self.FromNameAndEmailRE.match(line)
                    if matched:
                        #else:
                        #print "From: ", line
                        if matched.group(4): #email address is present in from
                            #possiblilites
                            #From: <reception@agc-nm.org>
                            #To: <Tom Savage>
                            
                            if self.EmailRE.match(matched.group(4)):
                                self.fromEmail = matched.group(4).strip()
                                if not EmailUtilities.LookupName(self.fromEmail):
                                    #No account was in the address book so add it
                                    firstName, middleName, lastName = self.GetNamesTuple(matched.group(2).strip())
                                    self.NewAccounts.append((self.fromEmail, firstName, middleName, lastName, 0))
                                    newID = len(Globals.AddressBookDict) + 1
                                    if Globals.AddressBookDict.has_key(newID):
                                        newID += 1
                                        Globals.AddressBookDict[newID] = {'EmailID': self.fromEmail, 'FirstName':firstName, 'MiddleName':middleName, 'LastName':lastName}
                            else:
                                self.fromEmail = EmailUtilities.LookupEmailID(matched.group(4).strip())
                            #print "From: ", self.fromEmail
                        else: #look up address book to find email address
                            print "no email From: ", matched.group(2)
                            self.fromEmail = EmailUtilities.LookupEmailID(matched.group(2).strip())
                            #print "no email From: ", self.fromEmail
                    else:
                        
                        matched = self.FromEmailOnlyRE.match(line)
                        if matched:
                            self.fromEmail = matched.group(2)
                        else:
                            matched = self.FromNameOnlyRE.match(line)
                            if matched:
                                self.fromEmail = EmailUtilities.LookupEmailID(matched.group(2).strip())
                            else:
                                print 'unmatched From: line %s'%line
                           
                line = self.GetLine()
                continue
            if line.startswith('To:'):
                line = self.ProcessTo(line)
                continue
                #self.CcRE = re.compile(r"\A(Cc: )(['A-Z.\- @%0-9]+)(<)*([A-Z0-9._%-]+@[A-Z0-9._%-]+\.[A-Z]+)*(>)*([,;])*", re.I)
            if line.startswith('Cc:'):
                matched = self.CcRE.match(line)
                if matched:
                    #print "Cc: ", line
                    line = self.ProcessTo(line)
                    continue
                else:
                    print "Cc found but didn't match with RE. :", line
            if line.startswith('Bcc:'):
                #self.BccRE = re.compile(r"\A(Bcc: )(['A-Z.\- @%0-9]+)(<)*([A-Z0-9._%-]+@[A-Z0-9._%-]+\.[A-Z]+)*(>)*([,;])*", re.I)
                matched = self.BccRE.match(line)
                if matched:
                    #print line
                    line = self.ProcessTo(line)
                    continue
                else:
                    print "Bcc found but didn't match with RE. :", line
                    
                    
            if line.startswith('Date:'):
                #self.DateRE = re.compile(r'\A(Date: )(.+)')
                """
                matched = self.DateRE.match(line)
                if matched:
                    #print "Date: ", line
                    #self.sentReceivedDate = matched.group(2)
                    line = self.GetLine()
                    continue
                else:
                    print "Date found but didn't match with RE. :", line
                """
                line = self.GetLine()
                continue
                 
            if line.startswith('Subject:'):
                #self.SubjectRE = re.compile(r'\A(Subject: )(.*)')
                matched = self.SubjectRE.match(line)
                if matched:
                    #print "Subject: ", line
                    self.subject = matched.group(2)
                    lineAfterSubject += 1
                    line = self.GetLine()
                    lineCount = 0
                    while not line.strip():
                        line = self.GetLine()
                        lineCount += 1
                        if lineCount >= 5:
                            print '5 Empty lines after Subject line in file: ', filePath
                            break
                        
                        #print 'line = ', line
                else:
                    print "Subject found but didn't match with RE. :", line
                    
            if line.startswith('Attachments:'):
                #self.AttachmentsRE = re.compile(r'\A(Attachments: )(.*)')
                matched = self.AttachmentsRE.match(line)
                if matched:
                    #print "Subject: ", line
                    attachment = matched.group(2)
                    attachList = attachment.split(',')
                    while (attachList[0]): # and len(attachList) > 1):
                        for attachment in attachList:
                            if attachment:
                                if self.attachments:
                                    self.attachments += "|"
                                self.attachments += attachment
                                dateTimefileName = "%s - %s"%(self.sentReceivedDate, attachment)
                                if self.AttachmentsDict.has_key(dateTimefileName):
                                    filePath = self.AttachmentsDict[dateTimefileName]
                                    #if  == attachment:
                                    if self.attachmentsPaths:
                                        self.attachmentsPaths += "|"
                                    self.attachmentsPaths += filePath
                                else:
                                    print 'No attachment file found for attachment name: '%(attachment)
                        
                        #look for an empty line before message body begins...
                        
                        attachList = self.GetLine().split(',')
                        """
                        for attachment in attachList:
                            if attachment:
                                if self.attachments:
                                    self.attachments += ","
                            self.attachments += attachment
                        """
                else:
                    print "Attachments: found but didn't match re: ", line
                    
                #line = self.GetLine()
                #while line:
                self.Message = "".join(self.fin.readlines())
                #line = self.GetLine()
                break
                    #break
            else:
                #if self.attachments:
                #line = self.GetLine()
                #while line:
                self.Message = "".join(self.fin.readlines())
                #line = self.GetLine()
                break
            
            """
            if self.subject:
                while not line.strip():
                    line = self.GetLine()
                
                if line.startswith('Attachments:'):
                #lineAfterSubject += 1
                    continue
                else:
                    while line:
                        self.Message += line
                        line = self.GetLine()
            """   
            line = self.GetLine()
            
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
                        
                    manyValues.append((self.DocID, self.fromEmail, email, self.sentReceivedDate, self.subject, self.attachments, filePath, self.attachmentsPaths, len(self.toEmails), 0, 0, 'N/A', self.Message))    
                    msg = Classes.EmailMessage()
                    msg.Sender = self.fromEmail
                    msg.Recipient = email
                    msg.Date = self.sentReceivedDate
                    msg.Subject = self.subject
                    msg.Attachments = self.attachments
                    msg.Size = 0
                    msg.TotalRecipients = len(self.toEmails)
                    msg.Group = 0
                    msg.filePath = filePath
                    msg.attachmentsPaths = self.attachmentsPath
                    if Globals.MessageDict.has_key(self.sentReceivedDate.lower()):
                        Globals.MessageDict[self.sentReceivedDate.lower()].append(msg)
                    else:
                        Globals.MessageDict[self.sentReceivedDate.lower()] = [msg]
            if db:
                values = tuple(self.toEmails)
                
                db.ExecuteMany(self.query, manyValues)
                db.ExecuteMany(self.query1, self.NewAccounts)
                
            """    
            print 'filePath ', filePath, " From: ", self.fromEmail
            print 'To: ', self.toEmails
            print " Date: ", self.sentReceivedDate, " Subject: ", self.subject, " Attachments: ", self.attachments
            """
            #update the database for each email
        
        for line in self.Message.split("\n"):
            self.handleLine(line)
        
        #add all phone numbers to database
        query = "insert into " + Constants.PhonesTable + "(Phone, DocID, Frequency) values (?,?,?)"
        manyValues = []
        for key in self.Phones:
            manyValues.append((key, self.DocID, self.Phones[key]['Count']))
            
        #print manyValues
        db.ExecuteMany(query, manyValues)
            
        
    def GetNamesTuple(self, fullName):
        names = fullName.split()
        firstName = ""
        middleName = ""
        lastName = ""
        if len(names) >= 1:
            firstName = names[0].lower().strip()
    
        if len(names) == 2:
            lastName = names[1].lower().strip()
            
        elif len(names) >= 3:
            middleName = names[1].lower().strip()
            lastName = names[2].lower().strip()
        return firstName, middleName, lastName
        
    def ProcessTo(self, line): #returns next unmatched line for processing in the main loop
        """
        if matchedRE.group(4): #there is an email address in to line
            if self.EmailRE.match(matchedRE.group(4)):
                self.toEmails.append(matchedRE.group(4).strip())
            else:
                self.toEmails.append(EmailUtilities.LookupEmailID(matchedRE.group(4).strip()))
        else: #no email address; so lookup address book
            self.toEmails.append(EmailUtilities.LookupEmailID(matchedRE.group(2).strip()))
            
        if matchedRE.group(6): #if there's a comma at the end of the line, there are more to's
            line = self.GetLine()
            #print "To: ", line
        """
        matched = self.ToNameOnlyRE.match(line)
        if matched:
            self.toEmails.append(EmailUtilities.LookupEmailID(matched.group(2).strip()))
        else:
            matched = self.ToEmailOnlyRE.match(line)
            if matched:
                self.toEmails.append(matched.group(2).strip())
            else:
                matched = self.ToNameAndEmail1RE.match(line)
                if matched:
                    if matched.group(4): #there is an email address in to line
                        if self.EmailRE.match(matched.group(4)):
                            self.toEmails.append(matched.group(4).strip())
                        else:
                            self.toEmails.append(EmailUtilities.LookupEmailID(matched.group(4).strip()))
                    else: #no email address; so lookup address book
                        self.toEmails.append(EmailUtilities.LookupEmailID(matched.group(2).strip()))
                else:
                    print 'Unmatched to line %s'%line
            
        line = self.GetLine()
        colonFound = line.find(":")
        if colonFound == -1:
            while line and colonFound == -1: #until no next : is found it is part of To:
                #print "To: ", line
                matched = self.ToNameOnlyRE.match(line)
                if matched:
                    self.toEmails.append(EmailUtilities.LookupEmailID(matched.group(2).strip()))
                else:
                    matched = self.ToEmailOnlyRE.match(line)
                    if matched:
                        self.toEmails.append(matched.group(2).strip())
                    else:
                        matched = self.ToNameAndEmail1RE.match(line)
                        if matched:
                            if matched.group(4): #there is an email address in to line
                                if self.EmailRE.match(matched.group(4)):
                                    self.toEmails.append(matched.group(4).strip())
                                else:
                                    self.toEmails.append(EmailUtilities.LookupEmailID(matched.group(4).strip()))
                            else: #no email address; so lookup address book
                                self.toEmails.append(EmailUtilities.LookupEmailID(matched.group(2).strip()))
                        else:
                            print 'unmatched to line %s'%line
                line = self.GetLine()
                #matched = self.CcRE.match(line)
                colonFound = line.find(":")
            return line
        else:
            return self.GetLine()

        
    def GetLine(self):
        line = ""
        achar = self.fin.readline(1)
        if not achar:
            return achar
        
        while achar and achar != '\n':
            line += achar
            achar = self.fin.readline(1)
        return line 

    def PrintEmails(self):
        for id in Globals.EmailsDict:
            print id, " -> ", Globals.EmailsDict[id]
   
   
    
        
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
    
    def handleLine(self, line):
        data = string.lower(line)
           
        phoneNums  = self.PhonePattern.search(data)
        if phoneNums:
            phoneList = phoneNums.groups()
            phone = ""
            for num in phoneList:
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
        if Globals.EmailsWordFrequency.has_key(word):
            Globals.EmailsWordFrequency[word]['count'] += 1
            self.WordCount += 1
        else:
            if word not in Globals.EmailsStopwords:
                self.WordCount += 1
                self.WordID += 1
                #print 'WordID ', self.WordID
                Globals.EmailsWordFrequency[word] = {'id': self.WordID, 'count' : 1}
        
        if not self.Stemmer:
            return
        #print 'stemmer'

        if Globals.EmailsStemmedWordFrequency.has_key(word):
            Globals.EmailsStemmedWordFrequency[word]['count'] += 1
            self.StemmedWordCount += 1
        else:
            if len(word) < 2:
                return
            if word not in Globals.EmailsStopwords:
                #if len(word) <=2:
                #    return
                word = self.Stemmer.stem(word, 0,len(word)-1) #Apply Porter Stemmer to each word
                if Globals.EmailsStemmedWordFrequency.has_key(word):
                    Globals.EmailsStemmedWordFrequency[word]['count'] += 1
                    self.StemmedWordCount += 1
                else:
                    self.StemmedWordCount += 1
                    self.StemmedWordID += 1
                    Globals.EmailsStemmedWordFrequency[word] = {'id' : self.StemmedWordID, 'count' : 1}
    
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
    EmailUtilities.SetupEmailsDB('Emails.db')
    Globals.AddressBookDict = {}
    #EmailUtilities.LoadAddressBookFromDB(Globals.AddressBookDict)
    
    dirName = r"..\test1"
    sums = [0, 1] # 0 files 1 directory so far
    #try:
    os.path.walk(dirName, ScanEmails, sums)
    #except Exception, value:
    #    print "Failed to walk directories. Error: %s"%(value)

    #for emailFile in os.listdir('..\EmailTest'):
        
    """
    parser.parse('sampleEmail1.txt', db)
    parser.parse('AttachmentEmail.txt', db)
    parser.PrintEmails()
    """
    



