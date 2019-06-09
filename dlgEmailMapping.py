#-----------------------------------------------------------------------------
# Name:        dlgEmailMapping.py
# Purpose:     
#
# Author:      Ram Basnet
#
# Created:     2008/04/17
# RCS-ID:      $Id: dlgEmailMapping.py $
# Copyright:   (c) 2008
# Licence:     All Rights Reserved.
#-----------------------------------------------------------------------------
#Boa:MDIChild:dlgEmailMapping

import wx
import wx.lib.buttons
import time
import os.path, sys

from wx.lib.anchors import LayoutAnchors
import images


def create(parent):
    return dlgEmailMapping(parent)

[wxID_DLGEMAILMAPPING, wxID_DLGEMAILMAPPINGBTNBROWSEATTACHMENTPATH, 
 wxID_DLGEMAILMAPPINGBTNBROWSEMESSAGEPATH, wxID_DLGEMAILMAPPINGBTNCANCEL, 
 wxID_DLGEMAILMAPPINGBTNOK, wxID_DLGEMAILMAPPINGPANSETTINGS, 
 wxID_DLGEMAILMAPPINGSTATICTEXT1, wxID_DLGEMAILMAPPINGSTATICTEXT2, 
 wxID_DLGEMAILMAPPINGTXTATTACHMENTFOLDERPATH, 
 wxID_DLGEMAILMAPPINGTXTMESSAGEFOLDERPATH, 
] = [wx.NewId() for _init_ctrls in range(10)]

class dlgEmailMapping(wx.Dialog):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_DLGEMAILMAPPING,
              name='dlgEmailMapping', parent=prnt, pos=wx.Point(594, 339),
              size=wx.Size(433, 244), style=wx.DEFAULT_DIALOG_STYLE,
              title='Map Emails With Attachments')
        self.SetClientSize(wx.Size(425, 210))
        self.SetAutoLayout(True)
        self.SetBackgroundColour(wx.Colour(125, 152, 221))
        self.SetCursor(wx.STANDARD_CURSOR)
        self.SetMinSize(wx.Size(-1, -1))
        self.Center(wx.BOTH)

        self.btnOK = wx.Button(id=wxID_DLGEMAILMAPPINGBTNOK,
              label='&Start Mapping', name=u'btnOK', parent=self,
              pos=wx.Point(232, 168), size=wx.Size(91, 23), style=0)
        self.btnOK.Bind(wx.EVT_BUTTON, self.OnBtnOKButton,
              id=wxID_DLGEMAILMAPPINGBTNOK)

        self.btnCancel = wx.Button(id=wxID_DLGEMAILMAPPINGBTNCANCEL,
              label=u'&Cancel', name=u'btnCancel', parent=self,
              pos=wx.Point(336, 168), size=wx.Size(75, 23), style=0)
        self.btnCancel.Bind(wx.EVT_BUTTON, self.OnBtnCancelButton,
              id=wxID_DLGEMAILMAPPINGBTNCANCEL)

        self.panSettings = wx.Panel(id=wxID_DLGEMAILMAPPINGPANSETTINGS,
              name='panSettings', parent=self, pos=wx.Point(16, 24),
              size=wx.Size(392, 128), style=wx.TAB_TRAVERSAL)
        self.panSettings.SetBackgroundColour(wx.Colour(225, 236, 255))
        self.panSettings.SetAutoLayout(True)

        self.txtAttachmentFolderPath = wx.TextCtrl(id=wxID_DLGEMAILMAPPINGTXTATTACHMENTFOLDERPATH,
              name='txtAttachmentFolderPath', parent=self.panSettings,
              pos=wx.Point(16, 80), size=wx.Size(312, 21), style=0, value='')
        self.txtAttachmentFolderPath.Enable(True)

        self.staticText2 = wx.StaticText(id=wxID_DLGEMAILMAPPINGSTATICTEXT2,
              label='Message Folder Path:', name='staticText2',
              parent=self.panSettings, pos=wx.Point(16, 16), size=wx.Size(104,
              13), style=0)

        self.staticText1 = wx.StaticText(id=wxID_DLGEMAILMAPPINGSTATICTEXT1,
              label='Attachment Folder Path:', name='staticText1',
              parent=self.panSettings, pos=wx.Point(16, 64), size=wx.Size(118,
              13), style=0)

        self.txtMessageFolderPath = wx.TextCtrl(id=wxID_DLGEMAILMAPPINGTXTMESSAGEFOLDERPATH,
              name='txtMessageFolderPath', parent=self.panSettings,
              pos=wx.Point(16, 32), size=wx.Size(312, 21), style=0, value='')

        self.btnBrowseMessagePath = wx.Button(id=wxID_DLGEMAILMAPPINGBTNBROWSEMESSAGEPATH,
              label='...', name='btnBrowseMessagePath', parent=self.panSettings,
              pos=wx.Point(336, 32), size=wx.Size(40, 23), style=0)
        self.btnBrowseMessagePath.Bind(wx.EVT_BUTTON,
              self.OnBtnBrowseMessagePathButton,
              id=wxID_DLGEMAILMAPPINGBTNBROWSEMESSAGEPATH)

        self.btnBrowseAttachmentPath = wx.Button(id=wxID_DLGEMAILMAPPINGBTNBROWSEATTACHMENTPATH,
              label='...', name='btnBrowseAttachmentPath',
              parent=self.panSettings, pos=wx.Point(336, 80), size=wx.Size(40,
              24), style=0)
        self.btnBrowseAttachmentPath.Bind(wx.EVT_BUTTON,
              self.OnBtnBrowseAttachmentPathButton,
              id=wxID_DLGEMAILMAPPINGBTNBROWSEATTACHMENTPATH)

    def __init__(self, parent):
        self._init_ctrls(parent)
        self.SetIcon(images.getMAKE2Icon())
                
    
    def OnBtnOKButton(self, event):
        busy = wx.BusyInfo("Mapping Emails with Attachments...It might take some time; just relax!")
        wx.Yield()
        import emailmapping
        emailmapping.msg_Folder_Path = self.txtMessageFolderPath.GetValue()
        emailmapping.att_Folder_Path = self.txtAttachmentFolderPath.GetValue()
        emailmapping.create_Interface()
        self.Close()
        event.Skip()
        
        
    def OnBtnCancelButton(self, event):
        self.Close()


    def OnBtnBrowseMessagePathButton(self, event):
        dlg = wx.DirDialog(self)
        try:
            if dlg.ShowModal() == wx.ID_OK:
                self.txtMessageFolderPath.SetValue(dlg.GetPath())
            
        finally:
            dlg.Destroy()
        event.Skip()
        

    def OnBtnBrowseAttachmentPathButton(self, event):
        dlg = wx.DirDialog(self)
        try:
            if dlg.ShowModal() == wx.ID_OK:
                self.txtAttachmentFolderPath.SetValue(dlg.GetPath())
            
        finally:
            dlg.Destroy()
        event.Skip()

    
