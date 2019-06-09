#-----------------------------------------------------------------------------
# Name:        dlgEmailPreprocessingProgress.py
# Purpose:     
#
# Author:      Ram Basnet
#
# Created:     2008/07/10
# RCS-ID:      $Id: dlgEmailPreprocessingProgress.py $
# Copyright:   (c) 2008
# Licence:     All Rights Reserved.
#-----------------------------------------------------------------------------
#Boa:dlg:dlgEmailPreprocessingProgress

import wx
import wx.lib.buttons
import time
import re, string
import os.path, sys
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

import EmailUtilities
import OutlookAddressBook
import OutlookTextParser

from PorterStemmer import *
import TextParser
import HTMLParser
import MSOfficeToText
import DocxParser
import DocParser
import PDFToText
import images
import BloomFilter

def create(parent, AddressBookPath, EmailsPath, AttachmentsPath, CheckedMimeTypes=[], IndexMessages=True, IndexAttachments=True):
    return dlgEmailPreprocessingProgress(parent, AddressBookPath, EmailsPath, AttachmentsPath, CheckedMimeTypes, IndexMessages, IndexAttachments)

[wxID_DLGEMAILPREPROCESSINGPROGRESS, 
 wxID_DLGEMAILPREPROCESSINGPROGRESSBTNCANCEL, 
 wxID_DLGEMAILPREPROCESSINGPROGRESSBTNOK, 
 wxID_DLGEMAILPREPROCESSINGPROGRESSLBLELAPSEDTIME, 
 wxID_DLGEMAILPREPROCESSINGPROGRESSLBLFILESCOUNT, 
 wxID_DLGEMAILPREPROCESSINGPROGRESSLBLSCANSTATUS, 
 wxID_DLGEMAILPREPROCESSINGPROGRESSLBLSTARTTIME, 
 wxID_DLGEMAILPREPROCESSINGPROGRESSPANSCANSTATUS, 
 wxID_DLGEMAILPREPROCESSINGPROGRESSSTATICTEXT2, 
 wxID_DLGEMAILPREPROCESSINGPROGRESSSTATICTEXT3, 
 wxID_DLGEMAILPREPROCESSINGPROGRESSSTATICTEXT5, 
] = [wx.NewId() for _init_ctrls in range(11)]

#----------------------------------------------------------------------

# This creates a new Event class and a EVT binder function
(UpdateLabelEvent, EVT_UPDATE_LABEL) = wx.lib.newevent.NewEvent()


#----------------------------------------------------------------------

[wxID_DLGEMAILPREPROCESSINGPROGRESSTIMER1] = [wx.NewId() for _init_utils in range(1)]

class dlgEmailPreprocessingProgress(wx.Dialog):
    def _init_utils(self):
        # generated method, don't edit
        self.timer1 = wx.Timer(id=wxID_DLGEMAILPREPROCESSINGPROGRESSTIMER1,
              owner=self)
        self.Bind(wx.EVT_TIMER, self.OnTimer1Timer,
              id=wxID_DLGEMAILPREPROCESSINGPROGRESSTIMER1)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_DLGEMAILPREPROCESSINGPROGRESS,
              name='dlgEmailPreprocessingProgress', parent=prnt,
              pos=wx.Point(746, 397), size=wx.Size(441, 277), style=0,
              title='Emails Preprocessing Status...')
        self._init_utils()
        self.SetClientSize(wx.Size(433, 246))
        self.SetAutoLayout(True)
        self.SetBackgroundColour(wx.Colour(125, 152, 221))
        self.SetCursor(wx.STANDARD_CURSOR)
        self.SetMinSize(wx.Size(-1, -1))
        self.Center(wx.BOTH)
        self.Bind(wx.EVT_CLOSE, self.OnDlgTextPreprocessingProgressClose)

        self.panScanStatus = wx.Panel(id=wxID_DLGEMAILPREPROCESSINGPROGRESSPANSCANSTATUS,
              name=u'panScanStatus', parent=self, pos=wx.Point(16, 16),
              size=wx.Size(400, 176), style=wx.TAB_TRAVERSAL)
        self.panScanStatus.SetBackgroundColour(wx.Colour(225, 236, 255))

        self.lblStartTime = wx.StaticText(id=wxID_DLGEMAILPREPROCESSINGPROGRESSLBLSTARTTIME,
              label=u'Start Time', name=u'lblStartTime',
              parent=self.panScanStatus, pos=wx.Point(104, 96), size=wx.Size(96,
              13), style=0)

        self.staticText2 = wx.StaticText(id=wxID_DLGEMAILPREPROCESSINGPROGRESSSTATICTEXT2,
              label=u'Start Time:', name='staticText2',
              parent=self.panScanStatus, pos=wx.Point(8, 96), size=wx.Size(88,
              13), style=wx.ALIGN_RIGHT)

        self.staticText3 = wx.StaticText(id=wxID_DLGEMAILPREPROCESSINGPROGRESSSTATICTEXT3,
              label=u'Elapsed Time:', name='staticText3',
              parent=self.panScanStatus, pos=wx.Point(16, 144), size=wx.Size(82,
              13), style=wx.ALIGN_RIGHT)

        self.lblElapsedTime = wx.StaticText(id=wxID_DLGEMAILPREPROCESSINGPROGRESSLBLELAPSEDTIME,
              label=u'0 s', name=u'lblElapsedTime', parent=self.panScanStatus,
              pos=wx.Point(104, 144), size=wx.Size(14, 13), style=0)

        self.staticText5 = wx.StaticText(id=wxID_DLGEMAILPREPROCESSINGPROGRESSSTATICTEXT5,
              label='Files Count:', name='staticText5',
              parent=self.panScanStatus, pos=wx.Point(40, 120), size=wx.Size(57,
              13), style=wx.ALIGN_RIGHT)

        self.lblFilesCount = wx.StaticText(id=wxID_DLGEMAILPREPROCESSINGPROGRESSLBLFILESCOUNT,
              label=u'0', name=u'lblFilesCount', parent=self.panScanStatus,
              pos=wx.Point(104, 120), size=wx.Size(6, 13), style=0)

        self.lblScanStatus = wx.StaticText(id=wxID_DLGEMAILPREPROCESSINGPROGRESSLBLSCANSTATUS,
              label='Done Email Preprocessing and Indexing!',
              name=u'lblScanStatus', parent=self.panScanStatus, pos=wx.Point(80,
              56), size=wx.Size(257, 16), style=0)
        self.lblScanStatus.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, u'MS Shell Dlg 2'))
        self.lblScanStatus.SetForegroundColour(wx.Colour(255, 0, 0))
        self.lblScanStatus.Show(True)

        self.btnOK = wx.Button(id=wxID_DLGEMAILPREPROCESSINGPROGRESSBTNOK,
              label=u'&OK', name=u'btnOK', parent=self, pos=wx.Point(176, 208),
              size=wx.Size(88, 24), style=0)
        self.btnOK.Show(False)
        self.btnOK.Bind(wx.EVT_BUTTON, self.OnBtnOKButton,
              id=wxID_DLGEMAILPREPROCESSINGPROGRESSBTNOK)

        self.btnCancel = wx.Button(id=wxID_DLGEMAILPREPROCESSINGPROGRESSBTNCANCEL,
              label=u'&Cancel', name=u'btnCancel', parent=self,
              pos=wx.Point(176, 208), size=wx.Size(88, 24), style=0)
        self.btnCancel.Bind(wx.EVT_BUTTON, self.OnBtnCancelButton,
              id=wxID_DLGEMAILPREPROCESSINGPROGRESSBTNCANCEL)

    def __init__(self, parent, AddressBookPath, EmailsPath, AttachmentsPath, CheckedMimeTypes, IndexMessages, IndexAttachments):
        self._init_ctrls(parent)
        self.SetIcon(images.getMAKE2Icon())
        
        #self.InitThrober()
        
        self.InitAnimatedImage()
        self.Bind(EVT_UPDATE_LABEL, self.OnUpdate)
        self.lblScanStatus.SetLabel("Preprocessing Emails and Attachments in Progress...")
        
        #self.CheckedMimeTypes = CheckedMimeTypes
        self.StartTime = 0
        self.scanStarted = False
        #self.ReadFilePropertiesToGet()
        self.jobID = 0
        self.StartTimer()
        #return
        self.scanThread = FileScanThread(self, self.StartTime, AddressBookPath, EmailsPath, AttachmentsPath, CheckedMimeTypes, IndexMessages, IndexAttachments)
        self.ScanFinished = False
        self.scanThread.Start()
        
    def InitAnimatedImage(self):
        import wx.animate
        ani = wx.animate.Animation("./Data/Spinning_wheel_throbber.gif")
        #ani.Load(images.getSpinningWheelImage())
        #ani = wx.animate.Animation(images.getSpinningWheelImage())
        #ani = wx.animate.Animation(images.getSpinningWheelBitmap())
        self.animationCtrl = wx.animate.AnimationCtrl(self, -1, ani, pos=wx.Point(184, 16), size=wx.Size(24, 24))
        #self.animationCtrl.SetUseWindowBackgroundColour()
        self.animationCtrl.Play()
        
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
        self.timer1.Start(10000) #10 sec
        self.lblStartTime.SetLabel(str(time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())))
        self.lblStartTime.Refresh()
        return None
    
       
        
    def OnUpdate(self, evt):
        #global filesCount
        #self.lblTotalDir.SetLabel(PlatformMethods.Decode(evt.totalDir))
        self.lblElapsedTime.SetLabel(PlatformMethods.Decode(evt.elapsedTime))
        #self.lblCurrentDir.SetLabel(PlatformMethods.Decode(evt.currentDir))
        self.lblFilesCount.SetLabel(PlatformMethods.Decode(evt.filesCount))
        #self.lblTotalFiles.SetLabel(PlatformMethods.Decode(evt.totalFiles))
        #self.CurrentFileName = file
        self.lblScanStatus.SetLabel(PlatformMethods.Decode(evt.scanStatus))
        if str(evt.scanStatus) == "Done Preprocessing/Indexing Emails!":
            #self.throbber1.Stop()
            self.animationCtrl.Stop()
            self.btnOK.Show(True)
            self.btnCancel.Show(False)
            self.timer1.Stop()
        self.RefreshLabels()
        evt.Skip()

        
    def RefreshLabels(self):
        self.lblFilesCount.Refresh()
        #self.lblTotalDir.Refresh()
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
            
    

    def OnTimer1Timer(self, event):
        ElapsedTime = CommonFunctions.ConvertSecondsToDayHourMinSec(time.time() - self.StartTime)
        #self.lblTotalDir.SetLabel(PlatformMethods.Decode(self.scanThread.GetDirCount()))
        self.lblElapsedTime.SetLabel(PlatformMethods.Decode(ElapsedTime))
        #self.lblCurrentDir.SetLabel(PlatformMethods.Decode(evt.currentDir))
        
        #self.lblFilesCount.SetLabel(PlatformMethods.Decode(self.scanThread.GetFilesCount()))
        self.RefreshLabels()
        event.Skip()

    def OnDlgTextPreprocessingProgressClose(self, event):
        busy = wx.BusyInfo("One moment please, gettng ready to close")
        wx.Yield()

        running = 1

        while self.scanThread.IsRunning():
            #running = 0
            #running = running + self.scanThread.IsRunning()

            time.sleep(0.1)
            
        event.Skip()

        
    
class FileScanThread:
    def __init__(self, win, startTime, AddressBookPath, EmailsPath, AttachmentsPath, CheckedMimeTypes, IndexMessages, IndexAttachments):
        #import HTMLParser

        self.win = win
        self.StartTime = startTime
        self.IndexMessages = IndexMessages
        self.IndexAttachments = IndexAttachments
        #self.DocID = 0
        #self.WordID = 0
        self.StemmedWordID = 0
        self.DirCount = 0
        self.FilesCount = 0
        self.WordCount = 0
        #self.StemmedWordCount = 0
        self.ElapsedTime = ""
        self.ParseStatus = "Processing in Progress..."
        Globals.EmailsDict = {}
        Globals.AddressBookDict = {}
        self.CheckedMimeTypes = CheckedMimeTypes
        
        EmailUtilities.SetupEmailsDB(Globals.EmailsFileName, createNew=False)
        #DBFunctions.SetupTextCatTables(Globals.EmailsFileName)
        #DBFunctions.SetupSqliteIndexTables(Globals.EmailsFileName)
        self.AddressBookPath = AddressBookPath
        self.EmailsPath = EmailsPath
        self.AttachmentsPath = AttachmentsPath
        
        self.EventStart = time.time()
        
        self.running = True
        self.keepGoing = True
        self.AttachmentsDict = {}
        self.Stemmer = None
        
        self.FileScanStartTime = time.time()
        
    def Start(self):
        #self.timerStatus.Start(1000000)
        self.keepGoing = self.running = True
        thread.start_new_thread(self.Run, ())
        #self.Run()
        
        
    def Stop(self):
        self.keepGoing = False
        #self.db.CloseConnection()

        
    def IsRunning(self):
        return self.running
    
    def Run(self):
        db = SqliteDatabase(Globals.EmailsFileName)
        if not db.OpenConnection():
            return
        
        self.bloomFilter = self.CreateBloomFilter()
        #self.bloomFilter = None
        
        logFileName = PlatformMethods.Decode(os.path.join(Globals.CasePath, (Globals.EmailsFileName[Globals.EmailsFileName.rfind(os.sep)+1:] + '.log')))
        self.fout = open(logFileName, 'ab')
        #print self.CheckedMimeTypes
        self.fout.write('Parsing/Indexing Emails Attachments Started at: %s\n'%(time.ctime()))
        
        if self.AddressBookPath:
            self.ParseStatus = "Parsing Address book..."
            self.SendEvent()
            AddressBookParser = OutlookAddressBook.AddressBookParser(Globals.AddressBookDict)
            for root, dirs, files in os.walk(self.AddressBookPath):
                for eachfile in files:
                    filePath = os.path.join(root, eachfile)
                    self.FilesCount += 1
                    if (filePath.rfind('.') == -1):
                        continue
                    #print filePath
                    extension = filePath[filePath.rfind('.'):]
                    #print 'extension ', extension
                    if extension.lower() == ".csv":
                        AddressBookParser.Parse(filePath)
                        #print 'add book parsed'
        else:
            self.fout.write('No Addressbook path found!\n')
        #Updte Addressbook
        query1 = "insert into " + Constants.AddressBookTable + "(EmailID, FirstName, MiddleName, LastName, InBook) values (?,?,?,?,?)"
        ManyValues = []
        for key in Globals.AddressBookDict:
            #'EmailID': email, 'FirstName': firstName, 'MiddleName': middleName, 'LastName': lastName, 'InBook':1}
            ManyValues.append((Globals.AddressBookDict[key]['EmailID'], Globals.AddressBookDict[key]['FirstName'], Globals.AddressBookDict[key]['MiddleName'], Globals.AddressBookDict[key]['LastName'], Globals.AddressBookDict[key]['InBook']))
            
        #query = "delete from %s"%Constants.AddressBookTable
        #db.ExecuteNonQuery(query)
        #print ManyValues
        db.ExecuteMany(query1, ManyValues)
        
        #self.ParseStatus = "Done Preprocessing/Indexing Emails!"
        #return
        
        textParser = TextParser.TextParser(db, Globals.EmailsStopwords, self.Stemmer, bloomFilter=self.bloomFilter)
        docxParser = DocxParser.DocxParser(db, Globals.EmailsStopwords, self.Stemmer, bloomFilter=self.bloomFilter)
        docParser = DocParser.DocParser(db, Globals.EmailsStopwords, self.Stemmer, bloomFilter=self.bloomFilter)        
        docQuery = "insert into %s (DocPath, DocType) values (?, ?)"%(Constants.TextCatDocumentsTable)
        
        if self.AttachmentsPath:
            for root, dirs, files in os.walk(self.AttachmentsPath):
                for eachfile in files:
                    filePath = os.path.join(root, eachfile)
                    
                    fileNameList = eachfile.split()
                    if len(fileNameList) >= 2:
                        dateTimeFileName = "%s %s - %s"%(fileNameList[0], (fileNameList[1].replace(".", ":")), (eachfile[eachfile.rfind('-')+1:]))
                        
                        if self.AttachmentsDict.has_key(dateTimeFileName):
                            self.AttachmentsDict[dateTimeFileName].append(filePath)
                        else:
                            self.AttachmentsDict[dateTimeFileName] = [filePath]
                            #print 'Intersting! more than 1 attach. file found with same date time: %s'%
                        #else:
                        #    self.AttachmentsDict[dateTimeFileName] = filePath
                    else:
                        self.fout.write('Attachment filename found without date time: %s\n'%(PlatformMethods.Encode(filePath)))
                      
        #AttachmentsDict, Stopwords=[], Stemmer=None
        self.outlookTextParser = OutlookTextParser.OutlookTextParser(db, self.AttachmentsDict, Globals.EmailsStopwords, self.Stemmer, bloomFilter=self.bloomFilter, logFile=self.fout)
        
        if self.IndexMessages:
            self.ParseStatus = "Parsing and Indexing Emails..."  
        else:
            self.ParseStatus = "Parsing Email Headers..."  
            
        self.SendEvent()
        for root, dirs, files in os.walk(self.EmailsPath):
            if not self.keepGoing:
                self.running = False
                return
            
            for eachfile in files:
                self.FilesCount += 1
                if not self.keepGoing:
                    self.running = False
                    return
                
                filePath = os.path.join(root, eachfile)
                #print filePath
                if (filePath.rfind('.') == -1):
                    continue
                
                try:
                    extension = filePath[filePath.rfind('.'):]
                    fileType = wx.TheMimeTypesManager.GetFileTypeFromExtension(extension)
                    if fileType:
                        mimeType = fileType.GetMimeType() or "unknown"
                        if mimeType == "text/plain":
                            try:
                                self.outlookTextParser.parse(filePath, self.IndexMessages)
                            except Exception, msg:
                                self.fout.write('Error Parsing Message: %s Msg:: %s\n'%(PlatformMethods.Encode(filePath), msg))
                                
                            self.ElapsedTime = CommonFunctions.ConvertSecondsToDayHourMinSec(time.time() - self.StartTime)
                            
                    if (time.time() - self.EventStart) > 10:
                        self.ElapsedTime = CommonFunctions.ConvertSecondsToDayHourMinSec(time.time() - self.StartTime)
                        self.SendEvent()
                    
                
                except Exception, value:
                    #try:
                    self.fout.write("Error Parsing Message: %s Msg: %s\n"%(PlatformMethods.Encode(filePath), str(value)))
                    self.fout.flush()
                    #except Exception, value:
                    #    print "Error in Emails Preprocessing...: ", value
                    #    continue
                
                
                
        self.fout.write('Done Indexing Emails!\n')
        self.fout.write('Finished at: %s\n'%(time.ctime()))
        self.fout.write('Total Time Taken: %s\n\n'%(self.ElapsedTime))
        
          
        if self.IndexAttachments:   
            self.ParseStatus = "Indexing Attachments..."
            self.SendEvent()
            for key in self.AttachmentsDict:
                for eachfile in self.AttachmentsDict[key]:
                    #try:
                    filePath = os.path.join(root, eachfile)
                    
                    self.FileScanStartTime = time.time()
                    self.FilesCount += 1
                    
                    dotIndex = filePath.rfind('.')
                    if dotIndex == -1:
                        self.ElapsedTime = CommonFunctions.ConvertSecondsToDayHourMinSec(time.time() - self.StartTime)
                        if (time.time() - self.EventStart) > 10:
                            self.ElapsedTime = CommonFunctions.ConvertSecondsToDayHourMinSec(time.time() - self.StartTime)
                            self.SendEvent()
                        continue
                        
                    extension = filePath[dotIndex:]
                    
                    fileType = wx.TheMimeTypesManager.GetFileTypeFromExtension(extension)
                    if fileType:
                        parsed = False
                        mimeType = fileType.GetMimeType() or "unknown"
                        #if self.CheckedMimeTypes:
                        if mimeType not in self.CheckedMimeTypes:
                               
                            self.ElapsedTime = CommonFunctions.ConvertSecondsToDayHourMinSec(time.time() - self.StartTime)
                                  
                            if mimeType == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' or extension == '.docx':
                                try:
                                    DocID = db.InsertAutoRow(docQuery, [(PlatformMethods.Encode(filePath),Constants.AttachmentDoc)])
                                    #docID, filePath, startTime, logFile, extractMedia = False, MediaPath=""
                                    docxParser.Parse(DocID, filePath, self.FileScanStartTime, self.fout, extractMedia = False, MediaPath="")
                                    parsed = True
                                except Exception, value:
                                    self.fout.write("Error in docxParser : %s Value: %s\n"%(filePath, value))
                                                    
                            if (time.time() - self.EventStart) > 10:
                                #print time.time() - self.EventStart
                                self.ElapsedTime = CommonFunctions.ConvertSecondsToDayHourMinSec(time.time() - self.StartTime)
                                self.SendEvent()
                                
                            continue
                        
                            
                        #print filePath
                        
                        DocID = db.InsertAutoRow(docQuery, [(PlatformMethods.Encode(filePath), Constants.AttachmentDoc)])
                        
                        if mimeType == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' or extension == '.docx':
                            try:
                                #docID, filePath, startTime, logFile, extractMedia = False, MediaPath=""
                                docxParser.Parse(DocID, filePath, self.FileScanStartTime, self.fout, extractMedia = False, MediaPath="")
                                parsed = True
                            except Exception, value:
                                #gives junk so let's not parse it using binary
                                parsed = True
                                self.fout.write("Error in docxParser : %s Value: %s\n"%(PlatformMethods.Encode(filePath), value))                                    
                                
                        elif mimeType == 'application/msword':
                            """
                            try:
                                textParser.parse(DocID, MSOfficeToText.WordToText(filePath), filePath, self.FileScanStartTime, self.fout)
                                parsed = True
                            except Exception, value:
                                self.fout.write("Error in MSOfficeToText.WordToText : %s Value: %s\n"%(filePath, value))
                            """
                            try:
                                #docID, filePath, startTime, logFile, extractMedia = False, MediaPath=""
                                docParser.Parse(DocID, filePath, self.FileScanStartTime, self.fout, extractMedia = False, MediaPath="")
                                parsed = True
                            except Exception, value:
                                #gives junk so let's not parse it using binary
                                self.fout.write("Error in DocParser : %s Value: %s\n"%(PlatformMethods.Encode(filePath), value))  
                                
                        elif mimeType == 'application/pdf':
                            try:
                                textParser.parse(DocID, PDFToText.GetText(filePath), filePath, self.FileScanStartTime, self.fout)
                                parsed = True
                            except Exception, value:
                                self.fout.write("Error in PDFToText: %s Value: %s\n"%(PlatformMethods.Encode(filePath), value))
                                
                            
                        elif mimeType == 'text/plain':
                            try:
                                fin = open(filePath, 'rb')
                                #data = fin.read(4096)
                                #while data:
                                textParser.parse(DocID, fin.read(), filePath, self.FileScanStartTime, self.fout)
                                parsed = True
                                fin.close()
                            
                            except Exception, value:
                                self.fout.write("Error in text/plain : %s Value: %s\n"%(PlatformMethods.Encode(filePath), value))
                                
                                
                        elif mimeType == 'text/html':
                            try:
                                textParser.parse(DocID, HTMLParser.getText(filePath), filePath, self.FileScanStartTime, self.fout)
                                parsed = True
                            except Exception, value:
                                self.fout.write("Error in HTMLParser : %s Value: %s\n"%(PlatformMethods.Encode(filePath), value))
                                
                            
                        elif mimeType == 'text/xml':
                            #db, docID, filePath, startTime, logFile, Stopwords=[], Stemmer=None)
                            try:
                                sgmlParser = SGMLParser.SGMLXMLParser(db, DocID, filePath, self.FileScanStartTime, self.fout, Globals.Stopwords, self.Stemmer)
                                fin = open(filePath, 'rb')
                                sgmlParser.feed(fin.read())
                                sgmlParser.handleWords()
                                fin.close()
                                parsed = True
                            except Exception, value:
                                self.fout.write("Error in SGMLXMLParser : %s Value: %s\n"%(PlatformMethods.Encode(filePath), value))
                                
                            
                        elif mimeType.find('text') == 0:
                            #db, docID, filePath, startTime, logFile, Stopwords=[], Stemmer=None)
                            try:
                                sgmlParser = SGMLParser.SGMLXMLParser(db, DocID, filePath, self.FileScanStartTime, self.fout, Globals.Stopwords, self.Stemmer)
                                fin = open(filePath, 'rb')
                                sgmlParser.feed(fin.read())
                                sgmlParser.handleWords()
                                fin.close()
                                parsed = True
                            except Exception, value:
                                self.fout.write("Error in SGMLXMLParser : %s Value: %s\n"%(PlatformMethods.Encode(filePath), value))
                                
                        else:
                            try:
                                #read everything else as binary file
                                fin = open(filePath, 'rb')
                                textParser.parse(DocID, fin.read(), filePath, self.FileScanStartTime, self.fout)
                                fin.close()
                                parsed = True
                            except Exception, value:
                                self.fout.write("Error in binary text : %s Value: %s\n"%(PlatformMethods.Encode(filePath), value))
                                parsed = True
                                
                    else:
                        parsed = True
                        
                    """
                    except Exception, value:
                        self.fout.write("Error in binary text : %s Value: %s\n"%(PlatformMethods.Encode(filePath), value))
                        parsed = True
                    """
                        
                    if not parsed:
                        try:
                            fin = open(filePath, 'rb')
                            textParser.parse(DocID, fin.read(), filePath, self.FileScanStartTime, self.fout)
                            fin.close()
                        except Exception, value:
                            self.fout.write("Error in binary text : %s Value: %s\n"%(PlatformMethods.Encode(filePath), value))
                            
                            
                    self.ElapsedTime = CommonFunctions.ConvertSecondsToDayHourMinSec(time.time() - self.StartTime)
                                      
                    if (time.time() - self.EventStart) > 10:
                        #print time.time() - self.EventStart
                        self.ElapsedTime = CommonFunctions.ConvertSecondsToDayHourMinSec(time.time() - self.StartTime)
                        self.SendEvent()
                        
        
            self.fout.write('Done Indexing Attachments!\n')
            self.fout.write('Finished at: %s\n'%(time.ctime()))
        else:
            self.fout.write('Not Indexing Attachments!\n')
        
        self.fout.write('Total Time Elapsed: %s\n'%CommonFunctions.ConvertSecondsToDayHourMinSec(time.time() - self.StartTime))
        self.fout.close()
        #CommonFunctions.ShowErrorMessage(self, 'Done Parsing Emails!', False)

        
        #print 'writing terms into database'
        #self.WriteTermsInDatabase(db)   
        #self.UpdateWordCount(db)
        #self.UpdateTF(db)
        
        #print 'dumping bitmap into database'
        #self.DumpBitMapInDatabase(db)
        #print 'All Done!'
        #self.UpdateIDF(db)
        db.CloseConnection()
        
        Globals.frmGlobalEmails.RefreshScreen()
        #self.ParseStatus = "Done Updating Inverse Document Frequency!"
        self.SendEvent()
        
        finishTime = time.time()
        self.ElapsedTime = CommonFunctions.ConvertSecondsToDayHourMinSec(finishTime - self.StartTime)
        self.ParseStatus = "Done Preprocessing/Indexing Emails!"
        self.SendEvent()
        self.running = False
               

    
    def GetDirCount(self):
        return self.DirCount
    
    def GetFilesCount(self):
        return self.FilesCount
    
    def SendEvent(self):
        evt = UpdateLabelEvent(elapsedTime = self.ElapsedTime, 
            filesCount = self.FilesCount, scanStatus = self.ParseStatus)
        wx.PostEvent(self.win, evt)
        self.EventStart = time.time()
        
    
    def WriteTermsInDatabase(self, db):
        manyValues = []
        query = "INSERT INTO %s (ID, Word) values (?, ?)"%(Constants.TextCatWordsTable)
        for fword in Globals.EmailsWordFrequency:
            manyValues.append((Globals.EmailsWordFrequency[fword]['id'], fword))
            #'" + str(Globals.EmailsWordFrequency[fword]['id']) + "' "
            #query += ", " + db.SqlSQuote(fword) + ");"
            #db.ExecuteNonQuery(query)
        #print query
        #print manyValues
        db.ExecuteMany(query, manyValues)
        
        manyValues = []
        if len(Globals.EmailsStemmedWordFrequency) > 0:
            query = "INSERT INTO %s (ID, Word) values (?, ?)"%(Constants.TextCatStemmedWordsTable)
            for fword in Globals.EmailsStemmedWordFrequency:
                tupleValues = (Globals.EmailsStemmedWordFrequency[fword]['id'], fword)
                manyValues.append(tupleValues)
                
            db.ExecuteMany(query, manyValues)
            
    
    """
    def InitializeDocsInfo(self):
        for fword in Globals.EmailsWordFrequency:
            Globals.EmailsWordFrequency[fword]['count'] = 0
        
        for fword in Globals.EmailsStemmedWordFrequency:
            Globals.EmailsStemmedWordFrequency[fword]['count'] = 0
        
        #self.WordCount = 0
        #self.StemmedWordCount = 0
    """        
    
    def UpdateDocumentDatabase(self, db, Path, fileName):
        query = "INSERT INTO %s (ID, Path, FileName) values (?,?,?)"%Constants.TextCatDocumentsTable
        #query += str(self.DocID) + ", " + db.SqlSQuote(Path) + "," + db.SqlSQuote(fileName) + ")"
        #print query
        db.ExecuteNonQuery(query, [(self.DocID, PlatformMethods.Encode(Path), PlatformMethods.Encode(fileName))])
        
        #BitMapKeys = Globals.EmailsBitMap.keys()
        #WordFreqKeys = Globals.EmailsWordFrequency.keys()
        query = "INSERT INTO " + Constants.TextCatBagOfWordsTable + "(DocID, WordID, Frequency, TF) values (?,?,?,?)"
        manyValues = []
        for fword in Globals.EmailsWordFrequency:
            #print str(Globals.EmailsWordFrequency[fword]['count'])
            #print str(Globals.EmailsWordFrequency[fword]['id'])
            if Globals.EmailsWordFrequency[fword]['count'] > 0:
                #if Path.find(fword) >= 0 or fileName.find(fword):
                #    inPath = 1
                #else:
                #    inPath = 0
                #inPath = 0   
                tupleValues = (self.DocID, Globals.EmailsWordFrequency[fword]['id'], Globals.EmailsWordFrequency[fword]['count'], float(Globals.EmailsWordFrequency[fword]['count'])/float(self.WordCount))
                manyValues.append(tupleValues)
                """
                query1 = "'" + str(Globals.EmailsWordFrequency[fword]['id']) + "' "
                query1 += ", '" + str(Globals.EmailsWordFrequency[fword]['count']) + "');"
                self.SqliteDB.ExecuteNonQuery(query + query1)
                """
                if Globals.EmailsBitMap.has_key(fword):
                    Globals.EmailsBitMap[fword]['bitmap'] += '1'
                else:
                    #fillzeros = ''
                    bit = '1'#Globals.EmailsBitMap[fword] = {'bitmap': '1'}
                    Globals.EmailsBitMap[fword] = {'bitmap':string.zfill(bit, self.DocID)}
        
        db.ExecuteMany(query, manyValues)

        #fill zeros for the existing keys but not in this doc
        for kword in Globals.EmailsBitMap:
            if len(Globals.EmailsBitMap[kword]['bitmap']) < self.DocID:
                Globals.EmailsBitMap[kword]['bitmap'] += '0'
        
        
        if len(Globals.EmailsStemmedWordFrequency) > 0:
            query = "INSERT INTO %s (DocId, WordID, Frequency, TF) values (?,?,?,?)"%(Constants.TextCatBagOfStemmedWordsTable)
            manyValues = []
            for fword in Globals.EmailsStemmedWordFrequency:
                #print str(Globals.EmailsWordFrequency[fword]['count'])
                #query = "update %s set TF = '%f' where DocID = '%d' and WordID = '%d';"%(float(rowTF[2])/float(row[1]), rowTF[0], rowTF[1]) 
                #print str(Globals.EmailsWordFrequency[fword]['id'])
                if Globals.EmailsStemmedWordFrequency[fword]['count'] > 0:
                    """
                    if Path.find(fword) >= 0 or fileName.find(fword):
                        inPath = 1
                    else:
                        inPath = 0
                    """
                    tupleValues = (self.DocID, Globals.EmailsStemmedWordFrequency[fword]['id'], Globals.EmailsStemmedWordFrequency[fword]['count'], float(Globals.EmailsStemmedWordFrequency[fword]['count'])/float(self.StemmedWordCount))
                    manyValues.append(tupleValues)
            db.ExecuteMany(query, manyValues)
        
        #Update WordCount
        query = "update %s set WordCount = ? where ID = ?;"%(Constants.TextCatDocumentsTable)
        db.ExecuteNonQuery(query, (self.outlookTextParser.GetWordCount(), self.DocID,))
        
        #Update StemmedWordCount
        query = "update %s set StemmedWordCount = ? where ID = ?;"%(Constants.TextCatDocumentsTable)
        db.ExecuteNonQuery(query, (self.outlookTextParser.GetStemmedWordCount(), self.DocID))
        

    def UpdateIDF(self, db):
        self.ElapsedTime = CommonFunctions.ConvertSecondsToDayHourMinSec(time.time() - self.StartTime)
        self.ParseStatus = "Updating Inverse Document Frequency!"
        self.SendEvent()
       
        
        #Update Stemmed Words IDF
        self.ElapsedTime = CommonFunctions.ConvertSecondsToDayHourMinSec(time.time() - self.StartTime)
        self.SendEvent()
        totalDocs = self.DocID
        queryIDF = "select WordID, Count(WordID) from " + Constants.TextCatBagOfStemmedWordsTable + " group by WordID order by WordID;"
        rowsIDF = db.FetchAllRows(queryIDF)
        #N = 21578.0
        #print 'doc count = %d' %docCount
        for row in rowsIDF:
            query = "update %s set IDF = ? where WordID = ?"%(Constants.TextCatBagOfStemmedWordsTable)
            #print query
            db.ExecuteNonQuery(query,  (math.log(totalDocs/float(row[1]), 10), row[0]))

        self.ParseStatus = "Done Updating Inverse Document Frequency!"
        self.SendEvent()

    def DumpBitMapInDatabase(self, db):
        
        """
        Encode bitmap for each word using RLE encoding technique
        and update the dictionary adding another field
        """
        self.ElapsedTime = CommonFunctions.ConvertSecondsToDayHourMinSec(time.time() - self.StartTime)
        self.ParseStatus = "Updating Database Index!"
        self.SendEvent()
        manyValues = []
        i = 0
        query = "INSERT INTO " + Constants.TextCatBitMapIndex + " (Keyword, Bitmap, Compressed) values (?,?,?)"
        for kword in Globals.EmailsBitMap:
            i += 1
            manyValues.append((kword, Globals.EmailsBitMap[kword]['bitmap'], MySQLdb.escape_string(binascii.rlecode_hqx(Globals.EmailsBitMap[kword]['bitmap']))))
            if i == 10000:
                try:
                    db.ExecuteMany(query, manyValues)
                except:
                    print "Exception query:: " + query + str(manyValues)
                manyValues = []
                 
        if len(manyValues) > 0:
            try:
                db.ExecuteMany(query, manyValues)
            except:
                print "Exception query:: " + query + str(manyValues[0])


    def CreateBloomFilter(self):
        #m = no. of bits for vector
        #n = no. of elements or keys to support queries
        #k = no. of hash functions
        m = 500000
        n = 100000
        k = 4
        return BloomFilter.BloomFilter(n=n, m=m, k=k)
    

# Every wxWidgets application must have a class derived from wx.App
class MyApp(wx.App):

	# wxWindows calls this method to initialize the application
	def OnInit(self):

		# Create an instance of our customized Frame class
		frame = create(None, "..\Montoya\AddressBook", "..\Montoya\Email")
		frame.Show(True)

		# Tell wxWindows that this is our main window
		self.SetTopWindow(frame)

		# Return a success flag
		return True


if __name__ == "__main__":
    app = MyApp(0)	# Create an instance of the application class
    app.MainLoop()	# Tell it to start processing events
