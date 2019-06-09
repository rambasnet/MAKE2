#-----------------------------------------------------------------------------
# Name:        dlgDDProgress.py
# Purpose:     
#
# Author:      Ram Basnet
#
# Created:     2007/11/01
# RCS-ID:      $Id: dlgDDProgress.py,v 1.4 2007/11/13 19:52:48 rbasnet Exp $
# Copyright:   (c) 2007
# Licence:     All Rights Reserved.
# New field:   Whatever
#-----------------------------------------------------------------------------
#Boa:MDIChild:dlgDDToDiskProgress

import wx
import wx.lib.buttons
import time
import os, os.path, sys
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
import hashlib
import Win32RawIO
import images

def create(parent, imagePath, listDriveNames):
    return dlgDDToDiskProgress(parent, imagePath, listDriveNames)

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


#----------------------------------------------------------------------

class dlgDDToDiskProgress(wx.Dialog):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_DLGDDTODISKPROGRESS,
              name=u'dlgDDToDiskProgress', parent=prnt, pos=wx.Point(565, 295),
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

    def __init__(self, parent, imagePath, listDriveNames):
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
        self.ddToDiskThread = DDToDiskThread(self, self.StartTime, self.imagePath, self.listDriveNames)
        #self.ScanFinished = False
        self.ddToDiskThread.Start()

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
        self.gaugeDDToDiskProgress.SetValue(int(evt.gaugeValue))
        self.lblEstimatedTime.SetLabel(evt.estimatedTime)
        self.lblRate.SetLabel(evt.rate)
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
        wx.PostEvent(self.win, evt)
        #self.EventStart = time.time()
