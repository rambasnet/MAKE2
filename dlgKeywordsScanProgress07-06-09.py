#-----------------------------------------------------------------------------
# Name:        dlgKeywordsScanProgress.py
# Purpose:     
#
# Author:      Ram Basnet
#
# Created:     2006/07/02
# Modified:    07/02/2009
# RCS-ID:      $Id: dlgKeywordsScanProgress.py $
# Copyright:   (c) 2006
# Licence:     <your licence>
# New field:   Whatever
#-----------------------------------------------------------------------------
#Boa:MDIChild:dlgKeywordsScanProgress

import wx
import wx.lib.buttons
import time
import re, string
import os.path, sys
#import wx.lib.delayedresult as delayedresult
import wx.lib.newevent
import  thread

from stat import *

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

def create(parent):
    return dlgKeywordsScanProgress(parent)

[wxID_DLGKEYWORDSSCANPROGRESS, wxID_DLGKEYWORDSSCANPROGRESSBTNCANCEL, 
 wxID_DLGKEYWORDSSCANPROGRESSBTNOK, 
 wxID_DLGKEYWORDSSCANPROGRESSLBLELAPSEDTIME, 
 wxID_DLGKEYWORDSSCANPROGRESSLBLFILESCOUNT, 
 wxID_DLGKEYWORDSSCANPROGRESSLBLSCANSTATUS, 
 wxID_DLGKEYWORDSSCANPROGRESSLBLSTARTTIME, 
 wxID_DLGKEYWORDSSCANPROGRESSLBLTOTALDIR, 
 wxID_DLGKEYWORDSSCANPROGRESSPANSCANSTATUS, 
 wxID_DLGKEYWORDSSCANPROGRESSSTATICTEXT2, 
 wxID_DLGKEYWORDSSCANPROGRESSSTATICTEXT3, 
 wxID_DLGKEYWORDSSCANPROGRESSSTATICTEXT4, 
 wxID_DLGKEYWORDSSCANPROGRESSSTATICTEXT5, 
] = [wx.NewId() for _init_ctrls in range(13)]

#----------------------------------------------------------------------

# This creates a new Event class and a EVT binder function
(UpdateLabelEvent, EVT_UPDATE_LABEL) = wx.lib.newevent.NewEvent()


#----------------------------------------------------------------------

class dlgKeywordsScanProgress(wx.Dialog):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_DLGKEYWORDSSCANPROGRESS,
              name=u'dlgKeywordsScanProgress', parent=prnt, pos=wx.Point(578,
              254), size=wx.Size(442, 260), style=0,
              title=u'Keywords Search Status...')
        self.SetClientSize(wx.Size(434, 226))
        self.SetAutoLayout(True)
        self.SetBackgroundColour(wx.Colour(125, 152, 221))
        self.SetCursor(wx.STANDARD_CURSOR)
        self.SetMinSize(wx.Size(-1, -1))
        self.Center(wx.BOTH)

        self.panScanStatus = wx.Panel(id=wxID_DLGKEYWORDSSCANPROGRESSPANSCANSTATUS,
              name=u'panScanStatus', parent=self, pos=wx.Point(16, 16),
              size=wx.Size(400, 160), style=wx.TAB_TRAVERSAL)
        self.panScanStatus.SetBackgroundColour(wx.Colour(225, 236, 255))

        self.lblStartTime = wx.StaticText(id=wxID_DLGKEYWORDSSCANPROGRESSLBLSTARTTIME,
              label=u'Start Time', name=u'lblStartTime',
              parent=self.panScanStatus, pos=wx.Point(104, 56), size=wx.Size(96,
              13), style=0)

        self.staticText2 = wx.StaticText(id=wxID_DLGKEYWORDSSCANPROGRESSSTATICTEXT2,
              label=u'Start Time:', name='staticText2',
              parent=self.panScanStatus, pos=wx.Point(8, 56), size=wx.Size(88,
              13), style=wx.ALIGN_RIGHT)

        self.staticText3 = wx.StaticText(id=wxID_DLGKEYWORDSSCANPROGRESSSTATICTEXT3,
              label=u'Elapsed Time:', name='staticText3',
              parent=self.panScanStatus, pos=wx.Point(16, 128), size=wx.Size(82,
              13), style=wx.ALIGN_RIGHT)

        self.lblElapsedTime = wx.StaticText(id=wxID_DLGKEYWORDSSCANPROGRESSLBLELAPSEDTIME,
              label=u'0 s', name=u'lblElapsedTime', parent=self.panScanStatus,
              pos=wx.Point(104, 128), size=wx.Size(14, 13), style=0)

        self.lblTotalDir = wx.StaticText(id=wxID_DLGKEYWORDSSCANPROGRESSLBLTOTALDIR,
              label=u'0', name=u'lblTotalDir', parent=self.panScanStatus,
              pos=wx.Point(104, 80), size=wx.Size(6, 13), style=0)

        self.staticText4 = wx.StaticText(id=wxID_DLGKEYWORDSSCANPROGRESSSTATICTEXT4,
              label=u'Directories Count:', name='staticText4',
              parent=self.panScanStatus, pos=wx.Point(8, 80), size=wx.Size(87,
              16), style=wx.ALIGN_RIGHT)

        self.staticText5 = wx.StaticText(id=wxID_DLGKEYWORDSSCANPROGRESSSTATICTEXT5,
              label=u'Files Count:', name='staticText5',
              parent=self.panScanStatus, pos=wx.Point(8, 104), size=wx.Size(89,
              13), style=wx.ALIGN_RIGHT)

        self.lblFilesCount = wx.StaticText(id=wxID_DLGKEYWORDSSCANPROGRESSLBLFILESCOUNT,
              label=u'0', name=u'lblFilesCount', parent=self.panScanStatus,
              pos=wx.Point(104, 104), size=wx.Size(6, 13), style=0)

        self.lblScanStatus = wx.StaticText(id=wxID_DLGKEYWORDSSCANPROGRESSLBLSCANSTATUS,
              label=u'Done Searching for Keywords!', name=u'lblScanStatus',
              parent=self.panScanStatus, pos=wx.Point(176, 8), size=wx.Size(197,
              16), style=0)
        self.lblScanStatus.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, u'MS Shell Dlg 2'))
        self.lblScanStatus.SetForegroundColour(wx.Colour(255, 0, 0))
        self.lblScanStatus.Show(True)

        self.btnOK = wx.Button(id=wxID_DLGKEYWORDSSCANPROGRESSBTNOK,
              label=u'&OK', name=u'btnOK', parent=self, pos=wx.Point(176, 192),
              size=wx.Size(88, 24), style=0)
        self.btnOK.Show(False)
        self.btnOK.Bind(wx.EVT_BUTTON, self.OnBtnOKButton,
              id=wxID_DLGKEYWORDSSCANPROGRESSBTNOK)

        self.btnCancel = wx.Button(id=wxID_DLGKEYWORDSSCANPROGRESSBTNCANCEL,
              label=u'&Cancel', name=u'btnCancel', parent=self,
              pos=wx.Point(176, 192), size=wx.Size(88, 24), style=0)
        self.btnCancel.Bind(wx.EVT_BUTTON, self.OnBtnCancelButton,
              id=wxID_DLGKEYWORDSSCANPROGRESSBTNCANCEL)

    def __init__(self, parent):
        
        self._init_ctrls(parent)
        self.SetIcon(images.getMAKE2Icon())
        
        self.InitThrober()
        self.Bind(EVT_UPDATE_LABEL, self.OnUpdate)
        self.FilePropertiesToRead = ""
        self.lblScanStatus.SetLabel("Keywords Search in Progress...")
        #self.db = SqliteDatabase(Globals.MACFileName)
        #self.db.OpenConnection()
        self.StartTime = 0
        self.scanStarted = False
        #self.ReadFilePropertiesToGet()
        self.jobID = 0
        self.StartScan()
        self.scanThread = KeywordsScanThread(self, self.StartTime)
        #self.ScanFinished = False
        self.scanThread.Start()
        
        
    def InitThrober(self):
        import  wx.lib.throbber as  throb
        import throbImages # this was created using a modified version of img2py
        # create the throbbers
        images = [throbImages.catalog[i].getBitmap()
                  for i in throbImages.index
                  if i not in ['eclouds', 'logo']]
                  
        self.throbber1 = throb.Throbber(self.panScanStatus, -1, images, frameDelay=0.07,
              pos=wx.Point(136, 8), size=wx.Size(36, 36))

        self.throbber1.Start()
        
    def StartTimer(self):
        self.StartTime = time.time()
        self.lblStartTime.SetLabel(str(time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())))
        self.lblStartTime.Refresh()
        return None
    
      
    def StartScan(self):
        self.StartTimer()
       
        
    def OnUpdate(self, evt):
        self.lblTotalDir.SetLabel(evt.totalDir)
        self.lblElapsedTime.SetLabel(PlatformMethods.Encode(evt.elapsedTime))
        #self.lblCurrentDir.SetLabel(PlatformMethods.Encode(evt.currentDir))
        self.lblFilesCount.SetLabel(evt.filesCount)
        #self.lblTotalFiles.SetLabel(PlatformMethods.Encode(evt.totalFiles))
        #self.CurrentFileName = file
        self.lblScanStatus.SetLabel(PlatformMethods.Encode(evt.scanStatus))
        if str(evt.scanStatus) == "Done Searching!":
            self.throbber1.Stop()
            self.btnOK.Show(True)
            self.btnCancel.Show(False)
        self.RefreshLabels()
        evt.Skip()

        
    def RefreshLabels(self):
        #self.panFrequencyCounts.Refresh()
        #self.lblTotalFiles.Refresh()
        self.lblFilesCount.Refresh()
        self.lblTotalDir.Refresh()
        #self.lblStartTime.Refresh()
        self.lblElapsedTime.Refresh()
        

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
                    self.scanThread.Stop()
                    #query = "delete from " + Constants.FileInfoTable
                    #self.db.ExecuteNonQuery(query)
                    self.Close()
        finally:
            dlg.Destroy()

            

    def OnDlgScanProgressClose(self, event):
        event.Skip()
            
    
class KeywordsScanThread:
    def __init__(self, win, startTime):
        self.win = win
        self.StartTime = startTime
        #self.dirName = dirName
        #self.CurrentFileName = ""
        #self.CurrentDirectory = ""
        self.DirCount = 0
        self.FilesCount = 0
        self.ElapsedTime = ""
        self.SearchStatus = "Search in Progress..."
        self.KeyColumnNames = ""
        """
        self.timerStatus = wx.Timer(id=wx.NewId(), owner=self)
        self.Bind(wx.EVT_TIMER, self.OnTimerStatusTimer,
              id=self.timerStatus.GetId())
        """
        self.EventStart = time.time()
        #Globals.frmGlobalMainForm.treeKeywords.GetKeywordsSearchDirList()
        DBFunctions.CreateKeywordsFrequencyTable(Globals.KeywordsFileName, True)
        self.InitializeKeyWordsFrequencyDictionary()
        
    def Start(self):
        #self.timerStatus.Start(10000)
        self.keepGoing = self.running = True
        thread.start_new_thread(self.Run, ())
        #self.Run()
        
    def Stop(self):
        self.keepGoing = False
        #self.db.CloseConnection()
        
    def IsRunning(self):
        return self.running
    
    def Run(self):
        db = SqliteDatabase(Globals.KeywordsFileName)
        if not db.OpenConnection():
            return
        #print Globals.KeywordsSearchDirList
        for dir in Globals.KeywordsSearchDirList:
            #print dir
            if dir.find("*.*") >= 0:
                continue
            if not os.path.isdir(dir):
                continue
            try:
                #print dir
                files = os.listdir(dir)
                self.DirCount += 1
                for file in files:
                    if not self.keepGoing:
                        return
                    filePath = dir + PlatformMethods.GetDirSeparator() + file
                    #print filePath
                    if os.path.isfile(filePath):
                        try:
                            if filePath.rfind('.') >= 0:
                                extension = filePath[filePath.rfind('.'):]
                                #print 'extension = ', extension
                                fileType = wx.TheMimeTypesManager.GetFileTypeFromExtension(extension)
                                if fileType:
                                    mimeType = fileType.GetMimeType() or "Unknown"
                                    #print "mimeType ", mimeType
                                    #try:
                                        #print Globals.KeywordsSearchCategoryList
                                    if mimeType in Globals.KeywordsSearchCategoryList:
                                        #print 'ReadFile being called'
                                        self.ReadFile(filePath, db)
                                        self.FilesCount += 1
                                        #self.ElapsedTime = CommonFunctions.ConvertSecondsToDayHourMinSec(time.time() - self.StartTime)
                                        """
                                        except Exception, value:
                                            print "Failed to read file: %s Error: %s"%(filePath, value)
                                            continue
                                        """
                                    #else:
                                    #    time.sleep(1)
                                #else:
                                #    time.sleep(1)
                            else:
                                self.ReadFile(filePath, db)
                                self.FilesCount += 1
                                        
                            if (time.time() - self.EventStart) > 10:
                                #print time.time() - self.EventStart
                                self.ElapsedTime = CommonFunctions.ConvertSecondsToDayHourMinSec(time.time() - self.StartTime)
                                self.SendEvent()
                            
                        except Exception, value:
                            print "Failed to read file: %s Error: %s"%(filePath, value)
                            
            except Exception, value:
                print "Failed to read directory: %s Error: %s"%(dir, value)
                continue
                        
        db.CloseConnection()
            
        finishTime = time.time()
        self.ElapsedTime = CommonFunctions.ConvertSecondsToDayHourMinSec(finishTime - self.StartTime)
        self.SearchStatus = "Done Searching!"
        self.SendEvent()
        #self.timerStatus.Stop()


    def ReadFile(self, fileName, db):
        #print 'ReadFile'
        query = "INSERT INTO " + Constants.KeywordsFrequencyTable + " ( FileName " 
        fin = open(fileName, "rb")
        #fileName = string.replace(filename, "\\", "\\\\")
        query += self.KeyColumnNames + ") VALUES (" + db.SqlSQuote(fileName) + ""
        while True:
            lines = fin.readlines()
            if not lines:
                break
            for line in lines:
                for word in Globals.KeywordsFrequency:
                    Globals.KeywordsFrequency[word]['count'] += len(re.findall(Globals.KeywordsFrequency[word]['re'], line))
                                 
            #line = fin.readline()
            """
            if time.time() - self.StartTime >= 10:
                self.UpdateTimeElapsed()
            """
                
        values = ""
        for word in Globals.KeywordsFrequency:
            values += ", '" + str(Globals.KeywordsFrequency[word]['count']) + "'"
            #print word + ": " + str(Globals.KeywordsFrequency[word]['count'])
            
        query += values + ")"
        
        #print query
        db.ExecuteNonQuery(query)
        fin.close()
        self.InitializeKeywordsFrequency()
        #return True


    def SendEvent(self):
        evt = UpdateLabelEvent(elapsedTime = self.ElapsedTime, 
            filesCount = self.FilesCount, totalDir = self.DirCount,
            scanStatus = self.SearchStatus)
        wx.PostEvent(self.win, evt)
        self.EventStart = time.time()
        
    def InitializeKeyWordsFrequencyDictionary(self):
        #self.ReadKeyWordsFromDatabase()
        Globals.KeywordsFrequency = {}
        for word in Globals.Keywords:
            Globals.KeywordsFrequency[word + '_CS'] = {'re': re.compile("\\b" + word + "\\b", re.S), 'count': 0} # Match only whole word case sensitive
            if Globals.KeywordsSearchCaseSensitive:
                Globals.KeywordsFrequency[word + '_CI'] = {'re': re.compile("\\b" + word + "\\b", re.I|re.S), 'count': 0} # match only whole word case insensitive
            
            """
            if Globals.CurrentProject.SearchInMiddle:
                Globals.KeywordsFrequency[word + '_EICI'] = {'re': re.compile("\\B" + word + "\\B", re.I|re.S), 'count': 0} # Embedded completely inside a word
            if Globals.CurrentProject.SearchAsPrefix:
                Globals.KeywordsFrequency[word + '_EBCI'] = {'re': re.compile("\\b" + word + "\\w+", re.I|re.S), 'count': 0} # Embedded in the beginning of a word
            if Globals.CurrentProject.SearchAsSuffix:
                Globals.KeywordsFrequency[word + '_EECI'] = {'re': re.compile("\\w+" + word + "\\b", re.I|re.S), 'count': 0} # Embedded at the end of a word
            """
            
        self.KeyColumnNames = ""
        for word in Globals.KeywordsFrequency:
            self.KeyColumnNames += ", " + word 
        
    def InitializeKeywordsFrequency(self):
        """
        for word in Globals.Keywords:
            Globals.KeywordsFrequency[word + '_CS']['count'] = 0 # Match only whole word case sensitive
            if Globals.CurrentProject.CaseSensitive:
                Globals.KeywordsFrequency[word + '_CI']['count'] = 0 # match only whole word case insensitive
        """
        for word in Globals.KeywordsFrequency:
            Globals.KeywordsFrequency[word]['count'] = 0
