#-----------------------------------------------------------------------------
# Name:        dlgDDParallelProgress.py
# Purpose:     
#
# Author:      Ram B. Basnet
#
# Created:     2009/03/05
# RCS-ID:      $Id: dlgDDParallelProgress.py $
# Copyright:   (c) 2006
# Licence:     All Rights Reserved.
# New field:   Whatever
#-----------------------------------------------------------------------------
#Boa:MDIChild:dlgDDProgress

import wx
import wx.lib.buttons
import time
import os.path, sys
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
from collections import deque
from Queue import Queue
import images


def create(parent, rootDrive, listImageNames, SourceType=Constants.LogicalDrive, verifyImages=True):
    return dlgDDProgress(parent, rootDrive, listImageNames, SourceType, verifyImages)

[wxID_DLGDDPROGRESS, wxID_DLGDDPROGRESSBTNCANCEL, wxID_DLGDDPROGRESSBTNOK, 
 wxID_DLGDDPROGRESSGAUGEDDPROGRESS, wxID_DLGDDPROGRESSGAUGEPULSE, 
 wxID_DLGDDPROGRESSLBLELAPSEDTIME, wxID_DLGDDPROGRESSLBLESTIMATEDTIME, 
 wxID_DLGDDPROGRESSLBLRATE, wxID_DLGDDPROGRESSLBLSCANSTATUS, 
 wxID_DLGDDPROGRESSPANSCANSTATUS, wxID_DLGDDPROGRESSSTATICTEXT2, 
 wxID_DLGDDPROGRESSSTATICTEXT3, 
] = [wx.NewId() for _init_ctrls in range(12)]

#----------------------------------------------------------------------

# This creates a new Event class and a EVT binder function
(UpdateLabelEvent, EVT_UPDATE_LABEL) = wx.lib.newevent.NewEvent()

#doneReading = False
buffer = Queue(10)
sentinel = object()
readThread = None
writeThread = None
#diskMD5 = None
diskSHA1 = None

#condition = threading.condition
#----------------------------------------------------------------------

class dlgDDProgress(wx.Dialog):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_DLGDDPROGRESS, name='dlgDDProgress',
              parent=prnt, pos=wx.Point(492, 221), size=wx.Size(451, 298),
              style=0, title='DD Status...')
        self.SetClientSize(wx.Size(443, 264))
        self.SetAutoLayout(True)
        self.SetBackgroundColour(wx.Colour(125, 152, 221))
        self.SetCursor(wx.STANDARD_CURSOR)
        self.SetMinSize(wx.Size(-1, -1))
        self.Center(wx.BOTH)

        self.panScanStatus = wx.Panel(id=wxID_DLGDDPROGRESSPANSCANSTATUS,
              name=u'panScanStatus', parent=self, pos=wx.Point(16, 16),
              size=wx.Size(416, 200), style=wx.TAB_TRAVERSAL)
        self.panScanStatus.SetBackgroundColour(wx.Colour(225, 236, 255))

        self.lblEstimatedTime = wx.StaticText(id=wxID_DLGDDPROGRESSLBLESTIMATEDTIME,
              label='    ', name='lblEstimatedTime', parent=self.panScanStatus,
              pos=wx.Point(96, 176), size=wx.Size(12, 13), style=0)

        self.staticText2 = wx.StaticText(id=wxID_DLGDDPROGRESSSTATICTEXT2,
              label='Estimated Time:', name='staticText2',
              parent=self.panScanStatus, pos=wx.Point(8, 176), size=wx.Size(76,
              13), style=wx.ALIGN_RIGHT)

        self.staticText3 = wx.StaticText(id=wxID_DLGDDPROGRESSSTATICTEXT3,
              label=u'Elapsed Time:', name='staticText3',
              parent=self.panScanStatus, pos=wx.Point(16, 152), size=wx.Size(66,
              13), style=wx.ALIGN_RIGHT)

        self.lblElapsedTime = wx.StaticText(id=wxID_DLGDDPROGRESSLBLELAPSEDTIME,
              label='    ', name=u'lblElapsedTime', parent=self.panScanStatus,
              pos=wx.Point(96, 152), size=wx.Size(12, 13), style=0)

        self.lblScanStatus = wx.StaticText(id=wxID_DLGDDPROGRESSLBLSCANSTATUS,
              label='Creating image...', name=u'lblScanStatus',
              parent=self.panScanStatus, pos=wx.Point(136, 8), size=wx.Size(109,
              16), style=0)
        self.lblScanStatus.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, u'MS Shell Dlg 2'))
        self.lblScanStatus.SetForegroundColour(wx.Colour(255, 0, 0))
        self.lblScanStatus.Show(True)

        self.btnOK = wx.Button(id=wxID_DLGDDPROGRESSBTNOK, label=u'&OK',
              name=u'btnOK', parent=self, pos=wx.Point(192, 224),
              size=wx.Size(88, 24), style=0)
        self.btnOK.Show(False)
        self.btnOK.Bind(wx.EVT_BUTTON, self.OnBtnOKButton,
              id=wxID_DLGDDPROGRESSBTNOK)

        self.btnCancel = wx.Button(id=wxID_DLGDDPROGRESSBTNCANCEL,
              label=u'&Cancel', name=u'btnCancel', parent=self,
              pos=wx.Point(192, 224), size=wx.Size(88, 24), style=0)
        self.btnCancel.Bind(wx.EVT_BUTTON, self.OnBtnCancelButton,
              id=wxID_DLGDDPROGRESSBTNCANCEL)

        self.gaugeDDProgress = wx.Gauge(id=wxID_DLGDDPROGRESSGAUGEDDPROGRESS,
              name='gaugeDDProgress', parent=self.panScanStatus, pos=wx.Point(8,
              48), range=100, size=wx.Size(400, 16), style=wx.GA_HORIZONTAL)
        self.gaugeDDProgress.SetToolTipString('DD Progress')

        self.lblRate = wx.StaticText(id=wxID_DLGDDPROGRESSLBLRATE, label='',
              name='lblRate', parent=self.panScanStatus, pos=wx.Point(8, 96),
              size=wx.Size(400, 21),
              style=wx.ST_NO_AUTORESIZE | wx.ALIGN_CENTRE)

        self.gaugePulse = wx.Gauge(id=wxID_DLGDDPROGRESSGAUGEPULSE,
              name='gaugePulse', parent=self.panScanStatus, pos=wx.Point(8, 72),
              range=1000, size=wx.Size(400, 16), style=wx.GA_HORIZONTAL)

    def __init__(self, parent, rootDrive, listImageNames, SourceType=Constants.LogicalDrive, verifyImages=True):
        self._init_ctrls(parent)
        self.SetIcon(images.getMAKE2Icon())
        #self.InitThrober()
        self.Bind(EVT_UPDATE_LABEL, self.OnUpdate)
        value = 'Creating Image...'
        if len(listImageNames) > 1:
            value = 'Creating Images...'
            
        self.lblScanStatus.SetLabel(value)
        #self.db = SqliteDatabase(Globals.MACFileName)
        #self.db.OpenConnection()
        self.StartTime = time.time()
        #self.scanStarted = False
        #self.ReadFilePropertiesToGet()
        self.jobID = 0
        #self.StartScan()
        self.Bind(wx.EVT_TIMER, self.TimerHandler)
        self.timer = wx.Timer(self)
        self.timer.Start(100)

        global writeThread
        global readThread
        #sched = Scheduler()
        writeThread = WriteThread(self, self.StartTime, listImageNames, SourceType, verifyImages)
        self.ScanFinished = False
        writeThread.start()
        
        readThread = ReadThread(self, self.StartTime, rootDrive, listImageNames, SourceType, verifyImages)
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
            self.gaugeDDProgress.SetValue(int(evt.gaugeValue))
            self.lblEstimatedTime.SetLabel(evt.estimatedTime)
            self.lblRate.SetLabel(evt.rate)
        except:
            pass
        
        if str(evt.scanStatus) == "Done Creating Image!":
            self.btnOK.Show(True)
            self.btnCancel.Show(False)
            self.gaugeDDProgress.SetValue(100)
            self.gaugePulse.SetValue(100)
            self.timer.Stop()
            #self.gaugePulse.Pulse(False)
            doneReading = True
            print "Done Creating Images at: %s"%time.asctime()
            
        self.RefreshLabels()
        evt.Skip()

        
    def RefreshLabels(self):
        self.lblElapsedTime.Refresh()
        

    def OnBtnOKButton(self, event):
        #Globals.frmGlobalMainForm.ShowDirectoryTreeView()
        self.Close()

    def OnBtnCancelButton(self, event):
        global readThread
        global writeThread
        dlg = wx.SingleChoiceDialog(self, 'Are you sure you want to cancel the scanning job?', 'Confirmation', ['Yes', 'No'])
        try:
            if dlg.ShowModal() == wx.ID_OK:
                selected = dlg.GetStringSelection()
                # Your code
                if selected == 'Yes':
                    readThread.Stop()
                    writeThread.Stop()
                    self.Close()
        finally:
            dlg.Destroy()

            

    def OnDlgScanProgressClose(self, event):
        event.Skip()
            
    
    
class ReadThread(Thread):
    def __init__(self, win, startTime, rootDrive, listImageNames, SourceType=Constants.LogicalDrive, verifyImages=True):
        Thread.__init__(self)
        self.win = win
        self.StartTime = startTime
        self.SourceType = SourceType
        self.rootDrive = rootDrive
        self.ElapsedTime = ""
        self.listImageNames = listImageNames
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
        global diskSHA1
        if self.verifyImages:
            diskSHA1 = hashlib.sha1()
        #m = hashlib.md5()
        #sha1 = hashlib.sha1()
        size = 0
        #try:
        rfin = Win32RawIO.Win32RAWIO(self.rootDrive, 'r')
        driveSize = rfin.size
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
                diskSHA1.update(data)
                self.EstimatedTime = CommonFunctions.ConvertSecondsToDayHourMinSec(float(driveSize*len(self.listImageNames))/rate)
            else:
                self.EstimatedTime = CommonFunctions.ConvertSecondsToDayHourMinSec(float(driveSize)/rate)
                
            size += len(data)
            self.gaugeValue = (float(size)/float(driveSize))*100
            self.rateInfo = "%.2fMB of %.2fMB at %.2fMB/sec" % (size/1024./1024, driveSize/1024./1024, rate/1024./1024)
            self.Status = "Creating Image... [%.2f%s"%(self.gaugeValue, "%]")
            self.SendEvent()
            
        rfin.close()
        if self.verifyImages:
            print "Disk SHA1: %s"%diskSHA1.hexdigest().upper()
        
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
        #wx.PostEvent(self.win, evt)
        #self.EventStart = time.time()

class WriteThread(Thread):
    def __init__(self, win, startTime, listImageNames, SourceType=Constants.LogicalDrive, verifyImages=True):
        Thread.__init__(self)
        self.win = win
        self.StartTime = startTime
        self.SourceType = SourceType
        #self.rootDrive = rootDrive
        self.ElapsedTime = ""
        #self.imageFileName = imageFileName
        self.listImageNames = listImageNames
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
        global diskSHA1
        #m = hashlib.md5()
        #sha1 = hashlib.sha1()
        #size = 0
        fileObjects = []
        for imageName in self.listImageNames:
            fileObjects.append(open(imageName, 'wb'))

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
            for imageName in self.listImageNames:
                sha1 = hashlib.sha1()
                fin = open(imageName, 'rb')
                while True:
                    data = fin.read(1024*1024*16)
                    if not data:
                        break
                    sha1.update(data)
                    self.ElapsedTime = time.time()
                    self.SendEvent()
                    
                fin.close()
                shas[imageName] = sha1
                
            for imageName in shas:
                digest = shas[imageName].hexdigest().upper()
                print 'Image: %s'%imageName
                print 'SHA1: %s'%digest
                if digest == diskSHA1.hexdigest().upper():
                    print 'MATCH'
                else:
                    print '** NO MATCH **'
        
        #print "Write Thread Endtime = %s"%time.asctime()
        #self.rfout.close()
        #print "MD5 Hash=%s"%m.hexdigest().upper()
        #print "SHA1 Hash=%s"%sha1.hexdigest().upper()
        self.running = False
        self.ElapsedTime = time.time()
        self.Status = 'Done Creating Image!'
        #self.gaugeValue = 100
        self.SendEvent()
        
    
    def SendEvent(self):
        evt = UpdateLabelEvent(elapsedTime = self.ElapsedTime, scanStatus = self.Status)
        wx.PostEvent(self.win, evt)


           
if __name__ == "__main__":
    app = wx.PySimpleApp()
    driveName = r'\\.\G:'
    imageFileNames = ['D:\\sandisk3.dd', 'D:\\sandisk4.dd']
    frame = create(None, driveName, imageFileNames, SourceType=Constants.LogicalDrive, verifyImages=True)
    frame.Show(True)
    app.MainLoop()
