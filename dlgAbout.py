#-----------------------------------------------------------------------------
# Name:        dlgAbout.py
# Purpose:     
#
# Author:      Ram Basnet
#
# Created:     2007/11/10
# RCS-ID:      $Id: dlgAbout.py,v 1.1 2007/11/13 19:52:48 rbasnet Exp $
# Copyright:   (c) 2006
# Licence:     <your licence>
# New field:   Whatever
#-----------------------------------------------------------------------------
#Boa:Dialog:dlgAbout

import wx
import images

def create(parent):
    return dlgAbout(parent)

[wxID_DLGABOUT, wxID_DLGABOUTBTNCLOSE, wxID_DLGABOUTLBLABOUT, 
 wxID_DLGABOUTPANABOUT, wxID_DLGABOUTSTATICTEXT1, wxID_DLGABOUTSTATICTEXT4, 
 wxID_DLGABOUTSTATICTEXT5, wxID_DLGABOUTSTATICTEXT6, 
] = [wx.NewId() for _init_ctrls in range(8)]

class dlgAbout(wx.Dialog):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_DLGABOUT, name='dlgAbout', parent=prnt,
              pos=wx.Point(424, 257), size=wx.Size(474, 396),
              style=wx.DEFAULT_DIALOG_STYLE, title='MAKE')
        self.SetClientSize(wx.Size(466, 362))
        self.SetBackgroundColour(wx.Colour(125, 152, 221))
        self.Center(wx.BOTH)

        self.panAbout = wx.Panel(id=wxID_DLGABOUTPANABOUT, name='panAbout',
              parent=self, pos=wx.Point(16, 16), size=wx.Size(432, 328),
              style=wx.TAB_TRAVERSAL)
        self.panAbout.SetBackgroundColour(wx.Colour(225, 236, 255))

        self.staticText1 = wx.StaticText(id=wxID_DLGABOUTSTATICTEXT1, label='',
              name='staticText1', parent=self, pos=wx.Point(0, 8),
              size=wx.Size(0, 13), style=0)

        self.btnClose = wx.Button(id=wxID_DLGABOUTBTNCLOSE, label='&OK',
              name='btnClose', parent=self.panAbout, pos=wx.Point(200, 296),
              size=wx.Size(75, 23), style=0)
        self.btnClose.Bind(wx.EVT_BUTTON, self.OnBtnCloseButton,
              id=wxID_DLGABOUTBTNCLOSE)

        self.staticText4 = wx.StaticText(id=wxID_DLGABOUTSTATICTEXT4,
              label='Copyright: 2008 Contributors. All Rights Reserved.',
              name='staticText4', parent=self.panAbout, pos=wx.Point(16, 248),
              size=wx.Size(400, 40),
              style=wx.ALIGN_CENTRE | wx.ST_NO_AUTORESIZE)
        self.staticText4.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.staticText4.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'Tahoma'))

        self.staticText5 = wx.StaticText(id=wxID_DLGABOUTSTATICTEXT5,
              label='MAKE2 - Media Analysis and Knowledge Extraction and Exploration',
              name='staticText5', parent=self.panAbout, pos=wx.Point(16, 16),
              size=wx.Size(400, 112),
              style=wx.ALIGN_CENTRE | wx.ST_NO_AUTORESIZE)
        self.staticText5.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.staticText5.SetFont(wx.Font(20, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, 'Tahoma'))

        self.lblAbout = wx.StaticText(id=wxID_DLGABOUTLBLABOUT,
              label='A Complete Digital Forensic Suite', name='lblAbout',
              parent=self.panAbout, pos=wx.Point(16, 128), size=wx.Size(400,
              48), style=wx.ALIGN_CENTRE | wx.ST_NO_AUTORESIZE)
        self.lblAbout.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.lblAbout.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'Tahoma'))

        self.staticText6 = wx.StaticText(id=wxID_DLGABOUTSTATICTEXT6,
              label=u'Version: Beta', name='staticText6', parent=self.panAbout,
              pos=wx.Point(16, 176), size=wx.Size(400, 72),
              style=wx.ALIGN_CENTRE | wx.ST_NO_AUTORESIZE)
        self.staticText6.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.staticText6.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, 'Tahoma'))

    def __init__(self, parent):
        self._init_ctrls(parent)
        self.SetIcon(images.getMAKE2Icon())

    def OnBtnCloseButton(self, event):
        self.Close()
