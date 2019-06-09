#-----------------------------------------------------------------------------
# Name:        Constants.py
# Purpose:     
#
# Author:      Ram B. Basnet
#
# Created:     2007/11/10
# RCS-ID:      $Id: Constants.py,v 1.9 2007/11/13 19:52:48 rbasnet Exp $
# Copyright:   (c) 2006
# Licence:     <your licence>
# New field:   Whatever
#-----------------------------------------------------------------------------
#Read only constants

HostName = "localhost"
Username = "root"
Password = "strike0717"
DBName = "digitalforensic"

CaseNameExtension = ".cfi"
MACExtension = ".mac"
FileSystemExtension = ".bfs"
KeywordsExtension = ".key"
TextCatExtension = ".tce"
EmailsExtension = ".eml"
ImagesExtension = ".img"
NSRLDBName = r"Data\NSRL.db"
NSRLFileTable = "NSRLFile"
NSRLProdTable = "NSRLProd"
# Settings and Stopwords tables are in .cfi db file
CaseSettingsTable = "Settings"
EvidencesTable = "Evidences"

MACRangeTable = "MACRange"

FileInfoTable = "FileInfo"
DirListTable = "DirList"

#.key db has followng tables
KeywordsSettingsTable = "Settings"
KeywordsFrequencyTable = "KeywordsFrequency"
#KeywordsTable = "Keywords"


#in .tce text categorization extension file
StopwordsTable = "Stopwords"

#Text Cat tablenames
TextCatSettingsTable = "Settings"
TextCatDocumentsTable = "Documents"
#TextCatBagOfWordsTable = "BagOfWords"
TextCatWordLocation = "WordLocation"
#TextCatBagOfStemmedWordsTable = "BagOfStemmedWords"
TextCatWordsTable = "Words"
#TextCatStemmedWordsTable = "StemmedWords"
#TextCatBitMapIndex = "BitMapIndex"

SettingsTable = "Settings"

DocumentsTable = "Documents"
WordLocation = "WordLocation"
WordsTable = "Words"
KeywordsTable = "Keywords"
KeywordFrequencyTable = "KeywordFrequency"

#Evidence source Types..
PhysicalDrive = 0
LogicalDrive = 1
DiskDrive = 2
ImageFile = 3
FolderContents = 4

#Email Tables name
EmailsTable = "Emails"
AddressBookTable = "AddressBook"
PhonesTable = "Phones"
MessageDoc = 0
AttachmentDoc = 1

#Image tables
ImagesTable = "Images"
ThumbnailWidth = 100
ThumbnailHeight = 100

#Timelines
TimelineKeys = ['Created', 'Modified', 'Accessed']

MaxFileInfoToHold = 100
MaxThumbnailsToHold = 25

MaxObjectsPerPage = 25
MaxThumbnailsPerPage = 25

MaxUnzipFileSize = 10000000 #bytes = 10 MB

UnzipRootFolderName = 'Unzip'

