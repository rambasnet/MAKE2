import cPickle
import time

from SqliteDatabase import *
import Globals
import Constants
import DBFunctions
import CommonFunctions
Hashes = {}

import BloomFilter



def SplitNSRLDBIntoBuckets():
    db = SqliteDatabase(Constants.NSRLDBName)
    if not db.OpenConnection():
        return

    newDB = SqliteDatabase("NSRL.db")
    if not newDB.OpenConnection():
        return
    
    createQuery = "CREATE TABLE IF NOT EXISTS a%d (MD5 varchar(32) primary key);"
    query = "select distinct MD5 from " + Constants.NSRLFileTable + " ;"
    rows = db.FetchAllRows(query)
    i = 0
    #values = []
    for row in rows:
        dec = 0
        
        if i != 0:
            for ch in row[0]:
                dec += int(ch, 16)
                
            dec = dec%100
            
            if not Hashes.has_key(dec):
                #Hashes[dec].append(row[0])
                #print createQuery%dec
                newDB.ExecuteNonQuery(createQuery%dec)
                Hashes[dec] = ''
                #else:
                #Hashes[dec] = [row[0]]
                
            #values.append((row[0]))
            
            #if len(values)%10000 == 0:
            query = "insert into a%d (MD5) values ('%s');"%(dec, row[0])
            newDB.ExecuteNonQuery(query)
               
            
            
        i += 1
        
    """
    print 'hash length ', len(Hashes)
    count = 0
    for key in Hashes:
        count += len(Hashes[key])
        
        print 'length of bucket ', len(Hashes[key])
        
    print 'count ', count
    """
    db.CloseConnection()
    newDB.CloseConnection()
    
    
    
def CreateBloomFilter():
    db = SqliteDatabase(Constants.NSRLDBName)
    if not db.OpenConnection():
        return
    #m = no. of bits for vector
    #n = no. of elements or keys to support queries
    #k = no. of hash functions
    m = 10000000
    n = 1000000
    k = 4
    
    BFilter = BloomFilter.BloomFilter(n=n, m=m, k=k)
    
       
    db1 = SqliteDatabase("NSRLBloom.db")
    if not db1.OpenConnection():
        return
    
    query = """create table if not exists BloomFilter(
        BloomFilter blob);"""
    db1.ExecuteNonQuery(query)
    
    query = """SELECT name FROM sqlite_master
        WHERE type='table'
        ORDER BY name;
        """
    tables = db.FetchAllRows(query)
    #i = 0
    start = time.time()
    for table in tables:
        rows = db.FetchAllRows('select * from %s;'%table)
        for row in rows:
            BFilter.add(row[0])
            
        #break
        
    end = time.time()
    print 'time taken = ', CommonFunctions.ConvertSecondsToDayHourMinSec(end - start)  
    #db1.ExecuteMany('insert into BloomFilter (BloomFilter) values (?)', [(cPickle.dumps(BFilter))])
    db.CloseConnection()
    db1.CloseConnection()
    
def TestTime():
    db = SqliteDatabase(Constants.NSRLDBName)
    if not db.OpenConnection():
        return

    newDB = SqliteDatabase("NewNSRL.db")
    if not newDB.OpenConnection():
        return
    
    md5 = "8BA8BC04896C421A704282E9B87B5520"
    query = "select MD5 from " + Constants.NSRLFileTable + " where MD5= '%s' ;"%md5
    start = time.time()
    rows = db.FetchAllRows(query)
    if len(rows) > 0:
        print 'found'
    else:
        print 'not found'
        
    end = time.time()
    print 'elapsed time ', end-start
    
    start = time.time()
    
    bucketID = CommonFunctions.GetMD5HashBucketID(md5)
    query = "select MD5 from a%d where MD5='%s';"%(bucketID, md5)
    rows = newDB.FetchAllRows(query)
    if len(rows) > 0:
        print 'found'
    else:
        print 'not found'
        
    end = time.time()
    print 'bucket elapsed time ', end-start
    
if __name__ == "__main__":
    #SplitNSRLDBIntoBuckets()
    #TestTime()
    CreateBloomFilter()