#-----------------------------------------------------------------------------
# Name:        Globals.py
# Purpose:     
#
# Author:      Ram Basnet
#
# Created:     2007/11/01
# RCS-ID:      $Id: Globals.py,v 1.9 2007/11/13 19:52:48 rbasnet Exp $
# Copyright:   (c) 2007
# Licence:     All Rights Reserved.
#-----------------------------------------------------------------------------

CurrentCase = None
CaseOpen = False
CurrentCaseFile = ""
CasePath = ""

MimeTypeSet = set([])

MACFileName = ""
FileSystemName = ""

CurrentEvidenceID = 'Evidence1'

#keep all the files in Memory

FilesDict = {}
FilesMimeTypesDict = {}

#DirectorySet = set([])
EvidencesDict = {}

frmGlobalMainForm = None
frmGlobalFileList = None
frmGlobalKeywords = None
frmGlobalTextCat = None
frmGlobalTimeline = None
frmGlobalEmails = None
frmGlobalImages = None
frmGlobalRegistry = None
frmGlobalLogs = None

fileTreeView = None
fileCategoryView = None

#Keywords Search
KeywordsFileName = ""
KeywordsSearchDirList = []
KeywordsSearchCategoryList = []
#KeywordsFrequency = {}
KeywordsDict = {}
#KeywordsSearchCaseSensitive = 1
#KeywordsSearchCaseInsensitive = 1

PropertiesRE = {}
    
# Globals for Text Categorization Modules
TextCatFileName = ""
FileExtensionList = set([])
Stopwords = set([])
BadChars = set([])
#BitMap = {}
#WordFrequency = {}
#StemmedWordFrequency = {}

TextCatDirList = []
TextCatCategoryList = []
Stemmer = ""
        
#Emails Stuff
EmailsFileName = ""
EmailsDict = {}
OrderedEmailDict = {}
AddressBookDict = {}
GroupEmailsDict = {}
TotalEmails = 0
CentralID = ""
CentralEmailSent = 0
CentralEmailReceived = 0
CentralMaxEmails = 0
CentralMinEmails = 0
#CentralTotalEmails = 0
MessageDict = {}
EmailsWordFrequency = {}
EmailsStemmedWordFrequency = {}
EmailsBitMap = {}
EmailsStopwords = set([])
AttachmentsCheckedMimes = []
#Images Stuff
ImagesFileName = ""
#ImagesDict = {}

#FileMimeTypes
#MimeTypesDict = {}

#Timelines stuff
TimelinesDict = {}

#CTimelineDict = {}
#MTimelineDict = {}
#ATimelineDict = {}
        