#-----------------------------------------------------------------------------
# Name:        MDIChildFileList.py
# Purpose:     
#
# Author:      Ram Basnet
#
# Created:     2007/11/01
# Modified:    6/30/2009
# RCS-ID:      $Id: MDIChildFileList.py,v 1.11 2007/11/15 07:56:38 rbasnet Exp $
# Copyright:   (c) 2007
# Licence:     All Rights Reserved.
# New field:   Whatever
#-----------------------------------------------------------------------------

import wx, sys, os, os.path
import shutil
import wx.lib.buttons
from wx.lib.anchors import LayoutAnchors
import  wx.lib.mixins.listctrl  as  listmix
#from wx.lib.mixins.listctrl import CheckListCtrlMixin

from SqliteDatabase import *
import Globals
import PlatformMethods
import CommonFunctions
import Constants

import  images
from DirectoryTreeView import *
from FileCategoryView import *

def create(parent):
    return MDIChildFileList(parent)

#class CustomListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
class CustomListCtrl(wx.ListCtrl, listmix.CheckListCtrlMixin):
    def __init__(self, parent, ID, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        #listmix.ListCtrlAutoWidthMixin.__init__(self)
        listmix.CheckListCtrlMixin.__init__(self)
        
        
[wxID_MDICHILDFILELIST, wxID_MDICHILDFILELISTBTNCATEGORYVIEW, 
 wxID_MDICHILDFILELISTBTNCLOSE, wxID_MDICHILDFILELISTBTNDIRTREEVIEW, 
 wxID_MDICHILDFILELISTBTNEXPORTMARKEDFILES, wxID_MDICHILDFILELISTIMGFOLDER, 
 wxID_MDICHILDFILELISTLBLDIRECTORYNAME, wxID_MDICHILDFILELISTLBLFILECOUNT, 
 wxID_MDICHILDFILELISTLISTFILESICONS, wxID_MDICHILDFILELISTPANFILELIST, 
 wxID_MDICHILDFILELISTPANPROJPROPERTIES, wxID_MDICHILDFILELISTPANTREE, 
 wxID_MDICHILDFILELISTSPLITTERWINFILELIST, wxID_MDICHILDFILELISTSTATICTEXT1, 
 wxID_MDICHILDFILELISTSTATICTEXTPAGE, wxID_MDICHILDFILELISTTREECATLIST, 
 wxID_MDICHILDFILELISTTREEDIRLIST, 
] = [wx.NewId() for _init_ctrls in range(17)]

[wxID_MDICHILDFILELISTPOPUPMENUDIRMARK_FILES_FOR_EXPORT, 
 wxID_MDICHILDFILELISTPOPUPMENUDIRMD5HASHCHILDREN, 
 wxID_MDICHILDFILELISTPOPUPMENUDIRMD5HASHSELECTED, 
 wxID_MDICHILDFILELISTPOPUPMENUDIRUNMARK_ALL_FILES_FOR_EXPORT, 
] = [wx.NewId() for _init_coll_popupMenuDir_Items in range(4)]

[wxID_MDICHILDFILELISTPOPUPMENUFILEGENMD5FILES, 
 wxID_MDICHILDFILELISTPOPUPMENUFILEGENSHA, 
 wxID_MDICHILDFILELISTPOPUPMENUFILEMARK_FOR_EXPORT, 
 wxID_MDICHILDFILELISTPOPUPMENUFILEMENUITEMOPENFILE, 
 wxID_MDICHILDFILELISTPOPUPMENUFILEMENUITEMVIEWFILE, 
 wxID_MDICHILDFILELISTPOPUPMENUFILEUNMARK_FOR_EXPORT, 
] = [wx.NewId() for _init_coll_popupMenuFile_Items in range(6)]

[wxID_MDICHILDFILELISTPOPUPMENUSHASHA1DIGEST, 
 wxID_MDICHILDFILELISTPOPUPMENUSHASHA224DIGEST, 
 wxID_MDICHILDFILELISTPOPUPMENUSHASHA256DIGEST, 
 wxID_MDICHILDFILELISTPOPUPMENUSHASHA384DIGEST, 
 wxID_MDICHILDFILELISTPOPUPMENUSHASHA512DIGEST, 
] = [wx.NewId() for _init_coll_popupMenuSHA_Items in range(5)]

[wxID_MDICHILDFILELISTPOPUPMENUCATEGORYMARK_FILES_FOR_EXPORT, 
 wxID_MDICHILDFILELISTPOPUPMENUCATEGORYMD5HASHCHILDREN, 
 wxID_MDICHILDFILELISTPOPUPMENUCATEGORYMD5HASHSELECTED, 
 wxID_MDICHILDFILELISTPOPUPMENUCATEGORYUNMARK_ALL_FILES_FOR_EXPORT, 
] = [wx.NewId() for _init_coll_popupMenuCategory_Items in range(4)]

class MDIChildFileList(wx.MDIChildFrame, listmix.ColumnSorterMixin):

    def _init_coll_popupMenuCategory_Items(self, parent):
        # generated method, don't edit

        parent.Append(help='',
              id=wxID_MDICHILDFILELISTPOPUPMENUCATEGORYMARK_FILES_FOR_EXPORT,
              kind=wx.ITEM_NORMAL, text='Mark All Files for Export')
        parent.Append(help='',
              id=wxID_MDICHILDFILELISTPOPUPMENUCATEGORYUNMARK_ALL_FILES_FOR_EXPORT,
              kind=wx.ITEM_NORMAL, text='Unmark All Files for Export')
        parent.AppendSeparator()
        parent.Append(help='',
              id=wxID_MDICHILDFILELISTPOPUPMENUCATEGORYMD5HASHSELECTED,
              kind=wx.ITEM_NORMAL,
              text=u'Generate MD5 Hash of Selected Folder')
        parent.Append(help='',
              id=wxID_MDICHILDFILELISTPOPUPMENUCATEGORYMD5HASHCHILDREN,
              kind=wx.ITEM_NORMAL, text=u'Generate MD5 Hash Recursively')
        self.Bind(wx.EVT_MENU, self.OnPopupMenuCategoryMd5hashselectedMenu,
              id=wxID_MDICHILDFILELISTPOPUPMENUCATEGORYMD5HASHSELECTED)
        self.Bind(wx.EVT_MENU, self.OnPopupMenuCategoryMd5hashchildrenMenu,
              id=wxID_MDICHILDFILELISTPOPUPMENUCATEGORYMD5HASHCHILDREN)
        self.Bind(wx.EVT_MENU,
              self.OnPopupMenuCategoryMark_files_for_exportMenu,
              id=wxID_MDICHILDFILELISTPOPUPMENUCATEGORYMARK_FILES_FOR_EXPORT)
        self.Bind(wx.EVT_MENU,
              self.OnPopupMenuCategoryUnmark_all_files_for_exportMenu,
              id=wxID_MDICHILDFILELISTPOPUPMENUCATEGORYUNMARK_ALL_FILES_FOR_EXPORT)

    def _init_coll_popupMenuFile_Items(self, parent):
        # generated method, don't edit

        parent.Append(help='',
              id=wxID_MDICHILDFILELISTPOPUPMENUFILEMENUITEMVIEWFILE,
              kind=wx.ITEM_NORMAL, text=u'Open File in Hex Viewer')
        parent.Append(help='',
              id=wxID_MDICHILDFILELISTPOPUPMENUFILEMENUITEMOPENFILE,
              kind=wx.ITEM_NORMAL, text=u'Open File in Native Viewer')
        parent.AppendSeparator()
        parent.Append(help='',
              id=wxID_MDICHILDFILELISTPOPUPMENUFILEMARK_FOR_EXPORT,
              kind=wx.ITEM_NORMAL, text='Mark for Export')
        parent.Append(help='',
              id=wxID_MDICHILDFILELISTPOPUPMENUFILEUNMARK_FOR_EXPORT,
              kind=wx.ITEM_NORMAL, text='Unmark for Export')
        parent.AppendSeparator()
        parent.Append(help='', id=wxID_MDICHILDFILELISTPOPUPMENUFILEGENMD5FILES,
              kind=wx.ITEM_NORMAL, text=u'Generate MD5 Hash')
        parent.AppendMenu(help='', id=wxID_MDICHILDFILELISTPOPUPMENUFILEGENSHA,
              submenu=self.popupMenuSHA, text='Generate SHA Hashs')
        self.Bind(wx.EVT_MENU, self.OnPopupMenuFileGenmd5filesMenu,
              id=wxID_MDICHILDFILELISTPOPUPMENUFILEGENMD5FILES)
        self.Bind(wx.EVT_MENU, self.OnPopupMenuFileMenuitemopenfileMenu,
              id=wxID_MDICHILDFILELISTPOPUPMENUFILEMENUITEMOPENFILE)
        self.Bind(wx.EVT_MENU, self.OnPopupMenuFileMenuitemviewfileMenu,
              id=wxID_MDICHILDFILELISTPOPUPMENUFILEMENUITEMVIEWFILE)
        self.Bind(wx.EVT_MENU, self.OnPopupMenuFileGensha1Menu,
              id=wxID_MDICHILDFILELISTPOPUPMENUFILEGENSHA)
        self.Bind(wx.EVT_MENU, self.OnPopupMenuFileMark_for_exportMenu,
              id=wxID_MDICHILDFILELISTPOPUPMENUFILEMARK_FOR_EXPORT)
        self.Bind(wx.EVT_MENU, self.OnPopupMenuFileUnmark_for_exportMenu,
              id=wxID_MDICHILDFILELISTPOPUPMENUFILEUNMARK_FOR_EXPORT)

    def _init_coll_popupMenuSHA_Items(self, parent):
        # generated method, don't edit

        parent.Append(help='', id=wxID_MDICHILDFILELISTPOPUPMENUSHASHA1DIGEST,
              kind=wx.ITEM_NORMAL, text='SHA1 Hash')
        parent.Append(help='', id=wxID_MDICHILDFILELISTPOPUPMENUSHASHA224DIGEST,
              kind=wx.ITEM_NORMAL, text='SHA224 Hash')
        parent.Append(help='', id=wxID_MDICHILDFILELISTPOPUPMENUSHASHA256DIGEST,
              kind=wx.ITEM_NORMAL, text='SHA256 Hash')
        parent.Append(help='', id=wxID_MDICHILDFILELISTPOPUPMENUSHASHA384DIGEST,
              kind=wx.ITEM_NORMAL, text='SHA384 Hash')
        parent.Append(help='', id=wxID_MDICHILDFILELISTPOPUPMENUSHASHA512DIGEST,
              kind=wx.ITEM_NORMAL, text='SHA512 Hash')
        self.Bind(wx.EVT_MENU, self.OnPopupMenuSHASha1digestMenu,
              id=wxID_MDICHILDFILELISTPOPUPMENUSHASHA1DIGEST)
        self.Bind(wx.EVT_MENU, self.OnPopupMenuSHASha224digestMenu,
              id=wxID_MDICHILDFILELISTPOPUPMENUSHASHA224DIGEST)
        self.Bind(wx.EVT_MENU, self.OnPopupMenuSHASha256digestMenu,
              id=wxID_MDICHILDFILELISTPOPUPMENUSHASHA256DIGEST)
        self.Bind(wx.EVT_MENU, self.OnPopupMenuSHASha384digestMenu,
              id=wxID_MDICHILDFILELISTPOPUPMENUSHASHA384DIGEST)
        self.Bind(wx.EVT_MENU, self.OnPopupMenuSHASha512digestMenu,
              id=wxID_MDICHILDFILELISTPOPUPMENUSHASHA512DIGEST)

    def _init_coll_popupMenuDir_Items(self, parent):
        # generated method, don't edit

        parent.Append(help='',
              id=wxID_MDICHILDFILELISTPOPUPMENUDIRMARK_FILES_FOR_EXPORT,
              kind=wx.ITEM_NORMAL, text='Mark All Files for Export')
        parent.Append(help='',
              id=wxID_MDICHILDFILELISTPOPUPMENUDIRUNMARK_ALL_FILES_FOR_EXPORT,
              kind=wx.ITEM_NORMAL, text='Unmark All Files for Export')
        parent.AppendSeparator()
        parent.Append(help='',
              id=wxID_MDICHILDFILELISTPOPUPMENUDIRMD5HASHSELECTED,
              kind=wx.ITEM_NORMAL,
              text=u'Generate MD5 Hash of Selected Folder')
        parent.Append(help='',
              id=wxID_MDICHILDFILELISTPOPUPMENUDIRMD5HASHCHILDREN,
              kind=wx.ITEM_NORMAL, text=u'Generate MD5 Hash Recursively')
        self.Bind(wx.EVT_MENU, self.OnPopupMenuDirMd5hashselectedMenu,
              id=wxID_MDICHILDFILELISTPOPUPMENUDIRMD5HASHSELECTED)
        self.Bind(wx.EVT_MENU, self.OnPopupMenuDirMd5hashchildrenMenu,
              id=wxID_MDICHILDFILELISTPOPUPMENUDIRMD5HASHCHILDREN)
        self.Bind(wx.EVT_MENU, self.OnPopupMenuDirMark_files_for_exportMenu,
              id=wxID_MDICHILDFILELISTPOPUPMENUDIRMARK_FILES_FOR_EXPORT)
        self.Bind(wx.EVT_MENU,
              self.OnPopupMenuDirUnmark_all_files_for_exportMenu,
              id=wxID_MDICHILDFILELISTPOPUPMENUDIRUNMARK_ALL_FILES_FOR_EXPORT)

    def _init_utils(self):
        # generated method, don't edit
        self.popupMenuDir = wx.Menu(title='')

        self.popupMenuFile = wx.Menu(title='')

        self.popupMenuSHA = wx.Menu(title='')

        self.popupMenuCategory = wx.Menu(title='')

        self._init_coll_popupMenuDir_Items(self.popupMenuDir)
        self._init_coll_popupMenuFile_Items(self.popupMenuFile)
        self._init_coll_popupMenuSHA_Items(self.popupMenuSHA)
        self._init_coll_popupMenuCategory_Items(self.popupMenuCategory)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.MDIChildFrame.__init__(self, id=wxID_MDICHILDFILELIST,
              name=u'MDIChildFileList', parent=prnt, pos=wx.Point(134, 196),
              size=wx.Size(1048, 714), style=wx.DEFAULT_FRAME_STYLE,
              title='File Explorer')
        self._init_utils()
        self.SetClientSize(wx.Size(1040, 680))
        self.SetBackgroundColour(wx.Colour(125, 152, 221))
        self.SetAutoLayout(True)

        self.splitterWinFileList = wx.SplitterWindow(id=wxID_MDICHILDFILELISTSPLITTERWINFILELIST,
              name=u'splitterWinFileList', parent=self, pos=wx.Point(4, 4),
              size=wx.Size(1032, 672), style=wx.SP_3D)
        self.splitterWinFileList.SetMinimumPaneSize(20)
        self.splitterWinFileList.SetAutoLayout(False)
        self.splitterWinFileList.SetConstraints(LayoutAnchors(self.splitterWinFileList,
              True, True, True, True))

        self.panFileList = wx.Panel(id=wxID_MDICHILDFILELISTPANFILELIST,
              name=u'panFileList', parent=self.splitterWinFileList,
              pos=wx.Point(204, 0), size=wx.Size(828, 672),
              style=wx.TAB_TRAVERSAL)
        self.panFileList.SetBackgroundColour(wx.Colour(225, 236, 255))
        self.panFileList.SetAutoLayout(True)

        self.imgFolder = wx.StaticBitmap(bitmap=wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN,
              wx.ART_OTHER, (24, 24)), id=wxID_MDICHILDFILELISTIMGFOLDER,
              name=u'imgFolder', parent=self.panFileList, pos=wx.Point(8, 40),
              size=wx.Size(24, 24), style=0)
        self.imgFolder.SetConstraints(LayoutAnchors(self.imgFolder, True, True,
              False, False))

        self.lblDirectoryName = wx.StaticText(id=wxID_MDICHILDFILELISTLBLDIRECTORYNAME,
              label=u'Dir Name', name=u'lblDirectoryName',
              parent=self.panFileList, pos=wx.Point(40, 48), size=wx.Size(51,
              13), style=0)
        self.lblDirectoryName.SetForegroundColour(wx.Colour(0, 0, 187))
        self.lblDirectoryName.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, u'Tahoma'))
        self.lblDirectoryName.SetConstraints(LayoutAnchors(self.lblDirectoryName,
              True, True, True, False))

        self.panTree = wx.Panel(id=wxID_MDICHILDFILELISTPANTREE,
              name=u'panTree', parent=self.splitterWinFileList, pos=wx.Point(0,
              0), size=wx.Size(200, 672), style=wx.TAB_TRAVERSAL)
        self.panTree.SetAutoLayout(True)
        self.panTree.SetBackgroundColour(wx.Colour(225, 236, 255))
        self.splitterWinFileList.SplitVertically(self.panTree, self.panFileList,
              200)

        self.btnClose = wx.Button(id=wxID_MDICHILDFILELISTBTNCLOSE,
              label=u'Close', name=u'btnClose', parent=self.panFileList,
              pos=wx.Point(741, 8), size=wx.Size(75, 23), style=0)
        self.btnClose.SetConstraints(LayoutAnchors(self.btnClose, False, True,
              True, False))
        self.btnClose.Bind(wx.EVT_BUTTON, self.OnBtnCloseButton,
              id=wxID_MDICHILDFILELISTBTNCLOSE)

        self.panProjProperties = wx.Panel(id=wxID_MDICHILDFILELISTPANPROJPROPERTIES,
              name=u'panProjProperties', parent=self.panTree, pos=wx.Point(8,
              8), size=wx.Size(184, 40), style=wx.TAB_TRAVERSAL)
        self.panProjProperties.SetBackgroundColour(wx.Colour(225, 225, 255))
        self.panProjProperties.SetConstraints(LayoutAnchors(self.panProjProperties,
              True, True, True, False))
        self.panProjProperties.Show(True)

        self.btnDirTreeView = wx.lib.buttons.GenToggleButton(id=wxID_MDICHILDFILELISTBTNDIRTREEVIEW,
              label='Folder View', name=u'btnDirTreeView',
              parent=self.panProjProperties, pos=wx.Point(8, 8),
              size=wx.Size(80, 25), style=0)
        self.btnDirTreeView.SetToggle(True)
        self.btnDirTreeView.SetToolTipString(u'Directory Tree View')
        self.btnDirTreeView.Enable(False)
        self.btnDirTreeView.Bind(wx.EVT_BUTTON, self.OnBtnDirTreeViewButton,
              id=wxID_MDICHILDFILELISTBTNDIRTREEVIEW)

        self.btnCategoryView = wx.lib.buttons.GenToggleButton(id=wxID_MDICHILDFILELISTBTNCATEGORYVIEW,
              label=u'Category View', name=u'btnCategoryView',
              parent=self.panProjProperties, pos=wx.Point(96, 8),
              size=wx.Size(80, 25), style=0)
        self.btnCategoryView.SetToggle(False)
        self.btnCategoryView.SetToolTipString(u'File Carved Category View')
        self.btnCategoryView.Bind(wx.EVT_BUTTON, self.OnBtnCategoryViewButton,
              id=wxID_MDICHILDFILELISTBTNCATEGORYVIEW)

        self.treeCatList = wx.TreeCtrl(id=wxID_MDICHILDFILELISTTREECATLIST,
              name=u'treeCatList', parent=self.panTree, pos=wx.Point(8, 56),
              size=wx.Size(184, 608),
              style=wx.HSCROLL | wx.VSCROLL | wx.TR_HAS_BUTTONS)
        self.treeCatList.SetConstraints(LayoutAnchors(self.treeCatList, True,
              True, True, True))
        self.treeCatList.Show(False)
        self.treeCatList.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, 'Tahoma'))
        self.treeCatList.Bind(wx.EVT_TREE_SEL_CHANGED,
              self.OnTreeCatListTreeSelChanged,
              id=wxID_MDICHILDFILELISTTREECATLIST)
        self.treeCatList.Bind(wx.EVT_CONTEXT_MENU, self.OnTreeCatListRightUp)

        self.treeDirList = wx.TreeCtrl(id=wxID_MDICHILDFILELISTTREEDIRLIST,
              name=u'treeDirList', parent=self.panTree, pos=wx.Point(8, 56),
              size=wx.Size(184, 608),
              style=wx.HSCROLL | wx.VSCROLL | wx.TR_HAS_BUTTONS)
        self.treeDirList.SetConstraints(LayoutAnchors(self.treeDirList, True,
              True, True, True))
        self.treeDirList.Show(True)
        self.treeDirList.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, u'Tahoma'))
        self.treeDirList.Bind(wx.EVT_TREE_SEL_CHANGED,
              self.OnTreeDirListTreeSelChanged,
              id=wxID_MDICHILDFILELISTTREEDIRLIST)
        self.treeDirList.Bind(wx.EVT_CONTEXT_MENU, self.OnTreeDirListRightUp)

        self.staticTextPage = wx.StaticText(id=wxID_MDICHILDFILELISTSTATICTEXTPAGE,
              label='Page', name='staticTextPage', parent=self.panFileList,
              pos=wx.Point(16, 72), size=wx.Size(28, 13), style=0)
        self.staticTextPage.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, 'Tahoma'))

        self.listFilesIcons = wx.ListCtrl(id=wxID_MDICHILDFILELISTLISTFILESICONS,
              name=u'listFilesIcons', parent=self.panFileList, pos=wx.Point(8,
              96), size=wx.Size(808, 566),
              style=wx.LC_AUTOARRANGE | wx.LC_ICON)
        self.listFilesIcons.Show(False)
        self.listFilesIcons.SetConstraints(LayoutAnchors(self.listFilesIcons,
              True, True, True, True))
        self.listFilesIcons.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, 'Tahoma'))
        self.listFilesIcons.Bind(wx.EVT_LEFT_DCLICK,
              self.OnListFilesIconsLeftDclick)
        self.listFilesIcons.Bind(wx.EVT_CONTEXT_MENU,
              self.OnListFilesIconsRightUp)

        self.lblFileCount = wx.StaticText(id=wxID_MDICHILDFILELISTLBLFILECOUNT,
              label='of 0:  Showing 0 File', name='lblFileCount',
              parent=self.panFileList, pos=wx.Point(136, 72), size=wx.Size(109,
              13), style=0)
        self.lblFileCount.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, 'Tahoma'))

        self.staticText1 = wx.StaticText(id=wxID_MDICHILDFILELISTSTATICTEXT1,
              label='All or part of file name:', name='staticText1',
              parent=self.panFileList, pos=wx.Point(421, 72), size=wx.Size(110,
              13), style=0)
        self.staticText1.SetConstraints(LayoutAnchors(self.staticText1, False,
              True, True, False))

        self.btnExportMarkedFiles = wx.Button(id=wxID_MDICHILDFILELISTBTNEXPORTMARKEDFILES,
              label='Export Marked (100000) Files', name='btnExportMarkedFiles',
              parent=self.panFileList, pos=wx.Point(565, 8), size=wx.Size(163,
              23), style=0)
        self.btnExportMarkedFiles.SetConstraints(LayoutAnchors(self.btnExportMarkedFiles,
              False, True, True, False))
        self.btnExportMarkedFiles.Bind(wx.EVT_BUTTON,
              self.OnBtnExportMarkedFilesButton,
              id=wxID_MDICHILDFILELISTBTNEXPORTMARKEDFILES)

    def __init__(self, parent):
        self._init_ctrls(parent)
        self.SetIcon(images.getMAKE2Icon())
        
        #to avoid the nasty icon not found error...ha finally found a fix for it... =)
        #wx.Log_SetActiveTarget(wx.LogStderr())
        wx.BeginBusyCursor()
        self.FileInfo = {}
        self.dirPath = ""
        self.newDirPath = ""
        #self.lblDirectoryName.SetLabel(PlatformMethods.Decode(self.dirPath))
        self.CreateListControl()
        self.treeDirView = True
        self.FileList = []
        #if len(Globals.FileInfoList) > 1:
            #if Globals.fileTreeView is None:
            #Globals.fileTreeView = FileTreeView(self, self.treeDirList)
        self.fileTreeView = DirectoryTreeView(self, self.treeDirList, Globals.EvidencesDict)
        self.treeDirList.Show(True)
        self.TreeViewRoot = self.fileTreeView.AddDirectories()
        self.root = self.TreeViewRoot
        self.CategoryViewRoot = None
        self.CreatePageSelection()
        self.CreateSearchControl()
        self.TotalPages = 0
        self.TotalFiles = 0
        self.UpdateExportButtonLabel()
        #self.CreateTreeControl()
        wx.EndBusyCursor()
        
    def CreateSearchControl(self):
        self.search = wx.SearchCtrl(self.panFileList, pos=wx.Point(544, 72), size=(264, -1), style=wx.TE_PROCESS_ENTER)
        self.search.SetConstraints(LayoutAnchors(self.search, False, True,
              True, False))
        self.search.ShowSearchButton(True)
        self.search.ShowCancelButton(True)
        
        self.SearchMenu = wx.Menu()
        item = self.SearchMenu.Append(-1, "Recent Searches")
        item.Enable(False)
        
        self.search.SetMenu(self.SearchMenu)
        
        self.Bind(wx.EVT_SEARCHCTRL_SEARCH_BTN, self.OnSearch, self.search)
        self.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, self.OnSearchCancel, self.search)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnDoSearch, self.search)
        
        """
        self.textCtrl1 = wx.TextCtrl(id=wxID_MDICHILDFILELISTTEXTCTRL1,
              name='textCtrl1', parent=self.panFileList, pos=wx.Point(544, 40),
              size=wx.Size(264, 21), style=0, value='textCtrl1')
        self.textCtrl1.SetConstraints(LayoutAnchors(self.textCtrl1, False, True,
              True, False))
        """
        
        
    def OnSearch(self, event):
        event.Skip()
            
    def OnSearchCancel(self, event):
        event.Skip()

    def OnDoSearch(self, event):
        busy = wx.BusyInfo("Searching Database...")
        wx.Yield()
        self.SearchFiles()
        self.AddFileDetailsToListView(searchResult=True)
        event.Skip()
        
    def SearchFiles(self):
        searchName = self.search.GetValue()
        if not searchName:
            return 
        
        db = SqliteDatabase(Globals.FileSystemName)
        if not db.OpenConnection():
            return
        
        #if  Globals.frmGlobalMainForm.GetViewsCheckedMenu() == 'Details':
        self.listFilesDetails.Show(True)
        self.listFilesIcons.Show(False)
                
        query = ""

        if searchName.find('*.') == 0:
            searchVal = searchName[searchName.find('*')+1:]
            query = """select Name, DirPath, Size, Created, Modified, Accessed, Category, MimeType, 
                Description, MD5,  KnownFile, NewPath, SHA1, SHA224, SHA256, SHA384, SHA512
                from %s where Name like '%s'"""%(Globals.CurrentEvidenceID, "%"+searchVal)
            
        else:
            query = """select Name, DirPath, Size, Created, Modified, Accessed, Category, MimeType, 
                Description, MD5,  KnownFile, NewPath, SHA1, SHA224, SHA256, SHA384, SHA512
                from %s where Name like '%s'"""%(Globals.CurrentEvidenceID, "%"+searchName+"%")
                
        self.FileList = db.FetchAllRows(query)
        self.TotalFiles = len(self.FileList)
        self.TotalPages = 1
        self.AddPageNumbersToChoice(self.TotalPages)
        self.choicePageNum.SetSelection(0)
            
        if self.SearchMenu.FindItem(searchName) < 0:
            id = wx.NewId()
            self.SearchMenu.Append(id, searchName)
            self.Bind(wx.EVT_MENU, self.OnSearchFromSearchMenu, id=id)

    def OnSearchFromSearchMenu(self, event):
        id = event.GetId()
        searchWords = self.SearchMenu.GetLabel(id)
        self.search.SetValue(searchWords)
        self.OnDoSearch(event)
        
        
    def CreatePageSelection(self):
        choiceId = wx.NewId()
        self.choicePageNum = wx.Choice(choices=[],
            id=choiceId, name='choicePageNum',
            parent=self.panFileList, pos=wx.Point(56, 72), size=wx.Size(64,
            21), style=0)
        self.choicePageNum.Bind(wx.EVT_CHOICE, self.OnChoicePageNumChoice,
          id=choiceId)
        #self.choicePageNum.SetSelection(0)
        
    def AddPageNumbersToChoice(self, pages):
        self.choicePageNum.Clear()
        for page in range(1, pages+1):
            self.choicePageNum.Append(str(page))
        
    def CreateTreeControl(self):
        self.treeDirList = Globals.fileTreeView
        self.treeDirList.Show(True)
        self.root = Globals.fileTreeView.GetRoot()

        
    def ShowDirectoryTreeView(self):
        #self.ShowProjectProperties(True)
        self.notebookProject.Show(True)
        
    
    def CreateListControl(self):
        listID = wx.NewId()
        self.listFilesDetails = CustomListCtrl(self.panFileList, listID,
                                 pos=wx.Point(8, 96), size=wx.Size(808, 566),
                                 style=wx.LC_REPORT 
                                 | wx.BORDER_NONE
                                 | wx.LC_SORT_ASCENDING
                                 )
        
        self.listFilesDetails.SetConstraints(LayoutAnchors(self.listFilesDetails, True,
              True, True, True))
        self.listFilesDetails.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, u'Tahoma'))
              
        # Now that the list exists we can init the other base class,
        # see wx/lib/mixins/listctrl.py
        listmix.ColumnSorterMixin.__init__(self, 14)
        
        self.Bind(wx.EVT_LIST_COL_CLICK, self.OnListColClick, self.listFilesDetails)
        self.listFilesDetails.Bind(wx.EVT_LEFT_DCLICK, self.OnListFilesDoubleClick)
        self.listFilesDetails.Bind(wx.EVT_CONTEXT_MENU, self.OnListFilesDetailsRightUp)
        self.imageListSmallIcon = None
        self.imageListSmallIcon = wx.ImageList(16, 16)
        #IconDict = {}
        #tbd: get file specific icon and display
        #self.idx1 = self.imageListSmallIcon.Add(images.getSmilesBitmap())
        self.sm_up = self.imageListSmallIcon.Add(images.getSmallUpArrowBitmap())
        self.sm_dn = self.imageListSmallIcon.Add(images.getSmallDnArrowBitmap())
        self.AddListColumnHeadings()
       
    def AddListColumnHeadings(self, searchResult=False):
        #want to add images on the column header..
        info = wx.ListItem()
        info.m_mask = wx.LIST_MASK_TEXT | wx.LIST_MASK_IMAGE | wx.LIST_MASK_FORMAT
        info.m_image = -1
        info.m_format = 0
        #info.m_text = "dabc"
        #self.listFilesDetails.InsertColumnInfo(0, info)
        
        info.m_text = "Name"
        self.listFilesDetails.InsertColumnInfo(0, info)
        
        index = 1
        if searchResult:
            info.m_text = "In Folder"
            self.listFilesDetails.InsertColumnInfo(index, info)
            index += 1
            
        info.m_format = wx.LIST_FORMAT_LEFT
        info.m_text = "Size"
        self.listFilesDetails.InsertColumnInfo(index, info)
        
        index += 1
        info.m_format = wx.LIST_FORMAT_LEFT
        info.m_text = "Created Time"
        self.listFilesDetails.InsertColumnInfo(index, info)
        
        index += 1
        info.m_text = "Modified Time"
        self.listFilesDetails.InsertColumnInfo(index, info)
        
        index += 1
        info.m_text = "Accessed Time"
        self.listFilesDetails.InsertColumnInfo(index, info)
        
        index += 1
        info.m_text = "Category"
        self.listFilesDetails.InsertColumnInfo(index, info)
        
        index += 1
        info.m_text = "File Type"
        self.listFilesDetails.InsertColumnInfo(index, info)
        
        index += 1
        info.m_text = "Description"
        self.listFilesDetails.InsertColumnInfo(index, info)
        
        index += 1
        info.m_text = "MD5 Hash"
        self.listFilesDetails.InsertColumnInfo(index, info)
        
        index += 1
        info.m_text = "Known"
        self.listFilesDetails.InsertColumnInfo(index, info)
        
        index += 1
        info.m_text = "Export"
        self.listFilesDetails.InsertColumnInfo(index, info)
        
        index += 1
        info.m_text = "Unzipped Path"
        self.listFilesDetails.InsertColumnInfo(index, info)
        
        
        index += 1
        info.m_text = "SHA1 Hash"
        self.listFilesDetails.InsertColumnInfo(index, info)
        
        index += 1
        info.m_text = "SHA224 Hash"
        self.listFilesDetails.InsertColumnInfo(index, info)
        
        index += 1
        info.m_text = "SHA256 Hash"
        self.listFilesDetails.InsertColumnInfo(index, info)
        
        index += 1
        info.m_text = "SHA384 Hash"
        self.listFilesDetails.InsertColumnInfo(index, info)
        
        index += 1
        info.m_text = "SHA512 Hash"
        self.listFilesDetails.InsertColumnInfo(index, info)
    
    def AddFileDetailsToListView(self, searchResult=False):
        #self.treeDirView = treeDirView
        #self.dirPath = dirPath
        self.SetCursor(wx.HOURGLASS_CURSOR)
        self.FileInfo = {}
        #if searchResult:
        self.listFilesDetails.ClearAll()
        self.AddListColumnHeadings(searchResult)
            
        #self.listFilesDetails.DeleteAllItems()
        totalFiles = 0
        #iconInfo = {}

        IconDict = {}
        NoLog = wx.LogNull()
        for fileInfoList in self.FileList:

            totalFiles += 1
            #print "totalFiles = " + str(totalFiles)
            listItem = []
            if self.treeDirView:
                listItem.append(PlatformMethods.Decode(fileInfoList[0]))
                if searchResult:
                    listItem.append(PlatformMethods.Decode(fileInfoList[1]))
            else:
                fullFilePath = os.path.join(PlatformMethods.Decode(fileInfoList[1]), PlatformMethods.Decode(fileInfoList[0]))
                if Globals.EvidencesDict[Globals.CurrentEvidenceID]['NewLocation']:
                    fullFilePath = fullFilePath.replace(Globals.EvidencesDict[Globals.CurrentEvidenceID]['Location'], Globals.EvidencesDict[Globals.CurrentEvidenceID]['NewLocation'])
                    
                listItem.append(fullFilePath)
                
            listItem.append(CommonFunctions.ConvertByteToKilobyte(fileInfoList[2]))
            listItem.append(CommonFunctions.GetShortDateTime(fileInfoList[3]))
            listItem.append(CommonFunctions.GetShortDateTime(fileInfoList[4]))
            listItem.append(CommonFunctions.GetShortDateTime(fileInfoList[5]))
            listItem.append(PlatformMethods.Decode(fileInfoList[6]))
            listItem.append(PlatformMethods.Decode(fileInfoList[7]))
            listItem.append(PlatformMethods.Decode(fileInfoList[8]))
            listItem.append(fileInfoList[9])
            try:
                if fileInfoList[10] == 1:
                    listItem.append('Yes')
                else:
                    listItem.append('No')
            except:
                listItem.append('No')
            
            try:
                if fileInfoList[17] == 1:
                    listItem.append('Yes')
                else:
                    listItem.append('No')
            except:
                listItem.append('No')
            
            newPath = fileInfoList[11]
            #print Globals.CasePath
            #print newPath
            if newPath:
                newPath = PlatformMethods.Decode(os.path.join(Globals.CasePath, newPath))
            
            #print newPath
            listItem.append(newPath)
            
            listItem.append(PlatformMethods.Decode(fileInfoList[12]))
            listItem.append(PlatformMethods.Decode(fileInfoList[13]))
            listItem.append(PlatformMethods.Decode(fileInfoList[14]))
            listItem.append(PlatformMethods.Decode(fileInfoList[15]))
            listItem.append(PlatformMethods.Decode(fileInfoList[16]))
            #self.listFilesDetails.Append(listItem)
            #print listItem
            self.FileInfo[totalFiles] = tuple(listItem)
            #print self.FileInfo
            iconFound = False
            if not (fileInfoList[0].rfind('.') == -1):
                fileExtension = fileInfoList[0][fileInfoList[0].rfind('.'):]
                #try:
                fileType = wx.TheMimeTypesManager.GetFileTypeFromExtension(fileExtension)

                if fileType:
                    info = fileType.GetIconInfo()

                    if info:
                        icon, file, idx = info
                        #print icon
                        if icon.Ok():
                            #iconInfo[totalFiles] = icon
                            #bmp = wx.Image(opj('bitmaps/image.bmp'), wx.BITMAP_TYPE_BMP).ConvertToBitmap()
                            icon.SetSize(wx.Size(16, 16))
                            IconDict[totalFiles] = self.imageListSmallIcon.AddIcon(icon)
                            iconFound = True
                    
                        
            if not iconFound:
                bmp = images.getNoFile16Icon()
                IconDict[totalFiles] = self.imageListSmallIcon.AddIcon(bmp)

                
        self.listFilesDetails.SetImageList(self.imageListSmallIcon, wx.IMAGE_LIST_SMALL)
        #self.CreateFileIconList(iconInfo)
        self.itemDataMap = self.FileInfo       
        items = self.FileInfo.items()
        #print items
        #print len(self.FileInfo)
        #print len(items)
        NoLog = None
        for key, data in items:
            #print str(key) + str(data)
            #try:
            index = self.listFilesDetails.InsertImageStringItem(sys.maxint, data[0], IconDict[key])
            self.listFilesDetails.SetStringItem(index, 1, data[1])
            self.listFilesDetails.SetStringItem(index, 2, data[2])
            self.listFilesDetails.SetStringItem(index, 3, data[3])
            self.listFilesDetails.SetStringItem(index, 4, data[4])
            self.listFilesDetails.SetStringItem(index, 5, data[5])
            self.listFilesDetails.SetStringItem(index, 6, data[6])
            self.listFilesDetails.SetStringItem(index, 7, data[7])
            self.listFilesDetails.SetStringItem(index, 8, data[8])
            self.listFilesDetails.SetStringItem(index, 9, data[9])
            self.listFilesDetails.SetStringItem(index, 10, data[10])
            self.listFilesDetails.SetStringItem(index, 11, data[11])
            self.listFilesDetails.SetStringItem(index, 12, data[12])
            self.listFilesDetails.SetStringItem(index, 13, data[13])
            self.listFilesDetails.SetStringItem(index, 14, data[14])
            self.listFilesDetails.SetStringItem(index, 15, data[15])
            self.listFilesDetails.SetStringItem(index, 16, data[16])
            self.listFilesDetails.SetItemData(index, key)
            #except:
            #    continue

           
        self.listFilesDetails.SetColumnWidth(0, 250)
        self.listFilesDetails.SetColumnWidth(1, 50)
        self.listFilesDetails.SetColumnWidth(2, 100)
        self.listFilesDetails.SetColumnWidth(3, 100)
        self.listFilesDetails.SetColumnWidth(4, 100)
        self.listFilesDetails.SetColumnWidth(5, 50)
        self.listFilesDetails.SetColumnWidth(6, 100)
        self.listFilesDetails.SetColumnWidth(7, 100)
        self.listFilesDetails.SetColumnWidth(8, 125)
        value = "File"
        if totalFiles > 1:
            value = "Files"
            
        if searchResult:
            self.lblDirectoryName.SetLabel("Search Results for: %s"%(self.search.GetValue()))
        else:
            self.lblDirectoryName.SetLabel(PlatformMethods.Decode(self.newDirPath))
        self.lblFileCount.SetLabel("of %s:  Showing %s of %s %s"%(CommonFunctions.GetCommaFormattedNumber(self.TotalPages), CommonFunctions.GetCommaFormattedNumber(totalFiles), CommonFunctions.GetCommaFormattedNumber(self.TotalFiles), value))
        self.SetCursor(wx.STANDARD_CURSOR)
    
    
    def UpdateFilesInDirectory(self, offset):
        self.FileList = []
        #print self.dirPath
        if self.treeDirView:
            self.FileList = DBFunctions.GetFileList(Globals.FileSystemName, Globals.CurrentEvidenceID, self.dirPath, offset)
        else:
            self.FileList = DBFunctions.GetFileList(Globals.FileSystemName, Globals.CurrentEvidenceID, self.dirPath, offset, mimeType=True)
        
    def AddFileIconsToListView(self):
        self.SetCursor(wx.HOURGLASS_CURSOR)
        #self.FileInfoDict = {}
        self.listFilesIcons.ClearAll()
        #self.AddListColumnHeadings()
        totalFiles = 0
        #iconInfo = {}
        self.imageListLargeIcon = None
        self.imageListLargeIcon = wx.ImageList(32, 32)
        
        #tbd: get file specific icon and display

        self.listFilesIcons.SetImageList(self.imageListLargeIcon, wx.IMAGE_LIST_NORMAL)
        NoLog = wx.LogNull()
        for fileInfo in self.FileList:
            totalFiles += 1
            #print "totalFiles = " + str(totalFiles)
            #listItem = []
            if self.treeDirView:
                #listItem.append(PlatformMethods.Decode(fileInfo.Name))
                fileName = PlatformMethods.Decode(fileInfo[0])
            else:
                #listItem.append(os.path.join(PlatformMethods.Decode(fileInfo.DirPath), PlatformMethods.Decode(fileInfo.Name)))
                fileName = os.path.join(PlatformMethods.Decode(fileInfo[1]), PlatformMethods.Decode(fileInfo[0]))
                if Globals.EvidencesDict[Globals.CurrentEvidenceID]['NewLocation']:
                    fileName = fileName.replace(Globals.EvidencesDict[Globals.CurrentEvidenceID]['Location'], Globals.EvidencesDict[Globals.CurrentEvidenceID]['NewLocation'])
                    
            iconFound = False
            if not (fileInfo[0].rfind('.') == -1):
                fileExtension = fileInfo[0][fileInfo[0].rfind('.'):]
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
                            icon.SetSize(wx.Size(32, 32))
                            ilMax = self.imageListLargeIcon.AddIcon(icon)
                            iconFound = True
                        
            if not iconFound:
                ilMax = self.imageListLargeIcon.AddIcon(images.getNoFile32Icon())
                    
            self.listFilesIcons.InsertImageStringItem(sys.maxint, fileName, ilMax)
       
        
        NoLog = None
        value = "File"
        if totalFiles > 0:
            value = "Files"
        self.lblDirectoryName.SetLabel(PlatformMethods.Decode(self.newDirPath))
        self.lblFileCount.SetLabel("of %d:  Showing %d of %d %s"%(self.TotalPages, totalFiles, self.TotalFiles, value))
        self.SetCursor(wx.STANDARD_CURSOR)
    
        
    # Used by the ColumnSorterMixin, see wx/lib/mixins/listctrl.py
    def GetListCtrl(self):
        return self.listFilesDetails

    # Used by the ColumnSorterMixin, see wx/lib/mixins/listctrl.py
    def GetSortImages(self):
        return (self.sm_dn, self.sm_up)
    
    def OnListColClick(self, event):
        event.Skip()
          
    def OnBtnCloseButton(self, event):
        self.Close()

    def OnListResultsListColClick(self, event):
        event.Skip()


    def GetFilePath(self, fileName, fullFilePath=""):
        filePath = ""
        self.fileInfo = None
        fileName = PlatformMethods.Encode(fileName)
        fullFilePath = PlatformMethods.Encode(fullFilePath)
        for fileinfo in self.FileList:
            if self.treeDirView:
                if fileinfo[0] == fileName and fileinfo[1] == self.dirPath:
                    if fileinfo[11]:
                        filePath = os.path.join(Globals.CasePath, fileinfo[11])
                        #filePath = os.path.join(Globals.CasePath, fileinfo[11])
                    else:
                        filePath = os.path.join(fileinfo[1], fileinfo[0])
                     
                    self.fileInfo = fileinfo
                    break
                    
            else:
                if os.path.join(fileinfo[1], fileinfo[0]) == fullFilePath:
                    if fileinfo[11]:
                        filePath = os.path.join(Globals.CasePath, fileinfo[11])
                        #filePath = os.path.join(Globals.CasePath, fileinfo[11])
                    else:
                        filePath = os.path.join(fileinfo[1], fileinfo[0])
                        """
                        if Globals.EvidencesDict[Globals.CurrentEvidenceID]['NewLocation']:
                            filePath = filePath.replace(Globals.EvidencesDict[Globals.CurrentEvidenceID]['Location'], Globals.EvidencesDict[Globals.CurrentEvidenceID]['NewLocation'])
                        """
                         
                    self.fileInfo = fileinfo
                    break
                    
        if Globals.EvidencesDict[Globals.CurrentEvidenceID]['NewLocation']:
            filePath = filePath.replace(Globals.EvidencesDict[Globals.CurrentEvidenceID]['Location'], Globals.EvidencesDict[Globals.CurrentEvidenceID]['NewLocation'])
            
        return filePath
         
        
    def IsFileSelected(self):
        if  Globals.frmGlobalMainForm.GetViewsCheckedMenu() == 'Details':
            self.index = self.listFilesDetails.GetFirstSelected()
        else:
            self.index = self.listFilesIcons.GetFirstSelected()
            
        self.fullFilePath = ""
        
        if self.index >=0:
            if self.treeDirView:
                if  Globals.frmGlobalMainForm.GetViewsCheckedMenu() == 'Details':
                    self.selectedFileName = PlatformMethods.Encode(self.listFilesDetails.GetItem(self.index).GetText())
 
                else:
                    self.selectedFileName = PlatformMethods.Encode(self.listFilesIcons.GetItem(self.index).GetText())
                    #self.fullFilePath = os.path.join(PlatformMethods.Decode(self.dirPath), self.selectedFileName) #self.GetFilePath(self.selectedFileName)
                self.fullFilePath = self.GetFilePath(self.selectedFileName)
                
            else:
                if  Globals.frmGlobalMainForm.GetViewsCheckedMenu() == 'Details':
                    fullFilePath = PlatformMethods.Encode(self.listFilesDetails.GetItem(self.index).GetText())
                else:
                    fullFilePath = PlatformMethods.Encode(self.listFilesIcons.GetItem(self.index).GetText())
                    
                if Globals.EvidencesDict[Globals.CurrentEvidenceID]['NewLocation']:
                    fullFilePath = fullFilePath.replace(Globals.EvidencesDict[Globals.CurrentEvidenceID]['NewLocation'], Globals.EvidencesDict[Globals.CurrentEvidenceID]['Location'])
                self.fullFilePath = self.GetFilePath("", fullFilePath)
                
            
        else:
            dlg = wx.MessageDialog(self, 'Please select a file from the list.',
              'Error', wx.OK | wx.ICON_ERROR)
            try:
                dlg.ShowModal()
            finally:
                dlg.Destroy()
                
        return self.fullFilePath
            
            
    def OnListFilesDoubleClick(self, event):
        """
        if self.IsFileSelected():
            self.OpenFile()
        event.Skip()
        """
        self.OnPopupMenuFileMenuitemfilepropertiesMenu(event)
           
    def OpenFile(self):
        try:
            os.startfile(PlatformMethods.Decode(self.fullFilePath))
        except Exception, value:
            CommonFunctions.ShowErrorMessage(self, value, error=True)
            
        """
        fileExtension = self.fullFilePath[self.fullFilePath.rfind('.'):]
        fileType = wx.TheMimeTypesManager.GetFileTypeFromExtension(fileExtension)
        cmd = ""
        if fileType:
            mimeType = fileType.GetMimeType() or ""
            cmd = fileType.GetOpenCommand(self.fullFilePath, mimeType)
            
        if cmd:
            try:
                os.system('start '+cmd)
            except Exception, value:
                CommonFunctions.ShowErrorMessage(self, value)
        else:
            CommonFunctions.ShowErrorMessage(self, "No associated program found for the file!", False)
        """
        
    def GetTreeItemText(self, treeCtrl, item):
        if item:
            return treeCtrl.GetItemText(item)
        else:
            return ""
        
    def GetPathName(self, item, treeCtrl):
        if treeCtrl is self.treeCatList:
            self.newDirPath = self.GetTreeItemText(treeCtrl, item)
            return self.newDirPath
        
        pathName = []
        pathName.append(self.GetTreeItemText(treeCtrl, item))
        #parentItem = self.treeDirList.GetItemParent(item)
        parentItem = treeCtrl.GetItemParent(item)
        while not (parentItem == self.root):
            pathName.insert(0, self.GetTreeItemText(treeCtrl, parentItem))
            #parentItem = self.treeDirList.GetItemParent(parentItem)
            parentItem = treeCtrl.GetItemParent(parentItem)
        
        #print pathName
        if self.treeDirView:
            dirPath = os.path.sep.join(pathName)
            self.newDirPath = dirPath.replace("\\\\", "\\")
            #return dirPath.replace('\\\\', '\\')
            #print dirPath
            if Globals.EvidencesDict[Globals.CurrentEvidenceID]['NewLocation']:
                dirPath = dirPath.replace(Globals.EvidencesDict[Globals.CurrentEvidenceID]['NewLocation'], Globals.EvidencesDict[Globals.CurrentEvidenceID]['Location'])
                #if Globals.EvidencesDict[Globals.CurrentEvidenceID]['NewLocation']:
            return dirPath.replace("\\\\", "\\")
        else:
            self.newDirPath ="/".join(pathName)
            return self.newDirPath
        
    
    def OnTreeDirListTreeSelChanged(self, event, treeCtrl=None):
        #item = self.treeDirList.GetSelection()
        if treeCtrl == None:
            treeCtrl = self.treeDirList
        #print treeCtrl.Name
        
        item = treeCtrl.GetSelection()
        if not self.root:
            self.root = self.fileTreeView.GetRoot()
            
        if not item == self.root:
            #
            self.dirPath = PlatformMethods.Encode(self.GetPathName(item, treeCtrl))
                
            db = SqliteDatabase(Globals.FileSystemName)
            if not db.OpenConnection():
                return
            if treeCtrl is self.treeCatList:
                query = "select count(*) from %s where MimeType = ?;"%(Globals.CurrentEvidenceID)
            else:
                query = "select count(*) from %s where DirPath = ?;"%(Globals.CurrentEvidenceID)
                
            #print query
            row = db.FetchOneRow(query, (self.dirPath,))
            self.TotalFiles = int(row[0])
            self.TotalPages = (self.TotalFiles/Constants.MaxObjectsPerPage)
            if (int(row[0])%Constants.MaxObjectsPerPage) > 0:
                self.TotalPages += 1
                
            self.AddPageNumbersToChoice(self.TotalPages)
            self.choicePageNum.SetSelection(0)
            self.UpdateFilesInDirectory(0)
            
            if  Globals.frmGlobalMainForm.GetViewsCheckedMenu() == 'Details':
                self.listFilesDetails.Show(True)
                self.listFilesIcons.Show(False)
                self.AddFileDetailsToListView()
            else:
                self.listFilesIcons.Show(True)
                self.listFilesDetails.Show(False)
                self.AddFileIconsToListView()
                
        event.Skip()


    def OnBtnDirTreeViewButton(self, event):
        self.btnDirTreeView.Enable(False)
        self.btnCategoryView.Enable(True)
        self.btnCategoryView.SetValue(False)
        self.treeDirView = True
        #if len(Globals.FileInfoList) > 1:
        self.ShowDirectoryTreeView()
        self.root = self.TreeViewRoot
        event.Skip()

    def OnBtnCategoryViewButton(self, event):
        self.btnDirTreeView.Enable(True)
        self.btnDirTreeView.SetValue(False)
        self.btnCategoryView.Enable(False)
        self.treeDirView = False
        #if len(Globals.FileInfoList) > 1:
        self.ShowFileCategoryView()
        self.root = self.CategoryViewRoot
        event.Skip()
        
    def ShowDirectoryTreeView(self):
        #self.ShowProjectProperties(True)
        #self.notebookProject.Show(True)
        if self.fileTreeView is None:
            self.fileTreeView = FileTreeView(self, self.treeDirList)
            self.TreeViewRoot = self.fileTreeView.AddDirectoryTreeNodes()
        
        self.treeDirList.Show(True)
        self.treeCatList.Show(False)
        
        
    def ShowFileCategoryView(self):
        if Globals.fileCategoryView is None or self.CategoryViewRoot is None:
            Globals.fileCategoryView = FileCategoryView(self, self.treeCatList, Globals.MimeTypeSet)
            self.CategoryViewRoot = Globals.fileCategoryView.AddCategories()
        
        self.treeCatList.Show(True)
        self.treeDirList.Show(False)
        

    def OnTreeCatListTreeSelChanged(self, event):
        self.OnTreeDirListTreeSelChanged(event, self.treeCatList)
        event.Skip()


    def OnTreeDirListRightUp(self, event):
        self.treeDirList.PopupMenu(self.popupMenuDir)
        event.Skip()

    def OnPopupMenuDirMd5hashselectedMenu(self, event):
        #tbd
        return
    
        if self.dirPath == "":
            return
        if not os.path.exists(self.dirPath):
            return
        
        files = os.listdir(self.dirPath)
        self.db = SqliteDatabase(Globals.FileSystemName)
        if not self.db.OpenConnection():
            return
        
        self.SetCursor(wx.HOURGLASS_CURSOR)
        for file in files:
            filePath = self.dirPath + PlatformMethods.GetDirSeparator() + file
            if os.path.isfile(filePath):
                self.UpdateMD5(self.dirPath, file)
        
        if  Globals.frmGlobalMainForm.GetViewsCheckedMenu() == 'Details':
            self.AddFileDetailsToListView()
        self.db.CloseConnection()
        self.SetCursor(wx.STANDARD_CURSOR)
        event.Skip()

    def UpdateMD5(self, dirPath, fileName):
        filePath = dirPath + PlatformMethods.GetDirSeparator() + fileName
        md5Hash = CommonFunctions.GetMD5HexHash(filePath)
        values = self.db.SqlSQuote(md5Hash) + " where DirPath='" + dirPath
        values += "'  and Name= '" + fileName + "';"
        #print query + values
        self.db.ExecuteNonQuery("update " + Constants.FileInfoTable + " set MD5 = " + values)
        """
        for file in Globals.FileInfoList:
            if filePath == file.DirPath + PlatformMethods.GetDirSeparator() + file.Name:
                file.MD5Hash = md5Hash
                break
        """
        
    def UpdateSHA224Hash(self, dirPath, fileName):
        filePath = dirPath + PlatformMethods.GetDirSeparator() + fileName
        digest = CommonFunctions.GetSHA224Hash(filePath)
        values = self.db.SqlSQuote(digest) + " where DirPath='" + dirPath
        values += "'  and Name= '" + fileName + "';"
        #print query + values
        self.db.ExecuteNonQuery("update " + Constants.FileInfoTable + " set SHA224 = " + values)
        
        """
        for file in Globals.FileInfoList:
            if filePath == file.DirPath + PlatformMethods.GetDirSeparator() + file.Name:
                file.SHA224Hash = digest
                break
        """
         
        if  Globals.frmGlobalMainForm.GetViewsCheckedMenu() == 'Details':  
            self.AddFileDetailsToListView()
        
    def UpdateSHA1Hash(self, dirPath, fileName):
        filePath = dirPath + PlatformMethods.GetDirSeparator() + fileName
        sha1 = CommonFunctions.GetSHA1Hash(filePath)
        values = self.db.SqlSQuote(sha1) + " where DirPath='" + dirPath
        values += "'  and Name= '" + fileName + "';"
        #print query + values
        self.db.ExecuteNonQuery("update " + Constants.FileInfoTable + " set SHA1 = " + values)
        """
        for file in Globals.FileInfoList:
            if filePath == file.DirPath + PlatformMethods.GetDirSeparator() + file.Name:
                file.SHA1Hash = sha1
                break
        """ 
        if  Globals.frmGlobalMainForm.GetViewsCheckedMenu() == 'Details':  
            self.AddFileDetailsToListView()
            
    def UpdateSHA256Hash(self, dirPath, fileName):
        filePath = dirPath + PlatformMethods.GetDirSeparator() + fileName
        digest = CommonFunctions.GetSHA256Hash(filePath)
        values = self.db.SqlSQuote(digest) + " where DirPath='" + dirPath
        values += "'  and Name= '" + fileName + "';"
        #print query + values
        self.db.ExecuteNonQuery("update " + Constants.FileInfoTable + " set SHA256 = " + values)
        
        """
        for file in Globals.FileInfoList:
            if filePath == file.DirPath + PlatformMethods.GetDirSeparator() + file.Name:
                file.SHA256Hash = digest
                break
        """
         
        if  Globals.frmGlobalMainForm.GetViewsCheckedMenu() == 'Details':  
            self.AddFileDetailsToListView()
            
    def UpdateSHA384Hash(self, dirPath, fileName):
        filePath = dirPath + PlatformMethods.GetDirSeparator() + fileName
        digest = CommonFunctions.GetSHA384Hash(filePath)
        values = self.db.SqlSQuote(digest) + " where DirPath='" + dirPath
        values += "'  and Name= '" + fileName + "';"
        #print query + values
        self.db.ExecuteNonQuery("update " + Constants.FileInfoTable + " set SHA384 = " + values)
        
        """
        for file in Globals.FileInfoList:
            if filePath == file.DirPath + PlatformMethods.GetDirSeparator() + file.Name:
                file.SHA384Hash = digest
                break
        """
         
        if  Globals.frmGlobalMainForm.GetViewsCheckedMenu() == 'Details':  
            self.AddFileDetailsToListView()
            
    def UpdateSHA512Hash(self, dirPath, fileName):
        filePath = dirPath + PlatformMethods.GetDirSeparator() + fileName
        digest = CommonFunctions.GetSHA512Hash(filePath)
        values = self.db.SqlSQuote(digest) + " where DirPath='" + dirPath
        values += "'  and Name= '" + fileName + "';"
        #print query + values
        self.db.ExecuteNonQuery("update " + Constants.FileInfoTable + " set SHA512 = " + values)
        
        """
        for file in Globals.FileInfoList:
            if filePath == file.DirPath + PlatformMethods.GetDirSeparator() + file.Name:
                file.SHA512Hash = digest
                break
        """
        
        if  Globals.frmGlobalMainForm.GetViewsCheckedMenu() == 'Details':  
            self.AddFileDetailsToListView()
            
    def OnPopupMenuDirMd5hashchildrenMenu(self, event):
        
        #tbd
        return
    
        if self.dirPath == "":
            return
        self.db = SqliteDatabase(Globals.FileSystemName)
        if not self.db.OpenConnection():
            return
        
        sums = [0, 1] # 0 files 1 directory so far
        self.SetCursor(wx.HOURGLASS_CURSOR)
        try:
            os.path.walk(self.dirPath, self.UpdateGroupMD5Hash, sums)
        except Exception, value:
            print "Failed to walk directories. Error: %s"%(value)
        
        self.db.CloseConnection()
        if Globals.frmGlobalMainForm.GetViewsCheckedMenu() == 'Details':
            self.AddFileDetailsToListView()
        self.SetCursor(wx.STANDARD_CURSOR)
        event.Skip()


    def UpdateGroupMD5Hash(self, sms, dirName, fileList):
        query = "update " + Constants.FileInfoTable + " set MD5 = "
        for file in fileList:
            filePath = dirName + PlatformMethods.GetDirSeparator() + file
            if os.path.isfile(filePath):
                self.UpdateMD5(dirName, file)

    def OnPopupMenuFileGenmd5filesMenu(self, event):
        self.GenerateHashes(self.UpdateMD5)
        
        if  Globals.frmGlobalMainForm.GetViewsCheckedMenu() == 'Details':
            self.AddFileDetailsToListView()
            
        event.Skip()
        
    def GenerateHashes(self, UpdateHashFunction):
        #need to fix a lot of stuff so don't do anything right now...
        return
    
        if not self.IsFileSelected():
            return
        self.db = SqliteDatabase(Globals.FileSystemName)
        if not self.db.OpenConnection():
            return
        
        dirPath = ""
        fileName = ""
        
        while self.index >= 0:
            if self.treeDirView:
                dirPath = self.dirPath
                if  Globals.frmGlobalMainForm.GetViewsCheckedMenu() == 'Details':
                    fileName = self.listFilesDetails.GetItem(self.index).GetText()
                    self.index = self.listFilesDetails.GetNextSelected(self.index)
                else:
                    fileName = self.listFilesIcons.GetItem(self.index).GetText()
                    self.index = self.listFilesIcons.GetNextSelected(self.index)
            else:
                if  Globals.frmGlobalMainForm.GetViewsCheckedMenu() == 'Details':
                    filePath = self.listFilesDetails.GetItem(self.index).GetText()
                    self.index = self.listFilesDetails.GetNextSelected(self.index)
                    #dirPath = filePath[:filePath.rfind(PlatformMethods.GetDirSeparator())]
                    #fileName = filePath[filePath.rfind(PlatformMethods.GetDirSeparator()) + 1:]
                else:
                    filePath = self.listFilesIcons.GetItem(self.index).GetText()
                    self.index = self.listFilesIcons.GetNextSelected(self.index)
                    
                dirPath = filePath[:filePath.rfind(PlatformMethods.GetDirSeparator())]
                fileName = filePath[filePath.rfind(PlatformMethods.GetDirSeparator()) + 1:]
            
            
            UpdateHashFunction(dirPath, fileName)
        
    def OnListFilesDetailsRightUp(self, event):
        #self.popupMenuFile.Enable(wxID_MDICHILDFILELISTPOPUPMENUFILEMENUITEMFILEPROPERTIES, False)
        self.listFilesDetails.PopupMenu(self.popupMenuFile)
        event.Skip()

    def OnListFilesIconsRightUp(self, event):
        #self.popupMenuFile.Enable(wxID_MDICHILDFILELISTPOPUPMENUFILEMENUITEMFILEPROPERTIES, True)
        self.listFilesIcons.PopupMenu(self.popupMenuFile)
        event.Skip()

    def OnListFilesIconsLeftDclick(self, event):
        
        """
        if self.IsFileSelected():
            self.OpenFile()
        event.Skip()
        """
        
        self.OnPopupMenuFileMenuitemfilepropertiesMenu(event)

    def OnPopupMenuFileMenuitemopenfileMenu(self, event):
        if self.IsFileSelected():
            self.OpenFile()
        event.Skip()
        
    """
    def GetSelectedFileInfo(self):
        self.fileInfo = None
        for fileinfo in self.FileList:
            if self.treeDirView:
                if PlatformMethods.Decode(fileinfo.Name) == self.selectedFileName and PlatformMethods.Decode(fileinfo.DirPath) == self.dirPath:
                    self.fileInfo = fileinfo
                    break
            else:
                if os.path.join(fileinfo.DirPath, fileinfo.Name) == self.fullFilePath:
                    self.fileInfo = fileinfo
                    
        return self.fileInfo
    """

    def OnPopupMenuFileMenuitemfilepropertiesMenu(self, event):
        if not self.IsFileSelected():
            return
        
        """
        if not self.GetSelectedFileInfo():
            return
        """
        
        import frmFileViewer
        fileProp = frmFileViewer.frmFileViewer(self, self.fileInfo)
        fileProp.Show()
        event.Skip()

    def OnPopupMenuFileMenuitemviewfileMenu(self, event):
        if not self.IsFileSelected():
            return

        import frmFileViewer
        fileProp = frmFileViewer.frmFileViewer(self, self.fileInfo)
        fileProp.Show()
        event.Skip()

    def OnPopupMenuFileGensha1Menu(self, event):
        event.Skip()

    def OnPopupMenuSHASha1digestMenu(self, event):
        self.GenerateHashes(self.UpdateSHA1Hash)
            
        event.Skip()

    def OnPopupMenuSHASha224digestMenu(self, event):
        self.GenerateHashes(self.UpdateSHA224Hash)
        event.Skip()

    def OnPopupMenuSHASha256digestMenu(self, event):
        self.GenerateHashes(self.UpdateSHA256Hash)
        event.Skip()

    def OnPopupMenuSHASha384digestMenu(self, event):
        self.GenerateHashes(self.UpdateSHA384Hash)
        event.Skip()

    def OnPopupMenuSHASha512digestMenu(self, event):
        self.GenerateHashes(self.UpdateSHA512Hash)
        event.Skip()

    def OnChoicePageNumChoice(self, event):
        self.UpdateFilesInDirectory((int(self.choicePageNum.GetStringSelection())-1)*Constants.MaxObjectsPerPage)
        
        if  Globals.frmGlobalMainForm.GetViewsCheckedMenu() == 'Details':
            self.listFilesDetails.Show(True)
            self.listFilesIcons.Show(False)
            self.AddFileDetailsToListView()
        else:
            self.listFilesIcons.Show(True)
            self.listFilesDetails.Show(False)
            self.AddFileIconsToListView()
            
        event.Skip()

    def OnPopupMenuDirMark_files_for_exportMenu(self, event):
        if self.dirPath == "":
            return
        
        db = SqliteDatabase(Globals.FileSystemName)
        if not db.OpenConnection():
            return
        query = "update %s set Export=1 where DirPath=?;"%(Globals.CurrentEvidenceID)
        db.ExecuteNonQuery(query, (self.dirPath,))
        db.CloseConnection()
        if  Globals.frmGlobalMainForm.GetViewsCheckedMenu() == 'Details':  
         
            for i in range(len(self.FileList)):
                self.listFilesDetails.SetStringItem(i, 10, 'Yes')

        self.UpdateExportButtonLabel()
        event.Skip()

    def OnPopupMenuDirUnmark_all_files_for_exportMenu(self, event):
        if self.dirPath == "":
            return
        
        db = SqliteDatabase(Globals.FileSystemName)
        if not db.OpenConnection():
            return
        query = "update %s set Export=0 where DirPath=?;"%(Globals.CurrentEvidenceID)
        db.ExecuteNonQuery(query, (self.dirPath,))
        db.CloseConnection()
        if  Globals.frmGlobalMainForm.GetViewsCheckedMenu() == 'Details':  
      
            for i in range(len(self.FileList)):
                self.listFilesDetails.SetStringItem(i, 10, 'No')

        self.UpdateExportButtonLabel()
        event.Skip()

    def OnPopupMenuFileMark_for_exportMenu(self, event):
        if not self.IsFileSelected():
            return
        
        db = SqliteDatabase(Globals.FileSystemName)
        if not db.OpenConnection():
            return
        
        query = "update %s set Export=1 where Name=? and DirPath=?;"%(Globals.CurrentEvidenceID)
        db.ExecuteNonQuery(query, (self.fileInfo[0], self.fileInfo[1],))
        db.CloseConnection()
        if  Globals.frmGlobalMainForm.GetViewsCheckedMenu() == 'Details':  
            self.listFilesDetails.SetStringItem(self.index, 10, 'Yes')
        
        self.UpdateExportButtonLabel()
        event.Skip()

    def OnPopupMenuFileUnmark_for_exportMenu(self, event):
        if not self.IsFileSelected():
            return
        
        db = SqliteDatabase(Globals.FileSystemName)
        if not db.OpenConnection():
            return
        query = "update %s set Export=0 where Name=? and DirPath=?;"%(Globals.CurrentEvidenceID)
        db.ExecuteNonQuery(query, (self.fileInfo[0], self.fileInfo[1],))
        db.CloseConnection()
        if  Globals.frmGlobalMainForm.GetViewsCheckedMenu() == 'Details':  
            self.listFilesDetails.SetStringItem(self.index, 10, 'No')
            
        self.UpdateExportButtonLabel()
        event.Skip()

    def OnTreeCatListRightUp(self, event):
        self.treeCatList.PopupMenu(self.popupMenuCategory)
        event.Skip()

    def OnPopupMenuCategoryMd5hashselectedMenu(self, event):
        event.Skip()

    def OnPopupMenuCategoryMd5hashchildrenMenu(self, event):
        event.Skip()

    def OnPopupMenuCategoryMark_files_for_exportMenu(self, event):
        if self.dirPath == "":
            return
        
        db = SqliteDatabase(Globals.FileSystemName)
        if not db.OpenConnection():
            return
        
        query = "update %s set Export=1 where MimeType=%s;"%(Globals.CurrentEvidenceID, db.SqlSQuote(self.dirPath))
        db.ExecuteNonQuery(query)
        db.CloseConnection()
        if  Globals.frmGlobalMainForm.GetViewsCheckedMenu() == 'Details':  
         
            for i in range(len(self.FileList)):
                self.listFilesDetails.SetStringItem(i, 10, 'Yes')
        
        self.UpdateExportButtonLabel()
        event.Skip()
        
    def OnPopupMenuCategoryUnmark_all_files_for_exportMenu(self, event):
        if self.dirPath == "":
            return
        
        db = SqliteDatabase(Globals.FileSystemName)
        if not db.OpenConnection():
            return
        query = "update %s set Export=0 where MimeType=%s;"%(Globals.CurrentEvidenceID, db.SqlSQuote(self.dirPath))
        db.ExecuteNonQuery(query)
        db.CloseConnection()
        
        if  Globals.frmGlobalMainForm.GetViewsCheckedMenu() == 'Details':  
            for i in range(len(self.FileList)):
                self.listFilesDetails.SetStringItem(i, 10, 'No')
        
        self.UpdateExportButtonLabel()
        event.Skip()

    def OnBtnExportMarkedFilesButton(self, event):
        
        dlg = wx.DirDialog(self, "Select Destination Folder")
        try:
            if dlg.ShowModal() == wx.ID_OK:
                dir = dlg.GetPath().encode('utf-8', 'replace')
                # Your code
                self.SetCursor(wx.HOURGLASS_CURSOR)
                busy = wx.BusyInfo("Exporting marked files. Please relax, it may take some time...")
                wx.Yield()
                self.ExportFiles(dir)
                self.SetCursor(wx.STANDARD_CURSOR)
        finally:
            dlg.Destroy()
        
        
        event.Skip()

        

    def UpdateExportButtonLabel(self):
        db = SqliteDatabase(Globals.FileSystemName)
        if not db.OpenConnection():
            return
        
        query = "select count(Export) from %s where Export=1;"%(Globals.CurrentEvidenceID)
        row = db.FetchOneRow(query)
        if row:
            self.btnExportMarkedFiles.SetLabel("Export Marked (%d) Files"%(row[0]))
        else:
            self.btnExportMarkedFiles.SetLabel("Export Marked (0) File")
        
        db.CloseConnection()
        
    
    def ExportFiles(self, destination):
        
        log = open(os.path.join(Globals.CasePath, 'Export.log'), 'ab')
        db = SqliteDatabase(Globals.FileSystemName)
        if not db.OpenConnection():
            return
    
        
        query = "select DirPath || '%s' || Name, NewPath from %s where Export = 1;"%(os.path.sep, Globals.CurrentEvidenceID)
        rows = db.FetchAllRows(query)
        db.CloseConnection()
        for row in rows:
            if row[1]:
                sourcePath = os.path.join(Globals.CasePath, PlatformMethods.Decode(row[1]))
                destPath = row[1][:row[1].rfind(os.path.sep)]
                destPath = PlatformMethods.Decode(os.path.join(destination, destPath))
            else:
                if Globals.EvidencesDict[Globals.CurrentEvidenceID]['NewLocation']:
                    sourcePath = row[0].replace(Globals.EvidencesDict[Globals.CurrentEvidenceID]['Location'], Globals.EvidencesDict[Globals.CurrentEvidenceID]['NewLocation'])
                    destPath = os.path.dirname(sourcePath).replace(Globals.EvidencesDict[Globals.CurrentEvidenceID]['NewLocation'], "")
                    if destPath.startswith(os.path.sep):
                        destPath = destPath.replace(os.path.sep, "", 1)
                    #print 'destPath ', destPath
                    destPath = os.path.join(destination, destPath)
                    #fileName = os.path.basename(sourcePath)
                    #print 'destPath ', destPath
                else:
                    sourcePath = row[0]
                    destPath = os.path.dirname(sourcePath).replace(Globals.EvidencesDict[Globals.CurrentEvidenceID]['Location'], "")
                    if destPath.startswith(os.path.sep):
                        destPath = destPath.replace(os.path.sep, "", 1)
                    #print 'destPath ', destPath
                    destPath = os.path.join(destination, destPath)
                    #print 'destPath ', destPath
                #fileName = os.path.basename(sourcePath)
            """
            if os.path.exists(sourcePath):
                print 'exists source path ', sourcePath.encode('utf-8', 'replace')
            if os.path.exists(destPath):
                print 'exists des path ', destPath.encode('utf-8', 'replace')
            """     
            if not os.path.exists(destPath):
                try:
                    os.makedirs(destPath)
                except Exception, msg:
                    log.write("%s Error: %s\n"%(sourcePath.encode('utf-8', 'replace'), msg))
                    #print 'make dirs msg, ', msg
                    #log.write(sourcePath)
        
            try:
                
                shutil.copy2(sourcePath, destPath)
            except Exception, msg:
                log.write("%s Error: %s\n"%(sourcePath.encode('utf-8', 'replace'), msg))
                #print 'shutil ', msg
                #log.write(sourcePath.encode('utf-8', 'replace'))
                
        log.close()
        
