#-----------------------------------------------------------------------------
# Name:        dlgNSRLProgress.py
# Purpose:     
#
# Author:      Ram B. Basnet
#
# Created:     2007/11/12
# RCS-ID:      $Id: dlgNSRLProgress.py,v 1.3 2007/11/13 19:52:48 rbasnet Exp $
# Copyright:   (c) 2006
# Licence:     <your licence>
# New field:   Whatever
#-----------------------------------------------------------------------------
#Boa:MDIChild:dlgNSRLProgress

import wx
import wx.lib.buttons
import time
import os.path, sys
#import wx.lib.delayedresult as delayedresult
import wx.lib.newevent
import  thread
import csv
import gzip

from wx.lib.anchors import LayoutAnchors

from SqliteDatabase import *
import Globals
import Constants
import PlatformMethods
import CommonFunctions
import images
import Queue
from threading import Thread

def create(parent, dirPath):
    return dlgNSRLProgress(parent, dirPath)

[wxID_DLGNSRLPROGRESS, wxID_DLGNSRLPROGRESSBTNCANCEL, 
 wxID_DLGNSRLPROGRESSBTNOK, wxID_DLGNSRLPROGRESSGAUGEDDPROGRESS, 
 wxID_DLGNSRLPROGRESSGAUGEPULSE, wxID_DLGNSRLPROGRESSLBLELAPSEDTIME, 
 wxID_DLGNSRLPROGRESSLBLESTIMATEDTIME, wxID_DLGNSRLPROGRESSLBLRATE, 
 wxID_DLGNSRLPROGRESSLBLSCANSTATUS, wxID_DLGNSRLPROGRESSPANSCANSTATUS, 
 wxID_DLGNSRLPROGRESSSTATICTEXT2, wxID_DLGNSRLPROGRESSSTATICTEXT3, 
] = [wx.NewId() for _init_ctrls in range(12)]

#----------------------------------------------------------------------

# This creates a new Event class and a EVT binder function
(UpdateLabelEvent, EVT_UPDATE_LABEL) = wx.lib.newevent.NewEvent()


#----------------------------------------------------------------------

class dlgNSRLProgress(wx.Dialog):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_DLGNSRLPROGRESS,
              name='dlgNSRLProgress', parent=prnt, pos=wx.Point(776, 357),
              size=wx.Size(451, 295), style=0,
              title='NSRL Software Hash Import Progress...')
        self.SetClientSize(wx.Size(443, 264))
        self.SetAutoLayout(True)
        self.SetBackgroundColour(wx.Colour(125, 152, 221))
        self.SetCursor(wx.STANDARD_CURSOR)
        self.SetMinSize(wx.Size(-1, -1))
        self.Center(wx.BOTH)

        self.panScanStatus = wx.Panel(id=wxID_DLGNSRLPROGRESSPANSCANSTATUS,
              name=u'panScanStatus', parent=self, pos=wx.Point(16, 16),
              size=wx.Size(416, 200), style=wx.TAB_TRAVERSAL)
        self.panScanStatus.SetBackgroundColour(wx.Colour(225, 236, 255))

        self.lblEstimatedTime = wx.StaticText(id=wxID_DLGNSRLPROGRESSLBLESTIMATEDTIME,
              label='    ', name='lblEstimatedTime', parent=self.panScanStatus,
              pos=wx.Point(96, 176), size=wx.Size(12, 13), style=0)

        self.staticText2 = wx.StaticText(id=wxID_DLGNSRLPROGRESSSTATICTEXT2,
              label='Estimated Time:', name='staticText2',
              parent=self.panScanStatus, pos=wx.Point(8, 176), size=wx.Size(76,
              13), style=wx.ALIGN_RIGHT)

        self.staticText3 = wx.StaticText(id=wxID_DLGNSRLPROGRESSSTATICTEXT3,
              label=u'Elapsed Time:', name='staticText3',
              parent=self.panScanStatus, pos=wx.Point(16, 152), size=wx.Size(66,
              13), style=wx.ALIGN_RIGHT)

        self.lblElapsedTime = wx.StaticText(id=wxID_DLGNSRLPROGRESSLBLELAPSEDTIME,
              label='    ', name=u'lblElapsedTime', parent=self.panScanStatus,
              pos=wx.Point(96, 152), size=wx.Size(12, 13), style=0)

        self.lblScanStatus = wx.StaticText(id=wxID_DLGNSRLPROGRESSLBLSCANSTATUS,
              label='Updating NSRL Software Hashes...', name=u'lblScanStatus',
              parent=self.panScanStatus, pos=wx.Point(0, 8), size=wx.Size(416,
              16), style=wx.ST_NO_AUTORESIZE | wx.ALIGN_CENTRE)
        self.lblScanStatus.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, u'MS Shell Dlg 2'))
        self.lblScanStatus.SetForegroundColour(wx.Colour(255, 0, 0))
        self.lblScanStatus.Show(True)

        self.btnOK = wx.Button(id=wxID_DLGNSRLPROGRESSBTNOK, label=u'&OK',
              name=u'btnOK', parent=self, pos=wx.Point(192, 224),
              size=wx.Size(88, 24), style=0)
        self.btnOK.Show(False)
        self.btnOK.Bind(wx.EVT_BUTTON, self.OnBtnOKButton,
              id=wxID_DLGNSRLPROGRESSBTNOK)

        self.btnCancel = wx.Button(id=wxID_DLGNSRLPROGRESSBTNCANCEL,
              label=u'&Cancel', name=u'btnCancel', parent=self,
              pos=wx.Point(192, 224), size=wx.Size(88, 24), style=0)
        self.btnCancel.Bind(wx.EVT_BUTTON, self.OnBtnCancelButton,
              id=wxID_DLGNSRLPROGRESSBTNCANCEL)

        self.gaugeDDProgress = wx.Gauge(id=wxID_DLGNSRLPROGRESSGAUGEDDPROGRESS,
              name='gaugeDDProgress', parent=self.panScanStatus, pos=wx.Point(8,
              48), range=100, size=wx.Size(400, 16), style=wx.GA_HORIZONTAL)
        self.gaugeDDProgress.SetToolTipString('DD Progress')

        self.lblRate = wx.StaticText(id=wxID_DLGNSRLPROGRESSLBLRATE, label='',
              name='lblRate', parent=self.panScanStatus, pos=wx.Point(8, 96),
              size=wx.Size(400, 21),
              style=wx.ST_NO_AUTORESIZE | wx.ALIGN_CENTRE)

        self.gaugePulse = wx.Gauge(id=wxID_DLGNSRLPROGRESSGAUGEPULSE,
              name='gaugePulse', parent=self.panScanStatus, pos=wx.Point(8, 72),
              range=1000, size=wx.Size(400, 16), style=wx.GA_HORIZONTAL)

    def __init__(self, parent, dirPath):
        self._init_ctrls(parent)
        self.SetIcon(images.getMAKE2Icon())
        
        #self.InitThrober()
        self.Bind(EVT_UPDATE_LABEL, self.OnUpdate)
        #self.dirName = dirName
        #print rootDrive
        #print imageFileName
        self.dirPath = dirPath
        
        #self.SetupNSRLDatabase()
        #self.db = SqliteDatabase(Globals.MACFileName)
        #self.db.OpenConnection()
        self.StartTime = time.time()
        self.scanStarted = False
        #self.ReadFilePropertiesToGet()
        self.jobID = 0
        #self.StartScan()
        self.Bind(wx.EVT_TIMER, self.TimerHandler)
        self.timer = wx.Timer(self)
        self.timer.Start(100)
        #q = Queue.Queue()
        self.scanThread = NSRLScanThread(self, self.StartTime, self.dirPath)
        #self.ScanFinished = False
        self.scanThread.Start()
        
        """
        t = Thread(target=worker, args=(q,))
        t.setDaemon(True)
        t.start()
        
        q.join()
        """

    def __del__(self):
        self.timer.Stop()

    def TimerHandler(self, event):
        #self.g1.SetValue(self.count)
        self.gaugePulse.Pulse()
        
        
    def StartTimer(self):
        self.StartTime = time.time()
        self.lblStartTime.SetLabel(str(time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())))
        self.lblStartTime.Refresh()
        return None
    

    
    def StartScan(self):
        self.StartTimer()


       
    def OnUpdate(self, evt):
        elapsedTime = CommonFunctions.ConvertSecondsToDayHourMinSec(evt.elapsedTime-self.StartTime)
        self.lblElapsedTime.SetLabel(elapsedTime)
        self.lblScanStatus.SetLabel(PlatformMethods.Convert(evt.scanStatus))
        self.gaugeDDProgress.SetValue(int(evt.gaugeValue))
        self.lblEstimatedTime.SetLabel(evt.estimatedTime)
        self.lblRate.SetLabel(evt.rate)
        if str(evt.scanStatus) == "Done Updating Hashes!":
            self.btnOK.Show(True)
            self.btnCancel.Show(False)
            self.gaugeDDProgress.SetValue(100)
            self.gaugePulse.SetValue(100)
            self.timer.Stop()
            #self.gaugePulse.Pulse(False)
            
        self.RefreshLabels()
        evt.Skip()

        
    def RefreshLabels(self):
        self.lblElapsedTime.Refresh()
        

    def OnBtnOKButton(self, event):
        #Globals.frmGlobalMainForm.ShowDirectoryTreeView()
        self.Close()

    def OnBtnCancelButton(self, event):
        dlg = wx.SingleChoiceDialog(self, 'Are you sure you want to cancel Hash Update?', 'Confirmation', ['Yes', 'No'])
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

    def SetupNSRLDatabase(self):
        db = SqliteDatabase(Constants.NSRLDBName)
        if not db.OpenConnection():
            return
        

        """
        query = "DROP TABLE IF EXISTS " + Constants.NSRLFileTable;
        db.ExecuteNonQuery(query)
        
        query = "CREATE TABLE `" + Constants.NSRLFileTable + "` ("
        query += "MD5 text, "
        query += "FileName text, "
        query += "ProductCode text, "
        query += "OSCode text);"
        db.ExecuteNonQuery(query)
        

        query = "delete from " + Constants.NSRLFileTable + ";"
        db.ExecuteNonQuery(query)

        
        query = "DROP TABLE IF EXISTS " + Constants.NSRLProdTable;
        db.ExecuteNonQuery(query)
        
        query = "CREATE TABLE `" + Constants.NSRLProdTable + "` ("
        query += "Code text, "
        query += "Name text, "
        query += "Version text, "
        query += "OSSystemCode text, "
        query += "ApplicationType );"
        db.ExecuteNonQuery(query)
        

        query = "delete from " + Constants.NSRLProdTable + ";"
        db.ExecuteNonQuery(query)
        """
        
        db.CloseConnection()

    def OnDlgScanProgressClose(self, event):
        event.Skip()
            
    
def worker(q):
    db = SqliteDatabase(Constants.NSRLDBName)
    if not db.OpenConnection():
        return
        
    Hashes = set()
    
    while True:
        table, md5 = q.get()
            
        #table = CommonFunctions.GetMD5HashBucketID(md5)
           
        if table not in Hashes:
            Hashes.add(table)
            db.ExecuteNonQuery("CREATE TABLE IF NOT EXISTS %s (MD5 varchar(32) primary key);"%table)
            #db.ExecuteNonQuery("CREATE INDEX Ind%s ON table (MD5);"%table)
        
        try:
            #print "insert into %s (MD5) values ('%s');"%(table, md5)
            
            db.ExecuteNonQuery("insert into %s (MD5) values ('%s');"%(table, md5))
        except Exception, error:
            #print 'Error: ', error
            pass
        
        q.task_done()
        
    db.CloseConnection()
    
    
class NSRLScanThread:
    def __init__(self, win, startTime, dirPath):
        self.win = win
        self.StartTime = startTime
        self.dirPath = dirPath
        self.ElapsedTime = ""
        self.query = ""
        
        self.EventStart = time.time()
        
    def Start(self):
        #self.timerStatus.Start(10000)
        self.keepGoing = self.running = True
        thread.start_new_thread(self.Run, ())
        
    def Stop(self):
        self.keepGoing = False
        #self.db.CloseConnection()
        
    def IsRunning(self):
        return self.running
    
    def Run(self):
        #if os.path.exists(Constants.NSRLDBName):
        #    os.remove(Constants.NSRLDBName)
        
        self.ImportNSRLHashAndProduct()
        #db.CloseConnection()
        #self.running = False
        
        evt = UpdateLabelEvent(elapsedTime = self.ElapsedTime, 
                gaugeValue = self.gaugeValue, rate= self.rateInfo, estimatedTime=self.EstimatedTime, scanStatus = "Done Updating Hashes!")
        wx.PostEvent(self.win, evt)
        #self.timerStatus.Stop()


    def ImportNSRLHashAndProduct(self):
        #q = Queue.Queue()
        
        
        db = SqliteDatabase(Constants.NSRLDBName)
        if not db.OpenConnection():
            return
        
        Hashes = set()
    
        
        #txtFile = False
        
        #query = "INSERT INTO " + Constants.NSRLFileTable + " (MD5, FileName, ProductCode, OSCode) values (?,?,?,?)"
        try:
            fin = open(os.path.join(self.dirPath, "NSRLFile.txt"))
            #fin = gzip.open(self.dirPath + PlatformMethods.GetDirSeparator() + "NSRLFile.txt.gz")
        except IOError:
            #fin = open(self.dirPath + PlatformMethods.GetDirSeparator() + "NSRLFile.txt")
            #txtFile = True
            print 'Error Opening file: ', os.path.join(self.dirPath, "NSRLFile.txt")
            return
            #pass
        
        # Get the file size:y
        try:
            fin.seek(0,2)
            size = fin.tell()
            fin.seek(0)
        except TypeError:
            size = None

         
            
        #finCSV = csv.reader(fin)
                
        #print "Startime = %s"%time.asctime()
        #i = 0
        self.EstimatedTime = ""
        #while self.keepGoing:
        count = 0
        self.startTime = time.time()
        #manyValues = []
        #totalRows = len(finCSV)
        skip = True
        
        """
        t = Thread(target=worker, args=(q,))
        t.setDaemon(True)
        t.start()
        """
        
        while fin:
            rows = fin.readlines(10000)
            if not rows:
                break
            
            #for row in finCSV:
            for row in rows:
                if not self.keepGoing:
                    break
                
                if skip:
                    skip = False
                    continue
                    
                md5 = row.split(',')[1].replace('"','')
                table = CommonFunctions.GetMD5HashBucketID(md5)
                #print col
                #return
                #q.put([table, md5])
                #md5 = row[1]
                
                if table not in Hashes:
                    Hashes.add(table)
                    db.ExecuteNonQuery("CREATE TABLE IF NOT EXISTS %s (MD5 varchar(32) primary key);"%table)
                    #db.ExecuteNonQuery("CREATE INDEX Ind%s ON table (MD5);"%table)
                
                try:
                    db.ExecuteNonQuery("insert into %s (MD5) values ('%s');"%(table, md5))
                except Exception, value:
                    #print 'Error :: ', value
                    pass
            
            
                if size and not count % 10000:
                    done = fin.tell()
                    self.gaugeValue = float(done*100)/float(size)
                    
                    #print "Progress %02u%% Done - %uk rows\r" % (done*100/size,count/1000)
                    
                    self.ElapsedTime = time.time()
                    #self.gaugeValue = (float(size)/float(driveSize))*100
                    timeTaken = float(self.ElapsedTime-self.startTime)
                    if timeTaken == 0:
                        timeTaken = 1
                    rate = float(done)/timeTaken
                    self.rateInfo = "%.2fMB of %.2fMB at %.2fMB/sec" % (done/1024./1024, size/1024./1024, rate/1024./1024)
                    self.Status = "Updating NSRL Software Hashes... [%.2f"% self.gaugeValue
                    self.Status += "%]"
                    #self.startTime = time.time()
                    self.SendEvent()
                
                    if count == 10000:
                        self.EstimatedTime = CommonFunctions.ConvertSecondsToDayHourMinSec(float(size)/rate)
                        
                count += 1
                
            
        fin.close()
        db.CloseConnection()
        #q.join()
    
        """
        try:
            finProd = gzip.open(self.dirPath + PlatformMethods.GetDirSeparator() + "NSRLProd.txt.gz")
        except IOError:
            finProd = open(self.dirPath + PlatformMethods.GetDirSeparator() + "NSRLProd.txt")
        
        # Get the file size:y
        try:
            finProd.seek(0,2)
            size += fin.tell()
            finProd.seek(0)
        except TypeError:
            size = size

        finCSV=csv.reader(finProd)
                
        manyValues = []
        #totalRows = len(finCSV)
        count = 0

        query = "INSERT INTO " + Constants.NSRLProdTable + " (Code, Name, Version, OSSystemCode, ApplicationType) values (?,?,?,?,?)"
        for row in finCSV:
            if not self.keepGoing:
                break
 
            manyValues.append((row[0], row[1], row[2], row[3], row[6]))
            if size and not count % 1000:
                db.ExecuteMany(query, manyValues)
                manyValues = []
                
            if size and not count % 10000:
                done += finProd.tell()
                self.gaugeValue = float(done*100)/float(size)
                self.ElapsedTime = time.time()
                #self.gaugeValue = (float(size)/float(driveSize))*100
                timeTaken = float(self.ElapsedTime-self.startTime)
                if timeTaken == 0:
                    timeTaken = 1
                rate = float(done)/float(timeTaken)
                self.rateInfo = "%.2fMB of %.2fMB at %.2fMB/sec" % (done/1024./1024, size/1024./1024, rate/1024./1024)
                self.Status = "Updating NSRL Software Hash Database... [%.2f"% self.gaugeValue
                self.Status += "%]"
                
                self.SendEvent()
                    
            count+=1
            
        fin.close()
        finProd.close()
        """

        
    
    def SendEvent(self):
        evt = UpdateLabelEvent(elapsedTime = self.ElapsedTime, estimatedTime=self.EstimatedTime,
                gaugeValue = self.gaugeValue, rate= self.rateInfo, scanStatus = self.Status)
        wx.PostEvent(self.win, evt)
        #self.EventStart = time.time()
