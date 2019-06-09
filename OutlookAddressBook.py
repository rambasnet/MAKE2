#-----------------------------------------------------------------------------
# Name:        OutlookAddressBook.py
# Purpose:     
#
# Author:      Ram B. Basnet
#
# Created:     2008/07/08
# RCS-ID:      $Id: OutlookAddressBook.py $
# Copyright:   (c) 2008
# Licence:     All Rights Reserved.
#-----------------------------------------------------------------------------

import string, re
from SqliteDatabase import *
import Constants
import Globals


class AddressBookParser():
    def __init__(self, AddressBookDict):
        #db = db
        self.EmailRE = re.compile('([\W]*)([A-Z0-9._%-]+@[A-Z0-9._%-]+\.[A-Z]+)([\W]*)', re.I)
        self.AddressBookDict = AddressBookDict
        
    def Parse(self, FileName):
        """
        db = SqliteDatabase(Globals.EmailsFileName)
        if not db.OpenConnection():
            return
        """
        self.fin = open(FileName, "rb")
        lines = self.fin.readlines()
        i = 0
        #values = []
        for line in lines[1:]:
            #ignore first line
            #if i== 0:
            #    i += 1
            #    continue
            items = line.split(",")
            #print len(items)
            #print items
            #for item in items:
            #may not always have 9 columns
            email = "" #try to find email from names
            firstName = ""
            middleName = ""
            lastName = ""
            if len(items) >=8:
                firstName = items[7].replace('"', '').strip()
                
            if len(items) >= 7:
                middleName = items[6].replace('"', '').strip()
                
            if len(items) >= 9:
                lastName = items[8].replace('"', '').strip()
                
            for item in items:
                matched = self.EmailRE.search(item.replace('"', '').strip())
                if matched:
                    email = matched.group(2)
                    break
                
            if not email: #no email format in individual column
                matched = self.EmailRE.search(firstName+lastName)
                if matched:
                    email = matched.group(2)
                
                if not email:
                    matched = self.EmailRE.search(firstName+middleName)
                    if matched:
                        email = matched.group(2)

                if not email:
                    matched = self.EmailRE.search(firstName+middleName+lastName)
                    if matched:
                        email = matched.group(2)
                if not email:
                    email = "%s %s %s"%(firstName, middleName, lastName)
                 
            if not email.strip() and not firstName.strip() and not middleName.strip() and not lastName.strip():
                continue
        
           
            self.AddressBookDict[i] = {'EmailID': email, 'FirstName': firstName, 'MiddleName': middleName, 'LastName': lastName, 'InBook':1}
            i += 1
            """
            #No need to add it here as addressbook values will be saved into database in dlgEmailPreprocessingProgres...
            query = "insert into %s (EmailID, FirstName, MiddleName, LastName, InBook) values (%s, %s, %s, %s, %d)"%(Constants.AddressBookTable,
                db.SqlSQuote(email.strip()), db.SqlSQuote(firstName.strip()), db.SqlSQuote(middleName.strip()), db.SqlSQuote(lastName.strip()), 1)
            try:
                db.ExecuteNonQuery(query)
            except:
                pass
            """
        self.fin.close()
        #db = SqliteDatabase('Emails.db')
        #if db.OpenConnection():
            #print "insert into " + Constants.AddressBookTable + "(EmailID, FirstName, MiddleName, LastName, InBook) values (?,?,?,?,?)", values
            
        
        #db.CloseConnection()
        
                
    def PrintAddressBook(self):
        for i in self.AddressBookDict:
           print "%s => %s %s %s"%(self.AddressBookDict[i]['EmailID'], self.AddressBookDict[i]['FirstName'], self.AddressBookDict[i]['MiddleName'], self.AddressBookDict[i]['LastName'], self.AddressBookDict[i]['InBook'])
            
    
    
def SetupAddressBookDB():

    db = SqliteDatabase('Emails.db')
    if not db.OpenConnection():
        return
        
    query = "DROP TABLE IF EXISTS " + Constants.AddressBookTable + ";"
    db.ExecuteNonQuery(query)
    
    query = "CREATE TABLE IF NOT EXISTS `" + Constants.AddressBookTable + "` ("
    query += "ID INTEGER PRIMARY KEY AUTOINCREMENT, "
    query += "EmailID varchar(200), "
    query += "FirstName varchar(100), "
    query += "MiddleName varchar(50), "
    query += "LastName varchar(100), "
    query += "InBook int); "
    
    db.ExecuteNonQuery(query)
    
   
    
    db.CloseConnection()
    
if __name__ == "__main__":
    import os
    """
    SetupAddressBookDB()
    parser = AddressBookParser()
    parser.Parse('Address.CSV')
    #parser.PrintAddressBook()
    """
    for root, dirs, files in os.walk("..\EmailTest"):
        print "root ", root
        for eachfile in files:
            print eachfile




