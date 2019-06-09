#-----------------------------------------------------------------------------
# Name:        dlgScanProgress.py
# Purpose:     
#
# Author:      Ram Basnet
#
# Created:     2007/11/10
# Last Modified: 06/29/2009
# RCS-ID:      $Id: dlgScanProgress.py,v 1.8 2008/03/17 04:18:38 rbasnet Exp $
# Copyright:   (c) 2007
# Licence:     All Rights Reserved.
#-----------------------------------------------------------------------------
#Boa:MDIChild:dlgScanProgress

import wx
import wx.lib.buttons
import time
import os.path, sys
#import wx.lib.delayedresult as delayedresult
import wx.lib.newevent
import  thread
import cPickle
import zipfile
from stat import *

from wx.lib.anchors import LayoutAnchors

from SqliteDatabase import *
import Globals
import Constants
import CommonFunctions
import DBFunctions
import Classes
import PlatformMethods
import images


def create(parent, dirPath):
    return dlgScanProgress(parent, dirPath)

[wxID_DLGSCANPROGRESS, wxID_DLGSCANPROGRESSBTNCANCEL, 
 wxID_DLGSCANPROGRESSBTNOK, wxID_DLGSCANPROGRESSLBLELAPSEDTIME, 
 wxID_DLGSCANPROGRESSLBLFILESCOUNT, wxID_DLGSCANPROGRESSLBLKNOWNFILESCOUNT, 
 wxID_DLGSCANPROGRESSLBLROOTDIR, wxID_DLGSCANPROGRESSLBLSCANSTATUS, 
 wxID_DLGSCANPROGRESSLBLSTARTTIME, wxID_DLGSCANPROGRESSLBLTOTALDIR, 
 wxID_DLGSCANPROGRESSPANSCANSTATUS, wxID_DLGSCANPROGRESSSTATICTEXT1, 
 wxID_DLGSCANPROGRESSSTATICTEXT2, wxID_DLGSCANPROGRESSSTATICTEXT3, 
 wxID_DLGSCANPROGRESSSTATICTEXT4, wxID_DLGSCANPROGRESSSTATICTEXT5, 
 wxID_DLGSCANPROGRESSSTATICTEXT6, 
] = [wx.NewId() for _init_ctrls in range(17)]

#----------------------------------------------------------------------

# This creates a new Event class and a EVT binder function
(UpdateLabelEvent, EVT_UPDATE_LABEL) = wx.lib.newevent.NewEvent()


#----------------------------------------------------------------------

[wxID_DLGSCANPROGRESSTIMER1] = [wx.NewId() for _init_utils in range(1)]

class dlgScanProgress(wx.Dialog):
    def _init_utils(self):
        # generated method, don't edit
        self.timer1 = wx.Timer(id=wxID_DLGSCANPROGRESSTIMER1, owner=self)
        self.Bind(wx.EVT_TIMER, self.OnTimer1Timer,
              id=wxID_DLGSCANPROGRESSTIMER1)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_DLGSCANPROGRESS,
              name=u'dlgScanProgress', parent=prnt, pos=wx.Point(549, 248),
              size=wx.Size(448, 337), style=0, title=u'Scan Status...')
        self._init_utils()
        self.SetClientSize(wx.Size(440, 303))
        self.SetAutoLayout(True)
        self.SetBackgroundColour(wx.Colour(125, 152, 221))
        self.SetCursor(wx.STANDARD_CURSOR)
        self.SetMinSize(wx.Size(-1, -1))
        self.Center(wx.BOTH)
        self.Bind(wx.EVT_CLOSE, self.OnDlgScanProgressClose)

        self.panScanStatus = wx.Panel(id=wxID_DLGSCANPROGRESSPANSCANSTATUS,
              name=u'panScanStatus', parent=self, pos=wx.Point(16, 16),
              size=wx.Size(408, 232), style=wx.TAB_TRAVERSAL)
        self.panScanStatus.SetBackgroundColour(wx.Colour(225, 236, 255))

        self.lblStartTime = wx.StaticText(id=wxID_DLGSCANPROGRESSLBLSTARTTIME,
              label=u'Start Time', name=u'lblStartTime',
              parent=self.panScanStatus, pos=wx.Point(104, 88), size=wx.Size(96,
              13), style=0)

        self.staticText2 = wx.StaticText(id=wxID_DLGSCANPROGRESSSTATICTEXT2,
              label=u'Root Directory:', name='staticText2',
              parent=self.panScanStatus, pos=wx.Point(24, 112), size=wx.Size(74,
              13), style=wx.ALIGN_RIGHT)

        self.staticText3 = wx.StaticText(id=wxID_DLGSCANPROGRESSSTATICTEXT3,
              label=u'Elapsed Time:', name='staticText3',
              parent=self.panScanStatus, pos=wx.Point(16, 208), size=wx.Size(82,
              13), style=wx.ALIGN_RIGHT)

        self.lblElapsedTime = wx.StaticText(id=wxID_DLGSCANPROGRESSLBLELAPSEDTIME,
              label=u'0 s', name=u'lblElapsedTime', parent=self.panScanStatus,
              pos=wx.Point(104, 208), size=wx.Size(14, 13), style=0)

        self.lblTotalDir = wx.StaticText(id=wxID_DLGSCANPROGRESSLBLTOTALDIR,
              label=u'0', name=u'lblTotalDir', parent=self.panScanStatus,
              pos=wx.Point(104, 136), size=wx.Size(6, 13), style=0)

        self.staticText4 = wx.StaticText(id=wxID_DLGSCANPROGRESSSTATICTEXT4,
              label=u'Directories Count:', name='staticText4',
              parent=self.panScanStatus, pos=wx.Point(8, 136), size=wx.Size(87,
              16), style=wx.ALIGN_RIGHT)

        self.staticText5 = wx.StaticText(id=wxID_DLGSCANPROGRESSSTATICTEXT5,
              label=u'Files Count:', name='staticText5',
              parent=self.panScanStatus, pos=wx.Point(8, 160), size=wx.Size(89,
              13), style=wx.ALIGN_RIGHT)

        self.lblFilesCount = wx.StaticText(id=wxID_DLGSCANPROGRESSLBLFILESCOUNT,
              label=u'0', name=u'lblFilesCount', parent=self.panScanStatus,
              pos=wx.Point(104, 160), size=wx.Size(6, 13), style=0)

        self.lblScanStatus = wx.StaticText(id=wxID_DLGSCANPROGRESSLBLSCANSTATUS,
              label=u'Done Scanning!', name=u'lblScanStatus',
              parent=self.panScanStatus, pos=wx.Point(8, 56), size=wx.Size(392,
              24), style=wx.ST_NO_AUTORESIZE | wx.ALIGN_CENTRE)
        self.lblScanStatus.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, u'MS Shell Dlg 2'))
        self.lblScanStatus.SetForegroundColour(wx.Colour(255, 0, 0))
        self.lblScanStatus.Show(True)

        self.btnOK = wx.Button(id=wxID_DLGSCANPROGRESSBTNOK, label=u'&OK',
              name=u'btnOK', parent=self, pos=wx.Point(176, 264),
              size=wx.Size(88, 24), style=0)
        self.btnOK.Show(False)
        self.btnOK.Bind(wx.EVT_BUTTON, self.OnBtnOKButton,
              id=wxID_DLGSCANPROGRESSBTNOK)

        self.btnCancel = wx.Button(id=wxID_DLGSCANPROGRESSBTNCANCEL,
              label=u'&Cancel', name=u'btnCancel', parent=self,
              pos=wx.Point(176, 264), size=wx.Size(88, 24), style=0)
        self.btnCancel.Bind(wx.EVT_BUTTON, self.OnBtnCancelButton,
              id=wxID_DLGSCANPROGRESSBTNCANCEL)

        self.staticText1 = wx.StaticText(id=wxID_DLGSCANPROGRESSSTATICTEXT1,
              label='Known Files Count:', name='staticText1',
              parent=self.panScanStatus, pos=wx.Point(8, 184), size=wx.Size(92,
              13), style=0)

        self.lblKnownFilesCount = wx.StaticText(id=wxID_DLGSCANPROGRESSLBLKNOWNFILESCOUNT,
              label='0', name='lblKnownFilesCount', parent=self.panScanStatus,
              pos=wx.Point(104, 184), size=wx.Size(6, 13), style=0)

        self.staticText6 = wx.StaticText(id=wxID_DLGSCANPROGRESSSTATICTEXT6,
              label=u'Start Time:', name='staticText6',
              parent=self.panScanStatus, pos=wx.Point(8, 88), size=wx.Size(88,
              13), style=wx.ALIGN_RIGHT)

        self.lblRootDir = wx.StaticText(id=wxID_DLGSCANPROGRESSLBLROOTDIR,
              label=u'Root Dir', name=u'lblRootDir', parent=self.panScanStatus,
              pos=wx.Point(104, 112), size=wx.Size(39, 13), style=0)

    def __init__(self, parent, dirPath):
        
        self._init_ctrls(parent)
        self.SetIcon(images.getMAKE2Icon())
        
        self.InitThrober()
        self.Bind(EVT_UPDATE_LABEL, self.OnUpdate)
        self.rootDir = dirPath
        self.FilePropertiesToRead = ""
        self.lblScanStatus.SetLabel("Scan in Progress...")
        self.lblRootDir.SetLabel(PlatformMethods.Encode(dirPath))
        self.StartTime = 0
        self.scanStarted = False
        #self.ReadFilePropertiesToGet()
        self.jobID = 0
        #self.StartScan()
        self.StartTimer()
        
        self.scanThread = MACScanThread(self, self.StartTime, self.rootDir)
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
              pos=wx.Point(184, 8), size=wx.Size(36, 36))

        self.throbber1.Start()

        
    def StartTimer(self):
        self.StartTime = time.time()
        self.timer1.Start(30000) #1/2 min
        self.lblStartTime.SetLabel(PlatformMethods.Encode(CommonFunctions.GetCurrentDisplayDateTime()))
        self.lblStartTime.Refresh()
        return None
    
       
        
    def OnUpdate(self, evt):
        self.lblTotalDir.SetLabel(PlatformMethods.Decode(evt.totalDir))
        self.lblElapsedTime.SetLabel(PlatformMethods.Decode(evt.elapsedTime))
        #self.lblCurrentDir.SetLabel(PlatformMethods.Decode(evt.currentDir))
        self.lblFilesCount.SetLabel(PlatformMethods.Decode(evt.filesCount))
        #self.lblTotalFiles.SetLabel(PlatformMethods.Decode(evt.totalFiles))
        #self.CurrentFileName = file
        self.lblScanStatus.SetLabel(PlatformMethods.Decode(evt.scanStatus))
        self.lblKnownFilesCount.SetLabel(PlatformMethods.Decode(evt.KnownFilesCount))
        if str(evt.scanStatus) == "Done Scanning!":
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
        self.lblKnownFilesCount.Refresh()
        

    def OnBtnOKButton(self, event):
        Globals.frmGlobalMainForm.ShowDirectoryTreeView()
        self.Close()

    def OnBtnCancelButton(self, event):
        dlg = wx.SingleChoiceDialog(self, 'Are you sure you want to cancel the scanning job?', 'Confirmation', ['Yes', 'No'])
        try:
            if dlg.ShowModal() == wx.ID_OK:
                selected = dlg.GetStringSelection()
                # Your code
                if selected == 'Yes':
                    self.timer1.Stop()
                    self.throbber1.Stop()
                    self.btnOK.Show(True)
                    self.btnCancel.Show(False)
                    self.scanThread.Stop()
                    self.lblScanStatus.SetLabel("Scan Stopped by the user!")
                    #query = "delete from " + Constants.FileInfoTable
                    #self.dbFileSystem.ExecuteNonQuery(query)
                    #self.Close()
        finally:
            dlg.Destroy()

            

    def OnDlgScanProgressClose(self, event):

        busy = wx.BusyInfo("One moment please, gettng ready to close")
        wx.Yield()

        running = 1
 
        """11/09/08
        for evidenceID in Globals.EvidencesDict:
            if not DBFunctions.GetFiles(Globals.FileSystemName, evidenceID):
                print "Couldn't read file properties from %s!" %Globals.FileSystemName
        """
        
        while self.scanThread.IsRunning():
            #running = 0
            #running = running + self.scanThread.IsRunning()
            time.sleep(0.1)
        event.Skip()

    def OnTimer1Timer(self, event):
        ElapsedTime = CommonFunctions.ConvertSecondsToDayHourMinSec(time.time() - self.StartTime)
        self.lblTotalDir.SetLabel(PlatformMethods.Decode(self.scanThread.GetDirCount()))
        self.lblElapsedTime.SetLabel(PlatformMethods.Decode(ElapsedTime))
        #self.lblCurrentDir.SetLabel(PlatformMethods.Decode(evt.currentDir))
        self.lblFilesCount.SetLabel(PlatformMethods.Decode(self.scanThread.GetFilesCount()))
        self.lblKnownFilesCount.SetLabel(PlatformMethods.Decode(self.scanThread.GetKnownFilesCount()))
        self.RefreshLabels()
        event.Skip()
            
    
class MACScanThread:
    def __init__(self, win, startTime, rootDir):
        self.win = win
        self.StartTime = startTime
        self.rootDir = rootDir
        #self.CurrentFileName = ""
        self.CurrentDirectory = ""
        self.DirCount = 0
        self.FilesCount = 0
        self.TotalFiles = 0
        self.KnownFilesCount = 0
        self.ElapsedTime = ""
        #self.MD5Hashes = {}
        self.TotalImages = 0
        self.ImageList = []
        self.UnzipRootFolder = "%s%s"%(Globals.CurrentEvidenceID, Constants.UnzipRootFolderName)

        self.dirListQuery = "INSERT INTO %s%s (DirPath, SubDirList) values (?,?)"%(Globals.CurrentEvidenceID, Constants.DirListTable)
        #self.mimeQuery = "INSERT INTO " + Globals.CurrentEvidenceID + "Mime (MimeType, FileList) values (?,?)"
        
        self.query = """INSERT INTO %s(Name, DirPath, Extension, MimeType, Category, Description, Size, Created, CDate, CMonth,
            Modified, MDate, MMonth, Accessed, ADate, AMonth, MD5,KnownFile,NewPath)
            values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""%(Globals.CurrentEvidenceID)
        
        self.imageQuery = """INSERT INTO %s (DirPath, Filename, Thumbnail ) VALUES (?,?,?)"""%(Globals.CurrentEvidenceID)
        
        self.EventStart = time.time()
        
    def Start(self):
        #self.timerStatus.Start(10000)
        self.keepGoing = self.running = True
        thread.start_new_thread(self.Run, ())
        #self.Run()
        
    def Stop(self):
        self.keepGoing = False
        #self.dbFileSystem.CloseConnection()
        
    def IsRunning(self):
        return self.running
    
    def GetDirCount(self):
        return self.DirCount
    
    def GetFilesCount(self):
        return self.FilesCount
    
    def GetKnownFilesCount(self):
        return self.KnownFilesCount
    
    def Run(self):
        #print 'run start'
        #knownFileLog = os.path.join(Globals.CasePath, 'KnownFiles.log')
        #self.knownFilesLog = open(knownFileLog, 'wb')
        
        errorLogFile = os.path.join(Globals.CasePath, 'Errors.log')
        
        self.errorLog = open(errorLogFile, 'wb')
        
        self.progressLog = open(os.path.join(Globals.CasePath, 'Progress.log'), 'wb')
        
        self.dbFileSystem = SqliteDatabase(Globals.FileSystemName)
        if not self.dbFileSystem.OpenConnection():
            return

        self.dbImage = SqliteDatabase(Globals.ImagesFileName)
        if not self.dbImage.OpenConnection():
            return
        
        self.dbMAC = SqliteDatabase(Globals.MACFileName)
        if not self.dbMAC.OpenConnection():
            return
        
        
        self.dbNSRL = None
        if os.path.exists(Constants.NSRLDBName):
            self.dbNSRL = SqliteDatabase(Constants.NSRLDBName)
            self.dbNSRL.OpenConnection()
                
        #query = "delete from " + Constants.FileInfoTable + ";"
        #self.dbFileSystem.ExecuteNonQuery(query)
        DBFunctions.CreateFileSystemTable(Globals.FileSystemName, Globals.CurrentEvidenceID, True)
        DBFunctions.CreateThumbnailsTable(Globals.ImagesFileName, Globals.CurrentEvidenceID, True)
        DBFunctions.CreateMACTables(Globals.MACFileName, Globals.CurrentEvidenceID, drop=True)
        
        if not Globals.EvidencesDict.has_key(Globals.CurrentEvidenceID):
            Globals.EvidencesDict[Globals.CurrentEvidenceID] = {}
            
        #11/06/08 Globals.EvidencesDict[Globals.CurrentEvidenceID]['DirTree'] = {}
        #11/06/08 Globals.EvidencesDict[Globals.CurrentEvidenceID]['Location'] = self.rootDir
        
        #11/06/08 Globals.FilesDict[Globals.CurrentEvidenceID] = {}
        #11/06/08 Globals.ImagesDict[Globals.CurrentEvidenceID] = {}
        #11/06/08 Globals.EvidencesDict[Globals.CurrentEvidenceID]['dirs'] = {}
        self.ElapsedTime = CommonFunctions.ConvertSecondsToDayHourMinSec(time.time() - self.StartTime)
        evt = UpdateLabelEvent(elapsedTime = self.ElapsedTime, KnownFilesCount = self.KnownFilesCount,
            totalDir = self.DirCount, filesCount=self.FilesCount, scanStatus = "Scan in progress...")
        wx.PostEvent(self.win, evt)
        
        self.MimeTypeDict = {}
        
        Globals.TimelinesDict['Created'] = {'MinDate': -1, 'MaxDate': -1, 'MinMonth': -1, 'MaxMonth': -1}
        Globals.TimelinesDict['Modified'] = {'MinDate': -1, 'MaxDate': -1, 'MinMonth': -1, 'MaxMonth': -1}
        Globals.TimelinesDict['Accessed'] = {'MinDate': -1, 'MaxDate': -1, 'MinMonth': -1, 'MaxMonth': -1}
        
        
        self.FileList = []
        #self.ThumbnailList = []
        self.SubDirList = []
        
        self.UnzipFileNameDict = {}
        
        for root, dirs, files in os.walk(self.rootDir):
            self.DirCount += len(dirs)
            
            #self.ImageCount = 0
            self.SubDirList = None
            self.SubDirList = dirs
            dirs = None
            for afile in files:
                #06/23/09 added try/catch block to catch runtime errors on long filenames
                try:
                    self.progressLog.write("%s\n"%(PlatformMethods.Encode(os.path.join(root, afile))))
                    self.ScanFileInfo(root, afile)
                    
                    """
                    if len(self.ThumbnailList) >= Constants.MaxThumbnailsToHold:
                        self.dbImage.ExecuteMany(self.imageQuery, self.ThumbnailList)
                        self.ThumbnailList = []
                    """
                    
                    if len(self.FileList) >= Constants.MaxFileInfoToHold:
                        self.dbFileSystem.ExecuteMany(self.query, self.FileList)
                        self.FileList = None
                        self.FileList = []
                        
                except Exception, value:
                    try:
                        self.errorLog.write('MAC Info Failed on %s; Error: %s\n'%(PlatformMethods.Encode(os.path.join(root, afile)), str(value)))
                        self.errorLog.flush()
                        #print "Failed to get information on file: %s Error: %s"%(fullFileName, value)
                    except Exception, value:
                        self.errorLog.write('MAC Info Failed; Error: %s\n'%(str(value)))
                        self.errorLog.flush()
            files = None
            self.dbFileSystem.ExecuteMany(self.dirListQuery, [(PlatformMethods.Encode(root), cPickle.dumps(self.SubDirList))])
            
        
        """
        self.dbImage.ExecuteMany(self.imageQuery, self.ThumbnailList)
        self.ThumbnailList = []
        """
            
        self.dbFileSystem.ExecuteMany(self.query, self.FileList)
        self.FileList = None
        #self.FileList = []
                
        query ="INSERT INTO %s%s (CMinDate,CMaxDate,CMinMonth,CMaxMonth, MMinDate,MMaxDate,MMinMonth,MMaxMonth,AMinDate,AMaxDate,AMinMonth,AMaxMonth) values (?,?,?,?,?,?,?,?,?,?,?,?)"%(Globals.CurrentEvidenceID, Constants.MACRangeTable)
            
        self.dbMAC.ExecuteMany(query, [(Globals.TimelinesDict['Created']['MinDate'],Globals.TimelinesDict['Created']['MaxDate'],
            Globals.TimelinesDict['Created']['MinMonth'], Globals.TimelinesDict['Created']['MaxMonth'],
            Globals.TimelinesDict['Modified']['MinDate'], Globals.TimelinesDict['Modified']['MaxDate'],
            Globals.TimelinesDict['Modified']['MinMonth'], Globals.TimelinesDict['Modified']['MaxMonth'],
            Globals.TimelinesDict['Accessed']['MinDate'], Globals.TimelinesDict['Accessed']['MaxDate'],
            Globals.TimelinesDict['Accessed']['MinMonth'], Globals.TimelinesDict['Accessed']['MaxMonth'])])
            
         
        self.dbFileSystem.CloseConnection()
        self.dbImage.CloseConnection()
        self.dbMAC.CloseConnection()
        
        self.UpdateEvidence(self.rootDir)
        if self.dbNSRL:
            self.dbNSRL.CloseConnection()
        
        self.ElapsedTime = CommonFunctions.ConvertSecondsToDayHourMinSec(time.time() - self.StartTime)
        evt = UpdateLabelEvent(elapsedTime = self.ElapsedTime, KnownFilesCount = self.KnownFilesCount,
            totalDir = self.DirCount, filesCount=self.FilesCount, scanStatus = "Done Scanning!")
        wx.PostEvent(self.win, evt)
        self.running = False
        #self.knownFilesLog.close()
        self.progressLog.close()
        self.errorLog.close()
        #self.timerStatus.Stop()


    def ScanFileInfo(self, dirPath, fileName):
        if not self.keepGoing:
            return

        fullFileName = os.path.join(dirPath, fileName)
        
        """Name, DirPath, Extension, MimeType, Category, Description, Size, Created, CDate, CMonth,
            Modified, MDate, MMonth, Accessed, ADate, AMonth, MD5,KnownFile,NewPath
        """
        #propList = []
        #propList.append(fileName)
        #propList.append(dirPath)

        if os.path.isfile(fullFileName):
            self.FilesCount += 1

            Extension, MimeType, Description, Category = self.GetFileMimeInfo(fullFileName)
                        
            try:
                st = os.stat(fullFileName)
                Modified = st[ST_MTIME]
                Size = st[ST_SIZE]
                Created = st[ST_CTIME]
                Accessed = st[ST_ATIME]
                
            except Exception, value:
                try:
                    self.errorLog.write('MAC Info Failed on %s; Error: %s\n'%(PlatformMethods.Encode(os.path.join(root, afile)), str(value)))
                    self.errorLog.flush()
                    #print "Failed to get information on file: %s Error: %s"%(fullFileName, value)
                except Exception, value:
                    self.errorLog.write('MAC Info Failed; Error: %s\n'%(str(value)))
                    self.errorLog.flush()
                    
                Modified = 'None'
                Size = 'None'
                Created = 'None'
                Accessed = 'None'
                
            
            
            #if not newFile.MimeType in Globals.MimeTypeSet:
            Globals.MimeTypeSet.add(MimeType)
             
            hashes = CommonFunctions.GetFileHashesAsDict(fullFileName, bufferSize=1024*1024*16, MD5=True, SHA1=False)
            KnownFile = 0
            MD5 = "None"
            if hashes:
                if self.dbNSRL:
                    if self.CheckMD5Hash(self.dbNSRL, hashes['MD5']):
                        #self.knownFilesLog.write("%s\t\t%s\n"%(unicode(fullFileName), unicode(hashes['MD5'])))
                        self.KnownFilesCount += 1
                        KnownFile = 1
                        #return
                        
                MD5 = hashes['MD5']
             
            mDate, mMonth, aDate, aMonth, cDate, cMonth = self.GetAllMACTimes(Modified, Accessed, Created)
            
            self.FileList.append((PlatformMethods.Encode(fileName), PlatformMethods.Encode(dirPath), Extension, MimeType, Category, Description, Size, Created, cDate, cMonth,
                Modified, mDate, mMonth, Accessed, aDate, aMonth,  MD5, KnownFile, ""))

            
            
            #work on image file
            #thumnail is not generated while scanning as it was taking way more time
            if MimeType.find("image/") == 0:
                self.TotalImages += 1
                
            """
                try:
                    thumbnail = CommonFunctions.GetThumbnail(fullFileName).GetData()
                     #= thumbnail.GetData()
                except:
                    thumbnail = 'None'
 
                self.ThumbnailList.append((dirPath, fileName, thumbnail))
            """
                
            #work on zip, rar and other compressed files
            if zipfile.is_zipfile(fullFileName):
                if Extension.find("x") == -1 and Extension.find("jar") == -1:
                    unzippedPath = os.path.join(dirPath, fileName)
                    self.SubDirList.append("%s.unzip"%fileName)
                    self.HandleRecursiveZipFile(unzippedPath, dirPath, fileName)
            
                
                
    def GetFileMimeInfo(self, fileName):
        if (fileName.rfind('.') >= 0):
            Extension = fileName[fileName.rfind('.'):]
            fileType = wx.TheMimeTypesManager.GetFileTypeFromExtension(Extension)
            if fileType:
                MimeType = PlatformMethods.Encode(fileType.GetMimeType()) or "unknown"
                if MimeType == "None":
                    MimeType = "unknown"
                 
                Description = PlatformMethods.Encode(fileType.GetDescription()) or "unknown"
                if Description == "None":
                    Description = "unknown"
                    
                Category = CommonFunctions.GetFileCategory(MimeType)
            else:
                MimeType = "unknown"
                Description = "unknown"
                Category = "unknown"
            
        else:
            Extension = "None"
            MimeType = "unknown"
            Description = "unknown"
            Category = "unknown"
            
        return Extension, MimeType, Description, Category

    def GetAllMACTimes(self, Modified, Accessed, Created):
        mDate = 0
        mMonth = 0
        aDate = 0
        aMonth = 0
        cDate = 0
        cMonth = 0
        if Created > 0:
            cDate = CommonFunctions.GetDateSeconds(Created)
            cMonth = CommonFunctions.GetMonthSeconds(Created)
            
            if (Globals.TimelinesDict['Created']['MinDate'] == -1 or Globals.TimelinesDict['Created']['MinDate'] > cDate):
                Globals.TimelinesDict['Created']['MinDate'] = cDate
            if (Globals.TimelinesDict['Created']['MaxDate'] == -1 or Globals.TimelinesDict['Created']['MaxDate'] < cDate):
                Globals.TimelinesDict['Created']['MaxDate'] = cDate
                
          
            if (Globals.TimelinesDict['Created']['MinMonth'] == -1 or Globals.TimelinesDict['Created']['MinMonth'] > cMonth):
                Globals.TimelinesDict['Created']['MinMonth'] = cMonth
            if (Globals.TimelinesDict['Created']['MaxMonth'] == -1 or Globals.TimelinesDict['Created']['MaxMonth'] < cMonth):
                Globals.TimelinesDict['Created']['MaxMonth'] = cMonth
            
        if Modified > 0:
            mDate = CommonFunctions.GetDateSeconds(Modified)
            mMonth = CommonFunctions.GetMonthSeconds(Modified)
        
            if (Globals.TimelinesDict['Modified']['MinDate'] == -1 or Globals.TimelinesDict['Modified']['MinDate'] > mDate):
                Globals.TimelinesDict['Modified']['MinDate'] = mDate
            if (Globals.TimelinesDict['Modified']['MaxDate'] == -1 or Globals.TimelinesDict['Modified']['MaxDate'] < mDate):
                Globals.TimelinesDict['Modified']['MaxDate'] = mDate
                
            if (Globals.TimelinesDict['Modified']['MinMonth'] == -1 or Globals.TimelinesDict['Modified']['MinMonth'] > mMonth):
                Globals.TimelinesDict['Modified']['MinMonth'] = mMonth
            if (Globals.TimelinesDict['Modified']['MaxMonth'] == -1 or Globals.TimelinesDict['Modified']['MaxMonth'] < mMonth):
                Globals.TimelinesDict['Modified']['MaxMonth'] = mMonth
                
        if Accessed > 0:
            aDate = CommonFunctions.GetDateSeconds(Accessed)
            aMonth = CommonFunctions.GetMonthSeconds(Accessed)
            if (Globals.TimelinesDict['Accessed']['MinDate'] == -1 or Globals.TimelinesDict['Accessed']['MinDate'] > aDate):
                Globals.TimelinesDict['Accessed']['MinDate'] = aDate
            if (Globals.TimelinesDict['Accessed']['MaxDate'] == -1 or Globals.TimelinesDict['Accessed']['MaxDate'] < aDate):
                Globals.TimelinesDict['Accessed']['MaxDate'] = aDate
                        
                        
            if (Globals.TimelinesDict['Accessed']['MinMonth'] == -1 or Globals.TimelinesDict['Accessed']['MinMonth'] > aMonth):
                Globals.TimelinesDict['Accessed']['MinMonth'] = aMonth
            if (Globals.TimelinesDict['Accessed']['MaxMonth'] == -1 or Globals.TimelinesDict['Accessed']['MaxMonth'] < aMonth):
                Globals.TimelinesDict['Accessed']['MaxMonth'] = aMonth
        
        return mDate, mMonth, aDate, aMonth, cDate, cMonth
        
    
       
    def HandleRecursiveZipFile(self, unzippedPath, dirPath, fileName):
        
        unzipFileName = "%s.unzip"%fileName
        zipFilePath = os.path.join(dirPath, unzipFileName)
        
        if self.UnzipFileNameDict.has_key(unzipFileName):
            self.UnzipFileNameDict[unzipFileName] += 1
        else:
            self.UnzipFileNameDict[unzipFileName] = 1
   
        NewRelativeRoot = "%s-%d"%(unzipFileName, self.UnzipFileNameDict[unzipFileName])
        extractRootPath = os.path.join(Globals.CasePath, self.UnzipRootFolder)
        extractRootPath = os.path.join(extractRootPath, NewRelativeRoot)
        if not os.path.exists(extractRootPath):
            try:
                os.makedirs(extractRootPath)
            except:
                try:
                    os.mkdir(extractRootPath)
                except:
                    pass
        
        
        ZipPath = {}
        try:
            unzip = zipfile.ZipFile(unzippedPath)
        except Exception, msg:
            try:
                self.errorLog.write('%s; UnzipError: %s\n'%(PlatformMethods.Encode(unzippedPath), msg))
                self.errorLog.flush()
            except Exception, msg:
                self.errorLog.write('UnzipError: %s\n'%(msg))
                self.errorLog.flush()

            return
        
            
        for name in unzip.namelist():
            pathlist = name.split("/")
            #filePath = zipFilePath
            dTree = zipFilePath
            #print 'pathlist ', pathlist
            adir = ""
            aPath = extractRootPath
            for adir in pathlist[:-1]:
                #print 'adir ',adir
                if not adir:
                    continue
                    
                if not ZipPath.has_key(dTree):
                    ZipPath[dTree] = set([adir])
                else:
                    ZipPath[dTree].add(adir)
                    
                aPath = os.path.join(aPath, adir)
                if not os.path.exists(aPath):
                    os.mkdir(aPath)
                
                dTree = os.path.join(dTree, adir)
                
                #print 'dTree ', dTree
            
            unzipFileName = pathlist[-1]
            #print unzipFileName
            
            #if no filename then its just directory name
            if not unzipFileName:
                continue
            
            unzipDirName = os.path.sep.join(pathlist[:-1])
            
            #Original/source dir hierarchy structure
            if unzipDirName:
                unzipDirPath = os.path.join(zipFilePath, unzipDirName)
                #Destination dir structure where the files will be unzipped
                extractDirPath = os.path.join(extractRootPath, unzipDirName)
            else:
                unzipDirPath = zipFilePath
                extractDirPath = extractRootPath
            
            
            if not ZipPath.has_key(unzipDirPath):
                #self.DirCount += 1
                ZipPath[unzipDirPath] = set([])

           
            extractFilePath = os.path.join(extractDirPath, unzipFileName)
            info = unzip.getinfo(name)
            
            #check unzip filesize
            if info.file_size > Constants.MaxUnzipFileSize:
                #skip the large file in zip
                self.errorLog.write('%s; Zip File Too Large :: %d\n'%(PlatformMethods.Encode(extractFilePath), info.file_size))
                self.errorLog.flush()
                continue
                
            try:
                buffer = unzip.read(name)
            except Exception, value:
                try:
                    self.errorLog.write('%s; UnzipError: %s\n'%(PlatformMethods.Encode(extractFilePath), value))
                    self.errorLog.flush()
                except Exception, value:
                    self.errorLog.write('UnzipError: %s\n'%(value))
                    self.errorLog.flush()
                    continue
                    
            fout = None
            
            try:
                fout = open(extractFilePath, 'wb')
            except Exception, msg:
                try:
                    os.makedirs(extractDirPath)
                    fout = open(extractFilePath, 'wb')
                except Exception, value:
                    try:
                        self.errorLog.write('%s; UnzipError: %s\n'%(PlatformMethods.Encode(extractFilePath), value))
                        self.errorLog.flush()
                    except Exception, value:
                        self.errorLog.write('UnzipError: %s\n'%(value))
                        self.errorLog.flush()
                        continue
                    
            if fout:
                fout.write(buffer)
                fout.close()
                
            MD5 = "None"
            KnownFile = 0
            hashes = CommonFunctions.GetBufferHashesAsDict(buffer, MD5=True, SHA1=False)
            buffer = None
            if hashes:
                if self.dbNSRL:
                    if self.CheckMD5Hash(self.dbNSRL, hashes['MD5']):
                        #self.knownFilesLog.write("%s\t\t%s\n"%(extractFilePath, hashes['MD5']))
                        self.KnownFilesCount += 1
                        #continue
                        KnownFile = 1
                        
                MD5 = hashes['MD5']

            Name = unzipFileName
            
            DirPath = unzipDirPath #os.path.join(zipFilePath, unzipDirName)
            NewPath = extractFilePath.replace(Globals.CasePath, "")
            if NewPath.find(os.path.sep) == 0:
                NewPath = NewPath.replace(os.path.sep, "", 1)
            
            Extension, MimeType, Description, Category = self.GetFileMimeInfo(unzipFileName)
            
            tList = list(info.date_time)
            tList.append(0)
            tList.append(0)
            tList.append(0)
            
            Modified = time.mktime(tList)
            Size = info.file_size
            Created = 0
            Accessed = 0

            mDate, mMonth, aDate, aMonth, cDate, cMonth = self.GetAllMACTimes(Modified, Accessed, Created)
            
            Globals.MimeTypeSet.add(MimeType)
            
            self.FileList.append((PlatformMethods.Encode(Name), PlatformMethods.Encode(DirPath), Extension, MimeType, Category, Description, Size, Created, cDate, cMonth,
                Modified, mDate, mMonth, Accessed, aDate, aMonth,  MD5, KnownFile, PlatformMethods.Encode(NewPath)))
                    
                
            if len(self.FileList) >= Constants.MaxFileInfoToHold:
                self.dbFileSystem.ExecuteMany(self.query, self.FileList)
                self.FileList = None
                self.FileList = []
                
            
            if MimeType.find("image/") == 0:
                self.TotalImages += 1
            
            """
                try:
                    Thumbnail = CommonFunctions.GetThumbnail(extractFilePath).GetData()
                except Exception, msg:
                    self.errorLog.write('%s; ThumbnailError: %s\n'%(os.path.join(DirPath, Name), msg))
                    self.errorLog.flush()
                    #print 'Error: msg:: ', msg
                    Thumbnail = 'None'
                    
                self.ThumbnailList.append((DirPath, Name, Thumbnail))
                if len(self.ThumbnailList) >= Constants.MaxThumbnailsToHold:
                    self.dbImage.ExecuteMany(self.imageQuery, self.ThumbnailList)
                    self.ThumbnailList = []
            """
            
            if zipfile.is_zipfile(extractFilePath):
                if Extension.find("x") == -1 and Extension.find('jar') == -1:
                    ZipPath[unzipDirPath].add("%s.unzip"%(Name))
                    self.HandleRecursiveZipFile(extractFilePath, DirPath, Name)
                
        for aPath in ZipPath:
            self.dbFileSystem.ExecuteMany(self.dirListQuery, [(PlatformMethods.Encode(aPath), cPickle.dumps(list(ZipPath[aPath])))])
        
        if len(self.FileList) >= Constants.MaxFileInfoToHold:
            self.dbFileSystem.ExecuteMany(self.query, self.FileList)
            self.FileList = None
            self.FileList = []

    def SendEvent(self):
        evt = UpdateLabelEvent(elapsedTime = self.ElapsedTime,  KnownFilesCount = self.KnownFilesCount,
            filesCount = self.FilesCount, totalDir = self.DirCount,
            scanStatus = "Scan in Progress...")
        wx.PostEvent(self.win, evt)
        self.EventStart = time.time()

 
    def UpdateEvidence(self, location):
        db = SqliteDatabase(Globals.CurrentCaseFile)
        if not db.OpenConnection():
            return

        query = "insert into " + Constants.EvidencesTable + " (ID, DisplayName, "
        query += "Location, Comment, AddedTimestamp, TotalFolders, TotalFiles, "
        query += "TotalImages, ScanStartTimestamp, ScanEndTimestamp) values (?,?,?,?,?,?,?,?,?,?)"
        #print query, ("Evidence1", 'Evd1', location, 'No comment',time.ctime()),
        #finishTime = time.time()
        #ElapsedTime = CommonFunctions.ConvertSecondsToDayHourMinSec(finishTime - self.StartTime)
        #DisplayName, Location
        Globals.EvidencesDict[Globals.CurrentEvidenceID] = {'DisplayName':'Evd1', 'Location':location, 'NewLocation':""}
        tuple = (Globals.CurrentEvidenceID, 'Evd1', location, 'No comment', self.StartTime, self.DirCount,
            self.FilesCount, self.TotalImages, self.StartTime,
            time.time())

        db.ExecuteMany(query, [tuple])
        
        db.ExecuteNonQuery("delete from " + Constants.CaseSettingsTable)
        query = "insert into " + Constants.CaseSettingsTable + " (ID, DisplayName, DateTimestamp, CreatedBy, Description, MimeTypes) values (?,?,?,?,?,?)"
        tuple = (Globals.CurrentCase.ID, Globals.CurrentCase.DisplayName, Globals.CurrentCase.DateTimestamp, Globals.CurrentCase.CreatedBy, Globals.CurrentCase.Description, "|".join(Globals.MimeTypeSet))
        #db.ExecuteMany("update " + Constants.CaseSettingsTable + " set MimeTypes = (?)", [tuple])
        db.ExecuteMany(query, [tuple])
        db.CloseConnection()
        

    def CheckMD5Hash(self, db, MD5Hash):
        
        tableName = CommonFunctions.GetMD5HashBucketID(MD5Hash)
        # = 'a%d'%bucketID
        query = "select MD5 from %s where MD5 = '%s';"%(tableName, MD5Hash)
        rows = db.FetchOneRow(query)
        if rows:
            return True
        else:
            return False
        
        

if __name__ == "__main__":
    print 'do nothing'
