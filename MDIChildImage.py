#-----------------------------------------------------------------------------
# Name:        MDIChilldImages.py
# Purpose:     
#
# Author:      Ram B. Basnet
#
# Created:     2007/11/01
# Last Modified: 06/29/2009
# RCS-ID:      $Id: MDIChildImage.py,v 1.4 2008/03/12 04:04:03 rbasnet Exp $
# Copyright:   (c) 2006
# Licence:     All Rights Reserved.
# New field:   Whatever
#-----------------------------------------------------------------------------

import wx
from wx.lib.anchors import LayoutAnchors
import  wx.lib.mixins.listctrl  as  listmix
import wx.grid
import wx.html
import wx.aui
import time
import re, string
import os, sys, os.path
import shutil

import cPickle


from SqliteDatabase import *
import Globals
import Constants
import CommonFunctions
import DBFunctions
import Classes
import PlatformMethods
import images
from ImageDirectoryTreeView import *
import CustomControls

def create(parent, ImagesDict=None):
    return MDIChildImage(parent, ImagesDict)

class MDIChildImage(wx.MDIChildFrame, listmix.ColumnSorterMixin):
    
    def __init__(self, prnt, ImagesDict):

        wx.MDIChildFrame.__init__(self, id=-1,
              name='MDIChildImages', parent=prnt, pos=wx.DefaultPosition,
              size=wx.Size(1050, 690), style=wx.DEFAULT_FRAME_STYLE, title='Image Analyzer')
        self.SetBackgroundColour(wx.Colour(125, 152, 221))
        self.SetClientSize(wx.Size(1040, 680))
        self.SetAutoLayout(True)
        self.Center(wx.BOTH)
        self.SetIcon(images.getMAKE2Icon())
        self.SetMinSize(wx.Size(400, 300))
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        
        self.panImages = wx.Panel(id=wx.NewId(),
              name='panImages', parent=self, pos=wx.Point(4, 4),
              size=wx.Size(1032, 672), style=wx.TAB_TRAVERSAL)
        self.panImages.SetBackgroundColour(wx.Colour(225, 236, 255))
        self.panImages.SetConstraints(LayoutAnchors(self.panImages, True, True,
              True, True))
        
        self.btnClose = wx.Button(id=wx.NewId(), label='Close',
              name='btnClose', parent=self.panImages, pos=wx.Point(952, 8),
              size=wx.Size(75, 23), style=0)
              
        self.btnClose.SetConstraints(LayoutAnchors(self.btnClose, False, True,
              True, False))
        self.btnClose.Bind(wx.EVT_BUTTON, self.OnBtnCloseButton,
              id=self.btnClose.GetId())
        
        self.btnExportMarkedFiles = wx.Button(id=wx.NewId(),
              label='Export Marked (100000) Files', name='btnExportMarkedFiles',
              parent=self.panImages, pos=wx.Point(773, 8), size=wx.Size(163,
              23), style=0)
              
        self.btnExportMarkedFiles.SetConstraints(LayoutAnchors(self.btnExportMarkedFiles,
              False, True, True, False))
        self.btnExportMarkedFiles.Bind(wx.EVT_BUTTON,
              self.OnBtnExportMarkedFilesButton,
              id=self.btnExportMarkedFiles.GetId())
              
        self.notebookImages = wx.Notebook(id=wx.NewId(),
              name='notebookImages', parent=self.panImages, pos=wx.Point(8, 40),
              size=wx.Size(1016, 626), style=0)
        self.notebookImages.SetAutoLayout(False)
        self.notebookImages.SetConstraints(LayoutAnchors(self.notebookImages,
              True, True, True, True))
        
        self.panView = wx.Panel(id=wx.NewId(), name='panView',
              parent=self.notebookImages, pos=wx.Point(0, 0), size=wx.Size(999,
              534), style=wx.TAB_TRAVERSAL)
        self.panView.SetAutoLayout(False)
        self.panView.SetBackgroundColour(wx.Colour(225, 236, 255))
        self.panView.SetConstraints(LayoutAnchors(self.panView, True, True,
              True, True))

        """
        self.panelTimeline = wx.Panel(id=wx.NewId(), name='panel1',
              parent=self.notebookImages, pos=wx.Point(0, 0), size=wx.Size(999,
              534), style=wx.TAB_TRAVERSAL)

        self.panelSteganalysis = wx.Panel(id=wx.NewId(), name='panel2',
              parent=self.notebookImages, pos=wx.Point(0, 0), size=wx.Size(999,
              534), style=wx.TAB_TRAVERSAL)
        """
                    
        self.notebookImages.AddPage(imageId=-1, page=self.panView, select=True, text='View')
        
        """
        self.notebookImages.AddPage(imageId=-1, page=self.panelTimeline, select=False,
              text='Timeline')
        self.notebookImages.AddPage(imageId=-1, page=self.panelSteganalysis, select=False,
              text='Steganalysis')
        """
        
        # tell FrameManager to manage this frame  
        self.auiManagerView = wx.aui.AuiManager()
                
        self.auiManagerView.SetManagedWindow(self.panView)

        self.FileInfo = {}

        self.FileList = []
            
        self.dirPath = ""
        self.newDirPath = ""
        self.TotalPages = 0
        self.log = open(os.path.join(Globals.CasePath, 'Images.log'), 'a')
        self.log.write('\n\n**********\n\nImage module started: %s\n'%CommonFunctions.GetCurrentDisplayDateTime())
        self.log.flush()
        
        self.popupMenuDir = wx.Menu(title='')
        self.popupMenuFile = wx.Menu(title='')
        self.popupSubMenuSHA = wx.Menu(title='')
        self.CreatePopupMenuDir(self.popupMenuDir)
        self.CreatePopupFileMenu()
        self.CreatePopupSHASubMenu()
        self.rightClickedOn = 0

        #self.LoadThumbnails()
        
        self.InitPanes()
        # "commit" all changes made to FrameManager   
        
        #self.auiManagerView.GetArtProvider().SetMetric(wx.aui.AUI_DOCKART_CAPTION_FONT, 10)
        self.auiManagerView.GetArtProvider().SetMetric(wx.aui.AUI_DOCKART_CAPTION_SIZE, 20)
        self.auiManagerView.GetArtProvider().SetColor(wx.aui.AUI_DOCKART_BACKGROUND_COLOUR, wx.Colour(125, 152, 221))
        self.auiManagerView.GetArtProvider().SetColor(wx.aui.AUI_DOCKART_SASH_COLOUR, wx.Colour(125, 152, 221))
        self.auiManagerView.GetArtProvider().SetColor(wx.aui.AUI_DOCKART_INACTIVE_CAPTION_COLOUR, wx.Colour(183, 183, 255))
        self.auiManagerView.GetArtProvider().SetColor(wx.aui.AUI_DOCKART_INACTIVE_CAPTION_GRADIENT_COLOUR, wx.Colour(125, 152, 221))
        self.auiManagerView.Update()
        self.UpdateExportButtonLabel()
        
        
 
    def InitPanes(self):
        # add bunch of floatable panes
        self.auiManagerView.AddPane(self.CreateThumbnailsPane(), wx.aui.AuiPaneInfo().
                        Name("Thumbnails").Caption("Thumbnails").
                        Top().Layer(1).Position(1).PinButton(True).MaximizeButton(True).CloseButton(False))
        
        self.auiManagerView.AddPane(self.CreateViewFoldersPane(), wx.aui.AuiPaneInfo().
                        Name("ViewFolders").Caption("Folders").
                        Left().Layer(1).Position(1).PinButton(True).CloseButton(False))

                        
        self.auiManagerView.AddPane(self.CreateFileListPane(), wx.aui.AuiPaneInfo().Name("ViewFileList").
                        Caption("File List").Bottom().Layer(1).Position(1).MaximizeButton(True).PinButton(True).CloseButton(False))
        
        self.auiManagerView.AddPane(self.CreateHTMLPane(), wx.aui.AuiPaneInfo().Name("ViewImage").
                          CenterPane())
        # Show How To Use The Closing Panes Event
        self.Bind(wx.aui.EVT_AUI_PANE_CLOSE, self.OnPaneClose)
        
        
    def OnPaneClose(self, event):
        event.GetPane().Hide()
        #event.Veto()

    def OnClose(self, event):
        self.auiManagerView.UnInit()
        self.Destroy()
        self.log.close()
        event.Skip()        
 
    def OnBtnCloseButton(self, event):
        self.OnClose(event)
        event.Skip()
        

    def CreateThumbnailsPane(self):
        self.panThumbnails = wx.Panel(id=wx.NewId(),
              name='panThumbnails', parent=self.panView, pos=wx.Point(0, 0),
              size=wx.Size(1024, 146), style=wx.TAB_TRAVERSAL)
        self.panThumbnails.SetBackgroundColour(wx.Colour(225, 236, 255))
        self.panThumbnails.SetAutoLayout(True)

        self.lblThumbnailPage = wx.StaticText(id=wx.NewId(),
              label='Page', name='lblThumbnailPage', parent=self.panThumbnails,
              pos=wx.Point(8, 8), size=wx.Size(28, 13), style=0)
        self.lblThumbnailPage.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, 'Tahoma'))

        choiceId = wx.NewId()
        self.choiceThumbnailPageNum = wx.Choice(choices=[], id=choiceId, name='choiceThumbnailPageNum', 
            parent=self.panThumbnails, pos=wx.Point(8, 32), size=wx.Size(64, 21), style=0)
        self.choiceThumbnailPageNum.Bind(wx.EVT_CHOICE, self.OnChoiceThumbnailPageNumChoice,
          id=choiceId)
          
        self.lblThumbnailTotalPages = wx.StaticText(id=wx.NewId(),
              label='of 0', name='lblThumbnailTotalPages', parent=self.panThumbnails, pos=wx.Point(8,
              64), size=wx.Size(36, 13), style=0)
        self.lblThumbnailTotalPages.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, 'Tahoma'))
              
        self.lblThumbnailCount = wx.StaticText(id=wx.NewId(),
            label='0 of 0', name='lblThumbnailCount', parent=self.panThumbnails,
              pos=wx.Point(8, 88), size=wx.Size(29, 13), style=0)
        self.lblThumbnailCount.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, 'Tahoma'))

        self.lblImage = wx.StaticText(id=wx.NewId(),
              label='Files', name='lblThumbnailCount', parent=self.panThumbnails,
              pos=wx.Point(8, 112), size=wx.Size(29, 13), style=0)
        self.lblImage.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, 'Tahoma'))

        self.listThumbnails = wx.ListCtrl(id=wx.NewId(),
              name='listThumbnails', parent=self.panThumbnails, pos=wx.Point(80,
              8), size=wx.Size(936, 130), style=wx.VSCROLL | wx.LC_ICON | wx.HSCROLL)
        self.listThumbnails.SetConstraints(LayoutAnchors(self.listThumbnails,
              True, True, True, True))
        
        self.listThumbnails.Bind(wx.EVT_LIST_ITEM_SELECTED,  self.OnListThumbnailsListItemSelected, id=self.listThumbnails.GetId())
              
        self.ThumbnailImageList = wx.ImageList(Constants.ThumbnailWidth, Constants.ThumbnailHeight)
        self.listThumbnails.SetImageList(self.ThumbnailImageList, wx.IMAGE_LIST_NORMAL)
        
        return self.panThumbnails
    

    def DisplayThumbnails(self):
        xPos = 10
        yPos = 10
        #print len(self.FileList)
        #print self.FileList
        dbImage = SqliteDatabase(Globals.ImagesFileName)
        if not dbImage.OpenConnection():
            return
        
        self.listThumbnails.DeleteAllItems()
        selectQuery = "select Thumbnail from %s where DirPath = ? and Filename = ?"%Globals.CurrentEvidenceID
        insertQuery = "insert into %s (DirPath, Filename, Thumbnail) values (?,?,?)"%Globals.CurrentEvidenceID
        busy = wx.BusyInfo("Generating Thumbnails Cache... Just Relax! It may take a few minutes...")
        wx.Yield()
        for imgFile in self.FileList:
            #print imgFile
            dirPath = imgFile[1]
            
            newPath = imgFile[11]
            #print 'newPath ', newPath
            if newPath:
                imagePath = os.path.join(Globals.CasePath.encode('utf-8', 'replace'), newPath)
            else:
                if Globals.EvidencesDict[Globals.CurrentEvidenceID]['NewLocation']:
                    dirPath = imgFile[1].replace(Globals.EvidencesDict[Globals.CurrentEvidenceID]['Location'], Globals.EvidencesDict[Globals.CurrentEvidenceID]['NewLocation'])
                    
                imagePath = os.path.join(dirPath, imgFile[0])
                    
            #print 'image Path ',imagePath
            row = dbImage.FetchOneRow(selectQuery, (imgFile[1], imgFile[0],))
            if row:
                Thumbnail = cPickle.loads(str(row[0]))
                #print 'loading thumbnails'
            else:
                try:
                    Thumbnail = CommonFunctions.GetThumbnail(imagePath).GetData()
                    dbImage.ExecuteMany(insertQuery, [(imgFile[1], imgFile[0], cPickle.dumps(Thumbnail))])
                except Exception, value:
                    self.log.write('Error Creating Thumbnail: %s Value: %s\n'%(PlatformMethods.Encode(imagePath), str(value)))
                    self.log.flush()
                    continue
            
            ilMax = self.ThumbnailImageList.Add(wx.BitmapFromBuffer(Constants.ThumbnailWidth, Constants.ThumbnailHeight, Thumbnail))
            li = self.listThumbnails.InsertImageStringItem(sys.maxint, imgFile[0], ilMax)
            self.listThumbnails.SetItemPosition(li, wx.Point(xPos, yPos))
            xPos += Constants.ThumbnailWidth + 10
            #yPos
        
        if len(self.FileList) > 1:
            value = "Images"
        else:
            value = "Image"
            
        self.lblThumbnailTotalPages.SetLabel("of %s"%(CommonFunctions.GetCommaFormattedNumber(self.TotalPages)))
        self.lblThumbnailCount.SetLabel("%s of %s"%(CommonFunctions.GetCommaFormattedNumber(len(self.FileList)), CommonFunctions.GetCommaFormattedNumber(self.TotalFiles)))
        self.lblImage.SetLabel(value)
        
        dbImage.CloseConnection()
    
    def CreateViewFoldersPane(self):
        self.panViewFolders = wx.Panel(id=wx.NewId(),
            name='panViewFolders', parent=self.panView, pos=wx.Point(0, 0),
            size=wx.Size(200, 304), style=wx.TAB_TRAVERSAL)
        self.panViewFolders.SetBackgroundColour(wx.Colour(225, 236, 255))
        self.panViewFolders.SetAutoLayout(True)

        treeID = wx.NewId()
        self.treeViewFolders = wx.TreeCtrl(id=treeID,
              name='treeViewFolders', parent=self.panViewFolders,
              pos=wx.Point(8, 8), size=wx.Size(184, 288),
              style=wx.HSCROLL | wx.VSCROLL | wx.TR_HAS_BUTTONS)
        self.treeViewFolders.SetConstraints(LayoutAnchors(self.treeViewFolders,
              True, True, True, True))
   
        self.treeViewFolders.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnTreeViewFoldersSelChanged, id=treeID)
        self.treeViewFolders.Bind(wx.EVT_CONTEXT_MENU, self.OnTreeViewFoldersRightUp, id=treeID)
        
        self.ImageTreeView = ImageDirectoryTreeView(self, self.treeViewFolders, Globals.EvidencesDict)
        self.root = self.ImageTreeView.AddDirectories()
        return self.panViewFolders
              
        
    def CreateHTMLPane(self):
        self.panIEView = wx.Panel(id=wx.NewId(), parent=self.panView, pos=wx.Point(0, 0), size=wx.Size(416, 316))
        self.panIEView.SetBackgroundColour(wx.Colour(225, 236, 255))
        self.panIEView.SetAutoLayout(True)
        
        self.htmlCtrl = wx.html.HtmlWindow(self.panIEView, -1, wx.Point(8,8), wx.Size(400, 300))
        if "gtk2" in wx.PlatformInfo:
            self.htmlCtrl.SetStandardFonts()
        self.htmlCtrl.SetConstraints(LayoutAnchors(self.htmlCtrl, True,
              True, True, True))
              
        return self.panIEView
        
    def CreateThumbnailPageSelection(self):
        choiceId = wx.NewId()
        self.choicePageNum = wx.Choice(choices=['1'],
            id=choiceId, name='choicePageNum',
            parent=self.panFileList, pos=wx.Point(56, 40), size=wx.Size(64,
            21), style=0)
        self.choicePageNum.Bind(wx.EVT_CHOICE, self.OnChoicePageNumChoice,
          id=choiceId)
          
    def CreateFileListPageSelection(self):
        choiceId = wx.NewId()
        self.choiceFileListPageNum = wx.Choice(choices=['0'],
            id=choiceId, name='choiceFileListPageNum',
            parent=self.panFileList, pos=wx.Point(56, 40), size=wx.Size(64,
            21), style=0)
        self.choiceFileListPageNum.Bind(wx.EVT_CHOICE, self.OnChoiceFileListPageNumChoice,
          id=choiceId)
          
    def CreateFileListPane(self):
        self.panFileList = wx.Panel(id=wx.NewId(),
              name='panThumbnails', parent=self.panView, pos=wx.Point(0, 0),
              size=wx.Size(1024, 276), style=wx.TAB_TRAVERSAL)
        self.panFileList.SetAutoLayout(True)
        self.panFileList.SetBackgroundColour(wx.Colour(225, 236, 255))
        
        self.staticTextPage = wx.StaticText(id=wx.NewId(),
              label='Page', name='staticTextPage', parent=self.panFileList,
              pos=wx.Point(16, 48), size=wx.Size(28, 13), style=0)
        self.staticTextPage.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, 'Tahoma'))
              
        self.lblFileListCount = wx.StaticText(id=wx.NewId(),
              label='of 0: Showing 0 File', name='lblFileListCount', parent=self.panFileList,
              pos=wx.Point(136, 48), size=wx.Size(35, 13), style=0)
        self.lblFileListCount.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, 'Tahoma'))
              
        self.CreateFileListPageSelection()
        
        listID = wx.NewId()
        self.listFilesDetails = CustomControls.CustomListCtrl(self.panFileList, listID, pos=wx.Point(8,72), size=wx.Size(1008, 191),
                                     style=wx.LC_REPORT | wx.BORDER_NONE | wx.LC_SORT_ASCENDING)
        
        self.listFilesDetails.SetConstraints(LayoutAnchors(self.listFilesDetails, True,
              True, True, True))
        self.listFilesDetails.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, u'Tahoma'))
              
        
        # Now that the list exists we can init the other base class,
        # see wx/lib/mixins/listctrl.py
        listmix.ColumnSorterMixin.__init__(self, 14)
        
        self.listFilesDetails.Bind(wx.EVT_LIST_COL_CLICK, self.OnListColClick, id=listID)
        self.listFilesDetails.Bind(wx.EVT_CONTEXT_MENU, self.OnListFilesDetailsRightUp, id=listID)
        self.listFilesDetails.Bind(wx.EVT_LIST_ITEM_SELECTED,  self.OnListFilesDetailsItemSelected, id=listID)
           
        self.fldrImg = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_OTHER, (24,24))
        self.imgFolder = wx.StaticBitmap(bitmap=self.fldrImg, id=-1, name=u'imgFolder', parent=self.panFileList, pos=wx.Point(8, 8),
              size=wx.Size(24, 24), style=0)
        self.imgFolder.SetConstraints(LayoutAnchors(self.imgFolder, True, True,
              False, False))

        self.lblDirectoryName = wx.StaticText(id=-1,
              label=u'NMT', name=u'lblDirectoryName', parent=self.panFileList, pos=wx.Point(40, 16), size=wx.Size(26, 16), style=0)
        self.lblDirectoryName.SetForegroundColour(wx.Colour(0, 0, 187))
        self.lblDirectoryName.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False, u'Tahoma'))
        self.lblDirectoryName.SetConstraints(LayoutAnchors(self.lblDirectoryName,
              True, True, False, False))
              
        #self.UpdateFilesInDirectory()
        #self.AddFileDetailsToListView()
        self.AddListColumnHeadings()

        self.imageListSmallIcon = wx.ImageList(16, 16)
        
        self.sm_up = self.imageListSmallIcon.Add(images.getSmallUpArrowBitmap())
        self.sm_dn = self.imageListSmallIcon.Add(images.getSmallDnArrowBitmap())
        
        return self.panFileList
    
    
    def CreatePopupMenuDir(self, parent):
        itemId = wx.NewId()
        parent.Append(help='', id=itemId, kind=wx.ITEM_NORMAL, text='Generate Thumbnails')
        self.Bind(wx.EVT_MENU, self.OnPopupMenuGenerateThumbnails, id=itemId)
        
        self.popupMenuDir.AppendSeparator()
        
        itemId = wx.NewId()
        parent.Append(help='', id=itemId, kind=wx.ITEM_NORMAL, text='Mark All Files for Export')
        self.Bind(wx.EVT_MENU, self.OnPopupMenuDirMarkAllFilesForExport, id=itemId)
        
        itemId = wx.NewId()
        parent.Append(help='',id=itemId, kind=wx.ITEM_NORMAL, text='Unmark All Files for Export')
        self.Bind(wx.EVT_MENU, self.OnPopupMenuDirUnmarkAllFilesForExport, id=itemId)
        parent.AppendSeparator()
        
        itemId = wx.NewId()
        parent.Append(help='', id=itemId, kind=wx.ITEM_NORMAL, text=u'Generate MD5 Hash of Selected Folder')
        self.Bind(wx.EVT_MENU, self.OnPopupMenuDirMd5hashselectedMenu, id=itemId)
        
        itemId = wx.NewId()
        parent.Append(help='', id=itemId, kind=wx.ITEM_NORMAL, text=u'Generate MD5 Hash Recursively')
        self.Bind(wx.EVT_MENU, self.OnPopupMenuDirMd5hashchildrenMenu, id=itemId)
        
                     
    def CreatePopupFileMenu(self):
        
        itemId = wx.NewId()
        self.popupMenuFile.Append(help='', id=itemId, kind=wx.ITEM_NORMAL, text='View in Hex Viewer')
        self.Bind(wx.EVT_MENU, self.OnPopupMenuFileHexView, id=itemId)
        
        self.popupMenuFile.AppendSeparator()
        
        itemId = wx.NewId()
        self.popupMenuFile.Append(help='',
              id=itemId, kind=wx.ITEM_NORMAL, text='Mark for Export')
              
        self.Bind(wx.EVT_MENU, self.OnPopupMenuFileMark_for_exportMenu, id=itemId)
              
        itemId = wx.NewId()      
        self.popupMenuFile.Append(help='',
              id=itemId,  kind=wx.ITEM_NORMAL, text='Unmark for Export')
        
        self.Bind(wx.EVT_MENU, self.OnPopupMenuFileUnmark_for_exportMenu, id=itemId)
              
        self.popupMenuFile.AppendSeparator()
        
        itemId = wx.NewId()
        self.popupMenuFile.Append(help='', id=itemId, kind=wx.ITEM_NORMAL, text=u'Generate MD5 Hash')
        self.Bind(wx.EVT_MENU, self.OnPopupMenuFileMD5Digest, id=itemId)
        
        itemId = wx.NewId()
        self.popupMenuFile.AppendMenu(help='', id=itemId, submenu=self.popupSubMenuSHA, text='Generate SHA Digests')
   
   
    def GetFilePath(self, fileName):
        filePath = u""
        self.fileInfo = None
        for fileinfo in self.FileList:
            #if fileinfo[0] == fileName.encode('utf-8') and PlatformMethods.Decode(fileinfo[1]) == self.dirPath:
            if fileinfo[0] == fileName.encode('utf-8', 'replace') and fileinfo[1] == self.dirPath.encode('utf-8', 'replace'):
                if fileinfo[11]:
                    filePath = os.path.join(Globals.CasePath.encode('utf-8', 'replace'), fileinfo[11])
                else:
                    filePath = os.path.join(fileinfo[1], fileinfo[0])
                    if Globals.EvidencesDict[Globals.CurrentEvidenceID]['NewLocation']:
                        filePath = filePath.replace(Globals.EvidencesDict[Globals.CurrentEvidenceID]['Location'], Globals.EvidencesDict[Globals.CurrentEvidenceID]['NewLocation'])
                    
                self.fileInfo = fileinfo
                break
                    
        return filePath
    
    def IsFileSelected(self):
        if self.rightClickedOn == 0:
            listCtrl = self.listFilesDetails 
        else:
            listCtrl = self.listThumbnails
            
        self.index = listCtrl.GetFirstSelected()
            
        self.fullFilePath = ""
        
        if self.index >=0:
            self.selectedFileName = PlatformMethods.Encode(self.listFilesDetails.GetItem(self.index).GetText())
            self.fullFilePath = self.GetFilePath(self.selectedFileName)
                   
            if Globals.EvidencesDict[Globals.CurrentEvidenceID]['NewLocation']:
                self.fullFilePath = self.fullFilePath.replace(Globals.EvidencesDict[Globals.CurrentEvidenceID]['NewLocation'], Globals.EvidencesDict[Globals.CurrentEvidenceID]['Location'])
            
                
            
        else:
            dlg = wx.MessageDialog(self, 'Please select a file from the list.',
              'Error', wx.OK | wx.ICON_ERROR)
            try:
                dlg.ShowModal()
            finally:
                dlg.Destroy()
                
        return self.fullFilePath
        
        
    def GetSelectedFileInfo(self):
        self.fileInfo = None
        for fileinfo in self.FileList:
            if fileinfo[0] == self.selectedFileName and fileinfo[1] == self.dirPath:
                self.fileInfo = fileinfo
        
        return self.fileInfo
    
    def OnPopupMenuFileHexView(self, event):
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
        
    def OnPopupMenuFileMD5Digest(self, event):
        busy = wx.BusyInfo("Please wait! Generating MD5 Hash...")
        wx.Yield()
        self.SetCursor(wx.HOURGLASS_CURSOR)
        self.GenerateHashes(self.UpdateMD5)
        self.AddFileDetailsToListView()
        self.SetCursor(wx.STANDARD_CURSOR)
        event.Skip()

    def UpdateMD5(self, dirPath, fileName):
        filePath = dirPath + PlatformMethods.GetDirSeparator() + fileName
        md5Digest = CommonFunctions.GetMD5HexDigest(filePath)

        """
        for file in Globals.FileInfoList:
            if filePath == file.DirectoryPath + PlatformMethods.GetDirSeparator() + file.Name:
                file.MD5Digest = md5Digest
                break
        """
         
        for fileInfo in Globals.ImagesList:
            if filePath == fileInfo.DirectoryPath + PlatformMethods.GetDirSeparator() + fileInfo.Name:
                fileInfo.MD5Digest = md5Digest
                break
    
        values = self.db.SqlSQuote(md5Digest) + " where Path='" + dirPath
        values += "'  and Name= '" + fileName + "';"
        #print query + values
        #self.db.ExecuteNonQuery("update " + Constants.FileInfoTable + " set MD5Digest = " + values)
        #query = "update %s 
        
        db = SqliteDatabase(Globals.ImagesFileName)
        if not db.OpenConnection():
            return
        db.ExecuteNonQuery("update " + Constants.ImagesTable + " set MD5Digest = " + values)
        db.CloseConnection()
        
    def GenerateHashes(self, UpdateHashFunction):
        if not self.IsFileSelected():
            return
        
        self.db = SqliteDatabase(Globals.ImagesFileName)
        if not self.db.OpenConnection():
            return
        
        dirPath = ""
        fileName = ""
        
        while self.index >= 0:
            dirPath = self.dirPath
            fileName = self.listFilesDetails.GetItem(self.index).GetText()
            self.index = self.listFilesDetails.GetNextSelected(self.index)

            UpdateHashFunction(dirPath, fileName)
            
    def UpdateSHA224Digest(self, dirPath, fileName):
        filePath = dirPath + PlatformMethods.GetDirSeparator() + fileName
        digest = CommonFunctions.GetSHA224Digest(filePath)
        values = self.db.SqlSQuote(digest) + " where Path='" + dirPath
        values += "'  and Name= '" + fileName + "';"
        #print query + values
        self.db.ExecuteNonQuery("update " + Constants.ImagesTable + " set SHA224Digest = " + values)
        
        """
        for fileInfo in Globals.ImagesList:
            if filePath == fileInfo.DirectoryPath + PlatformMethods.GetDirSeparator() + fileInfo.Name:
                fileInfo.SHA224Digest = digest
                break 
        """
        self.AddFileDetailsToListView()
        
    def UpdateSHA1Digest(self, dirPath, fileName):
        filePath = dirPath + PlatformMethods.GetDirSeparator() + fileName
        sha1 = CommonFunctions.GetSHA1Digest(filePath)
        values = self.db.SqlSQuote(sha1) + " where Path='" + dirPath
        values += "'  and Name= '" + fileName + "';"
        #print query + values
        self.db.ExecuteNonQuery("update " + Constants.ImagesTable + " set SHA1Digest = " + values)
        """
        for file in Globals.FileInfoList:
            if filePath == file.DirectoryPath + PlatformMethods.GetDirSeparator() + file.Name:
                file.SHA1Digest = sha1
                break
        
        for fileInfo in Globals.ImagesList:
            if filePath == fileInfo.DirectoryPath + PlatformMethods.GetDirSeparator() + fileInfo.Name:
                fileInfo.SHA1Digest = sha1
                break 
        """
        
        self.AddFileDetailsToListView()
            
    def UpdateSHA256Digest(self, dirPath, fileName):
        filePath = dirPath + PlatformMethods.GetDirSeparator() + fileName
        digest = CommonFunctions.GetSHA256Digest(filePath)
        values = self.db.SqlSQuote(digest) + " where Path='" + dirPath
        values += "'  and Name= '" + fileName + "';"
        #print query + values
        self.db.ExecuteNonQuery("update " + Constants.ImagesTable + " set SHA256Digest = " + values)
        
        """
        for file in Globals.FileInfoList:
            if filePath == file.DirectoryPath + PlatformMethods.GetDirSeparator() + file.Name:
                file.SHA256Digest = digest
                break
        
        for fileInfo in Globals.ImagesList:
            if filePath == fileInfo.DirectoryPath + PlatformMethods.GetDirSeparator() + fileInfo.Name:
                fileInfo.SHA256Digest = digest
                break
        """
        self.AddFileDetailsToListView()
            
    def UpdateSHA384Digest(self, dirPath, fileName):
        filePath = dirPath + PlatformMethods.GetDirSeparator() + fileName
        digest = CommonFunctions.GetSHA384Digest(filePath)
        values = self.db.SqlSQuote(digest) + " where Path='" + dirPath
        values += "'  and Name= '" + fileName + "';"
        #print query + values
        self.db.ExecuteNonQuery("update " + Constants.ImagesTable + " set SHA384Digest = " + values)
        
        """
        for file in Globals.FileInfoList:
            if filePath == file.DirectoryPath + PlatformMethods.GetDirSeparator() + file.Name:
                file.SHA384Digest = digest
                break
  
        for fileInfo in Globals.ImagesList:
            if filePath == fileInfo.DirectoryPath + PlatformMethods.GetDirSeparator() + fileInfo.Name:
                fileInfo.SHA384Digest = digest
                break 
        """
        self.AddFileDetailsToListView()
            
    def UpdateSHA512Digest(self, dirPath, fileName):
        filePath = dirPath + PlatformMethods.GetDirSeparator() + fileName
        digest = CommonFunctions.GetSHA512Digest(filePath)
        values = self.db.SqlSQuote(digest) + " where Path='" + dirPath
        values += "'  and Name= '" + fileName + "';"
        #print query + values
        self.db.ExecuteNonQuery("update " + Constants.ImagesTable + " set SHA512Digest = " + values)
        """
        for file in Globals.FileInfoList:
            if filePath == file.DirectoryPath + PlatformMethods.GetDirSeparator() + file.Name:
                file.SHA512Digest = digest
                break
        
        for fileInfo in Globals.ImagesList:
            if filePath == fileInfo.DirectoryPath + PlatformMethods.GetDirSeparator() + fileInfo.Name:
                fileInfo.SHA512Digest = digest
                break  
        """
        self.AddFileDetailsToListView()
        
    def CreatePopupSHASubMenu(self):
        Id = wx.NewId()
        self.popupSubMenuSHA.Append(help='', id=Id, kind=wx.ITEM_NORMAL, text='SHA1 Hash')
        self.Bind(wx.EVT_MENU, self.OnPopupMenuSHA1Digest, id=Id)
              
        Id = wx.NewId()
        self.popupSubMenuSHA.Append(help='', id=Id, kind=wx.ITEM_NORMAL, text='SHA224 Hash')
        self.Bind(wx.EVT_MENU, self.OnPopupMenuSHA224Digest, id=Id)
              
        Id = wx.NewId()
        self.popupSubMenuSHA.Append(help='', id=Id, kind=wx.ITEM_NORMAL, text='SHA256 Hash')
        self.Bind(wx.EVT_MENU, self.OnPopupMenuSHA256Digest, id=Id)
              
        Id = wx.NewId()
        self.popupSubMenuSHA.Append(help='', id=Id, kind=wx.ITEM_NORMAL, text='SHA384 Hash')
        self.Bind(wx.EVT_MENU, self.OnPopupMenuSHA384Digest, id=Id)
              
        Id = wx.NewId()
        self.popupSubMenuSHA.Append(help='', id=Id, kind=wx.ITEM_NORMAL, text='SHA512 Hash')
        self.Bind(wx.EVT_MENU, self.OnPopupMenuSHA512Digest, id=Id)

    def OnPopupMenuSHA1Digest(self, event):
        busy = wx.BusyInfo("Please wait! Generating SHA1 Hash...")
        wx.Yield()
        self.SetCursor(wx.HOURGLASS_CURSOR)
        self.GenerateHashes(self.UpdateSHA1Digest)
        self.AddFileDetailsToListView()
        self.SetCursor(wx.STANDARD_CURSOR)
        event.Skip()
    
    def OnPopupMenuSHA224Digest(self, event):
        busy = wx.BusyInfo("Please wait! Generating SHA224 Hash...")
        wx.Yield()
        self.SetCursor(wx.HOURGLASS_CURSOR)
        self.GenerateHashes(self.UpdateSHA224Digest)
        self.AddFileDetailsToListView()
        self.SetCursor(wx.STANDARD_CURSOR)
        event.Skip()
        
    def OnPopupMenuSHA256Digest(self, event):
        busy = wx.BusyInfo("Please wait! Generating SHA256 Hash...")
        wx.Yield()
        self.SetCursor(wx.HOURGLASS_CURSOR)
        self.GenerateHashes(self.UpdateSHA256Digest)
        self.AddFileDetailsToListView()
        self.SetCursor(wx.STANDARD_CURSOR)
        event.Skip()
        
    def OnPopupMenuSHA384Digest(self, event):
        busy = wx.BusyInfo("Please wait! Generating SHA384 Hash...")
        wx.Yield()
        self.SetCursor(wx.HOURGLASS_CURSOR)
        self.GenerateHashes(self.UpdateSHA384Digest)
        self.AddFileDetailsToListView()
        self.SetCursor(wx.STANDARD_CURSOR)
        event.Skip()
    
    def OnPopupMenuSHA512Digest(self, event):
        busy = wx.BusyInfo("Please wait! Generating SHA512 Hash...")
        wx.Yield()
        self.SetCursor(wx.HOURGLASS_CURSOR)
        self.GenerateHashes(self.UpdateSHA512Digest)
        self.AddFileDetailsToListView()
        self.SetCursor(wx.STANDARD_CURSOR)
        event.Skip()
        
    # Used by the ColumnSorterMixin, see wx/lib/mixins/listctrl.py
    def GetListCtrl(self):
        return self.listFilesDetails

    # Used by the ColumnSorterMixin, see wx/lib/mixins/listctrl.py
    def GetSortImages(self):
        return (self.sm_dn, self.sm_up)
    
    def OpenFileInHTMLView(self, path):
        try:
            self.htmlCtrl.LoadPage(path)
        except Exception, e:
            CommonFunctions.ShowErrorMessage(self, 'HTML Viewer could not open the file: "%s"\n Error: %s' % (path, e))
            
            
    def OnListThumbnailsListItemSelected(self, event):
        #if self.IsFileSelected():
            
        self.index = self.listThumbnails.GetFirstSelected()
            
        if self.index >=0:
            self.selectedFileName = PlatformMethods.Encode(self.listThumbnails.GetItem(self.index).GetText())
            self.fullFilePath = self.GetFilePath(self.selectedFileName)
            self.OpenFileInHTMLView(self.fullFilePath)
            #self.fullFilePath = os.path.join(PlatformMethods.Decode(self.dirPath), self.selectedFileName)
            
        
        event.Skip()
        
    def OnListFilesDetailsItemSelected(self, event):
        self.index = self.listFilesDetails.GetFirstSelected()
        if self.index >=0:

            self.selectedFileName = PlatformMethods.Encode(self.listFilesDetails.GetItem(self.index).GetText())
            #self.fullFilePath = os.path.join(PlatformMethods.Decode(self.dirPath), self.selectedFileName)
            self.fullFilePath = self.GetFilePath(self.selectedFileName)
            self.OpenFileInHTMLView(self.fullFilePath)
            
        event.Skip()
        
        
    def AddListColumnHeadings(self):
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
        
    def AddFileDetailsToListView(self):
        self.SetCursor(wx.HOURGLASS_CURSOR)
        self.FileInfo = {}
        self.listFilesDetails.DeleteAllItems()
        totalFiles = 0
        IconDict = {}
        
        NoLog = wx.LogNull()
        for fileInfoList in self.FileList:
            totalFiles += 1
            #print "totalFiles = " + str(totalFiles)
            listItem = []
            
            listItem.append(PlatformMethods.Decode(fileInfoList[0]))
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
                newPath = os.path.join(Globals.CasePath, newPath)
            
            #print newPath
            listItem.append(PlatformMethods.Decode(newPath))
            
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

        NoLog = None        
        self.listFilesDetails.SetImageList(self.imageListSmallIcon, wx.IMAGE_LIST_SMALL)
        #self.CreateFileIconList(iconInfo)
        self.itemDataMap = self.FileInfo       
        items = self.FileInfo.items()
        #print items
        #print len(self.FileInfo)
        #print len(items)
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
        value = "Image"
        if totalFiles > 0:
            value = "Images"
            
        self.lblDirectoryName.SetLabel(PlatformMethods.Decode(self.newDirPath))
        self.lblFileListCount.SetLabel("of %s:  Showing %s of %s %s"%(CommonFunctions.GetCommaFormattedNumber(self.TotalPages), CommonFunctions.GetCommaFormattedNumber(totalFiles), CommonFunctions.GetCommaFormattedNumber(self.TotalFiles), value))
        #self.lblFileCount.SetLabel("of %d:  Showing str(totalFiles) %s"%(self.TotalPages,value))
        self.SetCursor(wx.STANDARD_CURSOR)
    
    def OnListColClick(self, event):
        event.Skip()
        
    def OnListFilesDetailsRightUp(self, event):
        self.rightClickedOn = 0
        self.treeViewFolders.PopupMenu(self.popupMenuFile)
        event.Skip()
        
        
    def GetPathName(self, item, treeCtrl):
        
        pathName = []
        pathName.append(self.GetTreeItemText(treeCtrl, item))
        #parentItem = self.treeDirList.GetItemParent(item)
        parentItem = treeCtrl.GetItemParent(item)
        while not (parentItem == self.root):
            pathName.insert(0, self.GetTreeItemText(treeCtrl, parentItem))
            #parentItem = self.treeDirList.GetItemParent(parentItem)
            parentItem = treeCtrl.GetItemParent(parentItem)
        

        dirPath = os.path.sep.join(pathName)
        self.newDirPath = dirPath.replace("\\\\", "\\")
        if Globals.EvidencesDict[Globals.CurrentEvidenceID]['NewLocation']:
            #self.newDirPath = dirPath
            dirPath = dirPath.replace(Globals.EvidencesDict[Globals.CurrentEvidenceID]['NewLocation'], Globals.EvidencesDict[Globals.CurrentEvidenceID]['Location'])
        
        return PlatformMethods.Encode(dirPath.replace("\\\\", "\\"))

        
        
    def OnTreeViewFoldersSelChanged(self, event, treeCtrl=None):
        #item = self.treeViewFolders.GetSelection()
        if treeCtrl == None:
            treeCtrl = self.treeViewFolders
        
        item = treeCtrl.GetSelection()
        if not self.root:
            self.root = self.treeViewFolders.GetRoot()
            
        if not item == self.root:
            self.dirPath = self.GetPathName(item, treeCtrl)
            self.FileList = []
            self.ThumbnailList = []
            
            db = SqliteDatabase(Globals.FileSystemName)
            if not db.OpenConnection():
                return
            
            query = "select count(*) from %s where DirPath = ? and Category = 'image';"%(Globals.CurrentEvidenceID)
            row = db.FetchOneRow(query, (self.dirPath,))
            self.TotalFiles = int(row[0])
            self.TotalPages = (self.TotalFiles/Constants.MaxThumbnailsPerPage)
            if (int(row[0])%Constants.MaxThumbnailsPerPage) > 0:
                self.TotalPages += 1
                
            self.AddPageNumbersToListChoice(self.TotalPages)
            self.choiceFileListPageNum.SetSelection(0)
            self.choiceThumbnailPageNum.SetSelection(0)
            self.UpdateFilesInDirectory(0)
            db.CloseConnection()
 
        event.Skip()
  
     
    def AddPageNumbersToListChoice(self, pages):
        self.choiceFileListPageNum.Clear()
        self.choiceThumbnailPageNum.Clear()
        for page in range(1, pages+1):
            self.choiceFileListPageNum.Append(str(page))
            self.choiceThumbnailPageNum.Append(str(page))
        
    def OnTreeViewFoldersRightUp(self, event):
        self.rightClickedOn = 1
        self.treeViewFolders.PopupMenu(self.popupMenuDir)
        event.Skip()
        
    def GetTreeItemText(self, treeCtrl, item):
        if item:
            #return self.treeViewFolders.GetItemText(item)
            return treeCtrl.GetItemText(item)
        else:
            return ""
        
    
    def UpdateFilesInDirectory(self, offset):
        #self.FileList = DBFunctions.GetFileList(Globals.ImagesFileName, Globals.CurrentEvidenceID, self.dirPath, offset)
        self.FileList = DBFunctions.GetImageFileList(Globals.FileSystemName, Globals.CurrentEvidenceID, self.dirPath, offset=offset)
        self.DisplayThumbnails()
        self.AddFileDetailsToListView()
    
    def OnChoiceFileListPageNumChoice(self, event):
        selection = self.choiceFileListPageNum.GetStringSelection()
        self.UpdateFilesInDirectory(int(selection)-1)
        self.choiceThumbnailPageNum.SetStringSelection(selection)
        event.Skip()


    def OnChoiceThumbnailPageNumChoice(self, event):
        selection = self.choiceThumbnailPageNum.GetStringSelection()
        self.UpdateFilesInDirectory(int(selection)-1)
        self.choiceFileListPageNum.SetStringSelection(selection)
        event.Skip()
       
       
       
        
    def GenerateThumbnailsRecursively(self, dbFileSystem, dbImage, dirPath):
        
        deleteQuery = "delete from %s where DirPath = ?"%Globals.CurrentEvidenceID
        dbImage.ExecuteNonQuery(deleteQuery, (dirPath,))
        insertQuery = "insert into %s (DirPath, Filename, Thumbnail) values (?,?,?)"%Globals.CurrentEvidenceID
        selectSubDirQuery = "select SubDirList from  %s%s where DirPath = ?"%(Globals.CurrentEvidenceID, Constants.DirListTable)
        selectImageFiles = "select Name, NewPath from %s where DirPath = ? and Category = 'image';"%(Globals.CurrentEvidenceID)
 
        fileRows = dbFileSystem.FetchAllRows(selectImageFiles, (dirPath, ))
        for row in fileRows:
            if row[1]: #if the file has a new path; compressed files for ex.
                imagePath = os.path.join(Globals.CasePath.encode('utf-8', 'replace'), row[1])
            else:
                myDirPath = dirPath
                if Globals.EvidencesDict[Globals.CurrentEvidenceID]['NewLocation']:
                    myDirPath = row[0].replace(Globals.EvidencesDict[Globals.CurrentEvidenceID]['Location'], Globals.EvidencesDict[Globals.CurrentEvidenceID]['NewLocation'])
                    
                imagePath = os.path.join(myDirPath, row[0])
                    
            try:
                Thumbnail = CommonFunctions.GetThumbnail(imagePath).GetData()
                dbImage.ExecuteMany(insertQuery, [(dirPath, row[0], cPickle.dumps(Thumbnail))])
                Thumbnail = None
            except Exception, value:
                self.log.write('Error Creating Thumbnail for file %s : Value:: %s\n'%(PlatformMethods.Encode(imagePath), str(value)))
                self.log.flush()
                continue
            
        fileRows = None
        subDirRows = dbFileSystem.FetchAllRows(selectSubDirQuery, (dirPath,))
        for row in subDirRows:
            subDirList = cPickle.loads(str(row[0]))
            for subdir in subDirList:
                myDirPath = os.path.join(dirPath, subdir)
                self.GenerateThumbnailsRecursively(dbFileSystem, dbImage, myDirPath)

            subDirList = None
            
        subDirRows = None

        
    def OnPopupMenuGenerateThumbnails(self, event):
        
        item = self.treeViewFolders.GetSelection()
        if not self.root:
            self.root = self.treeViewFolders.GetRoot()
            
        if item == self.root:
            #root is not a directory path
            return
        
        self.dirPath = self.GetPathName(item, self.treeViewFolders)
        busy = wx.BusyInfo("Recursively Generating Thumbnails... Just Relax! It may take a few minutes...")
        wx.Yield()    

        dbFileSystem = SqliteDatabase(Globals.FileSystemName)
        if not dbFileSystem.OpenConnection():
            return
        

        dbImage = SqliteDatabase(Globals.ImagesFileName)
        if not dbImage.OpenConnection():
            return

        self.GenerateThumbnailsRecursively(dbFileSystem, dbImage, self.dirPath)

        dbImage.CloseConnection()
        dbFileSystem.CloseConnection()
        dbImage = None
        dbFileSystem = None
        event.Skip()
       
    def OnPopupMenuFileMark_for_exportMenu(self, event):
        
        db = SqliteDatabase(Globals.FileSystemName)
        if not db.OpenConnection():
            return
        
        #query = "update %s set Export=1 where Name=%s and DirPath=%s;"%(Globals.CurrentEvidenceID, db.SqlSQuote(self.fileInfo[0]), db.SqlSQuote(self.fileInfo[1]))
        query = "update %s set Export=1 where Name=? and DirPath=?;"%(Globals.CurrentEvidenceID) #, db.SqlSQuote(self.fileInfo[0]), db.SqlSQuote(self.fileInfo[1]))
        db.ExecuteNonQuery(query, (self.fileInfo[0], self.fileInfo[1],))
        db.CloseConnection()
        #if  Globals.frmGlobalMainForm.GetViewsCheckedMenu() == 'Details':  
        self.listFilesDetails.SetStringItem(self.index, 10, 'Yes')
        
        self.UpdateExportButtonLabel()
        event.Skip()

    def OnPopupMenuFileUnmark_for_exportMenu(self, event):
        if not self.IsFileSelected():
            return
        
        db = SqliteDatabase(Globals.FileSystemName)
        if not db.OpenConnection():
            return
        #query = "update %s set Export=0 where Name=%s and DirPath=%s;"%(Globals.CurrentEvidenceID, db.SqlSQuote(self.fileInfo[0]), db.SqlSQuote(self.fileInfo[1]))
        query = "update %s set Export=0 where Name=? and DirPath=?;"%(Globals.CurrentEvidenceID)#, db.SqlSQuote(self.fileInfo[0]), db.SqlSQuote(self.fileInfo[1]))
        db.ExecuteNonQuery(query, (self.fileInfo[0], self.fileInfo[1],))
        db.CloseConnection()
        #if  Globals.frmGlobalMainForm.GetViewsCheckedMenu() == 'Details':  
        self.listFilesDetails.SetStringItem(self.index, 10, 'No')
            
        self.UpdateExportButtonLabel()
        event.Skip()
        
    def OnBtnExportMarkedFilesButton(self, event):
        
        dlg = wx.DirDialog(self, "Select Destination Folder")
        try:
            if dlg.ShowModal() == wx.ID_OK:
                dir = dlg.GetPath()
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
        log = open(os.path.join(Globals.CasePath, 'Export.log'), 'a')
        db = SqliteDatabase(Globals.FileSystemName)
        if not db.OpenConnection():
            return
    
        query = "select DirPath || '%s' || Name, NewPath from %s where Export = 1;"%(os.path.sep, Globals.CurrentEvidenceID)
        rows = db.FetchAllRows(query)
        db.CloseConnection()
        for row in rows:
            if row[1]:
                sourcePath = Globals.CasePath + row[1]
                destPath = row[1][:row[1].rfind(os.path.sep)]
                destPath = destination + destPath
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
                
            if not os.path.exists(destPath):
                try:
                    os.makedirs(destPath)
                except Exception, msg:
                    log.write("%s Error: %s\n"%(PlatformMethods.Encode(sourcePath), str(msg)))
        
            try:
                shutil.copy2(sourcePath, destPath)
            except Exception, msg:
                log.write("%s Error: %s\n"%(sourcePath, msg))
                
        log.close()
        
    def OnPopupMenuDirMarkAllFilesForExport(self, event):
        if self.dirPath == "":
            return
        
        db = SqliteDatabase(Globals.FileSystemName)
        if not db.OpenConnection():
            return
        query = "update %s set Export=1 where DirPath=?;"%(Globals.CurrentEvidenceID)
        db.ExecuteNonQuery(query, (self.dirPath,))
        db.CloseConnection()
        #if  Globals.frmGlobalMainForm.GetViewsCheckedMenu() == 'Details':  
         
        for i in range(len(self.FileList)):
            self.listFilesDetails.SetStringItem(i, 10, 'Yes')

        self.UpdateExportButtonLabel()
        event.Skip()
        
    def OnPopupMenuDirUnmarkAllFilesForExport(self, event):
        if self.dirPath == "":
            return
        
        db = SqliteDatabase(Globals.FileSystemName)
        if not db.OpenConnection():
            return
        query = "update %s set Export=0 where DirPath=?;"%(Globals.CurrentEvidenceID)
        db.ExecuteNonQuery(query, (self.dirPath,))
        db.CloseConnection()
        #if  Globals.frmGlobalMainForm.GetViewsCheckedMenu() == 'Details':  
         
        for i in range(len(self.FileList)):
            self.listFilesDetails.SetStringItem(i, 10, 'No')

        self.UpdateExportButtonLabel()
        event.Skip()
        
    
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
            self.log.write("Error Failed to Generate MD5 Hash. Value: %s\n"%(str(value)))
            self.log.flush()
        
        self.db.CloseConnection()
        if Globals.frmGlobalMainForm.GetViewsCheckedMenu() == 'Details':
            self.AddFileDetailsToListView()
        self.SetCursor(wx.STANDARD_CURSOR)
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
        
def ReadImages():
    #from stat import *
    db = SqliteDatabase("caseNew.ima")
    if not db.OpenConnection():
        return
    query = "INSERT INTO " + Constants.ImagesTable + " (Name, Path, Category, " 
    query += "Extension, MimeType, Description, OpenCommand, Size, "
    query += "ModifiedTime, CreatedTime, AccessedTime, Width, Height, Thumbnail ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)"

    DBFunctions.SetupThumbnailsTable("caseNew.ima", True)
    dirPath = "C:\\Images"
    for root, dirs, files in os.walk(dirPath):
        
        #for dir in dirs:
            #dirPath = os.path.join(root, dir)
            #print 'dirPath = %s'%dir
            
            
            for afile in files:
                manyValues = []
                print 'fileName = %s'%afile
                filePath = os.path.join(root, afile)
                if (filePath.rfind('.') == -1):
                    continue


                #if not (filePath.rfind('.') == -1):
                extension = filePath[filePath.rfind('.'):]
                fileType = wx.TheMimeTypesManager.GetFileTypeFromExtension(extension)
                if not fileType:
                    continue
                
                mimeType = fileType.GetMimeType() or "Unknown"
                if mimeType.find("image/") != 0:
                    continue

                #self.CurrentFileName = fileName
                newFile = Classes.ImageFile()
                newFile.FileExtension = extension
                newFile.Name = afile
                newFile.DirectoryPath = root
                #fileExtension = ""
                newFile.MimeType = mimeType
                newFile.Description = fileType.GetDescription() or "Unknown"
                cmd = fileType.GetOpenCommand(filePath, mimeType)
                newFile.OpenCommand = PlatformMethods.Decode(cmd)
                category = CommonFunctions.GetFileCategory(newFile.FileExtension)
                newFile.Category = category

                try:
                    st = os.stat(filePath)
                except Exception, value:
                    print "Failed to get information on file: %s Error: %s"%(filePath, value)
                    continue
                else:
                    newFile.ModifiedTime = st[ST_MTIME]
                    newFile.Size = st[ST_SIZE]
                    newFile.CreatedTime = st[ST_CTIME]
                    newFile.AccessedTime = st[ST_ATIME]
                    """
                    def getDoubleRightHeadBitmap():
                    return BitmapFromImage(getDoubleRightHeadImage())

                    
                    """
                    thumbnail = GetThumbnail(filePath)
                    buf = thumbnail.GetData()
                    #print "buf len = ", len(buf)
                    #thumbnail.LoadStream(buf)
                    #im = getImageFromStream(buf)
                    size = thumbnail.GetSize()
                    newFile.Width = size[0]
                    newFile.Height = size[1]
                    newFile.Thumbnail = wx.BitmapFromBuffer(size[0], size[1], buf) #BitmapFromImage(im) #.ConvertToBitmap() #thumbnail.ConvertToBitmap()
                    #print newFile.Thumbnail
                    if not newFile.Thumbnail:
                        continue
                    
                    

                    #for byte in thumbnail.GetDataBuffer():
                    #    buf.append(byte)
                    #print buf
                    #buf = StringIO()
                    #thumbnail.SaveFile(buf, imghdr.what(filePath))
                    #return buf.getvalue()
                    #values.append(buffer(marshal.dumps(col)))
                    tupleValue = (newFile.Name, newFile.DirectoryPath,
                     newFile.Category, newFile.FileExtension,
                     newFile.MimeType, newFile.Description, newFile.OpenCommand,
                     newFile.Size, newFile.ModifiedTime,
                     newFile.CreatedTime, newFile.AccessedTime, newFile.Width, newFile.Height, buffer(buf))
                    Globals.ImagesList.append(newFile)
                    manyValues.append(tupleValue)

                    db.ExecuteMany(query, manyValues)  
                    
    db.CloseConnection()
    
def getImageFromStream(data):
    stream = cStringIO.StringIO(data)
    return ImageFromStream(stream)

def GetThumbnail(filePath):
    "Generate thumbnail (returns rawdata)"
    #try:
    im = wx.Image(filePath)
    #im.LoadFile(filePath)
    """

    if not im:
        return None
    except:
        return None
    """
    size = im.GetSize()
    if (size[0] <= 100 and size[1] <= 100):
        pos = wx.Point((100-size[0])/2, (100-size[1])/2)
        #Resize(self, Size size, Point pos, int r=-1, int g=-1, int b=-1) -> Image
        im.Resize(wx.Size(100, 100), pos, 202, 225, 255)
    else:
        oldWidth = size[0]
        oldHeight = size[1]
        newHeight = -1
        newWidth = -1
        aspectRatio = 1
        if oldHeight > oldWidth:
            newHeight = 100
            aspectRatio = oldHeight/float(oldWidth)
        else:
            newWidth = 100
            aspectRatio = oldWidth/float(oldHeight)
        
        if newHeight == 100:
            newWidth = int(newHeight/float(aspectRatio))
        else:
            newHeight = int(newWidth/float(aspectRatio))
            
        im.Rescale(newWidth, newHeight, wx.IMAGE_QUALITY_HIGH)
        pos = wx.Point((100-newWidth)/2, (100-newHeight)/2)
        im.Resize(wx.Size(100, 100), pos, 202, 225, 255)
        
    return im #.ConvertToBitmap()
    #im.thumbnail(Constants.ThumbnailSize, Image.ANTIALIAS)
    #print 'size ', im.size
    #return getImage(im.tostring())
    #return im
    """
    buf = StringIO()
    im.save(buf, imghdr.what(filePath))
    #return buf.getvalue()
    width = im.size[0]
    height = im.size[1]
    return wx.BitmapFromBuffer(width, height, buf.getvalue())
    """
    #im.show()
    #return im.tobitmap()
    #return None
def LoadThumbnails(self):
    if len(Globals.ImagesList) > 0:
        return
    
    db = SqliteDatabase("caseNew.ima")
    if not db.OpenConnection():
        return
    
    query = "select Name, Path, Width, Height, Thumbnail, Extension, Category, Size, CreatedTime, ModifiedTime, "
    query += "AccessedTime, FileOwner, MimeType, Description, MD5Digest, SHA1Digest, SHA224Digest, "
    query += "SHA256Digest, SHA384Digest, SHA512Digest from " + Constants.ImagesTable + ";"
    rows = db.FetchAllRows(query)
    """
           
    Extension, Category, Size, CreatedTime, ModifiedTime, "
    query += "AccessedTime, FileOwner, MimeType, Description, MD5Digest, SHA1Digest, SHA224Digest, "
    query += "SHA256Digest, SHA384Digest, SHA512Digest
     """
    for row in rows:
        imgFile = Classes.FileInfo()
        imgFile.Name = row[0]
        imgFile.DirectoryPath = row[1]
        imgFile.Width = int(row[2])
        imgFile.Height = int(row[3])
        imgFile.Thumbnail = wx.BitmapFromBuffer(imgFile.Width, imgFile.Height, row[4])
        imgFile.Extension = row[5]
        imgFile.Category = row[6]
        imgFile.Size = row[7]
        imgFile.CreatedTime = row[8]
        imgFile.ModifiedTime = row[9]
        imgFile.AccessedTime = row[10]
        imgFile.FileOwner = row[11]
        imgFile.MimeType = str(row[12])
        imgFile.Description = str(row[13])
        imgFile.MD5Digest = str(row[14])
        imgFile.SHA1Digest = str(row[15])
        imgFile.SHA224Digest = str(row[16])
        imgFile.SHA256Digest = str(row[17])
        imgFile.SHA384Digest = str(row[18])
        imgFile.SHA512Digest = str(row[19])
        Globals.ImagesList.append(imgFile)

      
    db.CloseConnection()
    

class WindowHolder(wx.MDIParentFrame):
    def __init__(self, prnt, id, title, CentralID = ""):
		# First, call the base class' __init__ method to create the frame
        wx.MDIParentFrame.__init__(self, id=id, name='', parent=prnt,
            pos=wx.Point(0, 0), size=wx.Size(1280, 1024),
            style=wx.DEFAULT_FRAME_STYLE, title=title)
              
        """
        self.imageViewer = create(self)
        self.imageViewer.Show(True)
        self.imageViewer.Activate()
        self.imageViewer.Maximize(True)
        """
        Globals.frmGlobalImages = create(self)
        Globals.frmGlobalImages.Show(True)
        Globals.frmGlobalImages.Activate()
        Globals.frmGlobalImages.Maximize(True)
    
# Every wxWidgets application must have a class derived from wx.App
class MyApp(wx.App):

	# wxWindows calls this method to initialize the application
    def OnInit(self):
        
       
        # Create an instance of our customized Frame class
        #ReadImages()
        Globals.ImagesFileName = "caseNew.ima"
        #LoadThumbnails()
        frame = WindowHolder(None, -1, "Image Viewer")
        frame.Show(True)

        # Tell wxWindows that this is our main window
        #self.SetTopWindow(frame)

        # Return a success flag
        return True



if __name__ == "__main__":
    app = MyApp(0)	# Create an instance of the application class
    app.MainLoop()	# Tell it to start processing events
    
"""
if __name__ == "__main__":
    app = wx.PySimpleApp()
    frame = MDIChildImages(None, None)
    frame.Show(True)
    app.MainLoop()
    
"""