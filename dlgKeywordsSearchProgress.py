#-----------------------------------------------------------------------------
# Name:        dlgTextPreprocessingProgress.py
# Purpose:     
#
# Author:      Ram B. Basnet
#
# Created:     2007/11/12
# Modified:    7/24/2009
# RCS-ID:      $Id: dlgTextPreprocessingProgress.py,v 1.8 2008/03/17 04:18:38 rbasnet Exp $
# Copyright:   (c) 2009
# Licence:     All Rights Reserved.
# New field:   Whatever
#-----------------------------------------------------------------------------
#Boa:MDIChild:dlgKeywordsSearchProgress

import wx
import time
import re, string
import os.path, sys, os
#import wx.lib.delayedresult as delayedresult
import wx.lib.newevent
import  thread
import pp

from SqliteDatabase import *
import Globals
import Constants
import CommonFunctions
import DBFunctions
import Classes
import PlatformMethods
from PorterStemmer import *
import TextParser
import HTMLParser
import MSOfficeToText
import PDFToText
import images
import DocxParser
import DocParser
import SGMLParser
import BloomFilter
import pyPdf

def create(parent):
    return dlgKeywordsSearchProgress(parent)

[wxID_DLGKEYWORDSSEARCHPROGRESS, wxID_DLGKEYWORDSSEARCHPROGRESSBTNCANCEL, 
 wxID_DLGKEYWORDSSEARCHPROGRESSBTNOK, 
 wxID_DLGKEYWORDSSEARCHPROGRESSLBLELAPSEDTIME, 
 wxID_DLGKEYWORDSSEARCHPROGRESSLBLFILESCOUNT, 
 wxID_DLGKEYWORDSSEARCHPROGRESSLBLSCANSTATUS, 
 wxID_DLGKEYWORDSSEARCHPROGRESSLBLSTARTTIME, 
 wxID_DLGKEYWORDSSEARCHPROGRESSLBLTOTALDIR, 
 wxID_DLGKEYWORDSSEARCHPROGRESSPANSCANSTATUS, 
 wxID_DLGKEYWORDSSEARCHPROGRESSSTATICTEXT1, 
 wxID_DLGKEYWORDSSEARCHPROGRESSSTATICTEXT3, 
 wxID_DLGKEYWORDSSEARCHPROGRESSSTATICTEXT4, 
 wxID_DLGKEYWORDSSEARCHPROGRESSSTATICTEXT5, 
] = [wx.NewId() for _init_ctrls in range(13)]

#----------------------------------------------------------------------

# This creates a new Event class and a EVT binder function
(UpdateLabelEvent, EVT_UPDATE_LABEL) = wx.lib.newevent.NewEvent()


#----------------------------------------------------------------------

[wxID_DLGKEYWORDSSEARCHPROGRESSTIMER1] = [wx.NewId() for _init_utils in range(1)]

class dlgKeywordsSearchProgress(wx.Dialog):
    def _init_utils(self):
        # generated method, don't edit
        self.timer1 = wx.Timer(id=wxID_DLGKEYWORDSSEARCHPROGRESSTIMER1,
              owner=self)
        self.Bind(wx.EVT_TIMER, self.OnTimer1Timer,
              id=wxID_DLGKEYWORDSSEARCHPROGRESSTIMER1)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_DLGKEYWORDSSEARCHPROGRESS,
              name=u'dlgKeywordsSearchProgress', parent=prnt, pos=wx.Point(556,
              314), size=wx.Size(559, 291), style=0,
              title=u'Keywords Search Progress')
        self._init_utils()
        self.SetClientSize(wx.Size(551, 257))
        self.SetAutoLayout(True)
        self.SetBackgroundColour(wx.Colour(125, 152, 221))
        self.SetCursor(wx.STANDARD_CURSOR)
        self.SetMinSize(wx.Size(-1, -1))
        self.Center(wx.BOTH)
        self.Bind(wx.EVT_CLOSE, self.OnDlgTextPreprocessingProgressClose)

        self.panScanStatus = wx.Panel(id=wxID_DLGKEYWORDSSEARCHPROGRESSPANSCANSTATUS,
              name=u'panScanStatus', parent=self, pos=wx.Point(16, 16),
              size=wx.Size(520, 184), style=wx.TAB_TRAVERSAL)
        self.panScanStatus.SetBackgroundColour(wx.Colour(225, 236, 255))

        self.lblStartTime = wx.StaticText(id=wxID_DLGKEYWORDSSEARCHPROGRESSLBLSTARTTIME,
              label=u'Start Time', name=u'lblStartTime',
              parent=self.panScanStatus, pos=wx.Point(104, 88),
              size=wx.Size(136, 13), style=0)

        self.staticText3 = wx.StaticText(id=wxID_DLGKEYWORDSSEARCHPROGRESSSTATICTEXT3,
              label=u'Elapsed Time:', name='staticText3',
              parent=self.panScanStatus, pos=wx.Point(16, 160), size=wx.Size(82,
              13), style=wx.ALIGN_RIGHT)

        self.lblElapsedTime = wx.StaticText(id=wxID_DLGKEYWORDSSEARCHPROGRESSLBLELAPSEDTIME,
              label=u'0 s', name=u'lblElapsedTime', parent=self.panScanStatus,
              pos=wx.Point(104, 160), size=wx.Size(14, 13), style=0)

        self.lblTotalDir = wx.StaticText(id=wxID_DLGKEYWORDSSEARCHPROGRESSLBLTOTALDIR,
              label=u'0', name=u'lblTotalDir', parent=self.panScanStatus,
              pos=wx.Point(104, 112), size=wx.Size(40, 13), style=0)

        self.staticText4 = wx.StaticText(id=wxID_DLGKEYWORDSSEARCHPROGRESSSTATICTEXT4,
              label=u'Directories Count:', name='staticText4',
              parent=self.panScanStatus, pos=wx.Point(8, 112), size=wx.Size(87,
              16), style=wx.ALIGN_RIGHT)

        self.staticText5 = wx.StaticText(id=wxID_DLGKEYWORDSSEARCHPROGRESSSTATICTEXT5,
              label=u'Files Count:', name='staticText5',
              parent=self.panScanStatus, pos=wx.Point(8, 136), size=wx.Size(89,
              13), style=wx.ALIGN_RIGHT)

        self.lblFilesCount = wx.StaticText(id=wxID_DLGKEYWORDSSEARCHPROGRESSLBLFILESCOUNT,
              label=u'0', name=u'lblFilesCount', parent=self.panScanStatus,
              pos=wx.Point(104, 136), size=wx.Size(6, 13), style=0)

        self.lblScanStatus = wx.StaticText(id=wxID_DLGKEYWORDSSEARCHPROGRESSLBLSCANSTATUS,
              label=u'Done Keywords Search!', name=u'lblScanStatus',
              parent=self.panScanStatus, pos=wx.Point(152, 48),
              size=wx.Size(155, 16), style=0)
        self.lblScanStatus.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, u'MS Shell Dlg 2'))
        self.lblScanStatus.SetForegroundColour(wx.Colour(255, 0, 0))
        self.lblScanStatus.Show(True)

        self.btnOK = wx.Button(id=wxID_DLGKEYWORDSSEARCHPROGRESSBTNOK,
              label=u'&OK', name=u'btnOK', parent=self, pos=wx.Point(224, 216),
              size=wx.Size(88, 24), style=0)
        self.btnOK.Show(False)
        self.btnOK.Bind(wx.EVT_BUTTON, self.OnBtnOKButton,
              id=wxID_DLGKEYWORDSSEARCHPROGRESSBTNOK)

        self.btnCancel = wx.Button(id=wxID_DLGKEYWORDSSEARCHPROGRESSBTNCANCEL,
              label=u'&Cancel', name=u'btnCancel', parent=self,
              pos=wx.Point(224, 216), size=wx.Size(88, 24), style=0)
        self.btnCancel.Bind(wx.EVT_BUTTON, self.OnBtnCancelButton,
              id=wxID_DLGKEYWORDSSEARCHPROGRESSBTNCANCEL)

        self.staticText1 = wx.StaticText(id=wxID_DLGKEYWORDSSEARCHPROGRESSSTATICTEXT1,
              label=u'Start Time:', name='staticText1',
              parent=self.panScanStatus, pos=wx.Point(8, 88), size=wx.Size(88,
              13), style=wx.ALIGN_RIGHT)

    def __init__(self, parent):
        
        self._init_ctrls(parent)
        self.SetIcon(images.getMAKE2Icon())
        
        self.InitThrober()
        self.Bind(EVT_UPDATE_LABEL, self.OnUpdate)
        self.lblScanStatus.SetLabel("Keywords Search in Progress...")
        self.StartTime = 0
        self.scanStarted = False
        #self.ReadFilePropertiesToGet()
        self.jobID = 0
        self.StartTimer()
        #return
        self.ScanFinished = False
        # tuple of all parallel python servers to connect with
        ppservers = ()
        #ppservers = ("localhost",)
        # Creates jobserver with automatically detected number of workers
        #workers = 
        jobServer = pp.Server(ppservers=ppservers)
        self.scanThread = KeywordsSearchThread(self, self.StartTime, jobServer)
        self.scanThread.Start()
        
        
    def InitThrober(self):
        import  wx.lib.throbber as  throb
        import throbImages # this was created using a modified version of img2py
        # create the throbbers
        images = [throbImages.catalog[i].getBitmap()
                  for i in throbImages.index
                  if i not in ['eclouds', 'logo']]
                  
        self.throbber1 = throb.Throbber(self.panScanStatus, -1, images, frameDelay=0.07,
              pos=wx.Point(248, 8), size=wx.Size(36, 36))
        self.throbber1.Start()
        
        
    def StartTimer(self):
        self.StartTime = time.time()
        self.timer1.Start(30000) #1/2 min
        self.lblStartTime.SetLabel(str(time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())))
        self.lblStartTime.Refresh()
        return None
    
       
        
    def OnUpdate(self, evt):
        self.lblTotalDir.SetLabel(PlatformMethods.Decode(evt.totalDir))
        self.lblElapsedTime.SetLabel(PlatformMethods.Decode(evt.elapsedTime))
        #self.lblFileName.SetLabel(PlatformMethods.Decode(evt.currentFileName))
        self.lblFilesCount.SetLabel(PlatformMethods.Decode(evt.filesCount))
        self.lblScanStatus.SetLabel(PlatformMethods.Decode(evt.scanStatus))
        if str(evt.scanStatus) == "Done Preprocessing/Indexing!":
            self.throbber1.Stop()
            self.btnOK.Show(True)
            self.btnCancel.Show(False)
            self.timer1.Stop()
        self.RefreshLabels()
        evt.Skip()

        
    def RefreshLabels(self):
        self.lblFilesCount.Refresh()
        self.lblTotalDir.Refresh()
        self.lblElapsedTime.Refresh()
        #self.lblScanStatus.Refresh()
        #self.lblFileName.Refresh()

        

    def OnBtnOKButton(self, event):
        #Globals.frmGlobalMainForm.ShowDirectoryTreeView()
        self.Close()

    def OnBtnCancelButton(self, event):
        dlg = wx.SingleChoiceDialog(self, 'Are you sure you want to cancel the scanning job?', 'Confirmation', ['Yes', 'No'])
        try:
            if dlg.ShowModal() == wx.ID_OK:
                selected = dlg.GetStringSelection()
                # Your code
                if selected == 'Yes':
                    self.timer1.Stop()
                    self.scanThread.Stop()
                    self.lblScanStatus.SetLabel("Scan Stopped by the user!")
                    #query = "delete from " + Constants.FileInfoTable
                    #db.ExecuteNonQuery(query)
                    self.Close()
        finally:
            dlg.Destroy()

            

    def OnDlgScanProgressClose(self, event):
        event.Skip()
            
    

    def OnTimer1Timer(self, event):
        ElapsedTime = CommonFunctions.ConvertSecondsToDayHourMinSec(time.time() - self.StartTime)
        self.lblTotalDir.SetLabel(PlatformMethods.Decode(self.scanThread.GetDirCount()))
        self.lblElapsedTime.SetLabel(PlatformMethods.Decode(ElapsedTime))
        #self.lblCurrentDir.SetLabel(PlatformMethods.Decode(evt.currentDir))
        #self.lblFileName.SetLabel(PlatformMethods.Decode(self.scanThread.GetCurrentFilePath()))
        self.lblFilesCount.SetLabel(PlatformMethods.Decode(self.scanThread.GetFilesCount()))
        timeElapsed = time.time() - self.scanThread.GetFileScanStartTime()
        if not self.scanThread.running:
            self.throbber1.Stop()
            if self.scanThread.fout:
                self.scanThread.fout.close()
                
            self.btnOK.Show(True)
            self.btnCancel.Show(False)
            self.timer1.Stop()
        
        self.RefreshLabels()
        event.Skip()

    def OnDlgTextPreprocessingProgressClose(self, event):
        busy = wx.BusyInfo("One moment please, gettng ready to close")
        wx.Yield()

        running = 1

        while self.scanThread.IsRunning():
            #running = 0
            #running = running + self.scanThread.IsRunning()
            self.scanThread.Stop()
            time.sleep(0.1)
            
        event.Skip()

        
    
class KeywordsSearchThread:
    def __init__(self, win, startTime, jobServer, rootPath=""):
        import HTMLParser
        self.win = win
        self.StartTime = startTime
        self.rootPath = rootPath
        self.DocID = 0
        self.WordID = 0
        self.StemmedWordID = 0
        self.DirCount = 0
        self.FilesCount = 0
        self.WordCount = 0
        self.StemmedWordCount = 0
        self.ElapsedTime = ""
        self.ParseStatus = "Keywords Search in Progress..."
        self.KeyColumnNames = ""
        self.lock = thread.allocate_lock()
        #DBFunctions.SetupSqliteKeywordsTables(Globals.KeywordsFileName)

        self.EventStart = time.time()
        self.jobServer = jobServer
           
        self.FileScanStartTime = time.time()
        self.fout = None

        
    def Start(self):
        #self.timerStatus.Start(1000000)
        self.keepGoing = self.running = True
        #thread.start_new_thread(self.Run, ())
        self.Run()
        
        
    def Stop(self):
        self.keepGoing = False
        #db.CloseConnection()
        
    """
    def OnTimerStatusTimer(self, event):
        self.SendEvent()
        event.Skip()
    """   
        
    def IsRunning(self):
        return self.running
    
    def GetNewDocID(self):
        self.lock.acquire()
        self.DocID += 1
        self.lock.release()
        return self.DocID
    
    
    def GetFileInfo(self, db, docID):
        #returns full filepath and mimetype
        query = "select DirPath, Name, NewPath, MimeType from Evidence1 where rowid=?"
        row = db.FetchOneRow(query, [(docID),])
        if row:
            if row[2]:
                return os.path.join(PlatformMethods.Decode(Globals.CasePath), PlatformMethods.Decode(row[2])), row[3]
            else:
                fullFilePath = os.path.join(PlatformMethods.Decode(row[0]), PlatformMethods.Decode(row[1]))
                if Globals.EvidencesDict[Globals.CurrentEvidenceID]['NewLocation']:
                    fullFilePath = fullFilePath.replace(Globals.EvidencesDict[Globals.CurrentEvidenceID]['Location'], Globals.EvidencesDict[Globals.CurrentEvidenceID]['NewLocation'])
                        
                return fullFilePath, row[3]
        else:
            return None
    
    def Run(self):
        #print Globals.TextCatCategoryList
        dbFileSystem = SqliteDatabase(Globals.FileSystemName)
        if not dbFileSystem.OpenConnection():
            return
        
        db = SqliteDatabase(Globals.KeywordsFileName)
        logFileName = PlatformMethods.Decode(os.path.join(Globals.CasePath, (Globals.KeywordsFileName[Globals.KeywordsFileName.rfind(os.sep)+1:] + '.log')))
        self.fout = open(logFileName, 'ab')
        if not db.OpenConnection():
            return
        
        totalCpus = self.jobServer.get_ncpus()
        DBFunctions.SetupSqliteKeywordsTables(Globals.KeywordsFileName, totalCpus)
        #docxParser = DocxParser.DocxParser(db, Globals.Stopwords, self.Stemmer)
        #docParser = DocParser.DocParser(db, Globals.Stopwords, self.Stemmer)
        #query = "insert into %s (DocPath) values (?)"%(Constants.TextCatDocumentsTable)
        #DocIDQuery = "select rowid from Evidence1 where Name=? and DirPath=?"
                
        dbFileID = 1
        #docID = 0
        cpuUsed = 0
        import KeywordsSearcher
        
        while cpuUsed < totalCpus:
            #for docID in range():
            docID = self.GetNewDocID()
            filePath, mimeType = self.GetFileInfo(dbFileSystem, docID)
            if mimeType in Globals.KeywordsSearchCategoryList:
                dbFileName = "%s%d"%(Globals.KeywordsFileName, dbFileID)
                #submit(self, func, args=(), depfuncs=(), modules=(), callback=None, callbackargs=(), group='default', globals=None)
                # args = DocID, KeywordsDict, filePath, dbFileName
                self.jobServer.submit(func=KeywordsSearcher.SearchKeywords, args=(docID, Globals.KeywordsDict, filePath, dbFileName), modules=("SqliteDatabase", "pyPdf", "PlatformMethods"), callback=self.CallbackFunction)
                cpuUsed += 1
                dbFileID += 1
            
            docID = self.GetNewDocID(newDocID)

        #wait for jobs in all groups to finish
        self.jobServer.wait()
    
    def CallbackFunction(self, dbFileName):
        """
        if not dbFileName:
            dbFileSystem = SqliteDatabase(Globals.FileSystemName)
            if not dbFileSystem.OpenConnection():
                return
        """
        while True:
            docID = self.GetNewDocID()
            filePath, mimeType = self.GetFileInfo(dbFileName, docID)
            if mimeType in Globals.KeywordsSearchCategoryList:
                #dbFileName = "%s%d"%(Globals.KeywordsFileName, dbFileID)
                #submit(self, func, args=(), depfuncs=(), modules=(), callback=None, callbackargs=(), group='default', globals=None)
                # args = DocID, KeywordsDict, filePath, dbFileName
                self.jobServer.submit(func=KeywordsSearcher.SearchKeywords, args=(docID, Globals.KeywordsDict, filePath, dbFileName), modules=("SqliteDatabase", "pyPdf", "PlatformMethods"), callback=self.CallbackFunction)
                break
            
        
    def SearchKeywords(self):           
        
        """
        if self.WordDict:
            self.ParseStatus = "Writing to database..."
            self.ElapsedTime = CommonFunctions.ConvertSecondsToDayHourMinSec(time.time() - self.StartTime)
            self.SendEvent()
            self.HandleWords(self.WordDict)
            self.WordDict = None
        """
        
        self.fout.close()
        db.CloseConnection()
        self.SendEvent()
        
        finishTime = time.time()
        self.ElapsedTime = CommonFunctions.ConvertSecondsToDayHourMinSec(finishTime - self.StartTime)
        self.ParseStatus = "Done Preprocessing/Indexing!"
        self.SendEvent()
        self.running = False

    """
    def HandleWords(self, WordDict):
        db = SqliteDatabase(Globals.KeywordsFileName)
        if not db.OpenConnection():
            return
        
        #print 'handling words'
        #print 'worddict len = ', len(WordDict)
        for word in WordDict:
            try:
                row = db.FetchOneRow("SELECT ROWID FROM %s WHERE Word=%s"%(Constants.WordsTable, db.SqlSQuote(word)))
                wordID = 1
                if row:
                    wordID = row[0]
                    #self.db.ExecuteNonQuery("UPDATE %s set Frequency = Frequency + %d where ROWID = %d"%(Constants.WordsTable, len(WordDict[word]), wordID))
                else:
                    stemmedWord = ""
                    if self.Stemmer:
                        stemmedWord = self.Stemmer.stem(word, 0, len(word)-1)
                        
                    query = "insert into %s (Word, StemmedWord, Frequency) values (?, ?, ?)"%(Constants.WordsTable)
                    wordID = db.InsertAutoRow(query, [word, stemmedWord, len(WordDict[word])])
                
                #WordDict[word][docID]['Location']
                for docID in WordDict[word]:
                    wordCount = len(WordDict[word][docID]['Location'])
                    for location in WordDict[word][docID]['Location']:
                        db.ExecuteNonQuery("insert into %s (DocID, WordID, Location, InPath) values (%d, %d, %d, %d)"%(Constants.WordLocation, docID, wordID, location, WordDict[word][docID]['InPath']))
                    
                db.ExecuteNonQuery("UPDATE %s set Frequency = Frequency + %d where ROWID = %d"%(Constants.WordsTable, wordCount, wordID))
                
            except:
                continue
            
        db.CloseConnection()
    """
        
    def SendEvent(self):
        evt = UpdateLabelEvent(elapsedTime = self.ElapsedTime, 
            filesCount = self.FilesCount, totalDir = self.DirCount,
            scanStatus = self.ParseStatus, currentFileName=self.filePath)
        wx.PostEvent(self.win, evt)
        self.EventStart = time.time()
        
    def GetDirCount(self):
        return self.DirCount
    
    def GetFilesCount(self):
        return self.FilesCount
    
    
    def GetCurrentFilePath(self):
        return self.filePath


    def GetFileScanStartTime(self):
        return self.FileScanStartTime

    def CreateBloomFilter(self):
        #m = no. of bits for vector
        #n = no. of elements or keys to support queries
        #k = no. of hash functions
        m = 500000
        n = 100000
        k = 4
        return BloomFilter.BloomFilter(n=n, m=m, k=k)
