#Boa:MiniFrame:MDIChildKeywords

#-----------------------------------------------------------------------------
# Name:        MDIChildEmails.py
# Purpose:     
#
# Author:      Ram Basnet
#
# Created:     2007/11/01
# Last Modified: 7/24/2009
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
    return MDIChildKeywords(parent)

class CustomListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, ID, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        
        
[wxID_MDICHILDKEYWORDS, wxID_MDICHILDKEYWORDSBTNCUSTOMIZESEARCH, 
 wxID_MDICHILDKEYWORDSBTNEXPORTALLTERMS, 
 wxID_MDICHILDKEYWORDSBTNEXPORTSTEMMEDTERMS, 
 wxID_MDICHILDKEYWORDSCHOICEPAGENUM, wxID_MDICHILDKEYWORDSLBLTOTALRESULTS, 
 wxID_MDICHILDKEYWORDSLISTKEYWORDLIST, 
 wxID_MDICHILDKEYWORDSNOTEBOOKKEYWORDSMINING, 
 wxID_MDICHILDKEYWORDSPANPREPROCESSING, wxID_MDICHILDKEYWORDSPANREPORTS, 
 wxID_MDICHILDKEYWORDSPANSEARCH, wxID_MDICHILDKEYWORDSSTATICTEXT1, 
 wxID_MDICHILDKEYWORDSSTATICTEXT2, wxID_MDICHILDKEYWORDSSTATICTEXT5, 
] = [wx.NewId() for _init_ctrls in range(14)]

class MDIChildKeywords(wx.MDIChildFrame, listmix.ColumnSorterMixin):

    def _init_coll_notebookKeywordsMining_Pages(self, parent):
        # generated method, don't edit

        parent.AddPage(imageId=-1, page=self.panPreprocessing, select=False,
              text=u'Preprocessing')
        parent.AddPage(imageId=-1, page=self.panSearch, select=False,
              text=u'Results')
        parent.AddPage(imageId=-1, page=self.panReports, select=True,
              text=u'Reports')

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.MDIChildFrame.__init__(self, id=wxID_MDICHILDKEYWORDS,
              name=u'MDIChildKeywords', parent=prnt, pos=wx.Point(72, 72),
              size=wx.Size(1048, 714), style=wx.DEFAULT_FRAME_STYLE,
              title=u'Keywords Mining')
        self.SetClientSize(wx.Size(1040, 680))
        self.SetBackgroundColour(wx.Colour(125, 152, 221))
        self.SetAutoLayout(True)

        self.notebookKeywordsMining = wx.Notebook(id=wxID_MDICHILDKEYWORDSNOTEBOOKKEYWORDSMINING,
              name=u'notebookKeywordsMining', parent=self, pos=wx.Point(4, 4),
              size=wx.Size(1032, 672), style=0)
        self.notebookKeywordsMining.SetConstraints(LayoutAnchors(self.notebookKeywordsMining,
              True, True, True, True))

        self.panSearch = wx.Panel(id=wxID_MDICHILDKEYWORDSPANSEARCH,
              name=u'panSearch', parent=self.notebookKeywordsMining,
              pos=wx.Point(0, 0), size=wx.Size(1024, 646),
              style=wx.TAB_TRAVERSAL)
        self.panSearch.SetBackgroundColour(wx.Colour(225, 236, 255))
        self.panSearch.SetAutoLayout(True)
        self.panSearch.SetAutoLayout(True)

        self.panPreprocessing = wx.Panel(id=wxID_MDICHILDKEYWORDSPANPREPROCESSING,
              name=u'panPreprocessing', parent=self.notebookKeywordsMining,
              pos=wx.Point(0, 0), size=wx.Size(1024, 646),
              style=wx.TAB_TRAVERSAL)
        self.panPreprocessing.SetBackgroundColour(wx.Colour(225, 236, 255))

        self.staticText2 = wx.StaticText(id=wxID_MDICHILDKEYWORDSSTATICTEXT2,
              label=u'Customize And Search Keywords:', name='staticText2',
              parent=self.panPreprocessing, pos=wx.Point(16, 16),
              size=wx.Size(218, 16), style=0)
        self.staticText2.SetForegroundColour(wx.Colour(0, 0, 187))
        self.staticText2.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, u'Tahoma'))
        self.staticText2.SetConstraints(LayoutAnchors(self.staticText2, True,
              True, False, False))

        self.panReports = wx.Panel(id=wxID_MDICHILDKEYWORDSPANREPORTS,
              name=u'panReports', parent=self.notebookKeywordsMining,
              pos=wx.Point(0, 0), size=wx.Size(1024, 646),
              style=wx.TAB_TRAVERSAL)
        self.panReports.SetBackgroundColour(wx.Colour(225, 236, 255))
        self.panReports.SetAutoLayout(True)

        self.btnExportAllTerms = wx.Button(id=wxID_MDICHILDKEYWORDSBTNEXPORTALLTERMS,
              label=u'Export All Terms', name=u'btnExportAllTerms',
              parent=self.panReports, pos=wx.Point(16, 16), size=wx.Size(168,
              24), style=0)
        self.btnExportAllTerms.Bind(wx.EVT_BUTTON,
              self.OnBtnExportAllTermsButton,
              id=wxID_MDICHILDKEYWORDSBTNEXPORTALLTERMS)

        self.btnExportStemmedTerms = wx.Button(id=wxID_MDICHILDKEYWORDSBTNEXPORTSTEMMEDTERMS,
              label=u'Export Stemmed Terms', name=u'btnExportStemmedTerms',
              parent=self.panReports, pos=wx.Point(16, 56), size=wx.Size(168,
              24), style=0)
        self.btnExportStemmedTerms.Bind(wx.EVT_BUTTON,
              self.OnBtnExportStemmedTerms,
              id=wxID_MDICHILDKEYWORDSBTNEXPORTSTEMMEDTERMS)

        self.btnCustomizeSearch = wx.Button(id=wxID_MDICHILDKEYWORDSBTNCUSTOMIZESEARCH,
              label='Customize And Search...', name=u'btnCustomizeSearch',
              parent=self.panPreprocessing, pos=wx.Point(248, 16),
              size=wx.Size(144, 23), style=0)
        self.btnCustomizeSearch.Bind(wx.EVT_BUTTON,
              self.OnBtnCustomizeSearchButton,
              id=wxID_MDICHILDKEYWORDSBTNCUSTOMIZESEARCH)

        self.listKeywordList = wx.ListCtrl(id=wxID_MDICHILDKEYWORDSLISTKEYWORDLIST,
              name=u'listKeywordList', parent=self.panSearch, pos=wx.Point(8,
              32), size=wx.Size(248, 608),
              style=wx.VSCROLL | wx.HSCROLL| wx.LC_ICON)
        self.listKeywordList.SetConstraints(LayoutAnchors(self.listKeywordList,
              True, True, False, True))
        self.listKeywordList.Bind(wx.EVT_LIST_ITEM_SELECTED,
              self.OnListKeywordListListItemSelected,
              id=wxID_MDICHILDKEYWORDSLISTKEYWORDLIST)

        self.staticText1 = wx.StaticText(id=wxID_MDICHILDKEYWORDSSTATICTEXT1,
              label=u'Keywords List:', name='staticText1',
              parent=self.panSearch, pos=wx.Point(8, 8), size=wx.Size(96, 16),
              style=0)
        self.staticText1.SetForegroundColour(wx.Colour(0, 0, 187))
        self.staticText1.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, u'Tahoma'))
        self.staticText1.SetConstraints(LayoutAnchors(self.staticText1, True,
              True, False, False))

        self.staticText5 = wx.StaticText(id=wxID_MDICHILDKEYWORDSSTATICTEXT5,
              label=u'Page', name='staticText5', parent=self.panSearch,
              pos=wx.Point(272, 32), size=wx.Size(24, 13), style=0)

        self.choicePageNum = wx.Choice(choices=[],
              id=wxID_MDICHILDKEYWORDSCHOICEPAGENUM, name=u'choicePageNum',
              parent=self.panSearch, pos=wx.Point(304, 32), size=wx.Size(64,
              21), style=0)
        self.choicePageNum.Bind(wx.EVT_CHOICE, self.OnChoicePageNumChoice,
              id=wxID_MDICHILDKEYWORDSCHOICEPAGENUM)

        self.lblTotalResults = wx.StaticText(id=wxID_MDICHILDKEYWORDSLBLTOTALRESULTS,
              label=u'of 1: Showing 0 Results', name=u'lblTotalResults',
              parent=self.panSearch, pos=wx.Point(376, 40), size=wx.Size(113,
              13), style=0)

        self._init_coll_notebookKeywordsMining_Pages(self.notebookKeywordsMining)

    def __init__(self, parent):
        self._init_ctrls(parent)
        
        self.SetIcon(images.getMAKE2Icon())
        
        DBFunctions.SetupSqliteKeywordsSettingsTables(Globals.KeywordsFileName)
        self.AddResultsListControl()

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


    
    def AddResultsListControl(self):
        """
           self.listSearchResults = wx.ListCtrl(id=wxID_MDICHILDKEYWORDSLISTSEARCHRESULTS,
              name=u'listSearchResults', parent=self.panSearch,
              pos=wx.Point(264, 64), size=wx.Size(752, 576),
              style=wx.VSCROLL | wx.HSCROLL | wx.LC_REPORT)
        self.listSearchResults.SetConstraints(LayoutAnchors(self.listSearchResults,
              True, True, True, True))
        """
              
        listID = wx.NewId()
        self.listSearchResults = CustomListCtrl(self.panSearch, listID,
                                 pos=wx.Point(264, 64), size=wx.Size(752, 576),
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
              heading='Document Path', width=500)
                  
        self.listSearchResults.InsertColumn(col=1, format=wx.LIST_FORMAT_RIGHT,
              heading='Frequency', width=100)
                  
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

    def OnBtnCustomizeSearchButton(self, event):
        import frmCustomizeKeywordSearch
        custSearch = frmCustomizeKeywordSearch.create(self)
        custSearch.Show()

    def OnListKeywordListLeftUp(self, event):
        event.Skip()

    def OnListKeywordListListItemSelected(self, event):
        event.Skip()


    
    
