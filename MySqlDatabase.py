import MySQLdb
import string

"""
    Class MySqlDB
"""

class MySqlDatabase:
    def __init__(self, hostName, userName, passWord, dbName="mysql"):
        """
            Constructor for MySqlDB
        """
        self.HostName = hostName
        self.UserName = userName
        self.PassWord = passWord
        self.DBName = dbName
        self.SqlCursor = None
        self.SqlConn = None
        
    def OpenConnection(self):
        success = False
        try:
            conn = MySQLdb.connect(self.HostName, 
                                  self.UserName, 
                                  self.PassWord,
                                  self.DBName)
            self.SqlConn = conn
            self.SqlCursor = self.SqlConn.cursor()
            success = True
        except MySQLdb.Error, e:
            success = False
            #    print "Error %d: %s" % (e.args[0], e.args[1])
            
        return success
            
    def CloseConnection(self):
        self.SqlCursor.close ()
        self.SqlConn.close ()
        return None
        
        
    def ExecuteNonQuery(self, query):
        self.SqlCursor.execute(query)
        self.SqlConn.commit()
        return None
    
    def ExecuteMany(self, query, values):
        self.SqlCursor.executemany(query, values)
        self.SqlConn.commit()
        return None
        
    def FetchOneRow(self, query):
        self.SqlCursor.execute (query)
        row = self.SqlCursor.fetchone ()
        return row
    
    def FetchAllRows(self, query):
        self.SqlCursor.execute (query)
        rows = self.SqlCursor.fetchall()
        return rows
    
    def SqlSQuote(self, strValue):
        strValue = str(strValue)
        newString = string.replace(strValue, '\'', '')
        newString = string.replace(newString, '\\', '\\\\')
        newString = "'" + newString + "'"
        return newString
    
        