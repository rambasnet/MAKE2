#-----------------------------------------------------------------------------
# Name:        DBFunctions.py
# Purpose:     
#
# Author:      Ram Basnet
#
# Created:     2007/11/10
# RCS-ID:      $Id: DBFunctions.py,v 1.11 2008/03/25 03:02:12 rbasnet Exp $
# Copyright:   (c) 2007
# Licence:     All Rights Reserved.
# New field:   Whatever
#-----------------------------------------------------------------------------
import string
#from MySqlDatabase import *
from SqliteDatabase import *
import Globals
import Constants
import PlatformMethods
import Classes
import cPickle
import CommonFunctions


def CreateCaseSettingsTable(CaseFileName):
    db = SqliteDatabase(CaseFileName)
    if not db.OpenConnection():
        return
        
    
    query = "CREATE TABLE IF NOT EXISTS `" + Constants.CaseSettingsTable + "` ("
    query += "ID text,"
    query += "DisplayName text, "
    query += "DateTimestamp text, "
    query += "Description text, "
    query += "CreatedBy text, "
    query += "MimeTypes text, "
    query += "`DBHostName` text, "
    query += "`DBUsername` text, "
    query += "`DBPassword` text, "
    query += "DBName text "
    query += ");"
    #query += "`GetKeywordFrequencyCount` integer, "
    #query += "`GetFileProperties` integer,"
    #query += "CaseSensitive integer,"
    #query += "SearchInPrefix integer,"
    #query += "SearchInSuffix integer,"
    #query += "SearchInMiddle integer,"
    #query += "GetFileExtension integer,"
    #query += "GetFileSize integer,"
    #query += "GetCreatedTime integer,"
    #query += "GetModifiedTime integer,"
    #query += "GetAccessedTime integer,"
    #query += "GetFileOwner integer, "
    #query += "MacStartTime text,"
    #query += "MacFinishTime text,"
    #query += "MacTotalTime text,"

    db.ExecuteNonQuery(query)
    
    
    
def CreateCaseEvidencesTable(CaseFileName, drop=True):
    db = SqliteDatabase(CaseFileName)
    if not db.OpenConnection():
        return
        
    if drop:
        query = "DROP TABLE IF EXISTS " + Constants.EvidencesTable
        db.ExecuteNonQuery(query)
        
    query = "CREATE TABLE IF NOT EXISTS `" + Constants.EvidencesTable + "` ("
    query += "`ID` text PRIMARY KEY, "
    query += "`DisplayName` text not null default 'N/A', "
    query += "`Location` text not null, "
    query += "Comment text not null default 'N/A',"
    query += "AddedBy text not null default 'N/A',"
    query += "AddedTimestamp text not null default 'N/A',"
    query += "GenMD5Hash integet not null default 1, "
    query += "GenSHA1Hash integer not null default 0, "
    query += "IgnoreKnownFile integer not null default 1, "
    query += "EntropyTest integer not null default 1, "
    query += "FullTextIndex integer not null default 1, "
    query += "DataCarve integer not null default 1, "
    query += "StoreThumbnails integer not null default 1,"
    query += "HTMLFileListing integer not null default 1,"
    query += "TotalFolders integer not null default 1,"
    query += "TotalFiles integer not null default 0,"
    query += "UnalocatedSpace integer not null default 0,"
    query += "TotalImages integer not null default 0,"
    query += "TotalEmails integer not null default 0,"
    query += "ScanStartTimestamp integer not null default 0,"
    query += "ScanEndTimestamp integer not null default 0"
    query += ");"
    db.ExecuteNonQuery(query)
    db.CloseConnection()

def GetCaseEvidences(fileName):
    db = SqliteDatabase(fileName)
    if not db.OpenConnection():
        return False
    query = "select ID, DisplayName, Location from " + Constants.EvidencesTable + ";"
    rows = db.FetchAllRows(query)
    
    for row in rows:
        Globals.EvidencesDict[row[0]] = {'DisplayName': row[1], 'Location':row[2]}
        
    
    
def GetCaseSettings(CaseFileName):
    db = SqliteDatabase(CaseFileName)
    if not db.OpenConnection():
        return False
    
    query = "select ID, DisplayName, DateTimestamp, CreatedBy, Description, "
    query += "DBHostName, DBUsername, DBPassword, DBName, MimeTypes from " + Constants.CaseSettingsTable + ";"
    
    rows = db.FetchAllRows(query)
    Globals.CurrentCase = Classes.CFICase()
    
    for row in rows:
        Globals.CurrentCase.ID = row[0]
        Globals.CurrentCase.DisplayName = row[1]
        Globals.CurrentCase.DateTimestamp = row[2]
        Globals.CurrentCase.CreatedBy = row[3]
        Globals.CurrentCase.Description = row[4]
        Globals.CurrentCase.DBHostName = row[5]
        Globals.CurrentCase.DBUsername = row[6]
        Globals.CurrentCase.DBPassword = row[7]
        Globals.CurrentCase.DBName = row[8]
        try:      
            Globals.MimeTypeSet = set(row[9].split("|"))
        except Exception, value:
            print "Failed to Load File System Database. Error: %s"%(value)
        
    db.CloseConnection()
    return True    
    
    
def CreateFileSystemTable(FileSystemName, tableName, drop=True):
    db = SqliteDatabase(FileSystemName)
    if not db.OpenConnection():
        return False
    
    
    if drop:
        query = "DROP TABLE IF EXISTS " + tableName
        db.ExecuteNonQuery(query)
    
    #for tableName in Constants.MACTables:
    query = """CREATE TABLE IF NOT EXISTS %s (
        Name text,
        DirPath text,
        Extension text, 
        Category text,
        Size float,
        Created number, 
        CDate number,
        CMonth number,
        Modified number, 
        MDate nuber,
        MMonth number,
        Accessed number, 
        ADate number,
        AMonth number,
        Owner text default 'None',
        MimeType text,
        Description text,
        MD5 text,
        SHA1 text default 'None',
        SHA224 text default 'None',
        SHA256 text default 'None',
        SHA384 text default 'None',
        SHA512 text default 'None',
        NewPath text default 'None',
        KnownFile Number,
        Export integer default 0)
        """%(tableName)
        
    db.ExecuteNonQuery(query)

    query = """CREATE INDEX IF NOT EXISTS FileNameIndex on %s(Name);"""%(tableName)
    db.ExecuteNonQuery(query)
        
        
    query = """CREATE INDEX IF NOT EXISTS MACDirPathIndex on %s(DirPath);"""%(tableName)
    db.ExecuteNonQuery(query)
    
    query = """CREATE INDEX IF NOT EXISTS ExtensionIndex on %s(Extension);"""%(tableName)
    db.ExecuteNonQuery(query)
    
    query = """CREATE INDEX IF NOT EXISTS MimeIndex on %s(MimeType);"""%(tableName)
    db.ExecuteNonQuery(query)
        
    query = """CREATE INDEX IF NOT EXISTS MDateIndex on %s(MDate);"""%(tableName)
    db.ExecuteNonQuery(query)
    
    query = """CREATE INDEX IF NOT EXISTS ADateIndex on %s(ADate);"""%(tableName)
    db.ExecuteNonQuery(query)
    
    query = """CREATE INDEX IF NOT EXISTS CDateIndex on %s(CDate);"""%(tableName)
    db.ExecuteNonQuery(query)
    
    query = """CREATE INDEX IF NOT EXISTS MMonthIndex on %s(MMonth);"""%(tableName)
    db.ExecuteNonQuery(query)
    
    query = """CREATE INDEX IF NOT EXISTS AMonthIndex on %s(AMonth);"""%(tableName)
    db.ExecuteNonQuery(query)
    
    query = """CREATE INDEX IF NOT EXISTS CMonthIndex on %s(CMonth);"""%(tableName)
    db.ExecuteNonQuery(query)
    
   
    table = "%s%s"%(tableName, Constants.DirListTable)
    if drop:
        query = """DROP TABLE IF EXISTS %s"""%(table)
        db.ExecuteNonQuery(query)
    
    query = """CREATE TABLE IF NOT EXISTS %s (
        DirPath text,
        SubDirList BLOB) """%table
    
    db.ExecuteNonQuery(query)
    
    query = """CREATE INDEX IF NOT EXISTS DirPathIndex on %s(DirPath);"""%(tableName)
    db.ExecuteNonQuery(query)
    
   
    db.CloseConnection()
    return True


def CreateMACTables(MACFileName, tableName, drop=True):
    db = SqliteDatabase(MACFileName)
    if not db.OpenConnection():
        return False
    

    query = """CREATE TABLE IF NOT EXISTS %s%s (
        MMinDate number,
        MMaxDate number,
        MMinMonth number,
        MMaxMonth number,
        AMinDate number,
        AMaxDate number,
        AMinMonth number,
        AMaxMonth number,
        CMinDate number, 
        CMaxDate number,
        CMinMonth number,
        CMaxMonth number) """%(tableName, Constants.MACRangeTable)
        
    db.ExecuteNonQuery(query)
    
    db.CloseConnection()
    return True

def LoadMACMinMaxValues():
    db = SqliteDatabase(Globals.MACFileName)
    if not db.OpenConnection():
        return False
    
    
    for evidenceID in Globals.EvidencesDict:
        query ="SELECT CMinDate, CMaxDate, CMinMonth, CMaxMonth, MMinDate, MMaxDate, MMinMonth, MMaxMonth, AMinDate, AMaxDate, AMinMonth, AMaxMonth from %s%s;"%(evidenceID, Constants.MACRangeTable)
        row = db.FetchOneRow(query)
        if not row:
            continue
        
        Globals.TimelinesDict['Created'] = {'MinDate': row[0], 'MaxDate': row[1], 'MinMonth': row[2], 'MaxMonth': row[3]}
        Globals.TimelinesDict['Modified'] = {'MinDate': row[4], 'MaxDate': row[5], 'MinMonth': row[6], 'MaxMonth': row[7]}
        Globals.TimelinesDict['Accessed'] = {'MinDate': row[8], 'MaxDate': row[9], 'MinMonth': row[10], 'MaxMonth': row[11]}
    
    
def UpdateDatabaseTables():
    db = SqliteDatabase(Globals.FileSystemName)
    if not db.OpenConnection():
        return False
    
    for evidenceID in Globals.EvidencesDict:
        try:
            row = db.FetchOneRow('select Export from %s'%evidenceID)
        except Exception, value:
            #print value
            query = "alter table %s add column Export integer default 0;"%evidenceID
            db.ExecuteNonQuery(query)
            
    db.CloseConnection()

    
def CreateKeywordsFrequencyTable(KeywordsFileName, drop=False):
    db = SqliteDatabase(KeywordsFileName)
    if not db.OpenConnection():
        return False
    
    if drop:
        query = "DROP TABLE IF EXISTS " + Constants.KeywordsFrequencyTable
        db.ExecuteNonQuery(query)
        
    query = "CREATE TABLE IF NOT EXISTS " + Constants.KeywordsFrequencyTable + " ( "
    query += "ID INTEGER PRIMARY KEY, "
    query += "FileName text"
    keycolumns = ""
    
    #print Globals.Keywords
    for keyword in Globals.Keywords:
        if keyword:
            keycolumns += "," + keyword + "_CI INTEGER"
            if Globals.CurrentCase.CaseSensitive:
                keycolumns += "," + keyword + "_CS INTEGER"
                    
    query += keycolumns
    query += " )"
   
    print query
    db.ExecuteNonQuery(query)
    db.CloseConnection()
    return True

  
def CreateStopwordsTable(TextCatFileName, drop=True):
    db = SqliteDatabase(TextCatFileName)
    if not db.OpenConnection():
        return False

    if drop:
        query = "DROP TABLE IF EXISTS " + Constants.StopwordsTable
        db.ExecuteNonQuery(query)
    
    query = "CREATE TABLE IF NOT EXISTS " + Constants.StopwordsTable + " ( "
    query += "ID INTEGER PRIMARY KEY, "
    query += "Stopword text )"
    
    db.ExecuteNonQuery(query)
    db.CloseConnection()
    return True


def CreateThumbnailsTable(ImagesFileName, tableName, drop=True):
    db = SqliteDatabase(ImagesFileName)
    if not db.OpenConnection():
        return False
    
    if drop:
        query = "DROP TABLE IF EXISTS " + tableName
        db.ExecuteNonQuery(query)
        
    query = """CREATE TABLE IF NOT EXISTS %s(
        DirPath text,
        Filename text, 
        Thumbnail BLOB )"""%(tableName)
        
    db.ExecuteNonQuery(query)
   
    query = """CREATE INDEX IF NOT EXISTS ImageDirPathIndex on %s(DirPath);"""%tableName
    db.ExecuteNonQuery(query)
    
    query = """CREATE INDEX IF NOT EXISTS ImageFileNameIndex on %s(Filename);"""%tableName
    db.ExecuteNonQuery(query)
    
    db.CloseConnection()
    return True



def SetupSqliteIndexTables(dbFileName):
    db = SqliteDatabase(dbFileName)
    if not db.OpenConnection():
        return
    
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
        DocPath text)
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

def GetImageFileList(fileName, tableName, dirPath, offset=0):
    db = SqliteDatabase(fileName)
    if not db.OpenConnection():
        return False
    
    query = query = """select Name, DirPath, Size, Created, Modified, Accessed, Category, MimeType, 
        Description, MD5,  KnownFile, NewPath, SHA1, SHA224, SHA256, SHA384, SHA512, Export
         from %s where DirPath = ? and Category = 'image' limit %d offset %d"""%(tableName, Constants.MaxObjectsPerPage, offset)

    #query = query%(tableName, "DirPath", dirPath, Constants.MaxObjectsPerPage, offset)
        
    #print query
    #row = db.FetchOneRow(query)
    #return db.FetchAllRows(query%(tableName, "DirPath", db.SqlSQuote(dirPath), Constants.MaxObjectsPerPage, offset))
    return db.FetchAllRows(query, (dirPath,))

def GetFileList(fileName, tableName, dirPath, offset=0, mimeType=False):
    db = SqliteDatabase(fileName)
    if not db.OpenConnection():
        return False
    
         
    if mimeType:
        query = query = """select Name, DirPath, Size, Created, Modified, Accessed, Category, MimeType, 
        Description, MD5,  KnownFile, NewPath, SHA1, SHA224, SHA256, SHA384, SHA512, Export
        from %s where MimeType = ? limit %d offset %d"""%(tableName, Constants.MaxObjectsPerPage, offset)
        #query = "select FileList from %s where MimeType = '%s' limit %d offset %d"%(tableName, dirPath, Constants.MaxObjectsPerPage, offset)
        #query = query%(tableName, "MimeType", db.SqlSQuote(dirPath), Constants.MaxObjectsPerPage, offset)
    else:
        query = query = """select Name, DirPath, Size, Created, Modified, Accessed, Category, MimeType, 
        Description, MD5,  KnownFile, NewPath, SHA1, SHA224, SHA256, SHA384, SHA512, Export
        from %s where DirPath = ? limit %d offset %d"""%(tableName, Constants.MaxObjectsPerPage, offset)
        
    #print query
    #row = db.FetchOneRow(query)
    return db.FetchAllRows(query, (dirPath,))
    """
    if row:
        return cPickle.loads(str(row[0]))
    else:
        return []
    """
    
def SetupSqliteKeywordsSettingsTables(dbFileName):
    db = SqliteDatabase(dbFileName)
    if not db.OpenConnection():
        return
    
    
    query = """CREATE TABLE IF NOT EXISTS %s (
        CaseInsensitive integer, CaseSensitive integer,
        CategoryList text, KeywordFreqFiles text)
        """%(Constants.KeywordsSettingsTable)
        
    db.ExecuteNonQuery(query)

    
    query = """CREATE TABLE IF NOT EXISTS %s (
            Keyword varchar(500) )
            """%(Constants.KeywordsTable)
        
    db.ExecuteNonQuery(query)
    
    query = """CREATE INDEX IF NOT EXISTS KeywordIndex ON %s (Keyword);"""%(Constants.KeywordsTable)
    db.ExecuteNonQuery(query)
    
    db.CloseConnection()


def SetupSqliteKeywordsTables(dbFileName, totalFiles):
    db = SqliteDatabase(dbFileName)
    if not db.OpenConnection():
        return
    
    query = """CREATE TABLE IF NOT EXISTS %s (
            Keyword varchar(500) )
            """%(Constants.KeywordsTable)
        
    db.ExecuteNonQuery(query)
    
    query = """CREATE INDEX IF NOT EXISTS KeywordIndex ON %s (Keyword);"""%(Constants.KeywordsTable)
    db.ExecuteNonQuery(query)
    
    db.CloseConnection()
    
    query = """CREATE TABLE IF NOT EXISTS %s (
            DocID INT UNSIGNED NOT NULL,
            KeywordID INT UNSIGNED NOT NULL,
            Frequency INT UNSIGNED NOT NULL,
            InPath INTEGER)
            """%(Constants.KeywordFrequencyTable)

    query1 = """CREATE INDEX IF NOT EXISTS KeywordDocFrequencyIndex on %s(KeywordID);"""%(Constants.KeywordFrequencyTable)
    for i in range(totalFiles):
        dbName = "%s%d"%(dbFileName, i+1)
        db = SqliteDatabase(dbName)
        if not db.OpenConnection():
            continue
    
        db.ExecuteNonQuery(query)
        db.ExecuteNonQuery(query1)
    
        db.CloseConnection()
        
if __name__=="__main__":
    #CreateDataBase("bla")
    #SetupCaseEvidencesTable("caseNew.cfi", True)
    SetupSqliteIndexTables('test.db')