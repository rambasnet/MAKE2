from SqliteDatabase import *

if __name__ == "__main__":
    db = SqliteDatabase(r'C:\Documents and Settings\Ram\Desktop\MAKE2Test\TestMAKE\APSDC002.img')
    db.OpenConnection()
    rows = db.FetchAllRows('select DirPath from Evidence1 order by DirPath')
    for row in rows:
        print row[0]
    db.CloseConnection()
    

