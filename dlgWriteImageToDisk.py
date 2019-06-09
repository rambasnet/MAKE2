#-----------------------------------------------------------------------------
# Name:        dlgWriteImageToDisk.py
# Purpose:     
#
# Author:      Ram B. Basnet
#
# Created:     2009/03/08
# RCS-ID:      $Id: dlgWriteImageToDisk.py $
# Copyright:   (c) 2006
# Licence:     All Rights Reserved
# New field:   Whatever
#-----------------------------------------------------------------------------
#Boa:MDIChild:dlgWriteImageToDisk

import wx
import os, os.path

import Constants
import Win32RawIO
import images
import CommonFunctions
from stat import *

def create(parent):
    return dlgWriteImageToDisk(parent)

[wxID_DLGWRITEIMAGETODISK, wxID_DLGWRITEIMAGETODISKBTNADDDESTINATION, 
 wxID_DLGWRITEIMAGETODISKBTNBROWSEIMAGEFILE, 
 wxID_DLGWRITEIMAGETODISKBTNCANCEL, 
 wxID_DLGWRITEIMAGETODISKBTNDELETEDESTINATION, wxID_DLGWRITEIMAGETODISKBTNOK, 
 wxID_DLGWRITEIMAGETODISKLBLPROJECTNAME, 
 wxID_DLGWRITEIMAGETODISKLSTDESTINATIONS, wxID_DLGWRITEIMAGETODISKPANEVIDENCE, 
 wxID_DLGWRITEIMAGETODISKSTATICBOX1, wxID_DLGWRITEIMAGETODISKSTATICBOX3, 
 wxID_DLGWRITEIMAGETODISKTXTIMAGEPATH, 
] = [wx.NewId() for _init_ctrls in range(12)]

class dlgWriteImageToDisk(wx.Dialog):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_DLGWRITEIMAGETODISK,
              name=u'dlgWriteImageToDisk', parent=prnt, pos=wx.Point(537, 248),
              size=wx.Size(434, 380), style=wx.DEFAULT_DIALOG_STYLE,
              title=u'Write Image To Disk')
        self.SetClientSize(wx.Size(426, 346))
        self.SetAutoLayout(True)
        self.SetBackgroundColour(wx.Colour(125, 152, 221))
        self.SetCursor(wx.STANDARD_CURSOR)
        self.SetMinSize(wx.Size(-1, -1))
        self.Center(wx.BOTH)

        self.lblProjectName = wx.StaticText(id=wxID_DLGWRITEIMAGETODISKLBLPROJECTNAME,
              label=u'Write DD Image To Disk    ', name='lblProjectName',
              parent=self, pos=wx.Point(0, 0), size=wx.Size(424, 32),
              style=wx.ALIGN_RIGHT | wx.RAISED_BORDER | wx.ST_NO_AUTORESIZE)
        self.lblProjectName.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, 'Tahoma'))
        self.lblProjectName.SetForegroundColour(wx.Colour(0, 78, 155))
        self.lblProjectName.SetBackgroundColour(wx.Colour(215, 235, 255))

        self.btnOK = wx.Button(id=wxID_DLGWRITEIMAGETODISKBTNOK, label=u'&OK',
              name=u'btnOK', parent=self, pos=wx.Point(248, 304),
              size=wx.Size(75, 23), style=0)
        self.btnOK.Bind(wx.EVT_BUTTON, self.OnBtnOKButton,
              id=wxID_DLGWRITEIMAGETODISKBTNOK)

        self.btnCancel = wx.Button(id=wxID_DLGWRITEIMAGETODISKBTNCANCEL,
              label=u'&Cancel', name=u'btnCancel', parent=self,
              pos=wx.Point(328, 304), size=wx.Size(75, 23), style=0)
        self.btnCancel.Bind(wx.EVT_BUTTON, self.OnBtnCancelButton,
              id=wxID_DLGWRITEIMAGETODISKBTNCANCEL)

        self.panEvidence = wx.Panel(id=wxID_DLGWRITEIMAGETODISKPANEVIDENCE,
              name='panEvidence', parent=self, pos=wx.Point(16, 48),
              size=wx.Size(392, 240), style=wx.TAB_TRAVERSAL)
        self.panEvidence.SetBackgroundColour(wx.Colour(225, 236, 255))

        self.lstDestinations = wx.ListCtrl(id=wxID_DLGWRITEIMAGETODISKLSTDESTINATIONS,
              name='lstDestinations', parent=self.panEvidence, pos=wx.Point(16,
              112), size=wx.Size(360, 72),
              style=wx.LC_LIST | wx.HSCROLL | wx.LC_SINGLE_SEL | wx.VSCROLL)

        self.btnAddDestination = wx.Button(id=wxID_DLGWRITEIMAGETODISKBTNADDDESTINATION,
              label='Add...', name='btnAddDestination', parent=self.panEvidence,
              pos=wx.Point(216, 192), size=wx.Size(75, 23), style=0)
        self.btnAddDestination.Bind(wx.EVT_BUTTON,
              self.OnBtnAddDestinationButton,
              id=wxID_DLGWRITEIMAGETODISKBTNADDDESTINATION)

        self.btnDeleteDestination = wx.Button(id=wxID_DLGWRITEIMAGETODISKBTNDELETEDESTINATION,
              label=u'Delete', name=u'btnDeleteDestination',
              parent=self.panEvidence, pos=wx.Point(304, 192), size=wx.Size(75,
              23), style=0)
        self.btnDeleteDestination.Enable(True)
        self.btnDeleteDestination.Bind(wx.EVT_BUTTON,
              self.OnBtnDeleteDestinationButton,
              id=wxID_DLGWRITEIMAGETODISKBTNDELETEDESTINATION)

        self.staticBox1 = wx.StaticBox(id=wxID_DLGWRITEIMAGETODISKSTATICBOX1,
              label=u'Enter DD Image File Path', name='staticBox1',
              parent=self.panEvidence, pos=wx.Point(8, 8), size=wx.Size(376,
              64), style=0)

        self.staticBox3 = wx.StaticBox(id=wxID_DLGWRITEIMAGETODISKSTATICBOX3,
              label=u'Select Device Drive To Write Image To:',
              name='staticBox3', parent=self.panEvidence, pos=wx.Point(8, 88),
              size=wx.Size(376, 136), style=0)

        self.txtImagePath = wx.TextCtrl(id=wxID_DLGWRITEIMAGETODISKTXTIMAGEPATH,
              name=u'txtImagePath', parent=self.panEvidence, pos=wx.Point(16,
              32), size=wx.Size(312, 21), style=0, value=u'')

        self.btnBrowseImageFile = wx.Button(id=wxID_DLGWRITEIMAGETODISKBTNBROWSEIMAGEFILE,
              label=u'...', name=u'btnBrowseImageFile', parent=self.panEvidence,
              pos=wx.Point(336, 32), size=wx.Size(43, 23), style=0)
        self.btnBrowseImageFile.Bind(wx.EVT_BUTTON,
              self.OnBtnBrowseImageFileButton,
              id=wxID_DLGWRITEIMAGETODISKBTNBROWSEIMAGEFILE)

    def __init__(self, parent):
        self._init_ctrls(parent)
        self.SetIcon(images.getMAKE2Icon())
        self.imageFileName = ""
        self.choiceSource = None
        self.IDLogicalDriveSource = wx.NewId()
        self.choiceSource = wx.Choice(choices=[],
          id=self.IDLogicalDriveSource, name='choiceSource',
          parent=self.panEvidence, pos=wx.Point(24, 112), size=wx.Size(192,
          21), style=0)
        #self.choiceSource.SetSelection(0)
        self.choiceSource.Show(False)
        self.listDriveNames = []
        
    def ShowErrorDialog(self, msg):
        dlg = wx.MessageDialog(self, msg,
              'Error', wx.OK | wx.ICON_ERROR)
        try:
            dlg.ShowModal()
        finally:
            dlg.Destroy()
            
    
    def OnBtnOKButton(self, event):
        msg = ""
            
        imagePath = self.txtImagePath.GetValue().strip()
        if not imagePath:
            msg = "Please select dd image file path!"
            
        elif not self.listDriveNames:
            msg = "Please add at least one destination device drive to write image to."
            
        elif not os.path.exists(imagePath):
            msg = "Please enter a valid image file path!"
        
        if msg <> "":
            CommonFunctions.ShowErrorMessage(self, msg, True)
            return

        try:
            import dlgDDToDiskParallelProgress
            ddDialog = dlgDDToDiskParallelProgress.create(self, imagePath, self.listDriveNames)
            ddDialog.ShowModal()

        finally:
            self.Destroy()


    def OnBtnCancelButton(self, event):
        self.Close()


    def OnBtnAddDestinationButton(self, event):
        imagePath = self.txtImagePath.GetValue().strip()
        if not imagePath:
            msg = "Please select dd image file path first!"
            CommonFunctions.ShowErrorMessage(self, msg, True)
            return
            
        if not os.path.exists(imagePath):
            CommonFunctions.ShowErrorMessage(self, "Please enter a valid image file path!", True)
            return
           
        st = os.stat(imagePath)
        imageSize = st[ST_SIZE]
                                 
        dlg = wx.DirDialog(self)
        try:
            if dlg.ShowModal() == wx.ID_OK:
                driveName = dlg.GetPath()
                driveName = driveName[:driveName.find(':')+1]
                #print driveName
                
                try:
                    rfin = Win32RawIO.Win32RAWIO(r'\\.\%s'%driveName, 'r')
                    if imageSize > rfin.size:
                        CommonFunctions.ShowErrorMessage(self, "Warning! Image file size bigger than the disk size!!", False)
                    rfin.close()
                    self.listDriveNames.append(r'\\.\%s'%driveName)
                    self.lstDestinations.Append([driveName])
                except Exception, msg:
                    CommonFunctions.ShowErrorMessage(self, str(msg), True)

        finally:
            dlg.Destroy()
        event.Skip()


    def OnBtnDeleteDestinationButton(self, event):
        #listItem = self.lstDestinations.get
        index = self.lstDestinations.GetFirstSelected()
        if index >=0:
            self.lstDestinations.DeleteItem(index)
            self.listDriveNames.pop(index)
        event.Skip()

    def OnBtnBrowseImageFileButton(self, event):
        dlg = wx.FileDialog(self, "Open DD Image File", ".", "", "All files (*.*)|*.*", wx.OPEN)
        try:
            if dlg.ShowModal() == wx.ID_OK:
                self.txtImagePath.SetValue(dlg.GetPath())
        
        finally:
            dlg.Destroy()
        event.Skip()


    
