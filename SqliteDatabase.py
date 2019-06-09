import sqlite3 as sqlite
import string

"""
    Class SqliteDatabase
"""

class SqliteDatabase:
    def __init__(self, dbName):
        """
            Constructor for SqliteDatabase
        """
        self.DBName = dbName
        self.SqlCursor = None
        self.SqlConn = None
        
    def OpenConnection(self):
        success = False
        try:
            self.SqlConn = sqlite.connect(self.DBName)
            #self.SqlConn.text_factory = sqlite3.OptimizedUnicode #doesn't work...
            self.SqlConn.text_factory = str
            self.SqlCursor = self.SqlConn.cursor()
            success = True
        except Exception, value:
            success = False
            print "Error Opennning Connection on %s." % (self.DBName)
            
        return success
            
    def CloseConnection(self):
        try:
            self.SqlCursor.close()
            self.SqlConn.close()
        except:
            pass
        return None
        
    
    def InsertAutoRow(self, query, values):
        self.SqlCursor.executemany(query, values)
        self.SqlConn.commit()
        return self.SqlCursor.lastrowid
    
    
    """
    def InsertAutoRow(self, query):
        self.SqlCursor.execute(query)
        self.SqlConn.commit()
        return self.SqlCursor.lastrowid
    """
    
    def ExecuteNonQuery(self, query, data=()):
        self.SqlCursor.execute(query, data)
        self.SqlConn.commit()
        return None
    
    def ExecuteNonQueryBlob(self, query, values):
        self.SqlCursor.execute(query, values)
        self.SqlConn.commit()
        return None
    
    def ExecuteMany(self, query, valueList):
        self.SqlCursor.executemany(query, valueList)
        self.SqlConn.commit()
        return None
        
    def FetchOneRow(self, query, data=()):
        self.SqlCursor.execute(query, data)
        row = self.SqlCursor.fetchone()
        return row
    
    def FetchAllRows(self, query, data=()):
        self.SqlCursor.execute(query, data)
        rows = self.SqlCursor.fetchall()
        return rows
    

    def SqlSQuote(self, strValue):
        #strValue = unicode(strValue, 'utf-8', 'replace')
        return "'%s'"%(strValue.replace("'", "''"))
        #newString = string.replace(newString, '\\', '\\\\')
        #newString = "'" + newString + "'"
        #return newString
    
    
    def EncodeBlob(self, data):
        #return "'%s'" % sqlite.encode(data)
        return "'%s'" % sqlite.Binary(data)

         

"""
if __name__ == '__main__':
    myDB = SqliteDatabase("mytestdb.db")
    myDB.OpenConnection()
    query = CREATE TABLE `nmapports1` (
    `ID` integer primary key autoincrement,
    `HostIP` varchar(128) NOT NULL,
    `PortID` integer NOT NULL,
    `Protocol` varchar(10) NOT NULL,
    `State` varchar(20) NOT NULL,
    `ServiceName` varchar(100) NOT NULL,
    `Product` varchar(100) NULL,
    `Version` varchar(45) NULL
    );
    
    myDB.ExecuteNonQuery(query)
    myDB.CloseConnection()
"""