#-----------------------------------------------------------------------------
# Name:        dlgTextPreprocessingProgress.py
# Purpose:     
#
# Author:      Ram B. Basnet
#
# Created:     2007/11/12
# RCS-ID:      $Id: dlgTextPreprocessingProgress.py,v 1.8 2008/03/17 04:18:38 rbasnet Exp $
# Copyright:   (c) 2006
# Licence:     <your licence>
# New field:   Whatever
#-----------------------------------------------------------------------------
#Boa:MDIChild:dlgTextPreprocessingProgress

import wx
import wx.lib.buttons
import time
import re, string
import os.path, sys, os
#import wx.lib.delayedresult as delayedresult
import wx.lib.newevent
import  thread
import binascii

from stat import *
import math
from wx.lib.anchors import LayoutAnchors

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

def create(parent, rootPath):
    return dlgTextPreprocessingProgress(parent, rootPath)

[wxID_DLGTEXTPREPROCESSINGPROGRESS, 
 wxID_DLGTEXTPREPROCESSINGPROGRESSBTNCANCEL, 
 wxID_DLGTEXTPREPROCESSINGPROGRESSBTNOK, 
 wxID_DLGTEXTPREPROCESSINGPROGRESSLBLELAPSEDTIME, 
 wxID_DLGTEXTPREPROCESSINGPROGRESSLBLFILENAME, 
 wxID_DLGTEXTPREPROCESSINGPROGRESSLBLFILESCOUNT, 
 wxID_DLGTEXTPREPROCESSINGPROGRESSLBLSCANSTATUS, 
 wxID_DLGTEXTPREPROCESSINGPROGRESSLBLSTARTTIME, 
 wxID_DLGTEXTPREPROCESSINGPROGRESSLBLTOTALDIR, 
 wxID_DLGTEXTPREPROCESSINGPROGRESSPANSCANSTATUS, 
 wxID_DLGTEXTPREPROCESSINGPROGRESSSTATICTEXT1, 
 wxID_DLGTEXTPREPROCESSINGPROGRESSSTATICTEXT2, 
 wxID_DLGTEXTPREPROCESSINGPROGRESSSTATICTEXT3, 
 wxID_DLGTEXTPREPROCESSINGPROGRESSSTATICTEXT4, 
 wxID_DLGTEXTPREPROCESSINGPROGRESSSTATICTEXT5, 
] = [wx.NewId() for _init_ctrls in range(15)]

#----------------------------------------------------------------------

# This creates a new Event class and a EVT binder function
(UpdateLabelEvent, EVT_UPDATE_LABEL) = wx.lib.newevent.NewEvent()


#----------------------------------------------------------------------

[wxID_DLGTEXTPREPROCESSINGPROGRESSTIMER1] = [wx.NewId() for _init_utils in range(1)]

class dlgTextPreprocessingProgress(wx.Dialog):
    def _init_utils(self):
        # generated method, don't edit
        self.timer1 = wx.Timer(id=wxID_DLGTEXTPREPROCESSINGPROGRESSTIMER1,
              owner=self)
        self.Bind(wx.EVT_TIMER, self.OnTimer1Timer,
              id=wxID_DLGTEXTPREPROCESSINGPROGRESSTIMER1)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_DLGTEXTPREPROCESSINGPROGRESS,
              name=u'dlgTextPreprocessingProgress', parent=prnt,
              pos=wx.Point(341, 190), size=wx.Size(916, 388), style=0,
              title=u'Text Preprocessing Status...')
        self._init_utils()
        self.SetClientSize(wx.Size(908, 354))
        self.SetAutoLayout(True)
        self.SetBackgroundColour(wx.Colour(125, 152, 221))
        self.SetCursor(wx.STANDARD_CURSOR)
        self.SetMinSize(wx.Size(-1, -1))
        self.Center(wx.BOTH)
        self.Bind(wx.EVT_CLOSE, self.OnDlgTextPreprocessingProgressClose)

        self.panScanStatus = wx.Panel(id=wxID_DLGTEXTPREPROCESSINGPROGRESSPANSCANSTATUS,
              name=u'panScanStatus', parent=self, pos=wx.Point(16, 16),
              size=wx.Size(872, 288), style=wx.TAB_TRAVERSAL)
        self.panScanStatus.SetBackgroundColour(wx.Colour(225, 236, 255))

        self.lblStartTime = wx.StaticText(id=wxID_DLGTEXTPREPROCESSINGPROGRESSLBLSTARTTIME,
              label=u'Start Time', name=u'lblStartTime',
              parent=self.panScanStatus, pos=wx.Point(96, 192),
              size=wx.Size(136, 13), style=0)

        self.staticText2 = wx.StaticText(id=wxID_DLGTEXTPREPROCESSINGPROGRESSSTATICTEXT2,
              label='Current File:', name='staticText2',
              parent=self.panScanStatus, pos=wx.Point(32, 80), size=wx.Size(60,
              13), style=wx.ALIGN_RIGHT)

        self.staticText3 = wx.StaticText(id=wxID_DLGTEXTPREPROCESSINGPROGRESSSTATICTEXT3,
              label=u'Elapsed Time:', name='staticText3',
              parent=self.panScanStatus, pos=wx.Point(8, 264), size=wx.Size(82,
              13), style=wx.ALIGN_RIGHT)

        self.lblElapsedTime = wx.StaticText(id=wxID_DLGTEXTPREPROCESSINGPROGRESSLBLELAPSEDTIME,
              label=u'0 s', name=u'lblElapsedTime', parent=self.panScanStatus,
              pos=wx.Point(96, 264), size=wx.Size(14, 13), style=0)

        self.lblTotalDir = wx.StaticText(id=wxID_DLGTEXTPREPROCESSINGPROGRESSLBLTOTALDIR,
              label=u'0', name=u'lblTotalDir', parent=self.panScanStatus,
              pos=wx.Point(96, 216), size=wx.Size(40, 13), style=0)

        self.staticText4 = wx.StaticText(id=wxID_DLGTEXTPREPROCESSINGPROGRESSSTATICTEXT4,
              label=u'Directories Count:', name='staticText4',
              parent=self.panScanStatus, pos=wx.Point(0, 216), size=wx.Size(87,
              16), style=wx.ALIGN_RIGHT)

        self.staticText5 = wx.StaticText(id=wxID_DLGTEXTPREPROCESSINGPROGRESSSTATICTEXT5,
              label=u'Files Count:', name='staticText5',
              parent=self.panScanStatus, pos=wx.Point(0, 240), size=wx.Size(89,
              13), style=wx.ALIGN_RIGHT)

        self.lblFilesCount = wx.StaticText(id=wxID_DLGTEXTPREPROCESSINGPROGRESSLBLFILESCOUNT,
              label=u'0', name=u'lblFilesCount', parent=self.panScanStatus,
              pos=wx.Point(96, 240), size=wx.Size(6, 13), style=0)

        self.lblScanStatus = wx.StaticText(id=wxID_DLGTEXTPREPROCESSINGPROGRESSLBLSCANSTATUS,
              label=u'Done Text Preprocessing and Indexing!',
              name=u'lblScanStatus', parent=self.panScanStatus,
              pos=wx.Point(152, 48), size=wx.Size(253, 16), style=0)
        self.lblScanStatus.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, u'MS Shell Dlg 2'))
        self.lblScanStatus.SetForegroundColour(wx.Colour(255, 0, 0))
        self.lblScanStatus.Show(True)

        self.btnOK = wx.Button(id=wxID_DLGTEXTPREPROCESSINGPROGRESSBTNOK,
              label=u'&OK', name=u'btnOK', parent=self, pos=wx.Point(408, 312),
              size=wx.Size(88, 24), style=0)
        self.btnOK.Show(False)
        self.btnOK.Bind(wx.EVT_BUTTON, self.OnBtnOKButton,
              id=wxID_DLGTEXTPREPROCESSINGPROGRESSBTNOK)

        self.btnCancel = wx.Button(id=wxID_DLGTEXTPREPROCESSINGPROGRESSBTNCANCEL,
              label=u'&Cancel', name=u'btnCancel', parent=self,
              pos=wx.Point(408, 312), size=wx.Size(88, 24), style=0)
        self.btnCancel.Bind(wx.EVT_BUTTON, self.OnBtnCancelButton,
              id=wxID_DLGTEXTPREPROCESSINGPROGRESSBTNCANCEL)

        self.staticText1 = wx.StaticText(id=wxID_DLGTEXTPREPROCESSINGPROGRESSSTATICTEXT1,
              label=u'Start Time:', name='staticText1',
              parent=self.panScanStatus, pos=wx.Point(0, 192), size=wx.Size(88,
              13), style=wx.ALIGN_RIGHT)

        self.lblFileName = wx.StaticText(id=wxID_DLGTEXTPREPROCESSINGPROGRESSLBLFILENAME,
              label='Current FileName', name='lblFileName',
              parent=self.panScanStatus, pos=wx.Point(104, 80),
              size=wx.Size(760, 104), style=wx.HSCROLL | wx.ST_NO_AUTORESIZE)

    def __init__(self, parent, rootPath):
        
        self._init_ctrls(parent)
        self.SetIcon(images.getMAKE2Icon())
        
        self.InitThrober()
        self.Bind(EVT_UPDATE_LABEL, self.OnUpdate)
        self.lblScanStatus.SetLabel("Indexing in Progress...")
        #db = SqliteDatabase(Globals.MACFileName)
        #db.OpenConnection()
        #self.rootPath = rootPath
        self.StartTime = 0
        self.scanStarted = False
        #self.ReadFilePropertiesToGet()
        self.jobID = 0
        self.StartTimer()
        #return
        self.ScanFinished = False
        self.scanThread = FileScanThread(self, self.StartTime, rootPath)
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
        self.lblFileName.SetLabel(PlatformMethods.Decode(evt.currentFileName))
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
        self.lblFileName.Refresh()

        

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
        self.lblFileName.SetLabel(PlatformMethods.Decode(self.scanThread.GetCurrentFilePath()))
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

        
    
class FileScanThread:
    def __init__(self, win, startTime, rootPath):
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
        self.ParseStatus = "Indexing in Progress..."
        self.KeyColumnNames = ""
        self.UseStemmer = False
        self.Stemmer = None
        #self.SetupTextCatDB()
        #DBFunctions.SetupTextCatTables(Globals.TextCatFileName)
        DBFunctions.SetupSqliteIndexTables(Globals.TextCatFileName)

        self.EventStart = time.time()
        if Globals.Stemmer == "Porter Stemmer":
            self.Stemmer = PorterStemmer()
            
        self.FileScanStartTime = time.time()
        self.fout = None

        
    def Start(self):
        #self.timerStatus.Start(1000000)
        self.keepGoing = self.running = True
        thread.start_new_thread(self.Run, ())
        #self.Run()
        
        
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
    
    def Run(self):
        #print Globals.TextCatCategoryList

        db = SqliteDatabase(Globals.TextCatFileName)
        logFileName = PlatformMethods.Decode(os.path.join(Globals.CasePath, (Globals.TextCatFileName[Globals.TextCatFileName.rfind(os.sep)+1:] + '.log')))
        self.fout = open(logFileName, 'ab')
        if not db.OpenConnection():
            return
        
        #self.bloomFilter = self.CreateBloomFilter()
        self.bloomFilter = None
        #self.htmlParser = HTMLParser.HTMLParser(self.Stemmer)   
        textParser = TextParser.TextParser(db, Globals.Stopwords, Stemmer=self.Stemmer, bloomFilter=self.bloomFilter)
        #self.WordDict = {}
        #print Globals.TextCatDirList
        docxParser = DocxParser.DocxParser(db, Globals.Stopwords, self.Stemmer)
        docParser = DocParser.DocParser(db, Globals.Stopwords, self.Stemmer)
        query = "insert into %s (DocPath) values (?)"%(Constants.TextCatDocumentsTable)
        
        
        self.filePath = ""
        for dirPath, dirs, files in os.walk(self.rootPath):
            self.DirCount += 1
            for afile in files:
                self.FileScanStartTime = time.time()
                self.FilesCount += 1
                """
                if (self.FilesCount % Globals.TotalFilesToHold) == 0 and self.WordDict:
                    self.ParseStatus = "Writing to database..."
                    self.ElapsedTime = CommonFunctions.ConvertSecondsToDayHourMinSec(time.time() - self.StartTime)
                    self.SendEvent()
                    self.HandleWords(self.WordDict)
                    self.ParseStatus = "Indexing in Progress..."
                    self.ElapsedTime = CommonFunctions.ConvertSecondsToDayHourMinSec(time.time() - self.StartTime)
                    self.SendEvent()
                    self.WordDict = {}
                """    
                if not self.keepGoing:
                    self.running = False
                    return
                
                self.filePath = os.path.join(dirPath, afile)
                try:
                    #print filePath
                    parsed = False
                    dotIndex = self.filePath.rfind('.')
                    extension = ""
                    if  dotIndex >= 0:
                        extension = self.filePath[dotIndex:]
                           
                        fileType = wx.TheMimeTypesManager.GetFileTypeFromExtension(extension)
                        if fileType:
                            mimeType = fileType.GetMimeType() or "unknown"
                            if Globals.TextCatCategoryList:
                                if mimeType not in Globals.TextCatCategoryList:
                                    
                                    self.FileScanStartTime = time.time()
                                    #self.fout.write('%s :'%(self.filePath))
                                    #query = "insert into %s (DocPath) values (?)"%(Constants.TextCatDocumentsTable)
                                    
                                    #default list of all the mime types doesn't seem to produce the mime type for
                                    # MS docx document
                                    if mimeType == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' or extension == '.docx':
                                        try:
                                            DocID = db.InsertAutoRow(query, [(PlatformMethods.Encode(self.filePath),)])
                                            #docID, filePath, startTime, logFile, extractMedia = False, MediaPath=""
                                            docxParser.Parse(DocID, self.filePath, self.FileScanStartTime, self.fout, extractMedia = False, MediaPath="")
                                            parsed = True
                                        except Exception, value:
                                            self.fout.write("Error in docxParser : %s Value: %s\n"%(self.filePath, value))
                                            #gives junk so let's not parse it using binary
                                            #parsed = True
                                            #docxParser.Parse(DocID, self.filePath, extractMedia = False, MediaPath="")
                                            
                                    curTime = time.time()
                                    self.ElapsedTime = CommonFunctions.ConvertSecondsToDayHourMinSec(curTime - self.StartTime)
                                                      
                                    #self.fout.write('%s\n'%(CommonFunctions.ConvertSecondsToDayHourMinSec(curTime - self.FileScanStartTime)))
                                    #self.fout.flush()
                                    
                                    if (curTime - self.EventStart) > 10:
                                        #print time.time() - self.EventStart
                                        self.ElapsedTime = CommonFunctions.ConvertSecondsToDayHourMinSec(curTime - self.StartTime)
                                        self.SendEvent()
                                        
                                    continue
                                else:
                                    pass
                                
                            #print filePath
                            self.FileScanStartTime = time.time()
                            #self.fout.write('%s :'%(self.filePath))
                            
                            DocID = db.InsertAutoRow(query, [(PlatformMethods.Encode(self.filePath),)])
                            #print 'mimeType ', mimeType
                            #print 'extension ', extension
                            if mimeType == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' or extension == '.docx':
                                try:
                                    #docID, filePath, startTime, logFile, extractMedia = False, MediaPath=""
                                    docxParser.Parse(DocID, self.filePath, self.FileScanStartTime, self.fout, extractMedia = False, MediaPath="")
                                    parsed = True
                                except Exception, value:
                                    #gives junk so let's not parse it using binary
                                    parsed = True
                                    self.fout.write("Error in docxParser : %s Value: %s\n"%(PlatformMethods.Encode(self.filePath), value))                                    
                                
                            elif mimeType == 'application/msword':
                                """
                                try:
                                    textParser.parse(DocID, MSOfficeToText.WordToText(self.filePath), self.filePath, self.FileScanStartTime, self.fout)
                                    parsed = True
                                except Exception, value:
                                    self.fout.write("Error in MSOfficeToText.WordToText : %s Value: %s\n"%(self.filePath, value))
                                """
                                try:
                                    #docID, filePath, startTime, logFile, extractMedia = False, MediaPath=""
                                    docParser.Parse(DocID, self.filePath, self.FileScanStartTime, self.fout, extractMedia = False, MediaPath="")
                                    parsed = True
                                except Exception, value:
                                    #gives junk so let's not parse it using binary
                                    self.fout.write("Error in DocParser : %s Value: %s\n"%(PlatformMethods.Encode(self.filePath), value))  
                                    
                            elif mimeType == 'application/pdf':
                                try:
                                    textParser.parse(DocID, PDFToText.GetText(self.filePath), self.filePath, self.FileScanStartTime, self.fout)
                                    parsed = True
                                except Exception, value:
                                    self.fout.write("Error in PDFToText: %s Value: %s\n"%(PlatformMethods.Encode(self.filePath), value))
                                    
                                
                            elif mimeType == 'text/plain':
                                try:
                                    fin = open(self.filePath, 'rb')
                                    #data = fin.read(4096)
                                    #while data:
                                    textParser.parse(DocID, fin.read(), self.filePath, self.FileScanStartTime, self.fout)
                                    parsed = True
                                    fin.close()
                                
                                except Exception, value:
                                    self.fout.write("Error in text/plain : %s Value: %s\n"%(PlatformMethods.Encode(self.filePath), value))
                                    
                                    
                            elif mimeType == 'text/html':
                                try:
                                    textParser.parse(DocID, HTMLParser.getText(self.filePath), self.filePath, self.FileScanStartTime, self.fout)
                                    parsed = True
                                except Exception, value:
                                    self.fout.write("Error in HTMLParser : %s Value: %s\n"%(PlatformMethods.Encode(self.filePath), value))
                                    
                                
                            elif mimeType == 'text/xml':
                                #db, docID, filePath, startTime, logFile, Stopwords=[], Stemmer=None)
                                try:
                                    sgmlParser = SGMLParser.SGMLXMLParser(db, DocID, self.filePath, self.FileScanStartTime, self.fout, Globals.Stopwords, self.Stemmer)
                                    fin = open(self.filePath, 'r')
                                    sgmlParser.feed(fin.read())
                                    sgmlParser.handleWords()
                                    fin.close()
                                    parsed = True
                                except Exception, value:
                                    self.fout.write("Error in SGMLXMLParser : %s Value: %s\n"%(PlatformMethods.Encode(self.filePath), value))
                                    
                                
                            elif mimeType.find('text') == 0:
                                #db, docID, filePath, startTime, logFile, Stopwords=[], Stemmer=None)
                                try:
                                    sgmlParser = SGMLParser.SGMLXMLParser(db, DocID, self.filePath, self.FileScanStartTime, self.fout, Globals.Stopwords, self.Stemmer)
                                    fin = open(self.filePath, 'rb')
                                    sgmlParser.feed(fin.read())
                                    sgmlParser.handleWords()
                                    fin.close()
                                    parsed = True
                                except Exception, value:
                                    self.fout.write("Error in SGMLXMLParser : %s Value: %s\n"%(PlatformMethods.Encode(self.filePath), value))
                                    
                            else:
                                try:
                                    #read everything else as binary file
                                    fin = open(self.filePath, 'rb')
                                    textParser.parse(DocID, fin.read(), self.filePath, self.FileScanStartTime, self.fout)
                                    fin.close()
                                    parsed = True
                                except Exception, value:
                                    self.fout.write("Error in binary text : %s Value: %s\n"%(PlatformMethods.Encode(self.filePath), value))
                                    parsed = True
                          
                        else:
                            parsed = True          
                    else:
                        parsed = True
                        
                    if not parsed:
                        try:
                            fin = open(self.filePath, 'rb')
                            textParser.parse(DocID, fin.read(), self.filePath, self.FileScanStartTime, self.fout)
                            fin.close()
                        except Exception, value:
                            self.fout.write("Error in binary text : %s Value: %s\n"%(PlatformMethods.Encode(self.filePath), value))
                            
                            
                    #self.ElapsedTime = CommonFunctions.ConvertSecondsToDayHourMinSec(curTime - self.StartTime)
                    curTime = time.time()
                    #self.fout.write('%s\n'%(CommonFunctions.ConvertSecondsToDayHourMinSec(curTime - self.FileScanStartTime)))
                    #self.fout.flush()
                    if (curTime - self.EventStart) > 10:
                        #print time.time() - self.EventStart
                        self.ElapsedTime = CommonFunctions.ConvertSecondsToDayHourMinSec(curTime - self.StartTime)
                        self.SendEvent()
                except Exception, value:
                    try:
                        #print "Error in Text Preprocessing: ", self.filePath, value
                        self.fout.write("Error in Text Preprocessing: %s Value: %s\n"%(PlatformMethods.Encode(self.filePath), value))
                    except:
                        #print "Error in Text Preprocessing..."
                        self.fout.write('Unknown Error in Text Preprocessing...\n')
                        #continue
                 
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
        db = SqliteDatabase(Globals.TextCatFileName)
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
