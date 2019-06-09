#-----------------------------------------------------------------------------
# Name:        Init.py
# Purpose:     
#
# Author:      Ram Basnet
#
# Created:     2007/11/01
# RCS-ID:      $Id: Init.py,v 1.6 2007/11/13 19:52:48 rbasnet Exp $
# Copyright:   (c) 2007
# Licence:     All Rights Reserved
# New field:   Whatever
#-----------------------------------------------------------------------------
import Constants
import Globals
import os.path
import DBFunctions


def InitGlobals():
    Globals.CurrentCase = None
    Globals.CaseOpen = False
    Globals.CurrentCaseFile = ""
    Globals.CasePath = ""

    Globals.MACFileName = ""
    Globals.FileSystemName = ""

    #keep all the files in Memory

    #Globals.FilesDict = {}
    #FilesMimeTypesDict = {}
    #Globals.DirectorySet = set([])
    Globals.EvidencesDict = {}

    Globals.frmGlobalFileList = None
    Globals.frmGlobalKeywords = None
    Globals.frmGlobalTextCat = None
    Globals.frmGlobalTimeline = None

    Globals.fileTreeView = None
    Globals.fileCategoryView = None
    Globals.frmGlobalImages = None
    Globals.frmGlobalRegistry = None
    Globals.frmGlobalLogs = None


    #Keywords Search
    Globals.KeywordsFileName = ""
    Globals.KeywordsSearchDirList = []
    Globals.KeywordsSearchCategoryList = []
    Globals.KeywordsFrequency = {}
    Globals.StemmedWordFrequency = {}
    Globals.Keywords = set()
    Globals.KeywordsSearchCaseSensitive = 1
    Globals.KeywordsSearchCaseInsensitive = 1

    Globals.PropertiesRE = {}
        
    # Globals for Text Categorization Modules
    Globals.TextCatFileName = ""
    Globals.FileExtensionList = set([])
    Globals.Stopwords = set([])
    Globals.BadChars = set([])
    Globals.BitMap = {}
    Globals.WordFrequency = {}
    Globals.TextCatDirList = []
    Globals.TextCatCategoryList = []
    Globals.Stemmer = ""
    
    Globals.EmailsFileName = ""
    Globals.EmailsDict = {}
    Globals.OrderedEmailDict = {}
    Globals.GroupEmailsDict = {}
    Globals.AddressBookDict = {}
    Globals.TotalEmails = 0
    Globals.CentralID = ""
    Globals.CentralEmailSent = 0
    Globals.CentralEmailReceived = 0
    Globals.frmGlobalEmails = None
    Globals.AttachmentsCheckedMimes = []
    
    Globals.ImagesFileName = ""
    #Globals.ImagesDict = {}
    
    #Globals.MimeTypesDict = {}
    Globals.MimeTypeSet = set([])
    
    #Timelines
    #Globals.TimelinesDict = {}
    #InitTimelines(Globals.TimelinesDict)

def InitAllDBFileNames():
    Globals.CasePath = os.path.dirname(Globals.CurrentCaseFile).encode('utf-8', 'replace')
    Globals.MACFileName = os.path.join(Globals.CasePath, Globals.CurrentCase.ID + Constants.MACExtension)
    Globals.FileSystemName = os.path.join(Globals.CasePath, Globals.CurrentCase.ID + Constants.FileSystemExtension)
    
    Globals.KeywordsFileName = os.path.join(Globals.CasePath, Globals.CurrentCase.ID + Constants.KeywordsExtension)
    #DBFunctions.SetupKeywordsTable(Globals.KeywordsFileName, True)
    Globals.TextCatFileName = os.path.join(Globals.CasePath, Globals.CurrentCase.ID + Constants.TextCatExtension)
    Globals.EmailsFileName = os.path.join(Globals.CasePath, Globals.CurrentCase.ID + Constants.EmailsExtension)
    Globals.ImagesFileName = os.path.join(Globals.CasePath, Globals.CurrentCase.ID + Constants.ImagesExtension)
    
#setup all the required database
def InitDatabases():
    #DBFunctions.SetupFileInfoDB(Globals.MACFileName)
    DBFunctions.CreateCaseEvidencesTable(Globals.CurrentCaseFile, True)
    #DBFunctions.SetupKeywordsTable(Globals.KeywordsFileName, True)
    DBFunctions.CreateStopwordsTable(Globals.TextCatFileName, True)
    #DBFunctions.SetupThumbnailsTable(Globals.ImagesFileName, True)
    
    
        