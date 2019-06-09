# Written by Ram Basnet
#Don't use it; Use OutlookTextParser.py instead

import string, re
from SqliteDatabase import *
import Constants
#from BeautifulSoup import *
import Globals
import EmailUtilities

class ParseError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


class HeaderParser():
    def __init__(self, EmailsDict):
        #self.FileName = FileName
        #db = db
        self.FromNameOnlyRE = re.compile(r"\A(From:\W*)([A-Z\.\- _0-9]+)([ >]*)", re.I)
        self.FromEmailOnlyRE = re.compile(r"\A(From:\W*)([A-Z0-9\._%\-]+@[A-Z0-9\._%\-]+\.[A-Z]+)*([ >]*)", re.I)
        #self.FromRE = re.compile(r"\A(From:\W*)([A-Z.\- _0-9]+)*(<)*([A-Z0-9._%-]+@*[A-Z0-9._%-]+\.[A-Z]+)*(>)*", re.I)
        self.FromNameAndEmail1RE = re.compile(r"\A(From:\W*)([A-Z\.\- _0-9]+)([ <]+)([A-Z0-9\._%\-]+@[A-Z0-9\._%\-]+\.[A-Z]+)*([ >]+)", re.I)
        
        self.ToNameOnlyRE = re.compile(r"\A(To:\W*)([A-Z\.\- _0-9]+)([ >]*)([ ,;]*)", re.I)
        self.ToEmailOnlyRE = re.compile(r"\A(To:\W*)([A-Z0-9\._%\-]+@[A-Z0-9\._%\-]+\.[A-Z]+)*([ >]*)([ ,;]*)", re.I)
        self.ToNameAndEmail1RE = re.compile(r"\A(To:\W*)([A-Z\.\- _0-9]+)([ <]+)([A-Z0-9\._%\-]+@[A-Z0-9\._%\-]+\.[A-Z]+)*([ >]+)([ ,;]*)", re.I)
        #self.ToRE = re.compile(r"\A(To:\W*)(['A-Z.\- @%0-9_]+)*(<)*([A-Z0-9._%-]+@*[A-Z0-9._%-]+\.[A-Z]+)*(>)*([,;])*", re.I)
        
        #self.RestToRE = re.compile(r"([ \t])*(['A-Z.\- @%0-9]+)*(<)*([A-Z0-9._%-]+@*[A-Z0-9._%-]+\.[A-Z]+)*(>)*", re.I)
        self.RestToNameOnlyRE = re.compile(r"([ \t]*)('[A-Z\.\- _0-9]+)([ >]*)([ ,;]*)", re.I)
        self.RestToEmailOnlyRE = re.compile(r"\A(To:\W*)([A-Z0-9\._%\-]+@[A-Z0-9\._%\-]+\.[A-Z]+)*([ >]*)([ ,;]*)", re.I)
        self.RestToNameAndEmail1RE = re.compile(r"\A(To:\W*)([A-Z\.\- _0-9]+)([ <]+)([A-Z0-9\._%\-]+@[A-Z0-9\._%\-]+\.[A-Z]+)*([ >]+)([ ,;]*)", re.I)
        self.CcRE = re.compile(r"\A(Cc:\W*)(['A-Z.\- @%0-9]+)(<)*([A-Z0-9._%-]+@*[A-Z0-9._%-]+\.[A-Z]+)*(>)*([,;])*", re.I)
        self.BccRE = re.compile(r"\A(Bcc:\W*)(['A-Z.\- @%0-9]+)*(<)*([A-Z0-9._%-]+@*[A-Z0-9._%-]+\.[A-Z]+)*(>)*([,;])*", re.I)
        self.DateRE = re.compile(r'\A(Date:\W*)(.+)')
        self.SubjectRE = re.compile(r'\A(Subject:\W*)(.*)')
        self.AttachmentsRE = re.compile(r'\A(Attachments:\W*)(.*)')
        #self.FooterLineRE = re.compile(r'[_-]{2,}')
        #self.ListSepRE = re.compile(r'[~`!#$^&*()+=|\\{}\'"?><\[\],;]')
        #self.Splitter = re.compile(r'\W+', re.I)
        self.EmailRE = re.compile(r"[A-Z0-9._%-]+@[A-Z0-9._%-]+\.[A-Z]+", re.I)
        self.EmailsDict = EmailsDict
        self.query = "insert into " + Constants.EmailsTable + "(FromID,ToID,EmailDate,Subject,Attachments,FilePath) values (?,?,?,?,?,?)"
        self.query1 = "insert into " + Constants.AddressBookTable + "(EmailID, FirstName, MiddleName, LastName, InBook) values (?,?,?,?,?)"
        
    def parse(self, FileName, db):
        
        self.fin = open(FileName, "r")
        line = self.GetLine()
        self.fromEmail = ""
        self.toEmails = []
        self.sentReceivedDate = ""
        self.subject = ""
        self.attachments = ""
        lineAfterSubject = 0
        self.NewAccounts = []
        
        while line:
            
            line = line.strip()
            print line
            if lineAfterSubject > 3:
                break
            #print line
            #self.FromRE = re.compile(r"\A(From: )([A-Z.\- _0-9]+)(<)*([A-Z0-9._%-]+@[A-Z0-9._%-]+\.[A-Z]+)*(>)*", re.I)
            if line.startswith('From:'):
                lastCNIndex = line.rfind('CN=')
                if lastCNIndex > 0:
                    self.fromEmails = EmailUtilities.LookupEmailID(line.strip()[lastCNIndex+3:-1])
                else:
                    matched = self.FromNameOnlyRE(line)
                    if matched:
                        self.fromEmail = EmailUtilities.LookupEmailID(matched.group(2).strip())
                        
                    else:
                        matched = self.FromEmailOnlyRE(line)
                        if matched:
                            self.fromEmail = matched.group(2)
                        else:
                            matched = self.FromNameAndEmail1RE.match(line)
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
                                    #print "no email From: ", matched.group(2)
                                    self.fromEmail = EmailUtilities.LookupEmailID(matched.group(2).strip())
                                    #print "no email From: ", self.fromEmail
                            
                       
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
                    line = self.ProcessTo(matched)
                    continue
                
            if line.startswith('Bcc:'):
                #self.BccRE = re.compile(r"\A(Bcc: )(['A-Z.\- @%0-9]+)(<)*([A-Z0-9._%-]+@[A-Z0-9._%-]+\.[A-Z]+)*(>)*([,;])*", re.I)
                matched = self.BccRE.match(line)
                if matched:
                    #print line
                    line = self.ProcessTo(matched)
                    
                    continue
            if line.startswith('Date:'):
                #self.DateRE = re.compile(r'\A(Date: )(.+)')
                matched = self.DateRE.match(line)
                if matched:
                    #print "Date: ", line
                    self.sentReceivedDate = matched.group(2)
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
            if line.startswith('Attachments:'):
                #self.AttachmentsRE = re.compile(r'\A(Attachments: )(.*)')
                matched = self.AttachmentsRE.match(line)
                if matched:
                    #print "Subject: ", line
                    attachment = matched.group(2)
                    attachList = attachment.split(',')
                    while (attachList and len(attachList) > 1):
                        for attachment in attachList:
                            if attachment:
                                if self.attachments:
                                    self.attachments += ","
                                self.attachments += attachment
                        attachList = self.GetLine().split(',')
                    if attachList:
                        for attachment in attachList:
                            if attachment:
                                if self.attachments:
                                    self.attachments += ","
                            self.attachments += attachment
                    break
            
            if self.subject:
                lineAfterSubject += 1    
            
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
                    manyValues.append((self.fromEmail, email, self.sentReceivedDate, self.subject, self.attachments, FileName))    
            
            if db:
                values = tuple(self.toEmails)
                
                db.ExecuteMany(self.query, manyValues)
                db.ExecuteMany(self.query1, self.NewAccounts)
                
            """    
            print 'FileName ', FileName, " From: ", self.fromEmail
            print 'To: ', self.toEmails
            print " Date: ", self.sentReceivedDate, " Subject: ", self.subject, " Attachments: ", self.attachments
            """
            #update the database for each email
        
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
        colonFound = line.find(":")
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
                    
        
            matched = self.RestToRE.match(line)
            if matched:
                if matched.group(4): #there is an email address in to line
                    if self.EmailRE.match(matched.group(4)):
                        self.toEmails.append(matched.group(4).strip())
                    else:
                        self.toEmails.append(EmailUtilities.LookupEmailID(matched.group(4).strip()))
                else: #no email address; so lookup address book
                    self.toEmails.append(EmailUtilities.LookupEmailID(matched.group(2).strip()))
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
   
   
def SetupEmailDB():

    db = SqliteDatabase('Emails.db')
    if not db.OpenConnection():
        return
    
    query = "DROP TABLE IF EXISTS " + Constants.EmailsTable + ";"
    db.ExecuteNonQuery(query)
      
    query = "CREATE TABLE IF NOT EXISTS `" + Constants.EmailsTable + "` ("
    query += "FromID varchar(200), "
    query += "ToID varchar(200), "
    query += "EmailDate varchar(50), "
    query += "Subject text,"
    query += "Attachments text,"
    query += "FilePath text );"
    
    db.ExecuteNonQuery(query)
    
    db.CloseConnection()
    
def ScanEmails(sms, dirName, fileList):
    parser = HeaderParser(Globals.EmailsDict)
    db = SqliteDatabase('Emails.db')
    if not db.OpenConnection():
        sys.exit(0)
    #self.CurrentDirectory = dirName
    #manyValues = [] 
    #self.TotalFiles = len(fileList)
    #self.ElapsedTime = CommonFunctions.ConvertSecondsToDayHourMinSec(time.time() - self.StartTime)

    for fileName in fileList:
        emailFile = os.path.join(dirName, fileName)
        #if os.path.islink(fullFileName): continue
        if os.path.isfile(emailFile):
            sms[0] += 1
            parser.parse(emailFile, db)
    db.CloseConnection()      
    
if __name__ == "__main__":
    import os, sys
    SetupEmailDB()
    EmailUtilities.LoadAddressBookFromDB(Globals.AddressBookDict)
    
    dirName = "..\Montoya\Email"
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
    



