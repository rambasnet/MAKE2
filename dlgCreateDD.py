#-----------------------------------------------------------------------------
# Name:        dlgCreateDD.py
# Purpose:     
#
# Author:      Ram B. Basnet
#
# Created:     2009/03/08
# RCS-ID:      $Id: dlgCreateDD.py $
# Copyright:   (c) 2006
# Licence:     All Rights Reserved.
# New field:   Whatever
#-----------------------------------------------------------------------------
#Boa:MDIChild:dlgCreateDD

import wx
import Constants
import Win32RawIO
import images
import CommonFunctions

def create(parent):
    return dlgCreateDD(parent)

[wxID_DLGCREATEDD, wxID_DLGCREATEDDBTNADDDESTINATION, 
 wxID_DLGCREATEDDBTNCANCEL, wxID_DLGCREATEDDBTNDELETEDESTINATION, 
 wxID_DLGCREATEDDBTNOK, wxID_DLGCREATEDDCHKVERIFYIMAGES, 
 wxID_DLGCREATEDDCHOICESOURCETYPE, wxID_DLGCREATEDDLBLPROJECTNAME, 
 wxID_DLGCREATEDDLSTDESTINATIONS, wxID_DLGCREATEDDNOTEBOOKASSESSMENT, 
 wxID_DLGCREATEDDPANEVIDENCE, wxID_DLGCREATEDDSTATICBOX1, 
 wxID_DLGCREATEDDSTATICBOX2, wxID_DLGCREATEDDSTATICBOX3, 
] = [wx.NewId() for _init_ctrls in range(14)]

class dlgCreateDD(wx.Dialog):
    def _init_coll_NoteBookAssessment_Pages(self, parent):
        # generated method, don't edit

        parent.AddPage(imageId=-1, page=self.panEvidence, select=False,
              text='Evidence')

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_DLGCREATEDD, name='dlgCreateDD',
              parent=prnt, pos=wx.Point(500, 118), size=wx.Size(437, 529),
              style=wx.DEFAULT_DIALOG_STYLE, title='RawImage')
        self.SetClientSize(wx.Size(429, 495))
        self.SetAutoLayout(True)
        self.SetBackgroundColour(wx.Colour(125, 152, 221))
        self.SetCursor(wx.STANDARD_CURSOR)
        self.SetMinSize(wx.Size(-1, -1))
        self.Center(wx.BOTH)

        self.NoteBookAssessment = wx.Notebook(id=wxID_DLGCREATEDDNOTEBOOKASSESSMENT,
              name='NoteBookAssessment', parent=self, pos=wx.Point(16, 48),
              size=wx.Size(400, 400), style=0)
        self.NoteBookAssessment.SetBackgroundColour(wx.Colour(125, 152, 221))
        self.NoteBookAssessment.SetAutoLayout(True)

        self.lblProjectName = wx.StaticText(id=wxID_DLGCREATEDDLBLPROJECTNAME,
              label='Create Raw DD Image    ', name='lblProjectName',
              parent=self, pos=wx.Point(0, 0), size=wx.Size(430, 32),
              style=wx.ALIGN_RIGHT | wx.RAISED_BORDER | wx.ST_NO_AUTORESIZE)
        self.lblProjectName.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, 'Tahoma'))
        self.lblProjectName.SetForegroundColour(wx.Colour(0, 78, 155))
        self.lblProjectName.SetBackgroundColour(wx.Colour(215, 235, 255))

        self.panEvidence = wx.Panel(id=wxID_DLGCREATEDDPANEVIDENCE,
              name='panEvidence', parent=self.NoteBookAssessment,
              pos=wx.Point(0, 0), size=wx.Size(392, 374),
              style=wx.TAB_TRAVERSAL)
        self.panEvidence.SetBackgroundColour(wx.Colour(225, 236, 255))

        self.btnOK = wx.Button(id=wxID_DLGCREATEDDBTNOK, label=u'&OK',
              name=u'btnOK', parent=self, pos=wx.Point(256, 456),
              size=wx.Size(75, 23), style=0)
        self.btnOK.Bind(wx.EVT_BUTTON, self.OnBtnOKButton,
              id=wxID_DLGCREATEDDBTNOK)

        self.btnCancel = wx.Button(id=wxID_DLGCREATEDDBTNCANCEL,
              label=u'&Cancel', name=u'btnCancel', parent=self,
              pos=wx.Point(336, 456), size=wx.Size(75, 23), style=0)
        self.btnCancel.Bind(wx.EVT_BUTTON, self.OnBtnCancelButton,
              id=wxID_DLGCREATEDDBTNCANCEL)

        self.choiceSourceType = wx.Choice(choices=[r'Select One...',
              r'Physical Drive', r'Logical Drive', r'Contents of a Folder'],
              id=wxID_DLGCREATEDDCHOICESOURCETYPE, name='choiceSourceType',
              parent=self.panEvidence, pos=wx.Point(24, 32), size=wx.Size(192,
              21), style=0)
        self.choiceSourceType.SetSelection(0)
        self.choiceSourceType.Bind(wx.EVT_CHOICE, self.OnChoiceSourceTypeChoice,
              id=wxID_DLGCREATEDDCHOICESOURCETYPE)

        self.lstDestinations = wx.ListCtrl(id=wxID_DLGCREATEDDLSTDESTINATIONS,
              name='lstDestinations', parent=self.panEvidence, pos=wx.Point(16,
              192), size=wx.Size(360, 72),
              style=wx.LC_LIST | wx.HSCROLL | wx.LC_SINGLE_SEL | wx.VSCROLL)

        self.staticBox1 = wx.StaticBox(id=wxID_DLGCREATEDDSTATICBOX1,
              label='Select Evidence Source Type:', name='staticBox1',
              parent=self.panEvidence, pos=wx.Point(8, 8), size=wx.Size(376,
              64), style=0)

        self.staticBox2 = wx.StaticBox(id=wxID_DLGCREATEDDSTATICBOX2,
              label='Select from the following available source:',
              name='staticBox2', parent=self.panEvidence, pos=wx.Point(8, 80),
              size=wx.Size(376, 80), style=0)

        self.staticBox3 = wx.StaticBox(id=wxID_DLGCREATEDDSTATICBOX3,
              label='Image Destination(s)', name='staticBox3',
              parent=self.panEvidence, pos=wx.Point(8, 168), size=wx.Size(376,
              136), style=0)

        self.btnAddDestination = wx.Button(id=wxID_DLGCREATEDDBTNADDDESTINATION,
              label='Add...', name='btnAddDestination', parent=self.panEvidence,
              pos=wx.Point(208, 272), size=wx.Size(75, 23), style=0)
        self.btnAddDestination.Bind(wx.EVT_BUTTON,
              self.OnBtnAddDestinationButton,
              id=wxID_DLGCREATEDDBTNADDDESTINATION)

        self.btnDeleteDestination = wx.Button(id=wxID_DLGCREATEDDBTNDELETEDESTINATION,
              label=u'Delete', name=u'btnDeleteDestination',
              parent=self.panEvidence, pos=wx.Point(296, 272), size=wx.Size(75,
              23), style=0)
        self.btnDeleteDestination.Enable(True)
        self.btnDeleteDestination.Bind(wx.EVT_BUTTON,
              self.OnBtnDeleteDestinationButton,
              id=wxID_DLGCREATEDDBTNDELETEDESTINATION)

        self.chkVerifyImages = wx.CheckBox(id=wxID_DLGCREATEDDCHKVERIFYIMAGES,
              label=u'Verify images after they are created',
              name='chkVerifyImages', parent=self.panEvidence, pos=wx.Point(16,
              328), size=wx.Size(216, 13), style=0)
        self.chkVerifyImages.SetValue(True)

        self._init_coll_NoteBookAssessment_Pages(self.NoteBookAssessment)

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
        self.listImageNames = []
        
    def ShowErrorDialog(self, msg):
        dlg = wx.MessageDialog(self, msg,
              'Error', wx.OK | wx.ICON_ERROR)
        try:
            dlg.ShowModal()
        finally:
            dlg.Destroy()
            
    
    def OnBtnOKButton(self, event):
        msg = ""
            
        if not self.choiceSourceType.GetStringSelection() == "Logical Drive":
            msg = "Please select Logical Drive which is the only supported source evidence type for now!"
            
        elif not self.listImageNames:
            msg = "Please add at least one destination image file path to the list."
            
        if msg <> "":
            CommonFunctions.ShowErrorMessage(self, msg, True)
            return

        driveName = self.choiceSource.GetStringSelection()
        self.rootDrive = r'\\.\%s:'%driveName[:driveName.find(':')]
            
        try:
            import dlgDDParallelProgress
            """
            PhysicalDrive = 0
            LogicalDrive = 1
            DiskDrive = 2
            ImageFile = 3
            FolderContents = 4
            """
            ddDialog = dlgDDParallelProgress.create(self, self.rootDrive,  self.listImageNames, Constants.LogicalDrive, self.chkVerifyImages.GetValue())
            #scanMAC.StartScan(dir)
            ddDialog.ShowModal()
            
            #self.Close()
        finally:
            self.Destroy()


    def OnBtnCancelButton(self, event):
        self.Close()

    def OnChoiceSourceTypeChoice(self, event):
        if self.choiceSourceType.GetStringSelection() == "Logical Drive":
            #if not hasattr(self, "IDLogicalDriveSource"):
            #logicalSources = []
            self.choiceSource.Show(True)
            self.choiceSource.Clear()
            for drive in Win32RawIO.GetWin32LogicalDrivesForDisplay():
                self.choiceSource.Append(drive)
            
                
        elif self.choiceSourceType == "Contents of a Folder":
            self.choiceSource.Clear()
            self.choiceSource.Show(False)
        else:
            self.choiceSource.Clear()
            self.choiceSourceType.Show(True)
            
        event.Skip()

    def OnBtnAddDestinationButton(self, event):
        dlg = wx.FileDialog(self, "Save Image File As", ".", "", "All files (*.*)|*.*", wx.SAVE)
        try:
            if dlg.ShowModal() == wx.ID_OK:
                imageFileName = dlg.GetPath()
                self.listImageNames.append(imageFileName)
                self.lstDestinations.Append([imageFileName])
            else:
                return False
        
        finally:
            dlg.Destroy()
        event.Skip()


    def OnBtnDeleteDestinationButton(self, event):
        #listItem = self.lstDestinations.get
        index = self.lstDestinations.GetFirstSelected()
        if index >=0:
            self.lstDestinations.DeleteItem(index)
            self.listImageNames.pop(index)
        event.Skip()


    
