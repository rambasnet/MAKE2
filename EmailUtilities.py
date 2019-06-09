#-----------------------------------------------------------------------------
# Name:        EmailUtilities.py
# Purpose:     
#
# Author:      Ram B. Basnet
#
# Created:     2007/10/31
# RCS-ID:      $Id: EmailUtilities.py,v 1.4 2008/03/17 04:18:38 rbasnet Exp $
# Copyright:   (c) 2006
# Licence:     All rights reserved.
# New field:   Whatever
#-----------------------------------------------------------------------------

import Globals
import os, os.path
import Constants
from SqliteDatabase import *
import Classes
import PlatformMethods


def LoadAddressBookFromDB(AddressBookDict):
    db = SqliteDatabase(Globals.EmailsFileName)
    if not db.OpenConnection():
        return
    
    #AddressBookDict = {}    
    query = "select ID, EmailID, FirstName, MiddleName, LastName, InBook from " + Constants.AddressBookTable + " order by ID;"
    rows = db.FetchAllRows(query)
    
    for row in rows:
        AddressBookDict[row[0]] = {'EmailID': row[1], 'FirstName':row[2], 'MiddleName':row[3], 'LastName':row[4], 'InBook':int(row[5])}
    
    db.CloseConnection()
    
def LookupEmailID(fullName):
    names = fullName.split()
    if not names:
        return fullName
    firstName = ""
    lastName = ""
    middleName = ""
    if len(names) >= 1:
        firstName = names[0].lower().strip()
    
    if not firstName:
        return fullName
    
    if len(names) == 2:
        lastName = names[1].lower().strip()
        
    elif len(names) >= 3:
        middleName = names[1].lower().strip()
        lastName = " ".join(names[2:]).lower().strip()
    

    emailID = fullName
    #print 'emailID ', emailID
    for key in Globals.AddressBookDict:
        firstNameMatched = False
        lastNameMatched = False
        middleNameMatched = False
        if (Globals.AddressBookDict[key]['FirstName'].lower() == firstName and Globals.AddressBookDict[key]['LastName'].lower() == 
            lastName and Globals.AddressBookDict[key]['MiddleName'].lower() == middleName):
                if Globals.AddressBookDict[key]['EmailID']:
                    emailID = Globals.AddressBookDict[key]['EmailID']
                    break
        if (Globals.AddressBookDict[key]['FirstName'].lower() == firstName and Globals.AddressBookDict[key]['LastName'].lower() == lastName):
            if Globals.AddressBookDict[key]['EmailID']:
                emailID = Globals.AddressBookDict[key]['EmailID']
        #print 'new emailID = ', emailID
        
    """
    if emailID == fullName:
        for key in Globals.AddressBookDict:
            if Globals.AddressBookDict[key]['EmailID'].find(fullName) ==0:
                emailID = Globals.AddressBookDict[key]['EmailID']
                break
    """ 
    return emailID

def LookupName(emailID):
    firstName = ""
    middleName = ""
    lastName = ""
    emailFound = False
    for key in Globals.AddressBookDict:
        if Globals.AddressBookDict[key]['EmailID'].lower() == emailID.lower():
            firstName = Globals.AddressBookDict[key]['FirstName']
            middleName = Globals.AddressBookDict[key]['MiddleName']
            lastName = Globals.AddressBookDict[key]['LastName']
            emailFound = True
            break
        
    if not emailFound:
        return None
    
    if middleName:
        return firstName + " " + middleName + " " + lastName
    else:
        return firstName + " " + lastName
    
    
def LoadEmailsFromDB(EmailDict):
    db = SqliteDatabase(Globals.EmailsFileName)
    if not db.OpenConnection():
        return
          
    query = "select FromID, ToID from " + Constants.EmailsTable + " order by FromID;"
    rows = db.FetchAllRows(query)
    #EmailDict = {}
    Globals.TotalEmails = len(rows)
    for row in rows:
        if not EmailDict.has_key(row[0].lower()):
            EmailDict[row[0].lower()] = {}
    
        if not EmailDict.has_key(row[1].lower()):
            EmailDict[row[1].lower()] = {}
                    
        if EmailDict[row[0].lower()].has_key(row[1].lower()):
            EmailDict[row[0].lower()][row[1].lower()]['Sent'] += 1
        else:
            EmailDict[row[0].lower()][row[1].lower()] = {'Sent': 1}
        
    db.CloseConnection()


#Function called to load messaged for displaying in the listview
def LoadMessagesFromDB(MessageDict):
    db = SqliteDatabase(Globals.EmailsFileName)
    if not db.OpenConnection():
        return
          
    query = "select FromID, ToID, EmailDate, Subject, Attachments, Size, TotalRecipients, `Group`, Label, DocID, FilePath, AttachmentsPath from " + Constants.EmailsTable + " order by EmailDate;"
    rows = db.FetchAllRows(query)
    
    #print 'query len ', len(rows)
    for row in rows:
        #totalAttachments = row[3].split(",")
        msg = Classes.EmailMessage()
        msg.Sender = row[0]
        msg.Recipient = row[1]
        msg.Date = row[2]
        msg.Subject = row[3]
        msg.Attachments = row[4]
        msg.Size = int(row[5])
        msg.TotalRecipients = int(row[6])
        msg.Group = int(row[7])
        msg.Label = row[8]
        msg.DocID = int(row[9])
        msg.filePath = row[10]
        msg.attachmentsPath = row[11]

        if MessageDict.has_key(row[2].lower()):
            MessageDict[row[2].lower()].append(msg)
        else:
            MessageDict[row[2].lower()] = [msg]
        
    #print 'msg dict ', len(MessageDict)
    db.CloseConnection()
    
    
def OrderEmailsToCentralEmail(CentralID, EmailDict, OrderedEmailDict, GroupEmailsDict):
    """
    CentralID: the email id under investigation
    EmailDict: All the emails
    OrderedEmailDict: This will contain the emails after them have been ordred around central id
    GroupEmailsDict: Dictionay with emails as keys contains the interesting email ids to find out the communication with central id
    """
    
    EmailsInfo = {}
    EmailsInfo['CentralEmailSent'] = 0
    EmailsInfo['CentralEmailReceived'] = 0
    
    CentralID = PlatformMethods.Encode(CentralID.lower().strip())
    
    #if not OrderedEmailDict.has_key(CentralID):
    OrderedEmailDict[CentralID] = {}
    
    checkWithGroup = False
    if len(GroupEmailsDict) > 0:
        checkWithGroup = True
    
    largestIndex = 1
    
    for fromEmail in EmailDict:
        if fromEmail == CentralID:
            index = 1
            for toEmail in EmailDict[fromEmail]:
                #if OrderedEmailDict[fromEmail].has_key(index):
                #    index += 1
                if toEmail != CentralID:
                    if checkWithGroup:
                        if GroupEmailsDict.has_key(toEmail):
                            #continue
                            #print 'to Email = ', toEmail
                            OrderedEmailDict[CentralID][index] = {'Email': toEmail, 'Sent':EmailDict[CentralID][toEmail]['Sent'], 'Received':0}
                            EmailsInfo['CentralEmailSent'] += EmailDict[CentralID][toEmail]['Sent']
                            index += 1
                    else:
                        #print 'first else'
                        OrderedEmailDict[CentralID][index] = {'Email': toEmail, 'Sent':EmailDict[CentralID][toEmail]['Sent'], 'Received':0}
                        EmailsInfo['CentralEmailSent'] += EmailDict[CentralID][toEmail]['Sent']
                        index += 1
                
            newIndex = index
            largestIndex = index
            for fromID in EmailDict:
                if fromID != CentralID:
                    if EmailDict[fromID].has_key(CentralID):
                        indexFound = False
                        for index in OrderedEmailDict[CentralID]:
                            if OrderedEmailDict[CentralID][index]['Email'] == fromID:
                                indexFound = True
                                #print 'EmailDict FromID', fromID, " ", EmailDict[fromID]
                                OrderedEmailDict[CentralID][index]['Received'] = EmailDict[fromID][CentralID]['Sent']
                                EmailsInfo['CentralEmailReceived'] += EmailDict[fromID][CentralID]['Sent']
                                break
                        if not indexFound:
                            if fromID != CentralID:
                                if checkWithGroup:
                                    if GroupEmailsDict.has_key(fromID):
                                        #continue
                                        #print 'toEmail fromID = ', fromID
                                        OrderedEmailDict[CentralID][newIndex] = {'Email': fromID, 'Sent':0, 'Received': EmailDict[fromID][CentralID]['Sent']}
                                        EmailsInfo['CentralEmailReceived'] += EmailDict[fromID][CentralID]['Sent']
                                        newIndex += 1
                                else:
                                    OrderedEmailDict[CentralID][newIndex] = {'Email': fromID, 'Sent':0, 'Received': EmailDict[fromID][CentralID]['Sent']}
                                    EmailsInfo['CentralEmailReceived'] += EmailDict[fromID][CentralID]['Sent']
                                    newIndex += 1
                                        
            largestIndex = newIndex               
        else: #just copy the rest as they are...
            OrderedEmailDict[fromEmail] = EmailDict[fromEmail]
            
    #bubble sort
    
    Emails = OrderedEmailDict[CentralID]
    #SortedEmails = {}
    #print Emails
    #PrintEmailDict(OrderedEmailDict)
    i = 0
    leastIndex = 1
    EmailsInfo['CentralMaxEmails'] = 0
    EmailsInfo['CentralMinEmails'] = 0
    
    for index in Emails:
        totalEmails = Emails[index]['Sent'] + Emails[index]['Received']
        maxIndex = index
        leastIndex = index
        for index1 in range(index, len(Emails)+1):
            if (Emails[index1]['Sent']+Emails[index1]['Received']) > (totalEmails):
                totalEmails = Emails[index1]['Sent']+Emails[index1]['Received']
                maxIndex = index1
        i += 1   
        #swap
        #print "largest index = %d and index= %d"%(largestIndex, index)
        #if index != largestIndex:
        if i == 1:
            EmailsInfo['CentralMaxEmails'] = totalEmails
            
        Email = Emails[index]['Email']
        Sent = Emails[index]['Sent']
        Received = Emails[index]['Received']
        
        Emails[index] = {'Email':Emails[maxIndex]['Email'], 'Sent': Emails[maxIndex]['Sent'], 'Received': Emails[maxIndex]['Received']}
        Emails[maxIndex] = {'Email':Email, 'Sent': Sent, 'Received': Received}
        leastIndex = maxIndex
        
    if Emails.has_key(leastIndex):
        EmailsInfo['CentralMinEmails'] = Emails[leastIndex]['Sent'] + Emails[leastIndex]['Received']

    
    
    if checkWithGroup:
        for email in GroupEmailsDict:
            emailFound = False
            for index in Emails:
                if email == Emails[index]['Email']:
                    emailFound = True
                    break
            if not emailFound:
                OrderedEmailDict[CentralID][largestIndex] = {'Email': email, 'Sent':0, 'Received':0}
                largestIndex += 1
                EmailsInfo['CentralMinEmails'] = 0
   
        
    OrderedEmailDict[CentralID] = Emails    
    return EmailsInfo
        #SortedEmails[index] = {'Email':Emails[largestIndex]['Email'], 'Sent': Emails[largestIndex]['Sent'], 'Received': Emails[largestIndex]['Received']}
    #OrderedEmailDict[CentralID] = SortedEmails

def PrintEmailDict(EmailDict):
    for fromEmail in EmailDict:
        print fromEmail, " -> ", EmailDict[fromEmail]
        
        
def GetCentralTotalEmails(CentralID, OrderedEmailDict):
    CentralID = CentralID.lower()
    if OrderedEmailDict.has_key(CentralID):
        CentralDict = OrderedEmailDict[CentralID.lower()]
        totalEmails = 0
        for id in CentralDict:
            totalEmails += CentralDict[id]['Sent'] + CentralDict[id]['Received']
        return totalEmails
    else:
        return 1
    
def SetupEmailsDB(emailFile, createNew=False):
    
    if createNew:
        if os.path.exists(emaiFile):
            try:
                os.remove(emailFile)
            except:
                pass
        
    db = SqliteDatabase(emailFile)
    if not db.OpenConnection():
        return
        
    query = "DROP TABLE IF EXISTS " + Constants.AddressBookTable + ";"
    db.ExecuteNonQuery(query)
    
    query = "CREATE TABLE IF NOT EXISTS `" + Constants.AddressBookTable + "` ("
    query += "EmailID varchar(200), "
    query += "FirstName varchar(100), "
    query += "MiddleName varchar(50), "
    query += "LastName varchar(100), "
    query += "InBook int); "
    
    db.ExecuteNonQuery(query)
    
    #query = "DROP TABLE IF EXISTS " + Constants.EmailsTable + ";"
    #db.ExecuteNonQuery(query)
      
    db.ExecuteNonQuery("DROP TABLE IF EXISTS %s"%Constants.EmailsTable)
    
    query = "CREATE TABLE IF NOT EXISTS `" + Constants.EmailsTable + "` ("
    query += "DocID int NOT NULL, "
    query += "FromID varchar(200), "
    query += "ToID varchar(200), "
    query += "EmailDate DATETIME, "
    query += "Subject text,"
    query += "Attachments text,"
    query += "FilePath text,"
    query += "AttachmentsPath text, "
    query += "TotalRecipients int, "
    query += "Size int, "
    query += "`Group` int,"
    query += "Label text,"
    query += "Message text);"
    
    db.ExecuteNonQuery(query)
    
   
    query = """CREATE TABLE IF NOT EXISTS %s (
            Word varchar(500),
            StemmedWord varchar(500),
            Frequency int unsigned,
            IDF float)
            """%(Constants.WordsTable)
        
    db.ExecuteNonQuery(query)
    
    query = """CREATE INDEX IF NOT EXISTS WordIndex ON %s (Word);"""%(Constants.WordsTable)
    db.ExecuteNonQuery(query)
    
    query = """CREATE INDEX IF NOT EXISTS StemmedWordIndex ON %s (StemmedWord);"""%(Constants.WordsTable)
    db.ExecuteNonQuery(query)

    query = """CREATE TABLE IF NOT EXISTS %s (
            DocID INT UNSIGNED NOT NULL,
            WordID INT UNSIGNED NOT NULL,
            Location INT UNSIGNED NOT NULL,
            InPath INTEGER)
            """%(Constants.WordLocation)
    db.ExecuteNonQuery(query)
    

    query = """CREATE INDEX IF NOT EXISTS WordDocLocationIndex on %s(WordID);"""%(Constants.WordLocation)
    db.ExecuteNonQuery(query)
    
    query = """CREATE INDEX IF NOT EXISTS DocWordLocationIndex on %s(DocID);"""%(Constants.WordLocation)
    db.ExecuteNonQuery(query)
    
               
    query = """CREATE TABLE IF NOT EXISTS %s (
        DocPath text,
        DocType short)
        """%(Constants.DocumentsTable)
        
    #print query
    db.ExecuteNonQuery(query)
    
    query = """CREATE INDEX IF NOT EXISTS DocIndex ON %s(DocPath);"""%(Constants.DocumentsTable)
    db.ExecuteNonQuery(query)
    
    
    query = "CREATE TABLE IF NOT EXISTS " + Constants.StopwordsTable + " ( "
    query += "Stopword text )"
    db.ExecuteNonQuery(query)
    
    query = """CREATE INDEX IF NOT EXISTS StopwordIndex ON %s(Stopword);"""%(Constants.StopwordsTable)
    db.ExecuteNonQuery(query)
    
    query = "CREATE TABLE  IF NOT EXISTS " + Constants.PhonesTable + " ( "
    query += "Phone text, "
    query += "DocID numeric,"
    query += "`Frequency` numeric)"
    
    db.ExecuteNonQuery(query)
    
    query = """CREATE INDEX IF NOT EXISTS PhoneIndex ON %s(Phone);"""%(Constants.PhonesTable)
    db.ExecuteNonQuery(query)
    
    db.CloseConnection()

    
if __name__ == "__main__":
    EmailDict = {}
    OrderedEmailDict = {}
    LoadEmailsFromDB(EmailDict)
    #PrintEmailDict(EmailDict)
    GroupEmailsDict = {}
    emails = "montoya_s@aps.edu, william moffatt, mezzoario@aol.com, ram basnet, louanne boothe, debbie nygaard, sandra jenkins, irene johnson, angelj7@msn.com, foust, tatspatton@msn.com, norine romero, director's secret, parra_lm@aps.edu, patrick garcia vera dallas, aileen baca, travel, sking, talmager7@hotmail.com"
    emailsList = emails.split(",")
    for email in emailsList:
        GroupEmailsDict[email.strip()] = {}
    
    OrderEmailsToCentralEmail('montoya_y@aps.edu', EmailDict, OrderedEmailDict, GroupEmailsDict)
    #PrintEmailDict(OrderedEmailDict)
    print OrderedEmailDict['montoya_y@aps.edu']
    print 'Max emails ', Globals.CentralMaxEmails
    print 'Min emails ', Globals.CentralMinEmails
    print 'Total Emails ', Globals.CentralEmailSent + Globals.CentralEmailReceived
    
    print 'Total actual = ', len(GroupEmailsDict)
    print 'Total comm for Montotya = ', len(OrderedEmailDict['montoya_y@aps.edu'])
    #print 'len emaildict =%d'%len(EmailDict)
    #print 'len orderdict =%d'%len(OrderedEmailDict)