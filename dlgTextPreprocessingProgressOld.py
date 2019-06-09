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
import os.path, sys
#import wx.lib.delayedresult as delayedresult
import wx.lib.newevent
import  thread
import binascii
import MySQLdb

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


def create(parent):
    return dlgTextPreprocessingProgress(parent)

[wxID_DLGTEXTPREPROCESSINGPROGRESS, 
 wxID_DLGTEXTPREPROCESSINGPROGRESSBTNCANCEL, 
 wxID_DLGTEXTPREPROCESSINGPROGRESSBTNOK, 
 wxID_DLGTEXTPREPROCESSINGPROGRESSLBLELAPSEDTIME, 
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
 wxID_DLGTEXTPREPROCESSINGPROGRESSSTATICTEXT6, 
 wxID_DLGTEXTPREPROCESSINGPROGRESSSTATICTEXT8, 
] = [wx.NewId() for _init_ctrls in range(16)]

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
              pos=wx.Point(846, 363), size=wx.Size(565, 315), style=0,
              title=u'Text Preprocessing Status...')
        self._init_utils()
        self.SetClientSize(wx.Size(557, 284))
        self.SetAutoLayout(True)
        self.SetIcon(wx.Icon('./Images/FNSFIcon.ico',wx.BITMAP_TYPE_ICO))
        self.SetBackgroundColour(wx.Colour(125, 152, 221))
        self.SetCursor(wx.STANDARD_CURSOR)
        self.SetMinSize(wx.Size(-1, -1))
        self.Center(wx.BOTH)
        self.Bind(wx.EVT_CLOSE, self.OnDlgTextPreprocessingProgressClose)

        self.panScanStatus = wx.Panel(id=wxID_DLGTEXTPREPROCESSINGPROGRESSPANSCANSTATUS,
              name=u'panScanStatus', parent=self, pos=wx.Point(16, 16),
              size=wx.Size(528, 224), style=wx.TAB_TRAVERSAL)
        self.panScanStatus.SetBackgroundColour(wx.Colour(225, 236, 255))

        self.lblStartTime = wx.StaticText(id=wxID_DLGTEXTPREPROCESSINGPROGRESSLBLSTARTTIME,
              label=u'Start Time', name=u'lblStartTime',
              parent=self.panScanStatus, pos=wx.Point(104, 128),
              size=wx.Size(136, 13), style=0)

        self.staticText2 = wx.StaticText(id=wxID_DLGTEXTPREPROCESSINGPROGRESSSTATICTEXT2,
              label='Current File:', name='staticText2',
              parent=self.panScanStatus, pos=wx.Point(32, 80), size=wx.Size(60,
              13), style=wx.ALIGN_RIGHT)

        self.staticText3 = wx.StaticText(id=wxID_DLGTEXTPREPROCESSINGPROGRESSSTATICTEXT3,
              label=u'Elapsed Time:', name='staticText3',
              parent=self.panScanStatus, pos=wx.Point(16, 200), size=wx.Size(82,
              13), style=wx.ALIGN_RIGHT)

        self.lblElapsedTime = wx.StaticText(id=wxID_DLGTEXTPREPROCESSINGPROGRESSLBLELAPSEDTIME,
              label=u'0 s', name=u'lblElapsedTime', parent=self.panScanStatus,
              pos=wx.Point(104, 200), size=wx.Size(14, 13), style=0)

        self.lblTotalDir = wx.StaticText(id=wxID_DLGTEXTPREPROCESSINGPROGRESSLBLTOTALDIR,
              label=u'0', name=u'lblTotalDir', parent=self.panScanStatus,
              pos=wx.Point(104, 152), size=wx.Size(40, 13), style=0)

        self.staticText4 = wx.StaticText(id=wxID_DLGTEXTPREPROCESSINGPROGRESSSTATICTEXT4,
              label=u'Directories Count:', name='staticText4',
              parent=self.panScanStatus, pos=wx.Point(8, 152), size=wx.Size(87,
              16), style=wx.ALIGN_RIGHT)

        self.staticText5 = wx.StaticText(id=wxID_DLGTEXTPREPROCESSINGPROGRESSSTATICTEXT5,
              label=u'Files Count:', name='staticText5',
              parent=self.panScanStatus, pos=wx.Point(8, 176), size=wx.Size(89,
              13), style=wx.ALIGN_RIGHT)

        self.lblFilesCount = wx.StaticText(id=wxID_DLGTEXTPREPROCESSINGPROGRESSLBLFILESCOUNT,
              label=u'0', name=u'lblFilesCount', parent=self.panScanStatus,
              pos=wx.Point(104, 176), size=wx.Size(6, 13), style=0)

        self.lblScanStatus = wx.StaticText(id=wxID_DLGTEXTPREPROCESSINGPROGRESSLBLSCANSTATUS,
              label=u'Done Text Preprocessing and Indexing!',
              name=u'lblScanStatus', parent=self.panScanStatus,
              pos=wx.Point(152, 48), size=wx.Size(253, 16), style=0)
        self.lblScanStatus.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, u'MS Shell Dlg 2'))
        self.lblScanStatus.SetForegroundColour(wx.Colour(255, 0, 0))
        self.lblScanStatus.Show(True)

        self.btnOK = wx.Button(id=wxID_DLGTEXTPREPROCESSINGPROGRESSBTNOK,
              label=u'&OK', name=u'btnOK', parent=self, pos=wx.Point(256, 248),
              size=wx.Size(88, 24), style=0)
        self.btnOK.Show(False)
        self.btnOK.Bind(wx.EVT_BUTTON, self.OnBtnOKButton,
              id=wxID_DLGTEXTPREPROCESSINGPROGRESSBTNOK)

        self.btnCancel = wx.Button(id=wxID_DLGTEXTPREPROCESSINGPROGRESSBTNCANCEL,
              label=u'&Cancel', name=u'btnCancel', parent=self,
              pos=wx.Point(256, 248), size=wx.Size(88, 24), style=0)
        self.btnCancel.Bind(wx.EVT_BUTTON, self.OnBtnCancelButton,
              id=wxID_DLGTEXTPREPROCESSINGPROGRESSBTNCANCEL)

        self.staticText1 = wx.StaticText(id=wxID_DLGTEXTPREPROCESSINGPROGRESSSTATICTEXT1,
              label=u'Start Time:', name='staticText1',
              parent=self.panScanStatus, pos=wx.Point(8, 128), size=wx.Size(88,
              13), style=wx.ALIGN_RIGHT)

        self.staticText6 = wx.StaticText(id=wxID_DLGTEXTPREPROCESSINGPROGRESSSTATICTEXT6,
              label='lblFileName', name='staticText6',
              parent=self.panScanStatus, pos=wx.Point(104, 80),
              size=wx.Size(416, 40), style=wx.ST_NO_AUTORESIZE)

        self.staticText8 = wx.StaticText(id=wxID_DLGTEXTPREPROCESSINGPROGRESSSTATICTEXT8,
              label='staticText8', name='staticText8',
              parent=self.panScanStatus, pos=wx.Point(248, 8), size=wx.Size(54,
              32), style=0)

    def __init__(self, parent):
        
        self._init_ctrls(parent)
        self.InitThrober()
        self.Bind(EVT_UPDATE_LABEL, self.OnUpdate)
        self.lblScanStatus.SetLabel("Indexing in Progress...")
        #self.db = SqliteDatabase(Globals.MACFileName)
        #self.db.OpenConnection()
        self.StartTime = 0
        self.scanStarted = False
        #self.ReadFilePropertiesToGet()
        self.jobID = 0
        self.StartTimer()
        #return
        self.scanThread = FileScanThread(self, self.StartTime)
        self.ScanFinished = False
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
        self.timer1.Start(30000) #1/2 min
        self.lblStartTime.SetLabel(str(time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())))
        self.lblStartTime.Refresh()
        return None
    
       
        
    def OnUpdate(self, evt):
        self.lblTotalDir.SetLabel(PlatformMethods.Convert(evt.totalDir))
        self.lblElapsedTime.SetLabel(PlatformMethods.Convert(evt.elapsedTime))
        #self.lblCurrentDir.SetLabel(PlatformMethods.Convert(evt.currentDir))
        self.lblFilesCount.SetLabel(PlatformMethods.Convert(evt.filesCount))
        #self.lblTotalFiles.SetLabel(PlatformMethods.Convert(evt.totalFiles))
        #self.CurrentFileName = file
        self.lblScanStatus.SetLabel(PlatformMethods.Convert(evt.scanStatus))
        if str(evt.scanStatus) == "Done Preprocessing/Indexing!":
            self.throbber1.Stop()
            self.btnOK.Show(True)
            self.btnCancel.Show(False)
            self.timer1.Stop()
        self.RefreshLabels()
        evt.Skip()

        
    def RefreshLabels(self):
        #self.panFrequencyCounts.Refresh()
        #self.lblTotalFiles.Refresh()
        self.lblFilesCount.Refresh()
        self.lblTotalDir.Refresh()
        #self.lblStartTime.Refresh()
        self.lblElapsedTime.Refresh()
        #self.lblCurrentDir.Refresh()
        #self.staticText1.Refresh()
        #self.staticText2.Refresh()
        #self.staticText3.Refresh()
        #self.staticText4.Refresh()
        #self.staticText5.Refresh()
        #self.staticText6.Refresh()
        #self.Refresh()
        

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
                    #self.db.ExecuteNonQuery(query)
                    self.Close()
        finally:
            dlg.Destroy()

            

    def OnDlgScanProgressClose(self, event):
        event.Skip()
            
    

    def OnTimer1Timer(self, event):
        ElapsedTime = CommonFunctions.ConvertSecondsToDayHourMinSec(time.time() - self.StartTime)
        self.lblTotalDir.SetLabel(PlatformMethods.Convert(self.scanThread.GetDirCount()))
        self.lblElapsedTime.SetLabel(PlatformMethods.Convert(ElapsedTime))
        #self.lblCurrentDir.SetLabel(PlatformMethods.Convert(evt.currentDir))
        self.lblFilesCount.SetLabel(PlatformMethods.Convert(self.scanThread.GetFilesCount()))
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
    def __init__(self, win, startTime):
        import HTMLParser
        self.win = win
        self.StartTime = startTime
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
        DBFunctions.SetupTextCatTables(Globals.TextCatFileName)
        
        """
        self.timerStatus = wx.Timer(id=wx.NewId(), owner=self)
        self.Bind(wx.EVT_TIMER, self.OnTimerStatusTimer,
              id=self.timerStatus.GetId())
        """
        self.EventStart = time.time()
        self.splitter = re.compile(r'\W*')
        #self.DigitWord = re.compile(r'[a-z]*\d+[a-z]*', re.I)
        if Globals.Stemmer == "Porter Stemmer":
            self.Stemmer = PorterStemmer()
            #self.UseStemmer = True
        self.htmlParser = HTMLParser.HTMLParser(self.Stemmer)   
        self.textParser = TextParser.TextParser(self.Stemmer)
        """
        self.timerStatus = wx.Timer(id=wx.NewId(),
              owner=self)
        self.Bind(wx.EVT_TIMER, self.OnTimerStatusTimer,
              id=timerStatus.GetId())
        #Globals.frmGlobalMainForm.treeKeywords.GetTextCatDirList()
        #DBFunctions.SetupKeywordsFrequencyTable(Globals.TextCatFileName)
        #self.InitializeKeyWordsFrequencyDictionary()
        """
        
    def Start(self):
        #self.timerStatus.Start(1000000)
        self.keepGoing = self.running = True
        thread.start_new_thread(self.Run, ())
        
        
    def Stop(self):
        self.keepGoing = False
        #self.db.CloseConnection()
        
    """
    def OnTimerStatusTimer(self, event):
        self.SendEvent()
        event.Skip()
    """   
        
    def IsRunning(self):
        return self.running
    
    def Run(self):
        db = SqliteDatabase(Globals.TextCatFileName)
        if not db.OpenConnection():
            return
        
        #print Globals.TextCatDirList
        for dir in Globals.TextCatDirList:
        #for dirName in Globals.EvidencesDict['Evidence1']['Dir
            #print dir
            if not os.path.isdir(dir):
                continue
            
            if not self.keepGoing:
                self.running = False
                return
            
            self.DirCount += 1
            #TotalDir += 1
            files = os.listdir(dir)
            for file in files:
                if not self.keepGoing:
                    self.running = False
                    return
                
                filePath = os.path.join(dir, file)
                if not os.path.isfile(filePath):
                    continue

                if (filePath.rfind('.') == -1):
                    continue
                
                try:
                    #if not (filePath.rfind('.') == -1):
                    extension = filePath[filePath.rfind('.'):]
                    fileType = wx.TheMimeTypesManager.GetFileTypeFromExtension(extension)
                    if fileType:
                        mimeType = fileType.GetMimeType() or "Unknown"
                        if mimeType in Globals.TextCatCategoryList:
                            #self.ReadFile(filePath)
                            
                            if mimeType == "text/plain":
                                #print 'plain text'
                                self.textParser.parse(filePath, self.WordID, self.StemmedWordID)
                                self.WordID = self.textParser.GetWordID()
                                self.StemmedWordID = self.textParser.GetStemmedWordID()
                                self.WordCount = self.textParser.GetWordCount()
                                self.StemmedWordCount = self.textParser.GetStemmedWordCount()
                            else: # mimeType == "text/html": 
                                fin = open(filePath, "r")
                                data = fin.read()
                                self.htmlParser.ResetCounters()
                                #while data:
                                self.htmlParser.parse(data, self.WordID, self.StemmedWordID)
                                """
                                for line in data:
                                    if self.UseStemmer:
                                        self.PreprocessDataUsingStemmer(line)
                                    else:
                                        self.PreprocessDataWithoutStemmer(line)
                                """
                                #data = fin.read()
                                #data = fin.readlines()
                                self.WordID = self.textParser.GetWordID()
                                self.StemmedWordID = self.textParser.GetStemmedWordID()

                                self.WordCount = self.htmlParser.GetWordCount()
                                self.StemmedWordCount = self.htmlParser.GetStemmedWordCount()
                                fin.close()
                                
                            self.FilesCount += 1
                            #TotalFiles += 1
                            self.ElapsedTime = CommonFunctions.ConvertSecondsToDayHourMinSec(time.time() - self.StartTime)
                            self.DocID += 1
                            
                            self.UpdateDocumentDatabase(db, dir, file)
                            self.InitializeDocsInfo()
                    
                    if (time.time() - self.EventStart) > 10:
                        #print time.time() - self.EventStart
                        self.ElapsedTime = CommonFunctions.ConvertSecondsToDayHourMinSec(time.time() - self.StartTime)
                        self.SendEvent()
                except Exception, value:
                    #print "Failed to read file: %s Error: %s"%(filePath, value)
                    try:
                        print filePath, value
                    except:
                        continue
                 
        self.WriteTermsInDatabase(db)   
        #self.UpdateWordCount(db)
        #self.UpdateTF(db)
        self.DumpBitMapInDatabase(db)
        #self.UpdateIDF(db)
        db.CloseConnection()
        
        #self.ParseStatus = "Done Updating Inverse Document Frequency!"
        self.SendEvent()
        
            
        #db = SqliteDatabase(Globals.CurrentProjectFile)
        #self.tokenizer.close()
        finishTime = time.time()
        self.ElapsedTime = CommonFunctions.ConvertSecondsToDayHourMinSec(finishTime - self.StartTime)
        self.ParseStatus = "Done Preprocessing/Indexing!"
        self.SendEvent()
        self.running = False

    
    def GetDirCount(self):
        return self.DirCount
    
    def GetFilesCount(self):
        return self.FilesCount
    
    def SendEvent(self):
        evt = UpdateLabelEvent(elapsedTime = self.ElapsedTime, 
            filesCount = self.FilesCount, totalDir = self.DirCount,
            scanStatus = self.ParseStatus)
        wx.PostEvent(self.win, evt)
        self.EventStart = time.time()
        
    
    def WriteTermsInDatabase(self, db):
        """
        db = SqliteDatabase(Globals.TextCatFileName)
        if not db.OpenConnection():
            return
        """
        manyValues = []
        query = "INSERT INTO " + Constants.TextCatWordsTable + " (ID, Word) values (?, ?)"
        for fword in Globals.WordFrequency:
            tupleValues = (Globals.WordFrequency[fword]['id'], MySQLdb.escape_string(fword))
            manyValues.append(tupleValues)
            #'" + str(Globals.WordFrequency[fword]['id']) + "' "
            #query += ", " + db.SqlSQuote(fword) + ");"
            #db.ExecuteNonQuery(query)
        db.ExecuteMany(query, manyValues)
        
        """
        manyValues = []
        query = "INSERT INTO " + Constants.TextCatStemmedWordsTable + " (ID, Word) values (?, ?)"
        for fword in Globals.StemmedWordFrequency:
            tupleValues = (Globals.StemmedWordFrequency[fword]['id'], MySQLdb.escape_string(fword))
            manyValues.append(tupleValues)
            
        db.ExecuteMany(query, manyValues)
        #db.CloseConnection()
        """
        
                
    """
    def PreprocessDataUsingStemmer(self, data):
        data = string.lower(data)
        #print data
        #myList = re.split(self.splitter, data)
        myList = data.split()
        #if data <> '\n' and data <> '\r\n' and (not re.search(r'(&nbsp;)+', data)):
        #print myList
        for word in myList:
            word = word.strip()
            #if len(word) <=2: 
            #    continue# meaningful word must be more than 2 chars long
                #if not re.match(self.badWords, word) and word <> '': # keep only the words that start with an alphabet                
                #if not self.CheckBadCharPresent(word) and word <> '':
                #if word <> '': # and not self.NonDigitWord.match(word):
            #if self.DigitWord.match(word):
            #    continue
            #if not self.AlphaNumericWord.match(word) and not self.DigitWord.match(word):
            #if self.AlphabeticWord.match(word):
            #print newWord
            word = string.replace(word, "'", '')
            word = string.replace(word, '"', '')
            word = string.replace(word, '?', '')
            #word = string.replace(newWord, '.', '') #email address may have .
            word = string.replace(word, ',', '')
            word = string.replace(word, ';', '')
            word = string.replace(word, ':', '')
            
            if Globals.WordFrequency.has_key(word):
                Globals.WordFrequency[word]['count'] += 1
                self.WordCount += 1
            else:
                if word not in Globals.Stopwords:
                    #if Globals.WordFrequency.has_key(word):
                    #Globals.WordFrequency[word]['count'] += 1
                    #else:
                    self.WordCount += 1
                    self.WordID += 1
                    Globals.WordFrequency[word] = {'id': self.WordID, 'count' : 1}
                
                #self.WordFrequency[word]['bitMapped'] = 1
            if Globals.StemmedWordFrequency.has_key(word):
                Globals.StemmedWordFrequency[word]['count'] += 1
                self.StemmedWordCount += 1
            else:
                if word not in Globals.Stopwords:
                    word = self.Stemmer.stem(word, 0,len(word)-1) #Apply Porter Stemmer to each word
                    if Globals.StemmedWordFrequency.has_key(word):
                        Globals.StemmedWordFrequency[word]['count'] += 1
                        self.StemmedWordCount += 1
                    else:
                        self.StemmedWordCount += 1
                        self.StemmedWordID += 1
                        Globals.StemmedWordFrequency[word] = {'id' : self.StemmedWordID, 'count' : 1}
     """                   
                            
       
    def InitializeDocsInfo(self):
        for fword in Globals.WordFrequency:
            Globals.WordFrequency[fword]['count'] = 0
        
        for fword in Globals.StemmedWordFrequency:
            Globals.StemmedWordFrequency[fword]['count'] = 0
        
        #self.WordCount = 0
        #self.StemmedWordCount = 0
             
    def UpdateDocumentDatabase(self, db, Path, fileName):
        query = "INSERT INTO " + Constants.TextCatDocumentsTable + " (ID, Path, FileName) values ("
        query += str(self.DocID) + ", " + db.SqlSQuote(Path) + "," + db.SqlSQuote(fileName) + ")"
        #print query
        db.ExecuteNonQuery(query)
        
        #BitMapKeys = Globals.BitMap.keys()
        #WordFreqKeys = Globals.WordFrequency.keys()
        query = "INSERT INTO " + Constants.TextCatBagOfWordsTable + "(DocID, WordID, InPath, Frequency, TF) values (?,?,?,?,?)"
        manyValues = []
        for fword in Globals.WordFrequency:
            #print str(Globals.WordFrequency[fword]['count'])
            #print str(Globals.WordFrequency[fword]['id'])
            if Globals.WordFrequency[fword]['count'] > 0:
                if Path.find(fword) >= 0 or fileName.find(fword):
                    inPath = 1
                else:
                    inPath = 0
                    
                tupleValues = (self.DocID, Globals.WordFrequency[fword]['id'], inPath, Globals.WordFrequency[fword]['count'], float(Globals.WordFrequency[fword]['count'])/float(self.WordCount))
                manyValues.append(tupleValues)
                """
                query1 = "'" + str(Globals.WordFrequency[fword]['id']) + "' "
                query1 += ", '" + str(Globals.WordFrequency[fword]['count']) + "');"
                self.SqliteDB.ExecuteNonQuery(query + query1)
                
                if Globals.BitMap.has_key(fword):
                    Globals.BitMap[fword]['bitmap'] += '1'
                else:
                    #fillzeros = ''
                    bit = '1'#Globals.BitMap[fword] = {'bitmap': '1'}
                    Globals.BitMap[fword] = {'bitmap':string.zfill(bit, self.DocID)}
                """
        
        db.ExecuteMany(query, manyValues)                 

        #fill zeros for the existing keys but not in this doc
        """
        for kword in Globals.BitMap:
            if len(Globals.BitMap[kword]['bitmap']) < self.DocID:
                Globals.BitMap[kword]['bitmap'] += '0'
        """
        """
        query = "INSERT INTO " + Constants.TextCatBagOfStemmedWordsTable + "(DocId, WordID, InPath, Frequency, TF) values (?,?,?,?,?)"
        manyValues = []
        for fword in Globals.StemmedWordFrequency:
            #print str(Globals.WordFrequency[fword]['count'])
            #query = "update %s set TF = '%f' where DocID = '%d' and WordID = '%d';"%(float(rowTF[2])/float(row[1]), rowTF[0], rowTF[1]) 
            #print str(Globals.WordFrequency[fword]['id'])
            if Globals.StemmedWordFrequency[fword]['count'] > 0:
                if Path.find(fword) >= 0 or fileName.find(fword):
                    inPath = 1
                else:
                    inPath = 0
                tupleValues = (self.DocID, Globals.StemmedWordFrequency[fword]['id'], inPath, Globals.StemmedWordFrequency[fword]['count'], float(Globals.StemmedWordFrequency[fword]['count'])/float(self.StemmedWordCount))
                manyValues.append(tupleValues)
        db.ExecuteMany(query, manyValues)
        """
        #Update WordCount
        query = "update " + Constants.TextCatDocumentsTable + " set WordCount = '%d' where ID = '%d';"%(self.htmlParser.GetWordCount(), self.DocID)
        db.ExecuteNonQuery(query)
        
        #Update StemmedWordCount
        query = "update " + Constants.TextCatDocumentsTable + " set StemmedWordCount = '%d' where ID = '%d';"%(self.htmlParser.GetStemmedWordCount(), self.DocID)
        db.ExecuteNonQuery(query)
        
        
   

    def UpdateIDF(self, db):
        self.ElapsedTime = CommonFunctions.ConvertSecondsToDayHourMinSec(time.time() - self.StartTime)
        self.ParseStatus = "Updating Inverse Document Frequency!"
        self.SendEvent()
        """
        query = "select count(ID) from " + Constants.TextCatDocumentsTable + ";"
        rows = db.FetchAllRows(query)
        docCount = 0.0
        for row in rows:
            docCount = float(row[0])
            
        queryIDF = "select WordID, Count(WordID) from " + Constants.TextCatBagOfWordsTable + " group by WordID order by WordID;"
        rowsIDF = db.FetchAllRows(queryIDF)
        #N = 21578.0
        #print 'doc count = %d' %docCount
        for row in rowsIDF:
            #idf = math.log(float(21578)/float(row[1]), 2)
            #print "row[1] = %d" %(row[1])
            query = "update " + Constants.TextCatBagOfWordsTable + " set IDF = '%f' where WordID = '%d'"%(math.log(docCount/float(row[1]), 10), row[0])
            #print query
            db.ExecuteNonQuery(query)      
            #break
        
        """
        
        
        #Update Stemmed Words IDF
        self.ElapsedTime = CommonFunctions.ConvertSecondsToDayHourMinSec(time.time() - self.StartTime)
        self.SendEvent()
        totalDocs = self.DocID
        queryIDF = "select WordID, Count(WordID) from " + Constants.TextCatBagOfStemmedWordsTable + " group by WordID order by WordID;"
        rowsIDF = db.FetchAllRows(queryIDF)
        #N = 21578.0
        #print 'doc count = %d' %docCount
        for row in rowsIDF:
            query = "update " + Constants.TextCatBagOfStemmedWordsTable + " set IDF = '%f' where WordID = '%d'"%(math.log(totalDocs/float(row[1]), 10), row[0])
            #print query
            db.ExecuteNonQuery(query)
        
        """
        totalDocs = self.DocID
        for fword in Globals.StemmedWordFrequency:
            #for kword in Globals.BitMap:
            wordDocCount = 0
            for bit in Globals.BitMap[fword]['bitmap']:
                docCount += int(bit)
            
            query = "update " + Constants.TextCatBagOfStemmedWordsTable + " set IDF = '%f' where WordID = '%d'"%(math.log(totalDocs/float(wordDocCount), 10), Globals.StemmedWordFrequency[fword]['id'])
            db.ExecuteNonQuery(query)
        """ 
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
        for kword in Globals.BitMap:
            i += 1
            manyValues.append((kword, Globals.BitMap[kword]['bitmap'], MySQLdb.escape_string(binascii.rlecode_hqx(Globals.BitMap[kword]['bitmap']))))
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
                
    """
    def UpdateWordCount(self, db):
        self.ElapsedTime = CommonFunctions.ConvertSecondsToDayHourMinSec(time.time() - self.StartTime)
        self.ParseStatus = "Updating Word Count!"
        self.SendEvent()
        query = "select DocID, Sum(Frequency) from " + Constants.TextCatBagOfWordsTable + " group by DocID order by DocID;"
        rows = db.FetchAllRows(query)
        i = 0
        query1 = "update " + Constants.TextCatDocumentsTable + " set WordCount = '"
        for row in rows:
            query2 = str(row[1]) + "' where ID = '" + str(row[0]) + "';"
            db.ExecuteNonQuery(query1 + query2)
            
        self.ElapsedTime = CommonFunctions.ConvertSecondsToDayHourMinSec(time.time() - self.StartTime)    
        self.SendEvent()
        #Update BagOfStemmedWords table
        query = "select DocID, Sum(Frequency) from " + Constants.TextCatBagOfStemmedWordsTable + " group by DocID order by DocID;"
        rows = db.FetchAllRows(query)
        i = 0
        query1 = "update " + Constants.TextCatDocumentsTable + " set StemmedWordCount = '"
        for row in rows:
            query2 = str(row[1]) + "' where ID = '" + str(row[0]) + "';"
            db.ExecuteNonQuery(query1 + query2)
        self.ParseStatus = "Done Updating Word Count!"
        self.SendEvent()
            
    def UpdateTF(self, db):
        
        self.ElapsedTime = CommonFunctions.ConvertSecondsToDayHourMinSec(time.time() - self.StartTime)
        self.ParseStatus = "Updating Term Frequency!"
        self.SendEvent()
           
        query = "select ID, WordCount from " + Constants.TextCatDocumentsTable + " order by ID;"
        
        rowsTotCount = db.FetchAllRows(query)
        for row in rowsTotCount:
            #db.ExecuteNonQuery(query1 + query2)
            #print row[0]
            query1 = "select DocID, WordID, Frequency from " + Constants.TextCatBagOfWordsTable + " where DocID = '%d';"%(int(row[0]))
            #print query1
            rowsTF = db.FetchAllRows(query1)
            for rowTF in rowsTF:
                #print "%d, %d, %d"%(rowIDF[0], rowIDF[1], rowIDF[2])
                #if int(row[0]) == int(rowTF[0]):
                query2 = " update " + Constants.TextCatBagOfWordsTable + " set TF = '%f' where DocID = '%d' and WordID = '%d';"%(float(rowTF[2])/float(row[1]), rowTF[0], rowTF[1]) 
                #print "word = %d, tf = %f"%(rowTF[1], float(rowTF[2])/float(row[1]))
                #print query2+query3
                db.ExecuteNonQuery(query2)
                #i += 1
            
        self.ElapsedTime = CommonFunctions.ConvertSecondsToDayHourMinSec(time.time() - self.StartTime)    
        self.SendEvent()
        
        
        self.ParseStatus = "Done Updating Term Frequency!"
        self.SendEvent()
    """
    
    """
    def SetupTextCatDB(self):
        db = SqliteDatabase(Globals.TextCatFileName)
        if not db.OpenConnection():
            return
            
        query = "DROP TABLE IF EXISTS " + Constants.TextCatDocumentsTable
        db.ExecuteNonQuery(query)
        
        query = "CREATE TABLE " + Constants.TextCatDocumentsTable + "( "
        query += "`ID` integer Primary Key,"
        query += "`Path` text,"
        query += "`FileName` text," #added later
        query += "`Title` text,"    #added later
        query += "`WordCount` integer," #added later
        query += "`StemmedWordCount` integer );" #added later
            
        db.ExecuteNonQuery(query)
        
        query = "DROP TABLE IF EXISTS " + Constants.TextCatBitMapIndex
        db.ExecuteNonQuery(query)
        
        query = "CREATE TABLE " + Constants.TextCatBitMapIndex + "( "
        query += "`Keyword` text Primary Key,"
        query += "`Bitmap` text,"
        query += "`Compressed` text );"
        db.ExecuteNonQuery(query)
        
        query = "DROP TABLE IF EXISTS " + Constants.TextCatBagOfWordsTable
        db.ExecuteNonQuery(query)
        
        query = "CREATE TABLE " + Constants.TextCatBagOfWordsTable + "( "
        query += "`DocID` numeric,"
        query += "`WordID` numeric,"
        query += "`InPath` integer,"
        query += "`Frequency` numeric,"
        query += "`TF` numeric,"
        query += "`IDF` numeric,"
        query += "Primary Key (DocID, WordID) );"
        
        db.ExecuteNonQuery(query)
        
        query = "DROP TABLE IF EXISTS " + Constants.TextCatBagOfStemmedWordsTable
        db.ExecuteNonQuery(query)
        
        query = "CREATE TABLE " + Constants.TextCatBagOfStemmedWordsTable + "( "
        query += "`DocID` numeric,"
        query += "`WordID` numeric,"
        query += "`InPath` integer,"
        query += "`Frequency` numeric,"
        query += "`TF` numeric,"
        query += "`IDF` numeric,"
        query += "Primary Key (DocID, WordID) );"
        
        db.ExecuteNonQuery(query)
        
        query = "DROP TABLE IF EXISTS " + Constants.TextCatWordsTable
        db.ExecuteNonQuery(query)
        
        query = "CREATE TABLE " + Constants.TextCatWordsTable + "( "
        #query += "`ID` integer Primary Key, "
        query += "`ID` integer, "
        query += "`Word` text);"
        db.ExecuteNonQuery(query)
        
        query = "DROP TABLE IF EXISTS " + Constants.TextCatStemmedWordsTable
        db.ExecuteNonQuery(query)
        
        query = "CREATE TABLE " + Constants.TextCatStemmedWordsTable + "( "
        query += "`ID` integer Primary Key, "
        query += "`Word` text);"
        db.ExecuteNonQuery(query)
        
        db.CloseConnection()

    """
