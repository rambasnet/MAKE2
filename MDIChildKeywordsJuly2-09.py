#-----------------------------------------------------------------------------
# Name:        MDIChildKeywords.py
# Purpose:     
#
# Author:      Ram B. Basnet
#
# Created:     2008/07/09
# Last Modified: 7/2/2009
# RCS-ID:      $Id: MDIChildKeywords.py $
# Copyright:   (c) 2006
# Licence:     All Rights Reserved.
# New field:   Whatever
#-----------------------------------------------------------------------------
#Boa:MiniFrame:MDIChildKeywords

import wx, sys, os
import re, string
from wx.lib.anchors import LayoutAnchors
import  wx.lib.mixins.listctrl  as  listmix
import shutil

from SqliteDatabase import *
import Globals
import PlatformMethods
import CommonFunctions
import Constants
import DBFunctions

import  images
from Search import *

def create(parent):
    return MDIChildKeywords(parent)

class CustomListCtrl(wx.ListCtrl):
    def __init__(self, parent, ID, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        #listmix.ListCtrlAutoWidthMixin.__init__(self)
        
        
[wxID_MDICHILDKEYWORDS, wxID_MDICHILDKEYWORDSBTNBATCHSEARCH, 
 wxID_MDICHILDKEYWORDSBTNCLOSE, wxID_MDICHILDKEYWORDSBTNCUSTOMIZESEARCH, 
 wxID_MDICHILDKEYWORDSBTNEXPORTSEARCHRESULTS, 
 wxID_MDICHILDKEYWORDSBTNSEARCHDOCUMENTS, 
 wxID_MDICHILDKEYWORDSLBLSEARCHRESULTS, wxID_MDICHILDKEYWORDSPANKEYWORDS, 
 wxID_MDICHILDKEYWORDSSTATICBOX5, 
] = [wx.NewId() for _init_ctrls in range(9)]

class MDIChildKeywords(wx.MDIChildFrame):


    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.MDIChildFrame.__init__(self, id=wxID_MDICHILDKEYWORDS,
              name=u'MDIChildKeywords', parent=prnt, pos=wx.Point(132, 97),
              size=wx.Size(1048, 714), style=wx.DEFAULT_FRAME_STYLE,
              title=u'Keywords Search')
        self.SetClientSize(wx.Size(1040, 680))
        self.SetBackgroundColour(wx.Colour(125, 152, 221))
        self.SetAutoLayout(True)

        self.panKeywords = wx.Panel(id=wxID_MDICHILDKEYWORDSPANKEYWORDS,
              name=u'panKeywords', parent=self, pos=wx.Point(4, 4),
              size=wx.Size(1032, 672), style=wx.TAB_TRAVERSAL)
        self.panKeywords.SetBackgroundColour(wx.Colour(225, 236, 255))
        self.panKeywords.SetConstraints(LayoutAnchors(self.panKeywords, True,
              True, True, True))

        self.btnClose = wx.Button(id=wxID_MDICHILDKEYWORDSBTNCLOSE,
              label=u'Close', name=u'btnClose', parent=self.panKeywords,
              pos=wx.Point(950, 8), size=wx.Size(75, 23), style=0)
        self.btnClose.SetConstraints(LayoutAnchors(self.btnClose, False, True,
              True, False))
        self.btnClose.Bind(wx.EVT_BUTTON, self.OnBtnCloseButton,
              id=wxID_MDICHILDKEYWORDSBTNCLOSE)

        self.btnCustomizeSearch = wx.Button(id=wxID_MDICHILDKEYWORDSBTNCUSTOMIZESEARCH,
              label='Customize And Search...', name=u'btnCustomizeSearch',
              parent=self.panKeywords, pos=wx.Point(176, 8), size=wx.Size(144,
              23), style=0)
        self.btnCustomizeSearch.Bind(wx.EVT_BUTTON,
              self.OnBtnCustomizeSearchButton,
              id=wxID_MDICHILDKEYWORDSBTNCUSTOMIZESEARCH)

        self.lblSearchResults = wx.StaticText(id=wxID_MDICHILDKEYWORDSLBLSEARCHRESULTS,
              label='Searh Results:', name=u'lblSearchResults',
              parent=self.panKeywords, pos=wx.Point(8, 112), size=wx.Size(95,
              16), style=0)
        self.lblSearchResults.SetForegroundColour(wx.Colour(0, 0, 187))
        self.lblSearchResults.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, u'Tahoma'))
        self.lblSearchResults.SetConstraints(LayoutAnchors(self.lblSearchResults,
              True, True, False, False))

        self.btnExportSearchResults = wx.Button(id=wxID_MDICHILDKEYWORDSBTNEXPORTSEARCHRESULTS,
              label='Export Search Results', name='btnExportSearchResults',
              parent=self.panKeywords, pos=wx.Point(888, 96), size=wx.Size(136,
              23), style=0)
        self.btnExportSearchResults.SetConstraints(LayoutAnchors(self.btnExportSearchResults,
              False, True, True, False))
        self.btnExportSearchResults.Bind(wx.EVT_BUTTON,
              self.OnBtnExportSearchResultsButton,
              id=wxID_MDICHILDKEYWORDSBTNEXPORTSEARCHRESULTS)

        self.btnSearchDocuments = wx.Button(id=wxID_MDICHILDKEYWORDSBTNSEARCHDOCUMENTS,
              label='Search', name='btnSearchDocuments',
              parent=self.panKeywords, pos=wx.Point(592, 64), size=wx.Size(59,
              23), style=0)
        self.btnSearchDocuments.Bind(wx.EVT_BUTTON,
              self.OnBtnSearchDocumentsButton,
              id=wxID_MDICHILDKEYWORDSBTNSEARCHDOCUMENTS)

        self.staticBox5 = wx.StaticBox(id=wxID_MDICHILDKEYWORDSSTATICBOX5,
              label='Search Documents Based on Keywords', name='staticBox5',
              parent=self.panKeywords, pos=wx.Point(8, 40), size=wx.Size(656,
              56), style=0)

        self.btnBatchSearch = wx.Button(id=wxID_MDICHILDKEYWORDSBTNBATCHSEARCH,
              label='Keywords Batch Search...', name='btnBatchSearch',
              parent=self.panKeywords, pos=wx.Point(16, 8), size=wx.Size(144,
              23), style=0)
        self.btnBatchSearch.Bind(wx.EVT_BUTTON, self.OnBtnBatchSearchButton,
              id=wxID_MDICHILDKEYWORDSBTNBATCHSEARCH)

    def __init__(self, parent):
        self._init_ctrls(parent)
        self.SetIcon(images.getMAKE2Icon())
        
        #self.FileInfo = {}
        #self.lblDirectoryName.SetLabel(PlatformMethods.Decode(self.dirPath))
        self.CreateSettingsTable()
        #self.CreateListControl()
        self.AddSearchControl()
        self.AddResultsListControl()
        self.Stopwords = []
        if len(Globals.Keywords) == 0:
            #self.ReadKeyWordsFromDatabase()
            try:
                self.ReadStopwordsFromDB()
            except:
                pass
            
        self.search = Search(Globals.TextCatFileName, self.Stopwords)
        #self.AddKeywordsToTree()
    
    
    def AddResultsListControl(self):
        """
        self.listCtrl1 = wx.ListCtrl(id=wxID_MDICHILDKEYWORDSLISTCTRL1,
              name='listCtrl1', parent=self.panKeywords, pos=wx.Point(8, 136),
              size=wx.Size(1016, 528), style=wx.LC_ICON)
        """
              
        listID = wx.NewId()
        self.listSearchResults = CustomListCtrl(self.panKeywords, listID,
                                 pos=wx.Point(8, 136), size=wx.Size(1016, 528),
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
        
    def AddSearchControl(self):
        """
        self.textCtrl1 = wx.TextCtrl(id=wxID_MDICHILDKEYWORDSTEXTCTRL1,
              name='textCtrl1', parent=self.panKeywords, pos=wx.Point(16, 64),
              size=wx.Size(288, 21), style=0, value='textCtrl1')
        """
        self.searchDocuments = wx.SearchCtrl(self.panKeywords, pos=wx.Point(16, 64),
              size=wx.Size(568, 21), style=wx.TE_PROCESS_ENTER)
        self.searchDocuments.ShowSearchButton(True)
        self.searchDocuments.ShowCancelButton(True)
        
        self.SearchDocumentsMenu = wx.Menu()
        item = self.SearchDocumentsMenu.Append(-1, "Recent Searches")
        item.Enable(False)
        
        self.searchDocuments.SetMenu(self.SearchDocumentsMenu)
        
        self.Bind(wx.EVT_SEARCHCTRL_SEARCH_BTN, self.OnSearchDocuments, self.searchDocuments)
        self.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, self.OnSearchAddressBookCancel, self.searchDocuments)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnDoSearchDocuments, self.searchDocuments)
        
        
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
        DocPaths =[]
        totalResults = 0
        try:
            DocPaths, totalResults = self.search.GetRankedDocuments(searchWords)
        except Exception, msg:
            CommonFunctions.ShowErrorMessage(self, 'No Indexing has been performed!', error=True)
            
        self.AddSearchResultsToListView(DocPaths, totalResults)
        
        
    def OnSearchDocumentsMenu(self, event):
        id = event.GetId()
        searchWords = self.SearchDocumentsMenu.GetLabel(id)
        self.searchDocuments.SetValue(searchWords)
        self.SearchDocuments(searchWords)
        event.Skip()

        
    def OnSearchAddressBookCancel(self, event):
        #self.AddAddressesToListView()
        event.Skip()
        
        
    def CreateSettingsTable(self):
        db = SqliteDatabase(Globals.KeywordsFileName)
        if not db.OpenConnection():
            return
                
        #query = "DROP TABLE IF EXISTS " + Constants.TextCatSettingsTable
        #db.ExecuteNonQuery(query)
        
        query = "CREATE TABLE IF NOT EXISTS " + Constants.KeywordsSettingsTable + " ( "
        query += "CaseInsensitive integer, CaseSensitive integer, "
        query += "KeywordList text, DirList text, CategoryList text )"
               
        db.ExecuteNonQuery(query)
        db.CloseConnection()
        return None
    
    
    def AddSearchResultsToListView(self, DocPaths, totalResults=0):
        wx.BeginBusyCursor()
        
        self.listSearchResults.ClearAll()
        self.AddListColumnHeadings()
        self.IconDict = {}
        totalFiles = 0
        self.il = wx.ImageList(16, 16)
        self.listSearchResults.AssignImageList(self.il, wx.IMAGE_LIST_SMALL)
        for doc in DocPaths:
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
        
        self.lblSearchResults.SetLabel("Search Results for word: " + self.searchDocuments.GetValue() + " (" + str(totalResults) + ")")
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

    def OnListCtrl1LeftDclick(self, event):
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
            

    def OnBtnKeywordsButton(self, event):
        import frmKeywords
        frmKey = frmKeywords.create(self)
        frmKey.ShowModal()

    def OnBtnCustomizeSearchButton(self, event):
        import frmCustomizeSearch
        custSearch = frmCustomizeSearch.create(self)
        custSearch.Show()

    def OnBtnSearchButton(self, event):
        # Your code
        #self.InitializeKeyWordsFrequencyDictionary()
        import dlgKeywordsScanProgress
        scanMAC = dlgKeywordsScanProgress.create(self)
        #scanMAC.StartScan(dir)
        scanMAC.Show()
        event.Skip()

    
    def ReadKeyWordsFromDatabase(self):
        db = SqliteDatabase(Globals.KeywordsFileName)
        if not db.OpenConnection():
            return
        query = "select KeywordList from " + Constants.KeywordsSettingsTable
        rows = db.FetchAllRows(query)
        for row in rows:
            Globals.Keywords = row[0].split(';')


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
                            print 'Error occured while exporting: Error: ', value
                            
                        fout.write("\n")
                    
                    fout.write("\n")
                    fout.write("%s\n"%("*".ljust(250, "*")))
                    
                db.CloseConnection()
                fout.close()
        
    def OnBtnSearchAddressBookButton(self, event):
        event.Skip()

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

    def OnBtnBatchSearchButton(self, event):
        import dlgKeywordsBatchSearch
        batchSearch = dlgKeywordsBatchSearch.create(self, self.Stopwords)
        batchSearch.ShowModal()
        event.Skip()


