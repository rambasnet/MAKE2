# class that holds file propertis  to read...

        
class CFICase:
    def __init__(self):

        self.ID = ""
        self.DisplayName = ""
        self.CreatedBy = ""
        self.DateTimestamp = ""
        self.Description = ""
        
        #TBD: Remove all these members from CFIClass? and put them in each individual 
        #modules settings?
    
        self.TotalDirectories = 0
        self.TotalFiles = 0
        
        self.MacStartTime = ""
        self.MacFinishTime = ""
        self.MacTotalTime = ""

        self.GetKeywordFrequencyCount = 1
        self.GetFileProperties = 1
        self.GetFileExtension = 1
        self.GetFileSize = 1
        self.GetCreatedTime = 1
        self.GetModifiedTime = 1
        self.GetAccessedTime = 1
        self.GetFileOwner = 0
        self.CaseSensitive = 1
        self.SearchInPrefix = 1
        self.SearchInSuffix = 1
        self.SearchInMiddle = 1

        
        self.DBHostName = "localhost" #default is localhost can use ip also
        self.DBUsername = "root" # default is root with admin priviledge
        self.DBPassword = "" #password for the username
        self.DBName = ""
        

class File:
    def __init__(self):
        self.Name = ""
        self.DirPath = "NULL"        
        self.Extension = "NULL"
        self.Category = "NULL"
        self.Size = 0
        self.Created = "NULL"
        self.Modified = "NULL"
        self.Accessed = "NULL"
        self.Owner = "NULL"
        self.MimeType = "NULL"
        self.Description = "NULL"
        #self.OpenCommand = "NULL"
        self.MD5 = "NULL"
        self.SHA1 = "NULL"
        self.SHA224 = "NULL"
        self.SHA256 = "NULL"
        self.SHA384 = "NULL"
        self.SHA512 = "NULL"
        self.NewPath = ""
        self.KnownFile = 0


        
class ImageFile:
    def __init__(self):
        #File.__init__(self)
        self.Name = "N/A"
        self.Thumbnail = "N/A"
        
    """
    def CopyFromFileInfo(self, File):
        self.DirPath = File.DirPath
        self.Name = File.Name
        self.Extension = File.Extension
        self.Category = File.Category
        self.Size = File.Size
        self.Created = File.Created
        self.Modified = File.Modified
        self.Accessed = File.Accessed
        #self.CDate = File.CDate
        #self.MDate = File.MDate
        #self.ADate = File.ADate
        self.Owner = File.Owner
        self.MimeType = File.MimeType
        self.Description = File.Description
        #self.OpenCommand = File.OpenCommand
        self.MD5 = File.MD5
        self.SHA1 = File.SHA1
        self.SHA224 = File.SHA224
        self.SHA256 = File.SHA256
        self.SHA384 = File.SHA384
        self.SHA512 = File.SHA512
    """
    
class EmailMessage:
    def __init__(self):
        self.DocID = 0
        self.Sender = "N/A"
        self.Recipient = "N/A"
        self.Attachments = "N/A"
        self.Date = "N/A"
        self.Subject = "N/A"
        self.Group = 0
        self.Size = 0
        self.TotalRecipients = 0
        self.Label = "N/A"
        self.filePath = ""
        self.attachmentsPaths = ""
        
        
        