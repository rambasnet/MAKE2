#Boa:MiniFrame:MDIChildEmails

#-----------------------------------------------------------------------------
# Name:        MDIChildEmails.py
# Purpose:     
#
# Author:      Ram Basnet
#
# Created:     2007/11/01
# Last Modified: 6/30/2009
# RCS-ID:      $Id: MDIChildEmails.py,v 1.5 2008/03/17 04:18:38 rbasnet Exp $
# Copyright:   (c) 2007
# Licence:     All Rights Reserved.
#-----------------------------------------------------------------------------

import wx, sys, os, time
import re, string
import binascii
from wx.lib.anchors import LayoutAnchors
import  wx.lib.mixins.listctrl  as  listmix

from SqliteDatabase import *
import Globals
import PlatformMethods
import CommonFunctions
import Constants
import DBFunctions
import EmailUtilities

import  images
import dlgEmailMessageViewer
from Search import *

def create(parent):
    return MDIChildEmails(parent)

class CustomListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, ID, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        
        
[wxID_MDICHILDEMAILS, wxID_MDICHILDEMAILSBTNCENTRALEMAILMAP, 
 wxID_MDICHILDEMAILSBTNDISPLAYALLMESSAGE, 
 wxID_MDICHILDEMAILSBTNDISPLAYTOPKEYWORDS, 
 wxID_MDICHILDEMAILSBTNDISPLAYTOPPHONES, 
 wxID_MDICHILDEMAILSBTNEXPORTTOPKEYWORDS, 
 wxID_MDICHILDEMAILSBTNEXPORTTOPPHONES, 
 wxID_MDICHILDEMAILSBTNEXTRACTEMAILSATTACHMENTS, 
 wxID_MDICHILDEMAILSBTNPREPROCESSING, wxID_MDICHILDEMAILSBTNSEARCH, 
 wxID_MDICHILDEMAILSBTNSEARCHADDRESSBOOK, 
 wxID_MDICHILDEMAILSBTNSHOWALLADDRESSES, 
 wxID_MDICHILDEMAILSBTNSHOWMESSAGESEMAILDATE, 
 wxID_MDICHILDEMAILSCHOICEADDRESSPAGE, wxID_MDICHILDEMAILSCHOICEMESSAGEPAGE, 
 wxID_MDICHILDEMAILSDATEEND, wxID_MDICHILDEMAILSDATESTART, 
 wxID_MDICHILDEMAILSLBLADDRESSBOOKHEADING, wxID_MDICHILDEMAILSLBLADDRESSPAGE, 
 wxID_MDICHILDEMAILSLBLKEYWORDSSEARCH, wxID_MDICHILDEMAILSLBLMESSAGESHEADING, 
 wxID_MDICHILDEMAILSLBLTOTALMESSAGES, wxID_MDICHILDEMAILSNOTEBOOKEMAILS, 
 wxID_MDICHILDEMAILSPANADDRESSBOOK, wxID_MDICHILDEMAILSPANKEYWORDS, 
 wxID_MDICHILDEMAILSPANMESSAGES, wxID_MDICHILDEMAILSPANTOOLS, 
 wxID_MDICHILDEMAILSSTATICBOX1, wxID_MDICHILDEMAILSSTATICBOX2, 
 wxID_MDICHILDEMAILSSTATICBOX3, wxID_MDICHILDEMAILSSTATICBOX4, 
 wxID_MDICHILDEMAILSSTATICBOX5, wxID_MDICHILDEMAILSSTATICTEXT1, 
 wxID_MDICHILDEMAILSSTATICTEXT2, wxID_MDICHILDEMAILSSTATICTEXT3, 
 wxID_MDICHILDEMAILSSTATICTEXT4, wxID_MDICHILDEMAILSSTATICTEXT5, 
 wxID_MDICHILDEMAILSSTATICTEXT6, wxID_MDICHILDEMAILSSTATICTEXT7, 
 wxID_MDICHILDEMAILSSTATICTEXT9, wxID_MDICHILDEMAILSTXTTOPKEYWORDS, 
 wxID_MDICHILDEMAILSTXTTOPPHONES, 
] = [wx.NewId() for _init_ctrls in range(42)]

class MDIChildEmails(wx.MDIChildFrame, listmix.ColumnSorterMixin):

    def _init_coll_notebookEmails_Pages(self, parent):
        # generated method, don't edit

        parent.AddPage(imageId=-1, page=self.panTools, select=True,
              text='Tools')
        parent.AddPage(imageId=-1, page=self.panMessages, select=False,
              text='Messages')
        parent.AddPage(imageId=-1, page=self.panAddressBook, select=False,
              text='Address Book')
        parent.AddPage(imageId=-1, page=self.panKeywords, select=False,
              text=u'Top: Terms | Phone Numbers')

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.MDIChildFrame.__init__(self, id=wxID_MDICHILDEMAILS,
              name='MDIChildEmails', parent=prnt, pos=wx.Point(171, 29),
              size=wx.Size(1048, 714), style=wx.DEFAULT_FRAME_STYLE,
              title='Emails Analysis')
        self.SetClientSize(wx.Size(1040, 680))
        self.SetBackgroundColour(wx.Colour(125, 152, 221))
        self.SetAutoLayout(True)

        self.notebookEmails = wx.Notebook(id=wxID_MDICHILDEMAILSNOTEBOOKEMAILS,
              name='notebookEmails', parent=self, pos=wx.Point(4, 4),
              size=wx.Size(1032, 672), style=0)
        self.notebookEmails.SetConstraints(LayoutAnchors(self.notebookEmails,
              True, True, True, True))

        self.panMessages = wx.Panel(id=wxID_MDICHILDEMAILSPANMESSAGES,
              name='panMessages', parent=self.notebookEmails, pos=wx.Point(0,
              0), size=wx.Size(1024, 646), style=wx.TAB_TRAVERSAL)
        self.panMessages.SetBackgroundColour(wx.Colour(225, 236, 255))
        self.panMessages.SetAutoLayout(True)
        self.panMessages.SetAutoLayout(True)

        self.panTools = wx.Panel(id=wxID_MDICHILDEMAILSPANTOOLS,
              name='panTools', parent=self.notebookEmails, pos=wx.Point(0, 0),
              size=wx.Size(1024, 646), style=wx.TAB_TRAVERSAL)
        self.panTools.SetBackgroundColour(wx.Colour(225, 236, 255))

        self.lblKeywordsSearch = wx.StaticText(id=wxID_MDICHILDEMAILSLBLKEYWORDSSEARCH,
              label='Visualization:', name=u'lblKeywordsSearch',
              parent=self.panTools, pos=wx.Point(16, 56), size=wx.Size(87, 16),
              style=0)
        self.lblKeywordsSearch.SetForegroundColour(wx.Colour(0, 0, 187))
        self.lblKeywordsSearch.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, u'Tahoma'))
        self.lblKeywordsSearch.SetConstraints(LayoutAnchors(self.lblKeywordsSearch,
              True, True, False, False))

        self.staticText2 = wx.StaticText(id=wxID_MDICHILDEMAILSSTATICTEXT2,
              label='Preprocessing:', name='staticText2', parent=self.panTools,
              pos=wx.Point(16, 16), size=wx.Size(97, 16), style=0)
        self.staticText2.SetForegroundColour(wx.Colour(0, 0, 187))
        self.staticText2.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, u'Tahoma'))
        self.staticText2.SetConstraints(LayoutAnchors(self.staticText2, True,
              True, False, False))

        self.btnPreprocessing = wx.Button(id=wxID_MDICHILDEMAILSBTNPREPROCESSING,
              label='Emails Preprocessing...', name=u'btnPreprocessing',
              parent=self.panTools, pos=wx.Point(144, 8), size=wx.Size(168, 24),
              style=0)
        self.btnPreprocessing.Bind(wx.EVT_BUTTON, self.OnBtnPreprocessingButton,
              id=wxID_MDICHILDEMAILSBTNPREPROCESSING)

        self.btnCentralEmailMap = wx.Button(id=wxID_MDICHILDEMAILSBTNCENTRALEMAILMAP,
              label='Central Email Graph...', name='btnCentralEmailMap',
              parent=self.panTools, pos=wx.Point(144, 48), size=wx.Size(168,
              23), style=0)
        self.btnCentralEmailMap.Bind(wx.EVT_BUTTON,
              self.OnBtnCentralEmailMapButton,
              id=wxID_MDICHILDEMAILSBTNCENTRALEMAILMAP)

        self.btnExtractEmailsAttachments = wx.Button(id=wxID_MDICHILDEMAILSBTNEXTRACTEMAILSATTACHMENTS,
              label='Generate Keywords Report',
              name='btnExtractEmailsAttachments', parent=self.panTools,
              pos=wx.Point(144, 88), size=wx.Size(168, 23), style=0)
        self.btnExtractEmailsAttachments.Bind(wx.EVT_BUTTON,
              self.OnBtnExtractEmailsAttachmentsButton,
              id=wxID_MDICHILDEMAILSBTNEXTRACTEMAILSATTACHMENTS)

        self.staticText1 = wx.StaticText(id=wxID_MDICHILDEMAILSSTATICTEXT1,
              label='Reports:', name='staticText1', parent=self.panTools,
              pos=wx.Point(16, 96), size=wx.Size(57, 16), style=0)
        self.staticText1.SetForegroundColour(wx.Colour(0, 0, 187))
        self.staticText1.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, u'Tahoma'))
        self.staticText1.SetConstraints(LayoutAnchors(self.staticText1, True,
              True, False, False))

        self.staticText4 = wx.StaticText(id=wxID_MDICHILDEMAILSSTATICTEXT4,
              label='End:', name='staticText4', parent=self.panMessages,
              pos=wx.Point(160, 32), size=wx.Size(28, 16), style=0)
        self.staticText4.SetForegroundColour(wx.Colour(0, 0, 187))
        self.staticText4.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, u'Tahoma'))
        self.staticText4.SetConstraints(LayoutAnchors(self.staticText4, True,
              True, False, False))

        self.lblMessagesHeading = wx.StaticText(id=wxID_MDICHILDEMAILSLBLMESSAGESHEADING,
              label='Displaying All Messages', name='lblMessagesHeading',
              parent=self.panMessages, pos=wx.Point(352, 72), size=wx.Size(153,
              16), style=wx.ALIGN_CENTRE)
        self.lblMessagesHeading.SetForegroundColour(wx.Colour(0, 0, 187))
        self.lblMessagesHeading.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL,
              wx.BOLD, False, u'Tahoma'))
        self.lblMessagesHeading.SetConstraints(LayoutAnchors(self.lblMessagesHeading,
              True, True, True, False))

        self.btnShowMessagesEmailDate = wx.Button(id=wxID_MDICHILDEMAILSBTNSHOWMESSAGESEMAILDATE,
              label='Show', name=u'btnShowMessagesEmailDate',
              parent=self.panMessages, pos=wx.Point(296, 32), size=wx.Size(56,
              23), style=0)
        self.btnShowMessagesEmailDate.Bind(wx.EVT_BUTTON,
              self.OnBtnShowMessagesEmailDateButton,
              id=wxID_MDICHILDEMAILSBTNSHOWMESSAGESEMAILDATE)

        self.panKeywords = wx.Panel(id=wxID_MDICHILDEMAILSPANKEYWORDS,
              name='panKeywords', parent=self.notebookEmails, pos=wx.Point(0,
              0), size=wx.Size(1024, 646), style=wx.TAB_TRAVERSAL)
        self.panKeywords.SetBackgroundColour(wx.Colour(225, 236, 255))
        self.panKeywords.SetAutoLayout(True)

        self.staticBox1 = wx.StaticBox(id=wxID_MDICHILDEMAILSSTATICBOX1,
              label=u'Terms', name='staticBox1', parent=self.panKeywords,
              pos=wx.Point(8, 8), size=wx.Size(392, 632), style=0)
        self.staticBox1.SetConstraints(LayoutAnchors(self.staticBox1, True,
              True, False, True))

        self.staticBox2 = wx.StaticBox(id=wxID_MDICHILDEMAILSSTATICBOX2,
              label='Phone Numbers', name='staticBox2', parent=self.panKeywords,
              pos=wx.Point(416, 8), size=wx.Size(424, 632), style=0)
        self.staticBox2.SetConstraints(LayoutAnchors(self.staticBox2, True,
              True, False, True))

        self.btnDisplayTopPhones = wx.Button(id=wxID_MDICHILDEMAILSBTNDISPLAYTOPPHONES,
              label='Display', name='btnDisplayTopPhones',
              parent=self.panKeywords, pos=wx.Point(592, 32), size=wx.Size(75,
              23), style=0)
        self.btnDisplayTopPhones.Bind(wx.EVT_BUTTON,
              self.OnBtnDisplayTopPhonesButton,
              id=wxID_MDICHILDEMAILSBTNDISPLAYTOPPHONES)

        self.staticText3 = wx.StaticText(id=wxID_MDICHILDEMAILSSTATICTEXT3,
              label='Top:', name='staticText3', parent=self.panKeywords,
              pos=wx.Point(16, 32), size=wx.Size(28, 16), style=0)
        self.staticText3.SetForegroundColour(wx.Colour(0, 0, 187))
        self.staticText3.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, u'Tahoma'))
        self.staticText3.SetConstraints(LayoutAnchors(self.staticText3, True,
              True, False, False))

        self.txtTopPhones = wx.TextCtrl(id=wxID_MDICHILDEMAILSTXTTOPPHONES,
              name='txtTopPhones', parent=self.panKeywords, pos=wx.Point(472,
              32), size=wx.Size(100, 21), style=0, value='')

        self.txtTopKeywords = wx.TextCtrl(id=wxID_MDICHILDEMAILSTXTTOPKEYWORDS,
              name='txtTopKeywords', parent=self.panKeywords, pos=wx.Point(48,
              32), size=wx.Size(100, 21), style=0, value='')

        self.staticText6 = wx.StaticText(id=wxID_MDICHILDEMAILSSTATICTEXT6,
              label='Top:', name='staticText6', parent=self.panKeywords,
              pos=wx.Point(440, 32), size=wx.Size(28, 16), style=0)
        self.staticText6.SetForegroundColour(wx.Colour(0, 0, 187))
        self.staticText6.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, u'Tahoma'))
        self.staticText6.SetConstraints(LayoutAnchors(self.staticText6, True,
              True, False, False))

        self.btnExportTopKeywords = wx.Button(id=wxID_MDICHILDEMAILSBTNEXPORTTOPKEYWORDS,
              label='Export...', name='btnExportTopKeywords',
              parent=self.panKeywords, pos=wx.Point(264, 32), size=wx.Size(75,
              23), style=0)
        self.btnExportTopKeywords.Bind(wx.EVT_BUTTON,
              self.OnBtnExportTopKeywordsButton,
              id=wxID_MDICHILDEMAILSBTNEXPORTTOPKEYWORDS)

        self.btnDisplayTopKeywords = wx.Button(id=wxID_MDICHILDEMAILSBTNDISPLAYTOPKEYWORDS,
              label='Display', name='btnDisplayTopKeywords',
              parent=self.panKeywords, pos=wx.Point(168, 32), size=wx.Size(75,
              23), style=0)
        self.btnDisplayTopKeywords.Bind(wx.EVT_BUTTON,
              self.OnBtnDisplayTopKeywordsButton,
              id=wxID_MDICHILDEMAILSBTNDISPLAYTOPKEYWORDS)

        self.btnExportTopPhones = wx.Button(id=wxID_MDICHILDEMAILSBTNEXPORTTOPPHONES,
              label='Export...', name='btnExportTopPhones',
              parent=self.panKeywords, pos=wx.Point(688, 32), size=wx.Size(75,
              23), style=0)
        self.btnExportTopPhones.Bind(wx.EVT_BUTTON,
              self.OnBtnExportTopPhonesButton,
              id=wxID_MDICHILDEMAILSBTNEXPORTTOPPHONES)

        self.staticBox3 = wx.StaticBox(id=wxID_MDICHILDEMAILSSTATICBOX3,
              label=u'Filter Messages Based on Email Date', name='staticBox3',
              parent=self.panMessages, pos=wx.Point(8, 8), size=wx.Size(448,
              56), style=0)

        self.staticBox4 = wx.StaticBox(id=wxID_MDICHILDEMAILSSTATICBOX4,
              label=u'Search Messages', name='staticBox4',
              parent=self.panMessages, pos=wx.Point(464, 8), size=wx.Size(376,
              56), style=0)

        self.btnSearch = wx.Button(id=wxID_MDICHILDEMAILSBTNSEARCH,
              label='Search', name='btnSearch', parent=self.panMessages,
              pos=wx.Point(768, 32), size=wx.Size(59, 23), style=0)
        self.btnSearch.Bind(wx.EVT_BUTTON, self.OnBtnSearchButton,
              id=wxID_MDICHILDEMAILSBTNSEARCH)

        self.btnDisplayAllMessage = wx.Button(id=wxID_MDICHILDEMAILSBTNDISPLAYALLMESSAGE,
              label=u'Show All', name=u'btnDisplayAllMessage',
              parent=self.panMessages, pos=wx.Point(368, 32), size=wx.Size(80,
              23), style=0)
        self.btnDisplayAllMessage.Bind(wx.EVT_BUTTON,
              self.OnBtnDisplayAllMessageButton,
              id=wxID_MDICHILDEMAILSBTNDISPLAYALLMESSAGE)

        self.staticText7 = wx.StaticText(id=wxID_MDICHILDEMAILSSTATICTEXT7,
              label='Start:', name='staticText7', parent=self.panMessages,
              pos=wx.Point(16, 32), size=wx.Size(39, 16), style=0)
        self.staticText7.SetForegroundColour(wx.Colour(0, 0, 187))
        self.staticText7.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, u'Tahoma'))
        self.staticText7.SetConstraints(LayoutAnchors(self.staticText7, True,
              True, False, False))

        self.panAddressBook = wx.Panel(id=wxID_MDICHILDEMAILSPANADDRESSBOOK,
              name='panAddressBook', parent=self.notebookEmails, pos=wx.Point(0,
              0), size=wx.Size(1024, 646), style=wx.TAB_TRAVERSAL)
        self.panAddressBook.SetBackgroundColour(wx.Colour(225, 236, 255))
        self.panAddressBook.SetAutoLayout(True)

        self.staticBox5 = wx.StaticBox(id=wxID_MDICHILDEMAILSSTATICBOX5,
              label='Search Address Book', name='staticBox5',
              parent=self.panAddressBook, pos=wx.Point(8, 8), size=wx.Size(376,
              56), style=0)

        self.btnSearchAddressBook = wx.Button(id=wxID_MDICHILDEMAILSBTNSEARCHADDRESSBOOK,
              label='Search', name='btnSearchAddressBook',
              parent=self.panAddressBook, pos=wx.Point(312, 32),
              size=wx.Size(59, 23), style=0)
        self.btnSearchAddressBook.Bind(wx.EVT_BUTTON,
              self.OnBtnSearchAddressBookButton,
              id=wxID_MDICHILDEMAILSBTNSEARCHADDRESSBOOK)

        self.lblAddressBookHeading = wx.StaticText(id=wxID_MDICHILDEMAILSLBLADDRESSBOOKHEADING,
              label='Displaying All Addresses', name='lblAddressBookHeading',
              parent=self.panAddressBook, pos=wx.Point(288, 72),
              size=wx.Size(158, 16), style=wx.ALIGN_CENTRE)
        self.lblAddressBookHeading.SetForegroundColour(wx.Colour(0, 0, 187))
        self.lblAddressBookHeading.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL,
              wx.BOLD, False, u'Tahoma'))
        self.lblAddressBookHeading.SetConstraints(LayoutAnchors(self.lblAddressBookHeading,
              True, True, True, False))

        self.staticText5 = wx.StaticText(id=wxID_MDICHILDEMAILSSTATICTEXT5,
              label=u'Page', name='staticText5', parent=self.panMessages,
              pos=wx.Point(8, 72), size=wx.Size(24, 13), style=0)

        self.choiceMessagePage = wx.Choice(choices=[],
              id=wxID_MDICHILDEMAILSCHOICEMESSAGEPAGE,
              name=u'choiceMessagePage', parent=self.panMessages,
              pos=wx.Point(40, 72), size=wx.Size(64, 21), style=0)
        self.choiceMessagePage.Bind(wx.EVT_CHOICE,
              self.OnChoiceMessagePageChoice,
              id=wxID_MDICHILDEMAILSCHOICEMESSAGEPAGE)

        self.lblTotalMessages = wx.StaticText(id=wxID_MDICHILDEMAILSLBLTOTALMESSAGES,
              label=u'of 1: Showing 0 Messages', name=u'lblTotalMessages',
              parent=self.panMessages, pos=wx.Point(112, 80), size=wx.Size(125,
              13), style=0)

        self.staticText9 = wx.StaticText(id=wxID_MDICHILDEMAILSSTATICTEXT9,
              label=u'Page', name='staticText9', parent=self.panAddressBook,
              pos=wx.Point(8, 72), size=wx.Size(24, 13), style=0)

        self.choiceAddressPage = wx.Choice(choices=[],
              id=wxID_MDICHILDEMAILSCHOICEADDRESSPAGE,
              name=u'choiceAddressPage', parent=self.panAddressBook,
              pos=wx.Point(40, 72), size=wx.Size(64, 21), style=0)
        self.choiceAddressPage.Bind(wx.EVT_CHOICE,
              self.OnChoiceAddressPageChoice,
              id=wxID_MDICHILDEMAILSCHOICEADDRESSPAGE)

        self.lblAddressPage = wx.StaticText(id=wxID_MDICHILDEMAILSLBLADDRESSPAGE,
              label=u'of 1: Showing 0 Messages', name=u'lblAddressPage',
              parent=self.panAddressBook, pos=wx.Point(112, 80),
              size=wx.Size(125, 13), style=0)

        self.btnShowAllAddresses = wx.Button(id=wxID_MDICHILDEMAILSBTNSHOWALLADDRESSES,
              label=u'Show All', name=u'btnShowAllAddresses',
              parent=self.panAddressBook, pos=wx.Point(400, 24),
              size=wx.Size(75, 23), style=0)
        self.btnShowAllAddresses.Bind(wx.EVT_BUTTON,
              self.OnBtnShowAllAddressesButton,
              id=wxID_MDICHILDEMAILSBTNSHOWALLADDRESSES)

        self.dateStart = wx.TextCtrl(id=wxID_MDICHILDEMAILSDATESTART,
              name=u'dateStart', parent=self.panMessages, pos=wx.Point(64, 32),
              size=wx.Size(80, 21), style=0, value=u'mm/dd/yyyy')

        self.dateEnd = wx.TextCtrl(id=wxID_MDICHILDEMAILSDATEEND,
              name=u'dateEnd', parent=self.panMessages, pos=wx.Point(192, 32),
              size=wx.Size(80, 21), style=0, value=u'mm/dd/yyyy')

        self._init_coll_notebookEmails_Pages(self.notebookEmails)

    def __init__(self, parent):
        self._init_ctrls(parent)
        
        self.SetIcon(images.getMAKE2Icon())
        
        self.CreateMessageListControl()
        self.CreateTopKeywordsListControl()
        self.CreateTopPhonesListControl()
        self.CreateAddressBookListControl()
        self.AddSearchControl()
        self.AddSearchControlToAddressBook()
        self.SearchDocIDList = []
        
        self.RefreshScreen()
        
        self.Stopwords = []
        if len(Globals.Keywords) == 0:
            #self.ReadKeyWordsFromDatabase()
            try:
                self.ReadStopwordsFromDB()
                db = SqliteDatabase(Globals.EmailsFileName)
                if not db.OpenConnection():
                    return
                
                row = db.FetchOneRow('select min(EmailDate) from %s'%Constants.EmailsTable)
                self.dateStart.SetValue(CommonFunctions.ConvertSqliteDatetimeFormatToUSDateTimeFormat(row[0]))
                row = db.FetchOneRow('select max(EmailDate) from %s'%Constants.EmailsTable)
                self.dateEnd.SetValue(CommonFunctions.ConvertSqliteDatetimeFormatToUSDateTimeFormat(row[0]))
                db.CloseConnection()
            except:
                pass
            
        self.search = Search(Globals.EmailsFileName, self.Stopwords, searchEmails=True)

        #dateStart = wx.DateTime()
        #dateStart.SetYear(2009)
        #dateStart.SetMonth(3)
        #dateStart.SetDay(29)
        #self.dateStart.SetValue(dateStart)
        
        #self.CreateSettingsTable()
    
    def AddPageNumbersToMessageChoice(self, totalMessages):
        self.TotalMessagePages = (totalMessages/Constants.MaxObjectsPerPage)
        if (totalMessages%Constants.MaxObjectsPerPage) > 0:
            self.TotalMessagePages += 1
            
        self.choiceMessagePage.Clear()
        for page in range(1, self.TotalMessagePages+1):
            self.choiceMessagePage.Append(str(page))
            
    def CreateSettingsTable(self):
        db = SqliteDatabase(Globals.EmailsFileName)
        if not db.OpenConnection():
            return
                
        
        query = """CREATE TABLE IF NOT EXISTS %s (
            Stemmer text, DirList text, CategoryList text )"""%Constants.SettingsTable
               
        db.ExecuteNonQuery(query)
        db.CloseConnection()

      
    def RefreshScreen(self):
        #self.MessageDict = Globals.MessageDict
        try:
            if len(Globals.EmailsDict) == 0:
                EmailUtilities.LoadEmailsFromDB(Globals.EmailsDict)
                       
            if len(Globals.AddressBookDict) == 0:
                EmailUtilities.LoadAddressBookFromDB(Globals.AddressBookDict)
                
            if len(Globals.MessageDict) == 0:
                EmailUtilities.LoadMessagesFromDB(Globals.MessageDict)
                
            self.ReadStopwordsFromDB()
            
        except:
            pass
    
        
        self.MessagesHeading = "Displaying All Messages"
        self.AddressBookHeading = "Displaying All Addresses"
        try:
            #self.AddMessagesToListView()
            #self.AddTopKeywordsToListView(20)
            #self.AddTopPhonesToListView(20)
            self.AddAddressesToListView()
        except:
            pass
        
        
    def OnBtnCloseButton(self, event):
        self.Close()

    def OnBtnPreprocessingButton(self, event):
        import frmEmailPreprocessing
        textPreprocessing = frmEmailPreprocessing.create(self)
        textPreprocessing.Show()
        event.Skip()

    def OnBtnEmailMapsButton(self, event):
        event.Skip()

    def OnBtnAutoEmailMapsButton(self, event):
        event.Skip()

    def OnBtnCentralEmailMapButton(self, event):
        import frmEmailCentralID
        dlg = frmEmailCentralID.create(self)
        dlg.Show(True)
        event.Skip()

    def OnBtnEmailAttachmentMapButton(self, event):
        import dlgEmailMapping
        dlg = dlgEmailMapping.create(self)
        dlg.Show(True)
        event.Skip()

    def OnBtnExtractEmailsAttachmentsButton(self, event):
        import dlgEmailKeywordsSearchReport
        dlg = dlgEmailKeywordsSearchReport.create(self)
        dlg.Show(True)
        event.Skip()

    def CreateMessageListControl(self):
        """
        
        self.listCtrl1 = wx.ListCtrl(id=wxID_MDICHILDEMAILSLISTCTRL1,
              name='listCtrl1', parent=self.panMessages, pos=wx.Point(8, 112),
              size=wx.Size(1008, 528), style=wx.LC_ICON)
        """
        listID = wx.NewId()
        self.listMessages = wx.ListCtrl(self.panMessages, listID,
                                pos=wx.Point(8,104), size=wx.Size(1008, 528),
                                 style=wx.LC_REPORT 
                                 | wx.BORDER_NONE
                                 )
        
        self.listMessages.SetConstraints(LayoutAnchors(self.listMessages, True,
              True, True, True))
        self.listMessages.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, u'Tahoma'))
              
        # Now that the list exists we can init the other base class,
        # see wx/lib/mixins/listctrl.py
        #listmix.ColumnSorterMixin.__init__(self, 9)
        
        #self.imageListSmallIcon = None
        #self.imageListSmallIcon = wx.ImageList(16, 16)
        
        #self.Bind(wx.EVT_LIST_COL_CLICK, self.OnListMessageColClick, self.listMessages)
        self.listMessages.Bind(wx.EVT_LEFT_DCLICK, self.OnListFilesDoubleClick)
        #self.listMessages.Bind(wx.EVT_CONTEXT_MENU, self.OnListFilesDetailsRightUp)
        #self.sm_up = self.imageListSmallIcon.Add(images.getSmallUpArrowBitmap())
        #self.sm_dn = self.imageListSmallIcon.Add(images.getSmallDnArrowBitmap())
        self.AddMessageListColumnHeadings()
        
    def CreateTopKeywordsListControl(self):
        """
              
        self.listCtrl1 = wx.ListCtrl(id=wxID_MDICHILDEMAILSLISTCTRL1,
              name='listCtrl1', parent=self.panKeywords, pos=wx.Point(16, 64),
              size=wx.Size(376, 568), style=wx.LC_ICON)

        """

        self.listTopKeywords = CustomListCtrl(self.panKeywords, wx.NewId(),
                                pos=wx.Point(16, 64), size=wx.Size(376, 568),
                                 style=wx.LC_REPORT 
                                 | wx.BORDER_NONE
                                 )
        
        self.listTopKeywords.SetConstraints(LayoutAnchors(self.listTopKeywords, True,
              True, False, True))
        self.listTopKeywords.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, u'Tahoma'))
              
        # Now that the list exists we can init the other base class,
        # see wx/lib/mixins/listctrl.py
        #listmix.ColumnSorterMixin.__init__(self, 2)
        
        #self.imageListSmallIcon = None
        #self.imageListSmallIcon = wx.ImageList(16, 16)
        
        #self.Bind(wx.EVT_LIST_COL_CLICK, self.OnListTopKeywordsColClick, self.listTopKeywords)
        #self.listTopKeywords.Bind(wx.EVT_LEFT_DCLICK, self.OnListFilesDoubleClick)
        #self.listMessages.Bind(wx.EVT_CONTEXT_MENU, self.OnListFilesDetailsRightUp)
        #self.sm_up = self.imageListSmallIcon.Add(images.getSmallUpArrowBitmap())
        #self.sm_dn = self.imageListSmallIcon.Add(images.getSmallDnArrowBitmap())
        self.AddTopKeywordsListColumnHeadings()
        
       
    def CreateTopPhonesListControl(self):
        """
        self.listCtrl1 = wx.ListCtrl(id=wxID_MDICHILDEMAILSLISTCTRL1,
              name='listCtrl1', parent=self.panKeywords, pos=wx.Point(424, 64),
              size=wx.Size(408, 384), style=wx.LC_ICON)
        """

        self.listTopPhones = CustomListCtrl(self.panKeywords, wx.NewId(),
                                pos=wx.Point(424, 64), size=wx.Size(408, 568),
                                 style=wx.LC_REPORT 
                                 | wx.BORDER_NONE
                                 )
        
        self.listTopPhones.SetConstraints(LayoutAnchors(self.listTopPhones, True,
              True, False, True))
        self.listTopPhones.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, u'Tahoma'))
              
        # Now that the list exists we can init the other base class,
        # see wx/lib/mixins/listctrl.py
        #listmix.ColumnSorterMixin.__init__(self, 2)
        
        #self.imageListSmallIcon = None
        #self.imageListSmallIcon = wx.ImageList(16, 16)
        
        #self.Bind(wx.EVT_LIST_COL_CLICK, self.OnListTopPhonesColClick, self.listTopKeywords)
        #self.listTopKeywords.Bind(wx.EVT_LEFT_DCLICK, self.OnListFilesDoubleClick)
        #self.listMessages.Bind(wx.EVT_CONTEXT_MENU, self.OnListFilesDetailsRightUp)
        #self.sm_up = self.imageListSmallIcon.Add(images.getSmallUpArrowBitmap())
        #self.sm_dn = self.imageListSmallIcon.Add(images.getSmallDnArrowBitmap())
        self.AddTopPhonesListColumnHeadings()
        
    
    def CreateAddressBookListControl(self):
        """
        self.listCtrl1 = wx.ListCtrl(id=wxID_MDICHILDEMAILSLISTCTRL1,
              name='listCtrl1', parent=self.panMessages, pos=wx.Point(8, 112),
              size=wx.Size(1008, 528), style=wx.LC_ICON)
        """

        self.listAddressBook = CustomListCtrl(self.panAddressBook, wx.NewId(),
                                pos=wx.Point(8, 104), size=wx.Size(1008, 528),
                                 style=wx.LC_REPORT 
                                 | wx.BORDER_NONE
                                 )
        
        self.listAddressBook.SetConstraints(LayoutAnchors(self.listAddressBook, True,
              True, True, True))
        self.listAddressBook.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, u'Tahoma'))
              
        # Now that the list exists we can init the other base class,
        # see wx/lib/mixins/listctrl.py
        #listmix.ColumnSorterMixin.__init__(self, 2)
        
        #self.imageListSmallIcon = None
        #self.imageListSmallIcon = wx.ImageList(16, 16)
        
        self.Bind(wx.EVT_LIST_COL_CLICK, self.OnListAddressBookColClick, self.listAddressBook)
        #self.listTopKeywords.Bind(wx.EVT_LEFT_DCLICK, self.OnListFilesDoubleClick)
        #self.listMessages.Bind(wx.EVT_CONTEXT_MENU, self.OnListFilesDetailsRightUp)
        #self.sm_up = self.imageListSmallIcon.Add(images.getSmallUpArrowBitmap())
        #self.sm_dn = self.imageListSmallIcon.Add(images.getSmallDnArrowBitmap())
        self.AddAddressBookListColumnHeadings()
        
    def AddMessageListColumnHeadings(self):
        #want to add images on the column header..
        info = wx.ListItem()
        info.m_mask = wx.LIST_MASK_TEXT | wx.LIST_MASK_IMAGE | wx.LIST_MASK_FORMAT
        info.m_image = -1
        info.m_format = 0
        #info.m_text = "dabc"
        #self.listMessages.InsertColumnInfo(0, info)
        #FromID, ToID, EmailDate, Subject, Attachments, FilePath, TotalRecipients, Size        
        info.m_text = "Sender"
        self.listMessages.InsertColumnInfo(0, info)
        
        info.m_format = wx.LIST_FORMAT_LEFT
        info.m_text = "Recipient"
        self.listMessages.InsertColumnInfo(1, info)
        info.m_text = "Date"
        self.listMessages.InsertColumnInfo(2, info)
        
        info.m_text = "Subject"
        self.listMessages.InsertColumnInfo(3, info)
        
        info.m_text = "Attachments"
        self.listMessages.InsertColumnInfo(4, info)
        
        info.m_text = "FilePath"
        self.listMessages.InsertColumnInfo(5, info)
        info.m_text = "#Recpts"
        self.listMessages.InsertColumnInfo(6, info)
        info.m_text = "Size"
        self.listMessages.InsertColumnInfo(7, info)
      
      
    def AddTopKeywordsListColumnHeadings(self):
        #want to add images on the column header..
        info = wx.ListItem()
        info.m_mask = wx.LIST_MASK_TEXT | wx.LIST_MASK_IMAGE | wx.LIST_MASK_FORMAT
        info.m_image = -1
        info.m_format = 0
        
        info.m_text = "Term"
        self.listTopKeywords.InsertColumnInfo(0, info)
        
        info.m_format = wx.LIST_FORMAT_LEFT
        info.m_text = "Occurance"
        self.listTopKeywords.InsertColumnInfo(1, info)
        
        
    def AddTopPhonesListColumnHeadings(self):
        #want to add images on the column header..
        info = wx.ListItem()
        info.m_mask = wx.LIST_MASK_TEXT | wx.LIST_MASK_IMAGE | wx.LIST_MASK_FORMAT
        info.m_image = -1
        info.m_format = 0
        
        info.m_text = "Phone"
        self.listTopPhones.InsertColumnInfo(0, info)
        
        info.m_format = wx.LIST_FORMAT_LEFT
        info.m_text = "Occurance"
        self.listTopPhones.InsertColumnInfo(1, info)
    
    
    def AddAddressBookListColumnHeadings(self):
        #want to add images on the column header..
        info = wx.ListItem()
        info.m_mask = wx.LIST_MASK_TEXT | wx.LIST_MASK_IMAGE | wx.LIST_MASK_FORMAT
        info.m_image = -1
        info.m_format = 0
        
        info.m_text = "First Name"
        self.listAddressBook.InsertColumnInfo(0, info)

        info.m_format = wx.LIST_FORMAT_LEFT
        info.m_text = "Middle Name"
        self.listAddressBook.InsertColumnInfo(1, info)
        info.m_text = "Last Name"
        self.listAddressBook.InsertColumnInfo(2, info)
        
        info.m_text = "Email"
        self.listAddressBook.InsertColumnInfo(3, info)
        
        
    # Used by the ColumnSorterMixin, see wx/lib/mixins/listctrl.py
    def GetListCtrl(self):
        return self.listMessages

    # Used by the ColumnSorterMixin, see wx/lib/mixins/listctrl.py
    def GetSortImages(self):
        return (self.sm_dn, self.sm_up)
    
    def OnListMessageColClick(self, event):
        event.Skip()
    
    
    def OnListTopKeywordsColClick(self, event):
        event.Skip()
        
    def OnListTopPhonesColClick(self, event):
        event.Skip()
        
    def OnListAddressBookColClick(self, event):
        event.Skip()
      
    def AddMessagesToListView(self, messagesList):  #, search=False):
        self.SetCursor(wx.HOURGLASS_CURSOR)
        self.lblMessagesHeading.SetLabel(self.MessagesHeading)
        self.listMessages.ClearAll()
        self.AddMessageListColumnHeadings()
        totalMessages = 0
        #MsgDict = {}
        #print ' globals len ', len(Globals.MessageDict)
        #FromID, ToID, EmailDate, Subject, Attachments, FilePath, AttachmentsPath, TotalRecipients, Size
        
        #for key in Globals.MessageDict:
        #`   for msg in Globals.MessageDict[key]:
        #print MessagesList
        for msg in messagesList:
            #print msgList        
            #for msg in msgList:
            if not msg:
                continue
            
            """
            if search:
                if msg.DocID not in self.SearchDocIDList:
                    continue
            """     
            totalMessages += 1
            
            #print "totalMessages = " + str(totalMessages)
            """
            listItem = []
            
            listItem.append(PlatformMethods.Decode(msg[0]))
            listItem.append(PlatformMethods.Decode(msg[1]))
            listItem.append(PlatformMethods.Decode(msg[2]))
            listItem.append(PlatformMethods.Decode(msg[3]))
            listItem.append(PlatformMethods.Decode(msg[4]))
                
            listItem.append(PlatformMethods.Decode(msg.Attachments))
            listItem.append(PlatformMethods.Decode(CommonFunctions.ConvertByteToKilobyte(msg.Size)))
            listItem.append(PlatformMethods.Decode(msg.Group))
            listItem.append(msg.Label)
            
            MsgDict[totalMessages] = tuple(listItem)
            """
            index = self.listMessages.InsertStringItem(sys.maxint, PlatformMethods.Decode(msg[0]))
            self.listMessages.SetStringItem(index, 1, PlatformMethods.Decode(msg[1]))
            self.listMessages.SetStringItem(index, 2, PlatformMethods.Decode(msg[2]))
            self.listMessages.SetStringItem(index, 3, PlatformMethods.Decode(msg[3]))
            self.listMessages.SetStringItem(index, 4, PlatformMethods.Decode(msg[4]))
            self.listMessages.SetStringItem(index, 5, PlatformMethods.Decode(msg[5]))
            self.listMessages.SetStringItem(index, 6, PlatformMethods.Decode(msg[6]))
            self.listMessages.SetStringItem(index, 7, PlatformMethods.Decode(CommonFunctions.ConvertByteToKilobyte(msg[7])))
            self.listMessages.SetItemData(index, totalMessages)
                    
                
        #self.listMessages.SetImageList(self.imageListSmallIcon, wx.IMAGE_LIST_SMALL)
        #self.CreateFileIconList(iconInfo)
        #self.itemDataMap = MsgDict       
        #items = MsgDict.items()
        #print items
        #print len(self.FileInfo)
        #print len(items)

        self.listMessages.SetColumnWidth(0, 250)
        self.listMessages.SetColumnWidth(1, 250)
        self.listMessages.SetColumnWidth(2, 50)
        self.listMessages.SetColumnWidth(3, 300)
        self.listMessages.SetColumnWidth(4, 30)
        self.listMessages.SetColumnWidth(5, 30)
        self.listMessages.SetColumnWidth(6, 50)
        self.listMessages.SetColumnWidth(7, 30)
        self.listMessages.SetColumnWidth(8, 50)
        
        """
        page= "Page"
        if self.TotalMessagePages > 0:
            page = "Pages"
        """
        
        self.lblTotalMessages.SetLabel('of %d : Displaying %d Messages'%(self.TotalMessagePages, totalMessages))
        self.SetCursor(wx.STANDARD_CURSOR)
        
    def AddTopKeywordsToListView(self, top=20):
        self.SetCursor(wx.HOURGLASS_CURSOR)
        
        self.listTopKeywords.DeleteAllItems()
        totalKeywords = 0
        #MsgDict = {}
        if top <=0:
            limit = ""
        else:
            limit = "limit %d"%top
            
        query = "select Word, Frequency from Words order by Frequency desc %s;"%limit
        
        self.txtTopKeywords.SetValue(str(top))
        db = SqliteDatabase(Globals.EmailsFileName)
        if not db.OpenConnection():
            return
        
        rows = db.FetchAllRows(query)
        
        for row in rows:
            totalKeywords += 1
            
            listItem = []
            
            #listItem.append(PlatformMethods.Decode(row[0]))
            #listItem.append(row[1])
            
            #MsgDict[totalKeywords] = tuple(listItem)
            
            index = self.listTopKeywords.InsertStringItem(sys.maxint, PlatformMethods.Decode(row[0]))
            self.listTopKeywords.SetStringItem(index, 1, PlatformMethods.Decode(row[1]))
            self.listTopKeywords.SetItemData(index, totalKeywords)
            
                
        #self.listTopKeywords.SetImageList(self.imageListSmallIcon, wx.IMAGE_LIST_SMALL)
        #self.itemDataMap = MsgDict      
        #items = MsgDict.items()
        #print items
        #print len(self.FileInfo)
        #print len(items)

        self.listTopKeywords.SetColumnWidth(0, 250)
        self.listTopKeywords.SetColumnWidth(1, 70)
        
        self.SetCursor(wx.STANDARD_CURSOR)
        
    def AddTopPhonesToListView(self, top=20):
        
        db = SqliteDatabase(Globals.EmailsFileName)
        if not db.OpenConnection():
            return
        
        self.SetCursor(wx.HOURGLASS_CURSOR)
        self.listTopPhones.DeleteAllItems()
        totalKeywords = 0
        #MsgDict = {}
        if top <= 0:
            limit = ""
        else:
            limit = "limit %d"%top
            
        query = "select Phone, sum(Frequency) as total from Phones "
        query += "group by Phone order by total desc %s;"%limit
        
        self.txtTopPhones.SetValue(str(top))
        
        
        rows = db.FetchAllRows(query)
        
        for row in rows:
            totalKeywords += 1
            
            #listItem = []
            
            #listItem.append(PlatformMethods.Decode(row[0]))
            #listItem.append(row[1])
            
            #MsgDict[totalKeywords] = tuple(listItem)
            
            index = self.listTopPhones.InsertStringItem(sys.maxint, PlatformMethods.Decode(row[0]))
            self.listTopPhones.SetStringItem(index, 1, PlatformMethods.Decode(row[1]))
            self.listTopPhones.SetItemData(index, totalKeywords)
            
                
        #self.listTopPhones.SetImageList(self.imageListSmallIcon, wx.IMAGE_LIST_SMALL)
        #self.itemDataMap = MsgDict       
        #items = MsgDict.items()
        #print items
        #print len(self.FileInfo)
        #print len(items)

        self.listTopPhones.SetColumnWidth(0, 250)
        self.listTopPhones.SetColumnWidth(1, 120)
        
        self.SetCursor(wx.STANDARD_CURSOR)


    def AddAddressesToListView(self, AddressList):#search=False):
        self.SetCursor(wx.HOURGLASS_CURSOR)
        
        self.listAddressBook.DeleteAllItems()
        totalAddresses = 0
        MsgDict = {}
        #print ' globals len ', len(Globals.MessageDict)
        """
        for key in Globals.AddressBookDict:
            if search:
                if len(self.SearchAddressList) >= 3:
                    if Globals.AddressBookDict[key]['FirstName'].lower() not in self.SearchAddressList and Globals.AddressBookDict[key]['MiddleName'].lower() not in self.SearchAddressList and Globals.AddressBookDict[key]['LastName'].lower() not in self.SearchAddressList:
                        continue
                elif len(self.SearchAddressList) == 2:
                    if Globals.AddressBookDict[key]['FirstName'].lower() not in self.SearchAddressList and Globals.AddressBookDict[key]['LastName'].lower() not in self.SearchAddressList:
                        continue
                elif len(self.SearchAddressList) == 1:
                    if Globals.AddressBookDict[key]['FirstName'].lower() not in self.SearchAddressList:
                        if Globals.AddressBookDict[key]['MiddleName'].lower() not in self.SearchAddressList:
                            if Globals.AddressBookDict[key]['LastName'].lower() not in self.SearchAddressList:
                                if Globals.AddressBookDict[key]['EmailID'].lower() not in self.SearchAddressList:
                                    continue
                    
        """
        for add in AddressList:        
            totalAddresses += 1
            
            #print "totalMessages = " + str(totalMessages)
            listItem = []
            
            listItem.append(PlatformMethods.Decode(add[0])) #Globals.AddressBookDict[key]['FirstName']))
            listItem.append(PlatformMethods.Decode(add[1])) #Globals.AddressBookDict[key]['MiddleName']))
            listItem.append(PlatformMethods.Decode(add[2])) #Globals.AddressBookDict[key]['LastName']))
            listItem.append(PlatformMethods.Decode(add[3])) #Globals.AddressBookDict[key]['EmailID']))
            
            MsgDict[totalAddresses] = tuple(listItem)
            
            index = self.listAddressBook.InsertStringItem(sys.maxint, listItem[0])
            self.listAddressBook.SetStringItem(index, 1, listItem[1])
            self.listAddressBook.SetStringItem(index, 2, listItem[2])
            self.listAddressBook.SetStringItem(index, 3, listItem[3])
            self.listAddressBook.SetItemData(index, totalAddresses)
                
                
        #self.listAddressBook.SetImageList(self.imageListSmallIcon, wx.IMAGE_LIST_SMALL)
        #self.CreateFileIconList(iconInfo)
        #self.itemDataMap = MsgDict       
        #items = MsgDict.items()
        #print items
        #print len(self.FileInfo)
        #print len(items)

        self.listAddressBook.SetColumnWidth(0, 225)
        self.listAddressBook.SetColumnWidth(1, 100)
        self.listAddressBook.SetColumnWidth(2, 225)
        self.listAddressBook.SetColumnWidth(3, 300)
  
        #if self.AddressHeading:
        self.lblAddressBookHeading.SetLabel(self.AddressHeading)
        #else:
        #self.lblAddressBookHeading.SetLabel('')
        
        self.lblAddressPage.SetLabel(' of %d : Showing %d Addresses'%(self.TotalAddressPages, totalAddresses))
        self.SetCursor(wx.STANDARD_CURSOR)
        
    
    def OnBtnRefreshMessagesButton(self, event):
        #self.AddMessagesToListView()
        pass
    
    def OnListFilesDoubleClick(self, event):
        if self.IsMessageSelected():
            msgV = dlgEmailMessageViewer.create(self, self.sender, self.recipient, self.date, self.subject)
            msgV.ShowModal()
        event.Skip()
        
    def IsMessageSelected(self):
        self.index = self.listMessages.GetFirstSelected()
        if self.index >=0:
            li = self.listMessages.GetItem(self.index, 0)
            self.sender = li.GetText()
            li = self.listMessages.GetItem(self.index, 1)
            self.recipient = li.GetText()
            li = self.listMessages.GetItem(self.index, 2)
            self.date = li.GetText()
            li = self.listMessages.GetItem(self.index, 3) #.GetText())
            self.subject = li.GetText()
            #print self.listMessages.GetItem(self.index).GetData()
            #print self.listMessages.GetItem(self.index).GetColumn()
            """
            db = SqliteDatabase(Globals.EmailsFileName)
            if not db.OpenConnection():
                return False
            
            query = "select Attachments, Message from %s where FromID = '%s' and ToID = '%s' and EmailDate = '%s' and Subject='%s';"%(Constants.EmailsTable, self.sender, self.receiver, self.date,self.subject)
            rows = db.FetchAllRows(query)
            """
            return True
            
        else:
            CommonFunctions.ShowErrorMessage(self, 'Please select a message from the list.')
            return False


    def OnBtnExportTopKeywordsButton(self, event):
        db = SqliteDatabase(Globals.EmailsFileName)
        if not db.OpenConnection():
            return
                
        dlg = wx.FileDialog(self, "Save Word List", ".", "", "*.csv", wx.SAVE)
        try:
            if dlg.ShowModal() == wx.ID_OK:
                if len(self.txtTopKeywords.GetValue()) == 0:
                    top = 0
                else:
                    try:
                        top = int(self.txtTopKeywords.GetValue())
                    except:
                        CommonFunctions.ShowErrorMessage(self, "Please Enter a Valid Number!", error=True)
                        return
                    
                    
                fileName = dlg.GetPath()
                busy = wx.BusyInfo("It might take some time to export word list; just sit back and relax...")
                wx.Yield()
                fout = open(fileName, 'wb')
                
                if top <=0:
                    limit = ""
                else:
                    limit = "limit %d"%top
                    
                #query = "select words.word, sum(bagofwords.frequency) as total from words left join bagofwords on words.id = bagofwords.wordid "
                #query += "group by bagofwords.wordid order by total desc %s;"%limit
                    
                #query = "select Words.word, count(WordLocation.WordID) as total from Words left join WordLocation on Words.ROWID = WordLocation.WordID "
                #query += "group by WordLocation.WordID order by total desc %s;"%limit
                
                #query = "select word from Words order by word %s;"%limit
                query = "select Word, Frequency from Words order by Frequency desc %s;"%limit
                
                rows = db.FetchAllRows(query)
                i = 1
                for row in rows:
                    fout.write(PlatfromMethods.Encode(row[0]))
                    fout.write(" (%d)"%row[1])
                    fout.write(", ,")
                    i += 1
                    if i == 8:
                        i = 0
                        fout.write("\n")

                db.CloseConnection()
                fout.close()
                
        except Exception, value:
            db.CloseConnection()
            fout.close()
            CommonFunctions.ShowErrorMessage(self, "Failed to Export Phone List. Error: %s"%value)
        finally:
            dlg.Destroy()
            
        event.Skip()

    def OnBtnDisplayTopKeywordsButton(self, event):
        try:
            top = int(self.txtTopKeywords.GetValue())
        except:
            top = 20
            
        self.AddTopKeywordsToListView(top)
        event.Skip()


    def OnBtnDisplayTopPhonesButton(self, event):
        try:
            top = int(self.txtTopPhones.GetValue())
        except:
            top = 20
            
        self.AddTopPhonesToListView(top)
        event.Skip()

    def OnBtnExportTopPhonesButton(self, event):
        db = SqliteDatabase(Globals.EmailsFileName)
        if not db.OpenConnection():
            return
                
        dlg = wx.FileDialog(self, "Save Phone List", ".", "", "*.csv", wx.SAVE)
        try:
            if dlg.ShowModal() == wx.ID_OK:
                if len(self.txtTopPhones.GetValue()) == 0:
                    top = 0
                else:
                    try:
                        top = int(self.txtTopPhones.GetValue())
                    except:
                        CommonFunctions.ShowErrorMessage(self, "Please Enter a Valid Number!", error=True)
                        return
                    
                fileName = dlg.GetPath()
                busy = wx.BusyInfo("It might take some time to export phone numbers; just sit back and relax...")
                wx.Yield()
                fout = open(fileName, 'wb')
                
                if top <=0:
                    limit = ""
                else:
                    limit = "limit %d"%top
                    
                query = "select Phone, sum(Frequency) as total from Phones "
                query += "group by Phone order by total desc %s;"%limit
  
                rows = db.FetchAllRows(query)
                i = 1
                for row in rows:
                    fout.write(PlatformMethods.Encode(row[0]))
                    fout.write(" (%d)"%row[1])
                    fout.write(", ,")
                    i += 1
                    if i == 4:
                        i = 0
                        fout.write("\n")

                db.CloseConnection()
                fout.close()
        except Exception, value:
            db.CloseConnection()
            fout.close()
            CommonFunctions.ShowErrorMessage(self, "Failed to Export Phone List. Error: %s"%value)
        finally:
            dlg.Destroy()
            
        event.Skip()

    def OnBtnSearchButton(self, event):
        self.OnDoSearch(event)
        #self.searchBitMap(True)
        #self.AddMessagesToListView(True)
        event.Skip()


    def AddSearchControl(self):
        """
        self.textCtrl1 = wx.TextCtrl(id=wxID_MDICHILDEMAILSTEXTCTRL1,
          name='textCtrl1', parent=self.panMessages, pos=wx.Point(480, 32),
          size=wx.Size(280, 21), style=0, value='textCtrl1')
        """
        self.searchMessages = wx.SearchCtrl(self.panMessages, pos=wx.Point(480, 32), size=(280,-1), style=wx.TE_PROCESS_ENTER)
        self.searchMessages.ShowSearchButton(True)
        self.searchMessages.ShowCancelButton(True)
        
        self.SearchMessagesMenu = wx.Menu()
        item = self.SearchMessagesMenu.Append(-1, "Recent Searches")
        item.Enable(False)
        
        self.searchMessages.SetMenu(self.SearchMessagesMenu)
        
        self.Bind(wx.EVT_SEARCHCTRL_SEARCH_BTN, self.OnSearch, self.searchMessages)
        self.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, self.OnSearchCancel, self.searchMessages)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnDoSearch, self.searchMessages)
        
    def AddSearchControlToAddressBook(self):
        """
        self.textCtrl1 = wx.TextCtrl(id=wxID_MDICHILDEMAILSTEXTCTRL1,
              name='textCtrl1', parent=self.panAddressBook, pos=wx.Point(16,
              32), size=wx.Size(288, 21), style=0, value='textCtrl1')
        """
        self.searchAddressBook = wx.SearchCtrl(self.panAddressBook, pos=wx.Point(16, 32), size=(288,-1), style=wx.TE_PROCESS_ENTER)
        self.searchAddressBook.ShowSearchButton(True)
        self.searchAddressBook.ShowCancelButton(True)
        
        self.SearchAddressBookMenu = wx.Menu()
        item = self.SearchAddressBookMenu.Append(-1, "Recent Searches")
        item.Enable(False)
        
        self.searchAddressBook.SetMenu(self.SearchAddressBookMenu)
        
        self.Bind(wx.EVT_SEARCHCTRL_SEARCH_BTN, self.OnSearchAddressBook, self.searchAddressBook)
        self.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, self.OnSearchAddressBookCancel, self.searchAddressBook)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnDoSearchAddressBook, self.searchAddressBook)
    
    def OnSearch(self, event):
        
        event.Skip()
            
    def OnSearchAddressBook(self, event):
        
        event.Skip()
    
    def SearchMessages(self, searchWords):
        if self.SearchMessagesMenu.FindItem(searchWords) < 0:
            id = wx.NewId()
            self.SearchMessagesMenu.Append(id, searchWords)
            self.Bind(wx.EVT_MENU, self.OnSearchFromSearchMenu,
              id=id)
        
        #print searchWords
        self.MessagesList = []
        self.TotalMessageResults = 0
        #totalResults = 0
        try:
            self.MessagesList, self.TotalMessageResults = self.search.GetRankedDocuments(searchWords)
        except Exception, msg:
            CommonFunctions.ShowErrorMessage(self, 'Error: %s'%msg, error=True)
        
        # = len(self.MessagesList)
        self.AddPageNumbersToMessageChoice(self.TotalMessageResults)
        self.choiceMessagePage.SetSelection(0)
        self.MessagesHeading = '%d Results for %s'%(self.TotalMessageResults, self.searchMessages.GetValue())
        self.AddMessagesToListView(self.MessagesList[0:Constants.MaxObjectsPerPage])
        

    def OnDoSearch(self, event):
        #self.searchBitMap(True)
        searchWords = self.searchMessages.GetValue()
        if not searchWords:
            return
        
        self.ShowAllMessages = False
        self.SearchMessages(searchWords)
        
        #self.AddMessagesToListView(True)
        event.Skip()
        
    def OnDoSearchAddressBook(self, event):
        searchWords = self.searchAddressBook.GetValue()
        if not searchWords:
            return
        
        self.SearchAddressBook(searchWords)
        event.Skip()
        
    def SearchAddressBook(self, searchWords):
        self.SearchAddressList = searchWords.lower().split(" ")
        if self.SearchAddressBookMenu.FindItem(searchWords) < 0:
            id = wx.NewId()
            self.SearchAddressBookMenu.Append(id, searchWords)
            self.Bind(wx.EVT_MENU, self.OnSearchFromAddressBookMenu,
              id=id)
            
        #self.AddAddressesToListView(True)
        db = SqliteDatabase(Globals.EmailsFileName)
        if not db.OpenConnection():
            return
        
        words = searchWords.split(' ')
        whereClause  = ''
        #values = []
        for word in words:
            searchWord = "%" + word + "%"
            if whereClause:
                whereClause += " or " #EmailID like '%s' or FirstName like '%s' or MiddleName like '%s' or LastName like '%s'"%(searchWord, searchWord, searchWord, searchWord)
            #else:
            whereClause += " EmailID like '%s' or FirstName like '%s' or MiddleName like '%s' or LastName like '%s'"%(searchWord, searchWord, searchWord, searchWord)
            
        self.AddressList = db.FetchAllRows('select FirstName, MiddleName, LastName, EmailID, InBook from %s where %s'%(Constants.AddressBookTable, whereClause))
        db.CloseConnection()
        self.TotalAddresses = len(self.AddressList)
        if not self.AddressList:
            self.TotalAddresses = 0
            
        self.choiceAddressPage.SetSelection(0)
        self.AddressHeading = "%d Results for %s"%(self.TotalAddresses, searchWords)
        self.AddPageNumbersToAddressChoice(self.TotalAddresses)
        self.AddAddressesToListView(self.AddressList[0:Constants.MaxObjectsPerPage])
        
    def OnSearchFromAddressBookMenu(self, event):
        id = event.GetId()
        searchWords = self.SearchAddressBookMenu.GetLabel(id)
        self.searchAddressBook.SetValue(searchWords)
        self.SearchAddressBook(searchWords)
        event.Skip()

    def OnSearchCancel(self, event):
        self.AddMessagesToListView()
        event.Skip()
        
    def OnSearchAddressBookCancel(self, event):
        self.AddAddressesToListView()
        event.Skip()

    def OnSearchFromSearchMenu(self, event):
        id = event.GetId()
        searchWords = self.SearchMessagesMenu.GetLabel(id)
        self.searchMessages.SetValue(searchWords)
        self.OnDoSearch(event)
        
    def searchBitMap(self, encoded=True):
        db = SqliteDatabase(Globals.EmailsFileName)
        if not db.OpenConnection():
            return
        
        self.SearchDocIDList = []
        self.webDocs = {}
        self.searchWords = ''
        self.wordList = []
        self.startTime = 0
        self.elapsedTime = ''
        
        self.encoded = encoded
        word = ''
        totalResult = 0
        
        self.searchWords = self.searchMessages.GetValue()
        if not self.searchWords:
            #CommonFunctions.ShowErrorMessage(self, "Failed to Export Phone List. Error: %s"%value)
            return
        
        
        if self.SearchMessagesMenu.FindItem(self.searchWords) < 0:
            id = wx.NewId()
            self.SearchMessagesMenu.Append(id, self.searchWords)
            self.Bind(wx.EVT_MENU, self.OnSearchFromSearchMenu, id=id)
        
        if encoded:
            query = "select keyword, compressed from %s where (Keyword = "%Constants.TextCatBitMapIndex
        else:
            query = "select keyword, bitmap from %s where (Keyword = '"%Constants.TextCatBitMapIndex
        
        i = 0    
        for word in string.split(self.searchWords, ' '):
            word = word.strip().lower()
            word = word.strip('"')
                    
            if word not in Globals.EmailsStopwords:
                i += 1
                self.wordList.append(word)
                if i == 1:
                    query += db.SqlSQuote(word)
                else:
                    query += " or keyword = %s"%(db.SqlSQuote(word))
        
        query += ")"
        if self.wordList < 0:
            return None
        
        #print query
        bitMap = []
        docIndex = 0

        self.startTime = time.time()
        #print query
        rows = db.FetchAllRows(query)
        totalResult = len(rows)
        """
        if totalResult < len(self.wordList):
            self.elapsedTime = CommonFunctions.ConvertSecondsToYearDayHourMinSec(time.time() - self.startTime)
            self.MessagesHeading = "%d Results for %s (%s)"%(len(self.SearchDocIDList), self.searchWords, self.elapsedTime)
            return None
        """
        
        if totalResult < 1:
            self.elapsedTime = CommonFunctions.ConvertSecondsToYearDayHourMinSec(time.time() - self.startTime)
            self.MessagesHeading = "%d Results for %s (%s)"%(len(self.SearchDocIDList), self.searchWords, self.elapsedTime)
            return None
        
        if totalResult == 1:
            if self.encoded:
                bitMap = binascii.rledecode_hqx(rows[0][1])
            else:
                bitMap = rows[0][1]
        elif totalResult > 1:
            if self.encoded:
                bits = binascii.rledecode_hqx(rows[0][1])
                for bit in bits:
                    bitMap.append(bit)
            else:
                for bit in rows[0][1]: # get the bitmap of first word/row
                    bitMap.append(bit)
        
        i = 1
        
        while i < totalResult:
            row = rows[i]
            i += 1
            index = 0 # start from the beginning of the bitmap
            if encoded:
                bits = binascii.rledecode_hqx(row[1])
            else:
                bits = row[1]
            
            for bit in bits:
                if self.searchWords.startswith('"'):
                    bitMap[index] = str(int(bitMap[index]) & int(bit))
                else:
                    bitMap[index] = str(int(bitMap[index]) | int(bit))
                index += 1
        
        #print bitMap
        docIndex = 1
        for bit in bitMap:
            if bit == '1':
                #if len(self.docIDString) >= 1:
                #    self.docIDString += ','
                self.SearchDocIDList.append(docIndex)
                #self.docIDString += str(docIndex)
            docIndex += 1
        
        
         
        #query = "select ID, Path, FileName from %s left join where docID in (" + self.docIDString + ");"       
        db.CloseConnection()
        
        self.elapsedTime = CommonFunctions.ConvertSecondsToYearDayHourMinSec(time.time() - self.startTime)
        self.MessagesHeading = "%d Results for %s (%s)"%(len(self.SearchDocIDList), self.searchWords, self.elapsedTime)
        #if totalResult > 0:
        #self.getWebDocs()
                
    
    def ReadStopwordsFromDB(self):
        if len(Globals.EmailsStopwords) > 0:
            return
        
        db = SqliteDatabase(Globals.EmailsFileName)
        if not db.OpenConnection():
            return
        
        query = "SELECT Stopword FROM " + Constants.StopwordsTable
        rows = db.FetchAllRows(query)
        #print len(rows)
        self.StopwordsValue = ""
        i = 0
        for row in rows:
            #print row[0]
            Globals.EmailsStopwords.add(row[0])
            
        #print Globals.KeyWords
        db.CloseConnection()

    def OnBtnSearchAddressBookButton(self, event):
        self.OnDoSearchAddressBook(event)
        event.Skip()

    def OnBtnDisplayAllMessageButton(self, event):
        db = SqliteDatabase(Globals.EmailsFileName)
        if not db.OpenConnection():
            return
        
        query = 'select count(*) from %s'%Constants.EmailsTable
        row = db.FetchOneRow(query)
        self.TotalMessageResults = 0
        if row:
            self.TotalMessageResults = int(row[0])
            
        query = 'select FromID, ToID, EmailDate, Subject, Attachments, FilePath, AttachmentsPath, TotalRecipients, Size from %s limit %d offset 0;'%(Constants.EmailsTable, Constants.MaxObjectsPerPage)
        self.MessagesList = db.FetchAllRows(query)
        #self.TotalMessageResults = len(self.MessagesList)
        #if not self.MessagesList:
            
            
        self.ShowAllMessages = True
        self.AddPageNumbersToMessageChoice(self.TotalMessageResults)
        self.choiceMessagePage.SetSelection(0)
        self.MessagesHeading = '%d Messages'%(self.TotalMessageResults)
        self.AddMessagesToListView(self.MessagesList)
        event.Skip()

    def OnChoiceMessagePageChoice(self, event):
        startIndex = int(int(self.choiceMessagePage.GetStringSelection())-1)*Constants.MaxObjectsPerPage
        endIndex = startIndex + Constants.MaxObjectsPerPage
        #print startIndex
        #print self.MessagesList
        #print self.MessagesList[startIndex:Constants.MaxObjectsPerPage]
        if self.ShowAllMessages:
            db = SqliteDatabase(Globals.EmailsFileName)
            if not db.OpenConnection():
                return
            query = 'select FromID, ToID, EmailDate, Subject, Attachments, FilePath, AttachmentsPath, TotalRecipients, Size from %s limit %d offset %d;'%(Constants.EmailsTable, Constants.MaxObjectsPerPage, startIndex)
            self.MessagesList = db.FetchAllRows(query)
            self.AddMessagesToListView(self.MessagesList)
        else:
            self.AddMessagesToListView(self.MessagesList[startIndex:endIndex])
        event.Skip()

    def AddPageNumbersToAddressChoice(self, totalAddresses):
        self.TotalAddressPages = (totalAddresses/Constants.MaxObjectsPerPage)
        if (totalAddresses%Constants.MaxObjectsPerPage) > 0:
            self.TotalAddressPages += 1
            
        self.choiceAddressPage.Clear()
        for page in range(1, self.TotalAddressPages+1):
            self.choiceAddressPage.Append(str(page))
            
    def OnChoiceAddressPageChoice(self, event):
        startIndex = int(int(self.choiceAddressPage.GetStringSelection())-1)*Constants.MaxObjectsPerPage
        endIndex = startIndex + Constants.MaxObjectsPerPage
        #print startIndex
        #print self.MessagesList
        #print self.MessagesList[startIndex:Constants.MaxObjectsPerPage]
        self.AddAddressesToListView(self.AddressList[startIndex:endIndex])
        
        event.Skip()

    def OnBtnShowAllAddressesButton(self, event):
        db = SqliteDatabase(Globals.EmailsFileName)
        if not db.OpenConnection():
            return
        
        
        self.AddressList = db.FetchAllRows('select FirstName, MiddleName, LastName, EmailID, InBook from %s'%(Constants.AddressBookTable))
        db.CloseConnection()
        self.TotalAddresses = len(self.AddressList)
        if not self.AddressList:
            self.TotalAddresses = 0
            
        self.AddPageNumbersToAddressChoice(self.TotalAddresses)
        self.choiceAddressPage.SetSelection(0)
        self.AddressHeading = "%d Addresses"%(self.TotalAddresses)
        self.AddAddressesToListView(self.AddressList[0:Constants.MaxObjectsPerPage])
        event.Skip()

    def OnBtnShowMessagesEmailDateButton(self, event):
        db = SqliteDatabase(Globals.EmailsFileName)
        if not db.OpenConnection():
            return
        
        dateStart = "%s 00:00:00"%(self.dateStart.GetValue())
        dateEnd = "%s 00:00:00"%(self.dateEnd.GetValue())
        #print dateStart
        #print dateEnd
        
        try:
            sqliteDateStart = CommonFunctions.ConvertUSDateTimeFormatToSqliteFormat(dateStart)
            sqliteDateEnd = CommonFunctions.ConvertUSDateTimeFormatToSqliteFormat(dateEnd)
            
        except Exception, msg:
            CommonFunctions.ShowErrorMessage(self, str(msg), True)
            return
            
            
        query = 'select FromID, ToID, EmailDate, Subject, Attachments, FilePath, AttachmentsPath, TotalRecipients, Size from %s'%Constants.EmailsTable
        query += " where EmailDate >= ? and EmailDate <= ?"
        self.MessagesList = db.FetchAllRows(query, (sqliteDateStart, sqliteDateEnd))
        self.TotalMessageResults = len(self.MessagesList)
        if not self.MessagesList:
            self.TotalMessageResults = 0
            
        self.AddPageNumbersToMessageChoice(self.TotalMessageResults)
        self.choiceMessagePage.SetSelection(0)
        self.MessagesHeading = '%d Messages from %s to %s'%(self.TotalMessageResults, dateStart, dateEnd)
        self.AddMessagesToListView(self.MessagesList[0:Constants.MaxObjectsPerPage])
        event.Skip()
        
        
        event.Skip()

    def OnDateEndDateChanged(self, event):
        #print self.dateEnd.GetValue()
        event.Skip()
        
    


if __name__ == "__main__":
    import sys
    
    
    db = SqliteDatabase(r"C:\Documents and Settings\Ram\Desktop\IBM vs Summit.eml")
    if not db.OpenConnection():
        sys.exit(0)
    
    fout = open(r"C:\Documents and Settings\Ram\Desktop\EmailTerms.csv", 'w')
        
    #query = "select words.word, sum(bagofwords.frequency) as total from words left join bagofwords on words.id = bagofwords.wordid "
    #query += "group by bagofwords.wordid order by total desc %s;"%limit
        
    #query = "select Words.word, count(WordLocation.WordID) as total from Words left join WordLocation on Words.ROWID = WordLocation.WordID "
    #query += "group by WordLocation.WordID order by total desc %s;"%limit
    
    query = "select word from Words order by word;"
    
    rows = db.FetchAllRows(query)
    i = 1
    for row in rows:
        fout.write(row[0])
        #fout.write(" (%d)"%row[1])
        fout.write(", ,")
        i += 1
        if i == 8:
            i = 0
            fout.write("\n")

    db.CloseConnection()
    fout.close()
    
