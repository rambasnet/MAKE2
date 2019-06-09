#Boa:MDIChild:dlgEmailMessageViewer

import wx
import wx.lib.buttons
import time
import os.path, sys

from wx.lib.anchors import LayoutAnchors

from SqliteDatabase import *
import Globals
import Constants
import CommonFunctions
import DBFunctions
import PlatformMethods
import Classes
import Win32RawIO
import images

def create(parent, sender, recipient, date, subject):
    return dlgEmailMessageViewer(parent, sender, recipient, date, subject)

[wxID_DLGEMAILMESSAGEVIEWER, wxID_DLGEMAILMESSAGEVIEWERBTNCLOSE, 
 wxID_DLGEMAILMESSAGEVIEWERNBMESSAGE, 
 wxID_DLGEMAILMESSAGEVIEWERPANHTMLMESSAGE, 
 wxID_DLGEMAILMESSAGEVIEWERPANMESSAGES, 
 wxID_DLGEMAILMESSAGEVIEWERPANTEXTMESSAGE, 
 wxID_DLGEMAILMESSAGEVIEWERSTATICTEXT1, 
 wxID_DLGEMAILMESSAGEVIEWERSTATICTEXT12, 
 wxID_DLGEMAILMESSAGEVIEWERSTATICTEXT13, 
 wxID_DLGEMAILMESSAGEVIEWERSTATICTEXT2, wxID_DLGEMAILMESSAGEVIEWERSTATICTEXT3, 
 wxID_DLGEMAILMESSAGEVIEWERSTATICTEXT4, 
 wxID_DLGEMAILMESSAGEVIEWERTXTATTACHMENTS, wxID_DLGEMAILMESSAGEVIEWERTXTDATE, 
 wxID_DLGEMAILMESSAGEVIEWERTXTFROM, wxID_DLGEMAILMESSAGEVIEWERTXTMESSAGE, 
 wxID_DLGEMAILMESSAGEVIEWERTXTSUBJECT, wxID_DLGEMAILMESSAGEVIEWERTXTTO, 
] = [wx.NewId() for _init_ctrls in range(18)]

class dlgEmailMessageViewer(wx.Dialog):
    def _init_coll_nbMessage_Pages(self, parent):
        # generated method, don't edit

        parent.AddPage(imageId=-1, page=self.panHTMLMessage, select=False,
              text='HTMLView')
        parent.AddPage(imageId=-1, page=self.panTextMessage, select=True,
              text='Text View')

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_DLGEMAILMESSAGEVIEWER,
              name='dlgEmailMessageViewer', parent=prnt, pos=wx.Point(366, 28),
              size=wx.Size(832, 648),
              style=wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.DEFAULT_DIALOG_STYLE,
              title='Email Message Deatails')
        self.SetClientSize(wx.Size(824, 614))
        self.SetAutoLayout(True)
        self.SetBackgroundColour(wx.Colour(125, 152, 221))
        self.SetCursor(wx.STANDARD_CURSOR)
        self.SetMinSize(wx.Size(-1, -1))
        self.Center(wx.BOTH)

        self.btnClose = wx.Button(id=wxID_DLGEMAILMESSAGEVIEWERBTNCLOSE,
              label='&Close', name='btnClose', parent=self, pos=wx.Point(728,
              580), size=wx.Size(81, 23), style=0)
        self.btnClose.SetConstraints(LayoutAnchors(self.btnClose, False, False,
              True, True))
        self.btnClose.Bind(wx.EVT_BUTTON, self.OnBtnCancelButton,
              id=wxID_DLGEMAILMESSAGEVIEWERBTNCLOSE)

        self.panMessages = wx.Panel(id=-1, name='panSettings', parent=self,
              pos=wx.Point(16, 16), size=wx.Size(792, 549),
              style=wx.TAB_TRAVERSAL)
        self.panMessages.SetBackgroundColour(wx.Colour(225, 236, 255))
        self.panMessages.SetAutoLayout(False)
        self.panMessages.SetConstraints(LayoutAnchors(self.panMessages, True,
              True, True, True))

        self.txtTo = wx.TextCtrl(id=wxID_DLGEMAILMESSAGEVIEWERTXTTO,
              name='txtTo', parent=self.panMessages, pos=wx.Point(80, 40),
              size=wx.Size(696, 48),
              style=wx.TE_READONLY | wx.TE_MULTILINE | wx.VSCROLL, value='')
        self.txtTo.Enable(True)

        self.staticText2 = wx.StaticText(id=wxID_DLGEMAILMESSAGEVIEWERSTATICTEXT2,
              label='From:', name='staticText2', parent=self.panMessages,
              pos=wx.Point(8, 8), size=wx.Size(28, 13), style=0)

        self.staticText1 = wx.StaticText(id=wxID_DLGEMAILMESSAGEVIEWERSTATICTEXT1,
              label='To:', name='staticText1', parent=self.panMessages,
              pos=wx.Point(8, 40), size=wx.Size(16, 13), style=0)

        self.staticText13 = wx.StaticText(id=wxID_DLGEMAILMESSAGEVIEWERSTATICTEXT13,
              label='Subject:', name='staticText13', parent=self.panMessages,
              pos=wx.Point(8, 136), size=wx.Size(40, 13), style=0)

        self.txtFrom = wx.TextCtrl(id=wxID_DLGEMAILMESSAGEVIEWERTXTFROM,
              name='txtFrom', parent=self.panMessages, pos=wx.Point(80, 8),
              size=wx.Size(392, 21), style=wx.TE_READONLY, value='')

        self.txtSubject = wx.TextCtrl(id=wxID_DLGEMAILMESSAGEVIEWERTXTSUBJECT,
              name='txtSubject', parent=self.panMessages, pos=wx.Point(80, 136),
              size=wx.Size(696, 21), style=wx.TE_READONLY, value='')

        self.txtDate = wx.TextCtrl(id=wxID_DLGEMAILMESSAGEVIEWERTXTDATE,
              name='txtDate', parent=self.panMessages, pos=wx.Point(80, 104),
              size=wx.Size(392, 21), style=wx.TE_READONLY, value='')

        self.staticText3 = wx.StaticText(id=wxID_DLGEMAILMESSAGEVIEWERSTATICTEXT3,
              label='Date:', name='staticText3', parent=self.panMessages,
              pos=wx.Point(8, 104), size=wx.Size(27, 13), style=0)

        self.staticText12 = wx.StaticText(id=wxID_DLGEMAILMESSAGEVIEWERSTATICTEXT12,
              label='Attachments:', name='staticText12',
              parent=self.panMessages, pos=wx.Point(8, 168), size=wx.Size(65,
              13), style=0)

        self.staticText4 = wx.StaticText(id=wxID_DLGEMAILMESSAGEVIEWERSTATICTEXT4,
              label='Message:', name='staticText4', parent=self.panMessages,
              pos=wx.Point(8, 200), size=wx.Size(46, 13), style=0)

        self.txtAttachments = wx.TextCtrl(id=wxID_DLGEMAILMESSAGEVIEWERTXTATTACHMENTS,
              name='txtAttachments', parent=self.panMessages, pos=wx.Point(80,
              168), size=wx.Size(696, 21), style=wx.TE_READONLY, value='')

        self.nbMessage = wx.Notebook(id=wxID_DLGEMAILMESSAGEVIEWERNBMESSAGE,
              name='nbMessage', parent=self.panMessages, pos=wx.Point(8, 224),
              size=wx.Size(776, 312), style=0)
        self.nbMessage.SetConstraints(LayoutAnchors(self.nbMessage, True, True,
              True, True))

        self.panTextMessage = wx.Panel(id=wxID_DLGEMAILMESSAGEVIEWERPANTEXTMESSAGE,
              name='panTextMessage', parent=self.nbMessage, pos=wx.Point(0, 0),
              size=wx.Size(768, 286), style=wx.TAB_TRAVERSAL)
        self.panTextMessage.SetAutoLayout(True)

        self.panHTMLMessage = wx.Panel(id=wxID_DLGEMAILMESSAGEVIEWERPANHTMLMESSAGE,
              name='panHTMLView', parent=self.nbMessage, pos=wx.Point(0, 0),
              size=wx.Size(768, 286), style=wx.TAB_TRAVERSAL)
        self.panHTMLMessage.SetAutoLayout(True)

        self.txtMessage = wx.TextCtrl(id=wxID_DLGEMAILMESSAGEVIEWERTXTMESSAGE,
              name='txtMessage', parent=self.panTextMessage, pos=wx.Point(0, 0),
              size=wx.Size(768, 286),
              style=wx.VSCROLL | wx.TE_WORDWRAP | wx.TE_READONLY | wx.TE_MULTILINE,
              value='')
        self.txtMessage.SetConstraints(LayoutAnchors(self.txtMessage, True,
              True, True, True))
        self.txtMessage.SetAutoLayout(False)

        self._init_coll_nbMessage_Pages(self.nbMessage)

    def __init__(self, parent, sender, recipient, date, subject):
        self._init_ctrls(parent)
        self.SetIcon(images.getMAKE2Icon())
        
        self.CreateHTMLCtrl()
        self.sender = sender
        self.recipient = recipient
        self.date = date
        self.subject = subject
        self.message = ""
        self.attachments = ""
        self.GetMessage()
        self.txtFrom.SetValue(self.sender)
        self.txtTo.SetValue(self.recipient)
        self.txtDate.SetValue(self.date)
        self.txtSubject.SetValue(PlatformMethods.Decode(self.subject))
        self.txtAttachments.SetValue(PlatformMethods.Decode(self.attachments))
        self.txtMessage.SetValue(self.message)
        self.htmlMessage.SetPage(self.message)

    def GetMessage(self):
        db = SqliteDatabase(Globals.EmailsFileName)
        if not db.OpenConnection():
            return
        query = "select Attachments, Message from %s where FromID = %s and ToID = %s and EmailDate = %s and Subject=%s;"%(db.SqlSQuote(Constants.EmailsTable), db.SqlSQuote(self.sender), db.SqlSQuote(self.recipient), db.SqlSQuote(self.date), db.SqlSQuote(self.subject))
        rows = db.FetchAllRows(query)
        
        #print 'query len ', len(rows)
        for row in rows:
            #totalAttachments = row[3].split(",")
            self.atachments = PlatformMethods.Decode(row[0])
            self.message = PlatformMethods.Decode(row[1])
            
        #print 'msg dict ', len(MessageDict)
        db.CloseConnection()
        
        
    def CreateHTMLCtrl(self):
        
        self.htmlMessage = wx.html.HtmlWindow(self.panHTMLMessage, -1, wx.Point(0, 0), wx.Size(768, 286))
        if "gtk2" in wx.PlatformInfo:
            self.htmlMessage.SetStandardFonts()
        self.htmlMessage.SetConstraints(LayoutAnchors(self.htmlMessage, True,
              True, True, True))
              
        
    def OnBtnCancelButton(self, event):
        self.Close()



    
