#-----------------------------------------------------------------------------
# Name:        dlgDDToDiskParallelProgress.py
# Purpose:     
#
# Author:      Ram B. Basnet
#
# Created:     2009/03/05
# RCS-ID:      $Id: dlgDDToDiskParallelProgress.py $
# Copyright:   (c) 2006
# Licence:     <your licence>
# New field:   Whatever
#-----------------------------------------------------------------------------


import wx
import wx.lib.buttons
import time
import os, os.path, sys
#import wx.lib.delayedresult as delayedresult
import wx.lib.newevent
#import  thread
from threading import *

from stat import *

from wx.lib.anchors import LayoutAnchors

from SqliteDatabase import *
import Globals
import Constants
import CommonFunctions
import DBFunctions
import Classes
import PlatformMethods
import hashlib
import Win32RawIO
import images
from Queue import Queue

def create(parent, imagePath, listDriveNames, verifyImages=False):
    return dlgDDToDiskProgress(parent, imagePath, listDriveNames, verifyImages=False)

[wxID_DLGDDTODISKPROGRESS, wxID_DLGDDTODISKPROGRESSBTNCANCEL, 
 wxID_DLGDDTODISKPROGRESSBTNOK, wxID_DLGDDTODISKPROGRESSGAUGEDDTODISKPROGRESS, 
 wxID_DLGDDTODISKPROGRESSGAUGEPULSE, wxID_DLGDDTODISKPROGRESSLBLELAPSEDTIME, 
 wxID_DLGDDTODISKPROGRESSLBLESTIMATEDTIME, wxID_DLGDDTODISKPROGRESSLBLRATE, 
 wxID_DLGDDTODISKPROGRESSLBLSCANSTATUS, wxID_DLGDDTODISKPROGRESSPANSCANSTATUS, 
 wxID_DLGDDTODISKPROGRESSSTATICTEXT2, wxID_DLGDDTODISKPROGRESSSTATICTEXT3, 
] = [wx.NewId() for _init_ctrls in range(12)]

#----------------------------------------------------------------------

# This creates a new Event class and a EVT binder function
(UpdateLabelEvent, EVT_UPDATE_LABEL) = wx.lib.newevent.NewEvent()

buffer = Queue(10)
sentinel = object()
readThread = None
writeThread = None
#diskMD5 = None
imageSHA1 = None

#----------------------------------------------------------------------

class dlgDDToDiskProgress(wx.Dialog):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_DLGDDTODISKPROGRESS,
              name=u'dlgDDToDiskProgress', parent=prnt, pos=wx.Point(528, 289),
              size=wx.Size(451, 298), style=0, title=u'DD To Disk Status...')
        self.SetClientSize(wx.Size(443, 264))
        self.SetAutoLayout(True)
        self.SetBackgroundColour(wx.Colour(125, 152, 221))
        self.SetCursor(wx.STANDARD_CURSOR)
        self.SetMinSize(wx.Size(-1, -1))
        self.Center(wx.BOTH)

        self.panScanStatus = wx.Panel(id=wxID_DLGDDTODISKPROGRESSPANSCANSTATUS,
              name=u'panScanStatus', parent=self, pos=wx.Point(16, 16),
              size=wx.Size(416, 200), style=wx.TAB_TRAVERSAL)
        self.panScanStatus.SetBackgroundColour(wx.Colour(225, 236, 255))

        self.lblEstimatedTime = wx.StaticText(id=wxID_DLGDDTODISKPROGRESSLBLESTIMATEDTIME,
              label='    ', name='lblEstimatedTime', parent=self.panScanStatus,
              pos=wx.Point(96, 176), size=wx.Size(12, 13), style=0)

        self.staticText2 = wx.StaticText(id=wxID_DLGDDTODISKPROGRESSSTATICTEXT2,
              label='Estimated Time:', name='staticText2',
              parent=self.panScanStatus, pos=wx.Point(8, 176), size=wx.Size(76,
              13), style=wx.ALIGN_RIGHT)

        self.staticText3 = wx.StaticText(id=wxID_DLGDDTODISKPROGRESSSTATICTEXT3,
              label=u'Elapsed Time:', name='staticText3',
              parent=self.panScanStatus, pos=wx.Point(16, 152), size=wx.Size(66,
              13), style=wx.ALIGN_RIGHT)

        self.lblElapsedTime = wx.StaticText(id=wxID_DLGDDTODISKPROGRESSLBLELAPSEDTIME,
              label='    ', name=u'lblElapsedTime', parent=self.panScanStatus,
              pos=wx.Point(96, 152), size=wx.Size(12, 13), style=0)

        self.lblScanStatus = wx.StaticText(id=wxID_DLGDDTODISKPROGRESSLBLSCANSTATUS,
              label=u'Writing image to disk...', name=u'lblScanStatus',
              parent=self.panScanStatus, pos=wx.Point(136, 8), size=wx.Size(149,
              16), style=0)
        self.lblScanStatus.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, u'MS Shell Dlg 2'))
        self.lblScanStatus.SetForegroundColour(wx.Colour(255, 0, 0))
        self.lblScanStatus.Show(True)

        self.btnOK = wx.Button(id=wxID_DLGDDTODISKPROGRESSBTNOK, label=u'&OK',
              name=u'btnOK', parent=self, pos=wx.Point(192, 224),
              size=wx.Size(88, 24), style=0)
        self.btnOK.Show(False)
        self.btnOK.Bind(wx.EVT_BUTTON, self.OnBtnOKButton,
              id=wxID_DLGDDTODISKPROGRESSBTNOK)

        self.btnCancel = wx.Button(id=wxID_DLGDDTODISKPROGRESSBTNCANCEL,
              label=u'&Cancel', name=u'btnCancel', parent=self,
              pos=wx.Point(192, 224), size=wx.Size(88, 24), style=0)
        self.btnCancel.Bind(wx.EVT_BUTTON, self.OnBtnCancelButton,
              id=wxID_DLGDDTODISKPROGRESSBTNCANCEL)

        self.gaugeDDToDiskProgress = wx.Gauge(id=wxID_DLGDDTODISKPROGRESSGAUGEDDTODISKPROGRESS,
              name=u'gaugeDDToDiskProgress', parent=self.panScanStatus,
              pos=wx.Point(8, 48), range=100, size=wx.Size(400, 16),
              style=wx.GA_HORIZONTAL)
        self.gaugeDDToDiskProgress.SetToolTipString('DD Progress')

        self.lblRate = wx.StaticText(id=wxID_DLGDDTODISKPROGRESSLBLRATE,
              label='', name='lblRate', parent=self.panScanStatus,
              pos=wx.Point(8, 96), size=wx.Size(400, 21),
              style=wx.ST_NO_AUTORESIZE | wx.ALIGN_CENTRE)

        self.gaugePulse = wx.Gauge(id=wxID_DLGDDTODISKPROGRESSGAUGEPULSE,
              name='gaugePulse', parent=self.panScanStatus, pos=wx.Point(8, 72),
              range=1000, size=wx.Size(400, 16), style=wx.GA_HORIZONTAL)

    def __init__(self, parent, imagePath, listDriveNames, verifyImages=False):
        self._init_ctrls(parent)
        self.SetIcon(images.getMAKE2Icon())
        self.Bind(EVT_UPDATE_LABEL, self.OnUpdate)
        self.imagePath = imagePath
        self.listDriveNames = listDriveNames
        self.lblScanStatus.SetLabel("Writing image to disk...")
        self.StartTime = time.time()
        self.scanStarted = False
        #self.ReadFilePropertiesToGet()
        self.jobID = 0
        #self.StartScan()
        self.Bind(wx.EVT_TIMER, self.TimerHandler)
        self.timer = wx.Timer(self)
        self.timer.Start(100)
        #self.ddToDiskThread = DDToDiskThread(self, self.StartTime, self.imagePath, self.listDriveNames)
        #self.ScanFinished = False
        #self.ddToDiskThread.Start()
        global writeThread
        global readThread
        #sched = Scheduler()
        writeThread = WriteThread(self, self.StartTime, listDriveNames, verifyImages)
        self.ScanFinished = False
        writeThread.start()
        
        readThread = ReadThread(self, self.StartTime, imagePath, listDriveNames, verifyImages)
        readThread.start()
        

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
        self.lblScanStatus.SetLabel(PlatformMethods.Decode(evt.scanStatus))
        try:
            self.gaugeDDToDiskProgress.SetValue(int(evt.gaugeValue))
            self.lblEstimatedTime.SetLabel(evt.estimatedTime)
            self.lblRate.SetLabel(evt.rate)
        except:
            pass
        if str(evt.scanStatus) == "Done Writing To Disk!":
            self.btnOK.Show(True)
            self.btnCancel.Show(False)
            self.gaugeDDToDiskProgress.SetValue(100)
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
        dlg = wx.SingleChoiceDialog(self, 'Are you sure you want to cancel the job?', 'Confirmation', ['Yes', 'No'])
        try:
            if dlg.ShowModal() == wx.ID_OK:
                selected = dlg.GetStringSelection()
                # Your code
                if selected == 'Yes':
                    self.ddToDiskThread.Stop()
                    #query = "delete from " + Constants.FileInfoTable
                    #self.db.ExecuteNonQuery(query)
                    self.Close()
        finally:
            dlg.Destroy()

            

    def OnDlgScanProgressClose(self, event):
        event.Skip()
            
    
class ReadThread(Thread):
    def __init__(self, win, startTime, imagePath, listDriveNames, verifyImages=False):
        Thread.__init__(self)
        self.win = win
        self.StartTime = startTime
        self.SourceType = SourceType
        self.imagePath = imagePath
        self.ElapsedTime = ""
        self.listDriveNames = listDriveNames
        self.query = ""
        #self.buffer = buffer
        self.keepGoing = self.running = True
        self.verifyImages = verifyImages
        self.EventStart = time.time()
        
    
    """    
    def start(self):
        #self.timerStatus.Start(10000)
        self.keepGoing = self.running = True
        #thread.start_new_thread(self.run, ())
    """
     
    def Stop(self):
        self.keepGoing = False
        #self.db.CloseConnection()
        
    def IsRunning(self):
        return self.running
    
    def run(self):
        global buffer, sentinel
        global writeThread
        global imageSHA1
        if self.verifyImages:
            imageSHA1 = hashlib.sha1()
        #m = hashlib.md5()
        #sha1 = hashlib.sha1()
        size = 0
        #try:
        rfin = open(self.imagePath, 'rb')
        st = os.stat(self.imagePath)
        imageSize = st[ST_SIZE]
        
        #driveSize = rfin.size
        #print "Read Thread Startime = %s"%time.asctime()
        #i = 0
        self.EstimatedTime = ""
        while self.keepGoing:
            self.readTime = time.time()
            data = rfin.read(1024*1024*16)
            
            if not data:
                buffer.put(sentinel)
                break
            
            buffer.put(data)

            self.ElapsedTime = time.time()
            rate = float(len(data))/float(self.ElapsedTime-self.readTime)
            #if size == 0:
            if self.verifyImages:
                imageSHA1.update(data)
                self.EstimatedTime = CommonFunctions.ConvertSecondsToDayHourMinSec(float(imageSize*len(self.listDriveNames))/rate)
            else:
                self.EstimatedTime = CommonFunctions.ConvertSecondsToDayHourMinSec(float(imageSize)/rate)
                
            size += len(data)
            self.gaugeValue = (float(size)/float(imageSize))*100
            self.rateInfo = "%.2fMB of %.2fMB at %.2fMB/sec" % (size/1024./1024, imageSize/1024./1024, rate/1024./1024)
            self.Status = "Creating Image... [%.2f%s"%(self.gaugeValue, "%]")
            self.SendEvent()
            
        rfin.close()
        if self.verifyImages:
            print "Image SHA1: %s"%imageSHA1.hexdigest().upper()
        
        self.running = False
        #writeThread.join()
        
        """
        self.ElapsedTime = time.time()
        self.Status = 'Done Creating Image!'
        self.gaugeValue = 100
        self.SendEvent()
        #self.timerStatus.Stop()
        """

    def SendEvent(self):
        evt = UpdateLabelEvent(elapsedTime = self.ElapsedTime, estimatedTime=self.EstimatedTime,
                gaugeValue = self.gaugeValue, rate= self.rateInfo, scanStatus = self.Status)
        wx.PostEvent(self.win, evt)
        

class WriteThread(Thread):
    def __init__(self, win, startTime, listDriveNames, verifyImages=False):
        Thread.__init__(self)
        self.win = win
        self.StartTime = startTime
        self.SourceType = SourceType
        #self.imagePath = imagePath
        self.ElapsedTime = ""
        #self.imageFileName = imageFileName
        self.listDriveNames = listDriveNames
        self.verifyImages = verifyImages
        self.query = ""
        #self.buffer = buffer
        self.EventStart = time.time()
        #Task.__init__(self)
        self.keepGoing = self.running = True
        
    
    """    
    def Start(self):
        #self.timerStatus.Start(10000)
        self.keepGoing = self.running = True
        thread.start_new_thread(self.run, ())
    """
     
    def Stop(self):
        self.keepGoing = False
        #self.db.CloseConnection()
        
    def IsRunning(self):
        return self.running
    
    def run(self):
        global sentinel, buffer
        global imageSHA1
        #m = hashlib.md5()
        #sha1 = hashlib.sha1()
        #size = 0
        fileObjects = []
        for dirName in self.listDriveNames:
            fileObjects.append(Win32RawIO.Win32RAWIO(dirName, 'w'))

        #print "Write Thread Starttime = %s"%time.asctime()
        while self.keepGoing:
            data = buffer.get()
            if data is sentinel:
                 break
            #else:    
                #print 'got data'
                #print data
            for rfout in fileObjects:
                rfout.write(data)
            
        for rfout in fileObjects:
            rfout.close()
            
        fileObjects = None
        self.ElapsedTime = time.time()
        
        if self.verifyImages:
            shas = {}
            self.Status = 'Verifying Images...'
            for driveName in self.listDriveNames:
                sha1 = hashlib.sha1()
                fin = Win32RawIO.Win32RAWIO(driveName, 'r')
                while True:
                    data = fin.read(1024*1024*16)
                    if not data:
                        break
                    sha1.update(data)
                    self.ElapsedTime = time.time()
                    self.SendEvent()
                    
                fin.close()
                shas[dirName] = sha1
                
            for driveName in shas:
                digest = shas[driveName].hexdigest().upper()
                print 'Disk: %s SHA1: '%(driveName, digest)
                #print 'SHA1: %s'%digest
                if digest == imageSHA1.hexdigest().upper():
                    print 'MATCH'
                else:
                    print '** NO MATCH **'
        
        #print "Write Thread Endtime = %s"%time.asctime()
        #self.rfout.close()
        #print "MD5 Hash=%s"%m.hexdigest().upper()
        #print "SHA1 Hash=%s"%sha1.hexdigest().upper()
        self.running = False
        self.ElapsedTime = time.time()
        print 'Done Writing To Disk!'
        self.Status = 'Done Writing To Disk!'
        #self.gaugeValue = 100
        self.SendEvent()
        
    
    def SendEvent(self):
        evt = UpdateLabelEvent(elapsedTime = self.ElapsedTime, scanStatus = self.Status)
        wx.PostEvent(self.win, evt)
        
    
class DDToDiskThread:
    def __init__(self, win, startTime, imagePath, listDriveNames):
        self.win = win
        self.StartTime = startTime
        self.imagePath = imagePath
        self.ElapsedTime = ""
        self.listDriveNames = listDriveNames
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
        m = hashlib.md5()
        #sha1 = hashlib.sha1()
        size = 0
        #try:
        rfin = open(self.imagePath, 'rb')
        fileObjects = []
        for dirName in self.listDriveNames:
            fileObjects.append(Win32RawIO.Win32RAWIO(dirName, 'w'))
            
        
        startTime = time.time()
        print "Startime = %s"%time.asctime()
        #i = 0
        self.EstimatedTime = ""
            
        st = os.stat(self.imagePath)
        imageSize = st[ST_SIZE]
        
        while self.keepGoing:
            self.readTime = time.time()
            data = rfin.read(1024*1024*16)
            if len(data) == 0:
                break
            for rfout in fileObjects:
                rfout.write(data)
                rfout.flush()
            #if self.verifyImages:
            m.update(data)
            #sha1.update(data)
                
            self.ElapsedTime = time.time()
            #print 'data len=%s'%len(data)
            #print 'time take=%s'%(self.ElapsedTime-self.readTime)
            rate = float(len(data))/float(self.ElapsedTime-self.readTime)
            if size == 0:
                self.EstimatedTime = CommonFunctions.ConvertSecondsToDayHourMinSec(float(imageSize)/rate)
            size += len(data)
            self.gaugeValue = (float(size)/float(imageSize))*100
            self.rateInfo = "%.2fMB of %.2fMB at %.2fMB/sec" % (size/1024./1024, imageSize/1024./1024, rate/1024./1024)
            self.Status = "Writing Disk... [%.2f%s"%(self.gaugeValue, "%]")
            #self.Status += "%]"
            self.SendEvent()
        #i += 1
        for rfout in fileObjects:
            rfout.close()
            
        self.ElapsedTime = time.time()
        #if self.verifyImages:
        print "MD5 Hash = %s"%m.hexdigest().upper()
        #print "SHA1 Hash = %s"%sha1.hexdigest().upper()
  
        rfin.close()
       
        print "Endtime = %s"%time.asctime()
        print "Total Elapsed Time = %s"%CommonFunctions.ConvertSecondsToDayHourMinSec(self.ElapsedTime-startTime)
        
    
        #except:
        #    print "Exception occured: %s"%sys.exc_info()[0]
        
        self.running = False
        
        evt = UpdateLabelEvent(elapsedTime = self.ElapsedTime, 
                gaugeValue = self.gaugeValue, rate= self.rateInfo, estimatedTime=self.EstimatedTime, scanStatus = "Done Writing To Disk!")
        wx.PostEvent(self.win, evt)
        #self.timerStatus.Stop()


    
    def SendEvent(self):
        evt = UpdateLabelEvent(elapsedTime = self.ElapsedTime, estimatedTime=self.EstimatedTime,
                gaugeValue = self.gaugeValue, rate= self.rateInfo, scanStatus = self.Status)
        wx.PostEvent(self.win, evt)

