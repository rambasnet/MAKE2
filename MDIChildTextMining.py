#Boa:MiniFrame:MDIChildTextMining

#-----------------------------------------------------------------------------
# Name:        MDIChildEmails.py
# Purpose:     
#
# Author:      Ram Basnet
#
# Created:     2007/11/01
# Last Modified: 7/2/2009
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
    return MDIChildTextMining(parent)

class CustomListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, ID, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        
        
[wxID_MDICHILDTEXTMINING, wxID_MDICHILDTEXTMININGBTNBATCHSEARCH, 
 wxID_MDICHILDTEXTMININGBTNDISPLAYTOPKEYWORDS, 
 wxID_MDICHILDTEXTMININGBTNDISPLAYTOPPHONES, 
 wxID_MDICHILDTEXTMININGBTNEXPORTALLTERMS, 
 wxID_MDICHILDTEXTMININGBTNEXPORTSEARCHRESULTS, 
 wxID_MDICHILDTEXTMININGBTNEXPORTSTEMMEDTERMS, 
 wxID_MDICHILDTEXTMININGBTNEXPORTTOPKEYWORDS, 
 wxID_MDICHILDTEXTMININGBTNEXPORTTOPPHONES, 
 wxID_MDICHILDTEXTMININGBTNPREPROCESSING, 
 wxID_MDICHILDTEXTMININGBTNSEARCHDOCUMENTS, 
 wxID_MDICHILDTEXTMININGCHOICEPAGENUM, wxID_MDICHILDTEXTMININGLBLTOTALRESULTS, 
 wxID_MDICHILDTEXTMININGNOTEBOOKTEXTMINING, 
 wxID_MDICHILDTEXTMININGPANPREPROCESSING, wxID_MDICHILDTEXTMININGPANREPORTS, 
 wxID_MDICHILDTEXTMININGPANSEARCH, wxID_MDICHILDTEXTMININGPANTOPTERMS, 
 wxID_MDICHILDTEXTMININGSTATICBOX1, wxID_MDICHILDTEXTMININGSTATICBOX2, 
 wxID_MDICHILDTEXTMININGSTATICBOXSEARCH, wxID_MDICHILDTEXTMININGSTATICTEXT2, 
 wxID_MDICHILDTEXTMININGSTATICTEXT3, wxID_MDICHILDTEXTMININGSTATICTEXT5, 
 wxID_MDICHILDTEXTMININGSTATICTEXT6, wxID_MDICHILDTEXTMININGTXTTOPKEYWORDS, 
 wxID_MDICHILDTEXTMININGTXTTOPPHONES, 
] = [wx.NewId() for _init_ctrls in range(27)]

class MDIChildTextMining(wx.MDIChildFrame, listmix.ColumnSorterMixin):

    def _init_coll_notebookTextMining_Pages(self, parent):
        # generated method, don't edit

        parent.AddPage(imageId=-1, page=self.panPreprocessing, select=False,
              text=u'Preprocessing')
        parent.AddPage(imageId=-1, page=self.panSearch, select=False,
              text=u'Search')
        parent.AddPage(imageId=-1, page=self.panTopTerms, select=False,
              text=u'Top: Terms | Phone Numbers')
        parent.AddPage(imageId=-1, page=self.panReports, select=True,
              text=u'Reports')

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.MDIChildFrame.__init__(self, id=wxID_MDICHILDTEXTMINING,
              name=u'MDIChildTextMining', parent=prnt, pos=wx.Point(148, 137),
              size=wx.Size(1048, 714), style=wx.DEFAULT_FRAME_STYLE,
              title=u'Text Mining')
        self.SetClientSize(wx.Size(1040, 680))
        self.SetBackgroundColour(wx.Colour(125, 152, 221))
        self.SetAutoLayout(True)

        self.notebookTextMining = wx.Notebook(id=wxID_MDICHILDTEXTMININGNOTEBOOKTEXTMINING,
              name=u'notebookTextMining', parent=self, pos=wx.Point(4, 4),
              size=wx.Size(1032, 672), style=0)
        self.notebookTextMining.SetConstraints(LayoutAnchors(self.notebookTextMining,
              True, True, True, True))

        self.panSearch = wx.Panel(id=wxID_MDICHILDTEXTMININGPANSEARCH,
              name=u'panSearch', parent=self.notebookTextMining, pos=wx.Point(0,
              0), size=wx.Size(1024, 646), style=wx.TAB_TRAVERSAL)
        self.panSearch.SetBackgroundColour(wx.Colour(225, 236, 255))
        self.panSearch.SetAutoLayout(True)
        self.panSearch.SetAutoLayout(True)

        self.panPreprocessing = wx.Panel(id=wxID_MDICHILDTEXTMININGPANPREPROCESSING,
              name=u'panPreprocessing', parent=self.notebookTextMining,
              pos=wx.Point(0, 0), size=wx.Size(1024, 646),
              style=wx.TAB_TRAVERSAL)
        self.panPreprocessing.SetBackgroundColour(wx.Colour(225, 236, 255))

        self.staticText2 = wx.StaticText(id=wxID_MDICHILDTEXTMININGSTATICTEXT2,
              label='Preprocessing:', name='staticText2',
              parent=self.panPreprocessing, pos=wx.Point(16, 16),
              size=wx.Size(97, 16), style=0)
        self.staticText2.SetForegroundColour(wx.Colour(0, 0, 187))
        self.staticText2.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, u'Tahoma'))
        self.staticText2.SetConstraints(LayoutAnchors(self.staticText2, True,
              True, False, False))

        self.btnPreprocessing = wx.Button(id=wxID_MDICHILDTEXTMININGBTNPREPROCESSING,
              label=u'Text Preprocessing...', name=u'btnPreprocessing',
              parent=self.panPreprocessing, pos=wx.Point(144, 8),
              size=wx.Size(168, 24), style=0)
        self.btnPreprocessing.Bind(wx.EVT_BUTTON, self.OnBtnPreprocessingButton,
              id=wxID_MDICHILDTEXTMININGBTNPREPROCESSING)

        self.panTopTerms = wx.Panel(id=wxID_MDICHILDTEXTMININGPANTOPTERMS,
              name=u'panTopTerms', parent=self.notebookTextMining,
              pos=wx.Point(0, 0), size=wx.Size(1024, 646),
              style=wx.TAB_TRAVERSAL)
        self.panTopTerms.SetBackgroundColour(wx.Colour(225, 236, 255))
        self.panTopTerms.SetAutoLayout(True)

        self.staticBox1 = wx.StaticBox(id=wxID_MDICHILDTEXTMININGSTATICBOX1,
              label=u'Terms', name='staticBox1', parent=self.panTopTerms,
              pos=wx.Point(8, 8), size=wx.Size(392, 632), style=0)
        self.staticBox1.SetConstraints(LayoutAnchors(self.staticBox1, True,
              True, False, True))

        self.staticBox2 = wx.StaticBox(id=wxID_MDICHILDTEXTMININGSTATICBOX2,
              label='Phone Numbers', name='staticBox2', parent=self.panTopTerms,
              pos=wx.Point(416, 8), size=wx.Size(424, 632), style=0)
        self.staticBox2.SetConstraints(LayoutAnchors(self.staticBox2, True,
              True, False, True))

        self.btnDisplayTopPhones = wx.Button(id=wxID_MDICHILDTEXTMININGBTNDISPLAYTOPPHONES,
              label='Display', name='btnDisplayTopPhones',
              parent=self.panTopTerms, pos=wx.Point(592, 32), size=wx.Size(75,
              23), style=0)
        self.btnDisplayTopPhones.Bind(wx.EVT_BUTTON,
              self.OnBtnDisplayTopPhonesButton,
              id=wxID_MDICHILDTEXTMININGBTNDISPLAYTOPPHONES)

        self.staticText3 = wx.StaticText(id=wxID_MDICHILDTEXTMININGSTATICTEXT3,
              label='Top:', name='staticText3', parent=self.panTopTerms,
              pos=wx.Point(16, 32), size=wx.Size(28, 16), style=0)
        self.staticText3.SetForegroundColour(wx.Colour(0, 0, 187))
        self.staticText3.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, u'Tahoma'))
        self.staticText3.SetConstraints(LayoutAnchors(self.staticText3, True,
              True, False, False))

        self.txtTopPhones = wx.TextCtrl(id=wxID_MDICHILDTEXTMININGTXTTOPPHONES,
              name='txtTopPhones', parent=self.panTopTerms, pos=wx.Point(472,
              32), size=wx.Size(100, 21), style=0, value='')

        self.txtTopKeywords = wx.TextCtrl(id=wxID_MDICHILDTEXTMININGTXTTOPKEYWORDS,
              name='txtTopKeywords', parent=self.panTopTerms, pos=wx.Point(48,
              32), size=wx.Size(100, 21), style=0, value='')

        self.staticText6 = wx.StaticText(id=wxID_MDICHILDTEXTMININGSTATICTEXT6,
              label='Top:', name='staticText6', parent=self.panTopTerms,
              pos=wx.Point(440, 32), size=wx.Size(28, 16), style=0)
        self.staticText6.SetForegroundColour(wx.Colour(0, 0, 187))
        self.staticText6.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, u'Tahoma'))
        self.staticText6.SetConstraints(LayoutAnchors(self.staticText6, True,
              True, False, False))

        self.btnExportTopKeywords = wx.Button(id=wxID_MDICHILDTEXTMININGBTNEXPORTTOPKEYWORDS,
              label='Export...', name='btnExportTopKeywords',
              parent=self.panTopTerms, pos=wx.Point(264, 32), size=wx.Size(75,
              23), style=0)
        self.btnExportTopKeywords.Bind(wx.EVT_BUTTON,
              self.OnBtnExportTopKeywordsButton,
              id=wxID_MDICHILDTEXTMININGBTNEXPORTTOPKEYWORDS)

        self.btnDisplayTopKeywords = wx.Button(id=wxID_MDICHILDTEXTMININGBTNDISPLAYTOPKEYWORDS,
              label='Display', name='btnDisplayTopKeywords',
              parent=self.panTopTerms, pos=wx.Point(168, 32), size=wx.Size(75,
              23), style=0)
        self.btnDisplayTopKeywords.Bind(wx.EVT_BUTTON,
              self.OnBtnDisplayTopKeywordsButton,
              id=wxID_MDICHILDTEXTMININGBTNDISPLAYTOPKEYWORDS)

        self.btnExportTopPhones = wx.Button(id=wxID_MDICHILDTEXTMININGBTNEXPORTTOPPHONES,
              label='Export...', name='btnExportTopPhones',
              parent=self.panTopTerms, pos=wx.Point(688, 32), size=wx.Size(75,
              23), style=0)
        self.btnExportTopPhones.Bind(wx.EVT_BUTTON,
              self.OnBtnExportTopPhonesButton,
              id=wxID_MDICHILDTEXTMININGBTNEXPORTTOPPHONES)

        self.panReports = wx.Panel(id=wxID_MDICHILDTEXTMININGPANREPORTS,
              name=u'panReports', parent=self.notebookTextMining,
              pos=wx.Point(0, 0), size=wx.Size(1024, 646),
              style=wx.TAB_TRAVERSAL)
        self.panReports.SetBackgroundColour(wx.Colour(225, 236, 255))
        self.panReports.SetAutoLayout(True)

        self.staticText5 = wx.StaticText(id=wxID_MDICHILDTEXTMININGSTATICTEXT5,
              label=u'Page', name='staticText5', parent=self.panSearch,
              pos=wx.Point(8, 72), size=wx.Size(24, 13), style=0)

        self.choicePageNum = wx.Choice(choices=[],
              id=wxID_MDICHILDTEXTMININGCHOICEPAGENUM, name=u'choicePageNum',
              parent=self.panSearch, pos=wx.Point(40, 72), size=wx.Size(64, 21),
              style=0)
        self.choicePageNum.Bind(wx.EVT_CHOICE, self.OnChoicePageNumChoice,
              id=wxID_MDICHILDTEXTMININGCHOICEPAGENUM)

        self.lblTotalResults = wx.StaticText(id=wxID_MDICHILDTEXTMININGLBLTOTALRESULTS,
              label=u'of 1: Showing 0 Results', name=u'lblTotalResults',
              parent=self.panSearch, pos=wx.Point(112, 80), size=wx.Size(113,
              13), style=0)

        self.staticBoxSearch = wx.StaticBox(id=wxID_MDICHILDTEXTMININGSTATICBOXSEARCH,
              label='Search Documents Based on Keywords',
              name=u'staticBoxSearch', parent=self.panSearch, pos=wx.Point(8,
              8), size=wx.Size(656, 56), style=0)

        self.btnSearchDocuments = wx.Button(id=wxID_MDICHILDTEXTMININGBTNSEARCHDOCUMENTS,
              label='Search', name='btnSearchDocuments', parent=self.panSearch,
              pos=wx.Point(592, 32), size=wx.Size(59, 23), style=0)
        self.btnSearchDocuments.Bind(wx.EVT_BUTTON,
              self.OnBtnSearchDocumentsButton,
              id=wxID_MDICHILDTEXTMININGBTNSEARCHDOCUMENTS)

        self.btnExportSearchResults = wx.Button(id=wxID_MDICHILDTEXTMININGBTNEXPORTSEARCHRESULTS,
              label='Export Search Results', name='btnExportSearchResults',
              parent=self.panSearch, pos=wx.Point(872, 56), size=wx.Size(144,
              23), style=0)
        self.btnExportSearchResults.SetConstraints(LayoutAnchors(self.btnExportSearchResults,
              False, True, True, False))
        self.btnExportSearchResults.Bind(wx.EVT_BUTTON,
              self.OnBtnExportSearchResultsButton,
              id=wxID_MDICHILDTEXTMININGBTNEXPORTSEARCHRESULTS)

        self.btnExportAllTerms = wx.Button(id=wxID_MDICHILDTEXTMININGBTNEXPORTALLTERMS,
              label=u'Export All Terms', name=u'btnExportAllTerms',
              parent=self.panReports, pos=wx.Point(16, 16), size=wx.Size(168,
              24), style=0)
        self.btnExportAllTerms.Bind(wx.EVT_BUTTON,
              self.OnBtnExportAllTermsButton,
              id=wxID_MDICHILDTEXTMININGBTNEXPORTALLTERMS)

        self.btnExportStemmedTerms = wx.Button(id=wxID_MDICHILDTEXTMININGBTNEXPORTSTEMMEDTERMS,
              label=u'Export Stemmed Terms', name=u'btnExportStemmedTerms',
              parent=self.panReports, pos=wx.Point(16, 56), size=wx.Size(168,
              24), style=0)
        self.btnExportStemmedTerms.Bind(wx.EVT_BUTTON,
              self.OnBtnExportStemmedTerms,
              id=wxID_MDICHILDTEXTMININGBTNEXPORTSTEMMEDTERMS)

        self.btnBatchSearch = wx.Button(id=wxID_MDICHILDTEXTMININGBTNBATCHSEARCH,
              label=u'Keywords Search Report...', name='btnBatchSearch',
              parent=self.panSearch, pos=wx.Point(872, 8), size=wx.Size(144,
              23), style=0)
        self.btnBatchSearch.Bind(wx.EVT_BUTTON, self.OnBtnBatchSearchButton,
              id=wxID_MDICHILDTEXTMININGBTNBATCHSEARCH)

        self._init_coll_notebookTextMining_Pages(self.notebookTextMining)

    def __init__(self, parent):
        self._init_ctrls(parent)
        
        self.SetIcon(images.getMAKE2Icon())
        
        self.CreateSettingsTable()
        
        self.AddSearchControl()
        self.CreateTopKeywordsListControl()
        self.CreateTopPhonesListControl()
        self.AddResultsListControl()
        self.Stopwords = []
        
        try:
            self.ReadStopwordsFromDB()
        except:
            pass
            
        self.search = Search(Globals.TextCatFileName, self.Stopwords)
        #self.AddKeywordsToTree()
    
    def CreateSettingsTable(self):
        db = SqliteDatabase(Globals.TextCatFileName)
        if not db.OpenConnection():
            return
                
        
        query = "CREATE TABLE IF NOT EXISTS " + Constants.TextCatSettingsTable + " ( "
        query += "Stemmer text, DirList text, CategoryList text )"
               
        db.ExecuteNonQuery(query)
        db.CloseConnection()
        return None
      

    def OnBtnPreprocessingButton(self, event):
        import frmTextPreprocessing
        textPreprocessing = frmTextPreprocessing.create(self)
        textPreprocessing.Show()
        event.Skip()

    def OnBtnExportAllTermsButton(self, event):
        db = SqliteDatabase(Globals.TextCatFileName)
        if not db.OpenConnection():
            return
                
        dlg = wx.FileDialog(self, "Save Words List", ".", "", "*.csv", wx.SAVE)
        try:
            if dlg.ShowModal() == wx.ID_OK:
                fileName = dlg.GetPath()
                busy = wx.BusyInfo("It might take some time depending on the total number of unique words...")
                wx.Yield()
                fout = open(fileName, 'wb')
                #query = "select ID, `Word` from " + Constants.TextCatWordsTable + " order by `ID`; "
                query = "select words.word, count(WordLocation.WordID) as total from words left join WordLocation on words.rowid = wordlocation.wordid "
                query += "group by wordlocation.wordid order by total desc;"
                #print 'before'
                rows = db.FetchAllRows(query)
                #rint 'after'
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
            if fout:
                fout.close()
            CommonFunctions.ShowErrorMessage(self, "Failed to Export Word List. Error: %s"%value)
        finally:
            dlg.Destroy()
        db = None

       
       
            
    def AddPageNumbersToPageChoice(self, totalResults):
        self.TotalPages = (totalResults/Constants.MaxObjectsPerPage)
        if (totalResults%Constants.MaxObjectsPerPage) > 0:
            self.TotalPages += 1
            
        self.choicePageNum.Clear()
        for page in range(1, self.TotalPages+1):
            self.choicePageNum.Append(str(page))
            


    def OnBtnPreprocessingButton(self, event):
        import frmEmailPreprocessing
        textPreprocessing = frmEmailPreprocessing.create(self)
        textPreprocessing.Show()
        event.Skip()

        
    def CreateTopKeywordsListControl(self):
        """
              
        self.listCtrl1 = wx.ListCtrl(id=wxID_MDICHILDEMAILSLISTCTRL1,
              name='listCtrl1', parent=self.panSearch, pos=wx.Point(16, 64),
              size=wx.Size(376, 568), style=wx.LC_ICON)

        """

        self.listTopKeywords = CustomListCtrl(self.panTopTerms, wx.NewId(),
                                pos=wx.Point(16, 64), size=wx.Size(376, 568),
                                 style=wx.LC_REPORT 
                                 | wx.BORDER_NONE
                                 )
        
        self.listTopKeywords.SetConstraints(LayoutAnchors(self.listTopKeywords, True,
              True, False, True))
        self.listTopKeywords.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, u'Tahoma'))
              
        self.AddTopKeywordsListColumnHeadings()
        
       
    def CreateTopPhonesListControl(self):
        """
        self.listCtrl1 = wx.ListCtrl(id=wxID_MDICHILDEMAILSLISTCTRL1,
              name='listCtrl1', parent=self.panSearch, pos=wx.Point(424, 64),
              size=wx.Size(408, 384), style=wx.LC_ICON)
        """

        self.listTopPhones = CustomListCtrl(self.panTopTerms, wx.NewId(),
                                pos=wx.Point(424, 64), size=wx.Size(408, 568),
                                 style=wx.LC_REPORT 
                                 | wx.BORDER_NONE
                                 )
        
        self.listTopPhones.SetConstraints(LayoutAnchors(self.listTopPhones, True,
              True, False, True))
        self.listTopPhones.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, u'Tahoma'))
              
        self.AddTopPhonesListColumnHeadings()
        
      
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
    
       
    # Used by the ColumnSorterMixin, see wx/lib/mixins/listctrl.py
    def GetListCtrl(self):
        return self.listMessages

    # Used by the ColumnSorterMixin, see wx/lib/mixins/listctrl.py
    def GetSortImages(self):
        return (self.sm_dn, self.sm_up)

    def OnListTopKeywordsColClick(self, event):
        event.Skip()
        
    def OnListTopPhonesColClick(self, event):
        event.Skip()
        
     
        
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
        db = SqliteDatabase(Globals.TextCatFileName)
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
            
                
        self.listTopKeywords.SetColumnWidth(0, 250)
        self.listTopKeywords.SetColumnWidth(1, 70)
        
        self.SetCursor(wx.STANDARD_CURSOR)
        
    def AddTopPhonesToListView(self, top=20):
        
        db = SqliteDatabase(Globals.TextCatFileName)
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
            
            index = self.listTopPhones.InsertStringItem(sys.maxint, PlatformMethods.Decode(row[0]))
            self.listTopPhones.SetStringItem(index, 1, PlatformMethods.Decode(row[1]))
            self.listTopPhones.SetItemData(index, totalKeywords)
            
                
        self.listTopPhones.SetColumnWidth(0, 250)
        self.listTopPhones.SetColumnWidth(1, 120)
        
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
            return True
            
        else:
            CommonFunctions.ShowErrorMessage(self, 'Please select a message from the list.')
            return False


    def OnBtnExportTopKeywordsButton(self, event):
        db = SqliteDatabase(Globals.TextCatFileName)
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
                query = "select Word, Frequency from Words order by Word %s;"%limit
                
                rows = db.FetchAllRows(query)
                i = 1
                for row in rows:
                    fout.write(PlatformMethods.Encode(row[0]))
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
            CommonFunctions.ShowErrorMessage(self, "Failed to Export Top Keywords List. Error: %s"%value)
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
        db = SqliteDatabase(Globals.TextCatFileName)
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


    def AddSearchControl(self):
        """
        
        self.textCtrl1 = wx.TextCtrl(id=wxID_MDICHILDTEXTMININGTEXTCTRL1,
              name='textCtrl1', parent=self.panSearch, pos=wx.Point(16, 32),
              size=wx.Size(568, 21), style=0, value='textCtrl1')
              
        """
        self.searchDocuments = wx.SearchCtrl(self.panSearch, pos=wx.Point(16, 32),
              size=wx.Size(568, -1), style=wx.TE_PROCESS_ENTER)
        self.searchDocuments.ShowSearchButton(True)
        self.searchDocuments.ShowCancelButton(True)
        
        self.SearchDocumentsMenu = wx.Menu()
        item = self.SearchDocumentsMenu.Append(-1, "Recent Searches")
        item.Enable(False)
        
        self.searchDocuments.SetMenu(self.SearchDocumentsMenu)
        
        self.Bind(wx.EVT_SEARCHCTRL_SEARCH_BTN, self.OnSearchDocuments, self.searchDocuments)
        self.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, self.OnSearchDocumentsCancel, self.searchDocuments)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnDoSearchDocuments, self.searchDocuments)
        
        
                      
    def OnBtnSearchDocumentsButton(self, event):
        self.OnDoSearchDocuments(event)
        event.Skip()
        
    
    def AddResultsListControl(self):
        """
        self.listCtrl1 = wx.ListCtrl(id=wxID_MDICHILDTEXTMININGLISTCTRL1,
              name='listCtrl1', parent=self.panSearch, pos=wx.Point(8, 104),
              size=wx.Size(1008, 536), style=wx.LC_ICON)
        """
              
        listID = wx.NewId()
        self.listSearchResults = CustomListCtrl(self.panSearch, listID,
                                 pos=wx.Point(8, 104), size=wx.Size(1008, 536),
                                 style=wx.LC_REPORT | wx.BORDER_NONE
                                 )
        
        self.listSearchResults.SetConstraints(LayoutAnchors(self.listSearchResults,
              True, True, True, True))
        self.listSearchResults.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, u'Tahoma'))
              
        # Now that the list exists we can init the other base class,
        # see wx/lib/mixins/listctrl.py
        #listmix.ColumnSorterMixin.__init__(self, 1)
        
        #self.Bind(wx.EVT_LIST_COL_CLICK, self.OnListColClick, self.listSearchResults)
        self.listSearchResults.Bind(wx.EVT_LEFT_DCLICK, self.OnListSearchResultsLeftDclick)
        self.AddListColumnHeadings()
    
    def AddListColumnHeadings(self):
        #want to add images on the column header..
        """
        info = wx.ListItem()
        info.m_mask = wx.LIST_MASK_TEXT | wx.LIST_MASK_IMAGE | wx.LIST_MASK_FORMAT
        info.m_image = -1
        info.m_format = 0
        info.m_text = "Document Path"
        self.listSearchResults.InsertColumnInfo(0, info)
        """
        self.listSearchResults.InsertColumn(col=0, format=wx.LIST_FORMAT_LEFT,
              heading='Document Path', width=700)
                  
                  
    # Used by the ColumnSorterMixin, see wx/lib/mixins/listctrl.py
    def GetListCtrl(self):
        return self.listSearchResults

    # Used by the ColumnSorterMixin, see wx/lib/mixins/listctrl.py
    def GetSortImages(self):
        return (self.sm_dn, self.sm_up)
    
    def OnListColClick(self, event):
        event.Skip()
        
        
    def OnSearchDocuments(self, event):
        event.Skip()
        
    def OnDoSearchDocuments(self, event):
        searchWords = self.searchDocuments.GetValue()
        if not searchWords:
            return
        
        self.SearchDocuments(searchWords)
        event.Skip()
        
    def SearchDocuments(self, searchWords):
        if self.SearchDocumentsMenu.FindItem(searchWords) < 0:
            id = wx.NewId()
            self.SearchDocumentsMenu.Append(id, searchWords)
            self.Bind(wx.EVT_MENU, self.OnSearchDocumentsMenu,
              id=id)
        
        #print searchWords
        self.DocPaths =[]
        #totalResults = 0
        self.TotalResults = 0
        try:
            self.DocPaths, self.TotalResults = self.search.GetRankedDocuments(searchWords)
        except Exception, msg:
            CommonFunctions.ShowErrorMessage(self, 'No Indexing has been performed!', error=True)
            
        
        self.AddPageNumbersToPageChoice(self.TotalResults)

        self.choicePageNum.SetSelection(0)
                       
        self.AddSearchResultsToListView(1)
        
        
    def OnSearchDocumentsMenu(self, event):
        id = event.GetId()
        searchWords = self.SearchDocumentsMenu.GetLabel(id)
        self.searchDocuments.SetValue(searchWords)
        self.SearchDocuments(searchWords)
        event.Skip()

        
    def OnSearchDocumentsCancel(self, event):
        #self.AddAddressesToListView()
        event.Skip()
        
    
    
    def AddSearchResultsToListView(self, pageNum):
        wx.BeginBusyCursor()
        
        self.listSearchResults.ClearAll()
        self.AddListColumnHeadings()
        self.IconDict = {}
        totalFiles = 0
        self.il = wx.ImageList(16, 16)
        self.listSearchResults.AssignImageList(self.il, wx.IMAGE_LIST_SMALL)
        NoLog = wx.LogNull()
        startIndex = ((pageNum-1)*Constants.MaxObjectsPerPage)
        endIndex = (pageNum * Constants.MaxObjectsPerPage)
        for doc in self.DocPaths[startIndex:endIndex]:
            fileName = PlatformMethods.Decode(doc)
            iconFound = False
            if not (fileName.rfind('.') == -1):
                fileExtension = fileName[fileName.rfind('.'):]
                fileType = wx.TheMimeTypesManager.GetFileTypeFromExtension(fileExtension)
                if fileType:
                    #fullFileName = os.path.join(self.dirPath, data[0])
                    #try:
                    info = fileType.GetIconInfo()
                    if info:
                        icon, file, idx = info
                        #print icon
                        if icon.Ok():
                            #iconInfo[totalFiles] = icon
                            #bmp = wx.Image(opj('bitmaps/image.bmp'), wx.BITMAP_TYPE_BMP).ConvertToBitmap()
                            icon.SetSize(wx.Size(16, 16))
                            self.IconDict[totalFiles] = self.il.AddIcon(icon)
                            iconFound = True
                        
            if not iconFound:
                icon = images.getNoFile16Icon()
                self.IconDict[totalFiles] = self.il.AddIcon(icon)
                
            self.listSearchResults.InsertImageStringItem(sys.maxint, fileName, self.IconDict[totalFiles])
            totalFiles += 1
        
        NoLog = None
        self.lblTotalResults.SetLabel(" of %d: %d Search Results for: %s (%d)"%(self.TotalPages, self.TotalResults, self.searchDocuments.GetValue()))
        #self.lblSearchResults.SetLabel("Search Results for word: " + self.searchDocuments.GetValue() + " (" + str(totalResults) + ")")
        self.SetCursor(wx.STANDARD_CURSOR)
        wx.EndBusyCursor()
    
    # Used by the ColumnSorterMixin, see wx/lib/mixins/listctrl.py
    def GetListCtrl(self):
        return self.listSearchResults

    # Used by the ColumnSorterMixin, see wx/lib/mixins/listctrl.py
    def GetSortImages(self):
        return (self.sm_dn, self.sm_up)
    
    def OnListColClick(self, event):
        event.Skip()
          
    def OnBtnCloseButton(self, event):
        self.Close()


    def OnListResultsListColClick(self, event):
        event.Skip()
        
    def IsFileSelected(self):
        index = self.listSearchResults.GetFirstSelected()
        if index >=0:
            self.fullFilePath = PlatformMethods.Decode(self.listSearchResults.GetItem(index).GetText())
            return True
        else:
            dlg = wx.MessageDialog(self, 'Please select a file from the list.',
              'Error', wx.OK | wx.ICON_ERROR)
            try:
                dlg.ShowModal()
            finally:
                dlg.Destroy()
                return False
            

    
    def ReadStopwordsFromDB(self):
        db = SqliteDatabase(Globals.TextCatFileName)
        if not db.OpenConnection():
            return
        
        query = "SELECT Stopword FROM " + Constants.StopwordsTable
        rows = db.FetchAllRows(query)
        for row in rows:
            self.Stopwords.append(row[0])
            
        #print Globals.KeyWords
        db.CloseConnection()
        
    def OnBtnExportSearchResultsButton(self, event):
        #tbd: need to fix this so that only the current search view is exported
        return
        db = SqliteDatabase(Globals.KeywordsFileName)
        if not db.OpenConnection():
            return
           
        dlg = wx.DirDialog(self, message="Empty Directory to Save Search Results")
        #try:
        if dlg.ShowModal() == wx.ID_OK:
            dirPath = dlg.GetPath()
            if os.listdir(dirPath):
                CommonFunctions.ShowErrorMessage(self, "Selected directory is not empty! Please select an empty directory!")
            else:
                busy = wx.BusyInfo("It may take some time depending on the total number of kewywords...")
                wx.Yield()
                fout = open(os.path.join(dirPath, "SearchResultsSummary.txt"), 'wb')
                fout.write("%s%s%s%s\n"%("Keyword".ljust(20, " "), "File Path".ljust(200, " "), "Case Sens.".rjust(12, " "), "Case Insens.".rjust(12, " ")))
                fout.write("%s%s%s%s\n"%("=".ljust(20, "="), "=".ljust(200, "="), "=".rjust(12, "="), "=".rjust(12, "="))) 
                for word in Globals.Keywords:
                    keywordPath = os.path.join(dirPath, word)
                    if not os.path.isdir(keywordPath):
                        os.mkdir(keywordPath)
                        
                    fout.write(word.ljust(20, " "))
                    query = "select FileName, " + word + "_CS," + word + "_CI from " + Constants.KeywordsFrequencyTable
                    query += " where " + word + "_CI > 0 or " + word + "_CS > 0;"  
                    
                    rows = db.FetchAllRows(query)
                    i = 0
                    for row in rows:
                        try:
                            if i> 0:
                                fout.write(" ".ljust(20, " "))
                            i += 1
                            srcFilePath = PlatformMethods.Decode(row[0]) #.replace("\\\\", "\\") 
                            fileName = os.path.basename(row[0])
                            dstFilePath = PlatformMethods.Decode(os.path.join(keywordPath, fileName))
                            fout.write(srcFilePath.ljust(200, " "))
                            fout.write(PlatformMethods.Encode(row[1]).rjust(12, " "))
                            fout.write(PlatformMethods.Encode(row[2]).rjust(12, " "))
                            shutil.copyfile(srcFilePath, dstFilePath)
                            shutil.copystat(srcFilePath, dstFilePath)
                        except Exception, value:
                            print 'Error occured while exporting search results: Error: ', value
                            
                        fout.write("\n")
                    
                    fout.write("\n")
                    fout.write("%s\n"%("*".ljust(250, "*")))
                    
                db.CloseConnection()
                fout.close()
        

    def OnListSearchResultsLeftDclick(self, event):
        if self.IsFileSelected():
            """
            for fileInfo in Globals.FileInfoList:
                if self.fullFilePath == os.path.join(PlatformMethods.Decode(fileInfo.DirectoryPath), PlatformMethods.Decode(fileInfo.Name)):
                    cmd = PlatformMethods.Decode(fileInfo.OpenCommand)
                    os.system('start '+cmd)
                    break
            """
            fileExtension = self.fullFilePath[self.fullFilePath.rfind('.'):]
            fileType = wx.TheMimeTypesManager.GetFileTypeFromExtension(fileExtension)
            if fileType:
                mimeType = fileType.GetMimeType() or ""
                #newFile.MimeType = mimeType
                #newFile.Description = fileType.GetDescription() or "Unknown"
                cmd = fileType.GetOpenCommand(self.fullFilePath, mimeType)
                os.system('start '+cmd)
        event.Skip()

    def OnBtnSearchDocumentsButton(self, event):
        self.OnDoSearchDocuments(event)
        event.Skip()


    def OnBtnExportStemmedTerms(self, event):
        db = SqliteDatabase(Globals.TextCatFileName)
        if not db.OpenConnection():
            return
                
        #CommonFunctions.ShowErrorMessage(self, 'This is not yet implemented!', False)
        #return
    
        dlg = wx.FileDialog(self, "Save Stemmed Words List", ".", "", "*.csv", wx.SAVE)
        try:
            if dlg.ShowModal() == wx.ID_OK:
                fileName = dlg.GetPath()
                busy = wx.BusyInfo("It might take some time depending on the word feature size...")
                wx.Yield()
                fout = open(fileName, 'w')
                query = "select distinct(StemmedWord) from Words order by StemmedWord;"
                rows = db.FetchAllRows(query)
                i = 1
                noRow = True
                for row in rows:
                    if row[0]:
                        noRow = False
                    fout.write(PlatformMethods.Encode(row[0]))
                    fout.write(", ,")
                    i += 1
                    if i == 4:
                        i = 0
                        fout.write("\n")

                db.CloseConnection()
                fout.close()
                if noRow:
                    CommonFunctions.ShowErrorMessage(self, "No Stemming was done while Preprocessing!")
        except Exception, value:
            db.CloseConnection()
            fout.close()
            CommonFunctions.ShowErrorMessage(self, "Failed to Export Stemmed Word List. Error: %s"%value)
        finally:
            dlg.Destroy()
        
        db = None
        event.Skip()

    def OnChoicePageNumChoice(self, event):
        pageNum = int(self.choiceMessagePage.GetStringSelection())
        self.AddSearchResultsToListView(pageNum)
        event.Skip()

    def OnBtnBatchSearchButton(self, event):
        import dlgKeywordsBatchSearch
        batchSearch = dlgKeywordsBatchSearch.create(self, self.Stopwords)
        batchSearch.ShowModal()
        event.Skip()


    
    
