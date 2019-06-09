#Boa:MiniFrame:MDIChildImages

import wx, sys, os
import wx.lib.buttons
from wx.lib.anchors import LayoutAnchors
import  wx.lib.mixins.listctrl  as  listmix

from SqliteDatabase import *
import Globals
import PlatformMethods
import CommonFunctions
import Constants

import  images
from FileTreeView import *
from FileCategoryView import *

def create(parent):
    return MDIChildImages(parent)

class CustomListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, ID, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        
        
[wxID_MDICHILDIMAGES, wxID_MDICHILDIMAGESBTNCLOSE, 
 wxID_MDICHILDIMAGESIMGFOLDER, wxID_MDICHILDIMAGESLBLDIRECTORYNAME, 
 wxID_MDICHILDIMAGESLISTCTRL1, wxID_MDICHILDIMAGESLISTTHUMBNAILS, 
 wxID_MDICHILDIMAGESNOTEBOOKIMAGES, wxID_MDICHILDIMAGESPANEL1, 
 wxID_MDICHILDIMAGESPANEL2, wxID_MDICHILDIMAGESPANIMAGES, 
 wxID_MDICHILDIMAGESPANTHUMBNAILS, wxID_MDICHILDIMAGESPANVIEW, 
 wxID_MDICHILDIMAGESPANVIEWFOLDERS, wxID_MDICHILDIMAGESTREEVIEWFOLDERS, 
] = [wx.NewId() for _init_ctrls in range(14)]

[wxID_MDICHILDIMAGESPOPUPMENUDIRMD5HASHCHILDREN, 
 wxID_MDICHILDIMAGESPOPUPMENUDIRMD5HASHSELECTED, 
] = [wx.NewId() for _init_coll_popupMenuDir_Items in range(2)]

[wxID_MDICHILDIMAGESPOPUPMENUFILEGENMD5FILES, 
 wxID_MDICHILDIMAGESPOPUPMENUFILEGENSHA, 
 wxID_MDICHILDIMAGESPOPUPMENUFILEMENUITEMOPENFILE, 
 wxID_MDICHILDIMAGESPOPUPMENUFILEMENUITEMVIEWFILE, 
] = [wx.NewId() for _init_coll_popupMenuFile_Items in range(4)]

[wxID_MDICHILDIMAGESPOPUPMENUSHASHA1DIGEST, 
 wxID_MDICHILDIMAGESPOPUPMENUSHASHA224DIGEST, 
 wxID_MDICHILDIMAGESPOPUPMENUSHASHA256DIGEST, 
 wxID_MDICHILDIMAGESPOPUPMENUSHASHA384DIGEST, 
 wxID_MDICHILDIMAGESPOPUPMENUSHASHA512DIGEST, 
] = [wx.NewId() for _init_coll_popupMenuSHA_Items in range(5)]

class MDIChildImages(wx.MDIChildFrame, listmix.ColumnSorterMixin):

    def _init_coll_popupMenuFile_Items(self, parent):
        # generated method, don't edit

        parent.Append(help='',
              id=wxID_MDICHILDIMAGESPOPUPMENUFILEMENUITEMVIEWFILE,
              kind=wx.ITEM_NORMAL, text='View File/Properties')
        parent.Append(help='',
              id=wxID_MDICHILDIMAGESPOPUPMENUFILEMENUITEMOPENFILE,
              kind=wx.ITEM_NORMAL, text='Open File')
        parent.AppendSeparator()
        parent.Append(help='', id=wxID_MDICHILDIMAGESPOPUPMENUFILEGENMD5FILES,
              kind=wx.ITEM_NORMAL, text=u'Generate MD5 Digest')
        parent.AppendMenu(help='', id=wxID_MDICHILDIMAGESPOPUPMENUFILEGENSHA,
              submenu=self.popupMenuSHA, text='Generate SHA Digests')
        self.Bind(wx.EVT_MENU, self.OnPopupMenuFileGenmd5filesMenu,
              id=wxID_MDICHILDIMAGESPOPUPMENUFILEGENMD5FILES)
        self.Bind(wx.EVT_MENU, self.OnPopupMenuFileMenuitemopenfileMenu,
              id=wxID_MDICHILDIMAGESPOPUPMENUFILEMENUITEMOPENFILE)
        self.Bind(wx.EVT_MENU, self.OnPopupMenuFileMenuitemviewfileMenu,
              id=wxID_MDICHILDIMAGESPOPUPMENUFILEMENUITEMVIEWFILE)
        self.Bind(wx.EVT_MENU, self.OnPopupMenuFileGensha1Menu,
              id=wxID_MDICHILDIMAGESPOPUPMENUFILEGENSHA)

    def _init_coll_popupMenuSHA_Items(self, parent):
        # generated method, don't edit

        parent.Append(help='', id=wxID_MDICHILDIMAGESPOPUPMENUSHASHA1DIGEST,
              kind=wx.ITEM_NORMAL, text='SHA1 Digest')
        parent.Append(help='', id=wxID_MDICHILDIMAGESPOPUPMENUSHASHA224DIGEST,
              kind=wx.ITEM_NORMAL, text='SHA224 Digest')
        parent.Append(help='', id=wxID_MDICHILDIMAGESPOPUPMENUSHASHA256DIGEST,
              kind=wx.ITEM_NORMAL, text='SHA256Digest')
        parent.Append(help='', id=wxID_MDICHILDIMAGESPOPUPMENUSHASHA384DIGEST,
              kind=wx.ITEM_NORMAL, text='SHA384 Digest')
        parent.Append(help='', id=wxID_MDICHILDIMAGESPOPUPMENUSHASHA512DIGEST,
              kind=wx.ITEM_NORMAL, text='SHA512 Digest')
        self.Bind(wx.EVT_MENU, self.OnPopupMenuSHASha1digestMenu,
              id=wxID_MDICHILDIMAGESPOPUPMENUSHASHA1DIGEST)
        self.Bind(wx.EVT_MENU, self.OnPopupMenuSHASha224digestMenu,
              id=wxID_MDICHILDIMAGESPOPUPMENUSHASHA224DIGEST)
        self.Bind(wx.EVT_MENU, self.OnPopupMenuSHASha256digestMenu,
              id=wxID_MDICHILDIMAGESPOPUPMENUSHASHA256DIGEST)
        self.Bind(wx.EVT_MENU, self.OnPopupMenuSHASha384digestMenu,
              id=wxID_MDICHILDIMAGESPOPUPMENUSHASHA384DIGEST)
        self.Bind(wx.EVT_MENU, self.OnPopupMenuSHASha512digestMenu,
              id=wxID_MDICHILDIMAGESPOPUPMENUSHASHA512DIGEST)

    def _init_coll_popupMenuDir_Items(self, parent):
        # generated method, don't edit

        parent.Append(help='',
              id=wxID_MDICHILDIMAGESPOPUPMENUDIRMD5HASHSELECTED,
              kind=wx.ITEM_NORMAL, text=u'Generate MD5 Hash Selected Folder')
        parent.Append(help='',
              id=wxID_MDICHILDIMAGESPOPUPMENUDIRMD5HASHCHILDREN,
              kind=wx.ITEM_NORMAL, text=u'Generate MD5 Hash Children')
        self.Bind(wx.EVT_MENU, self.OnPopupMenuDirMd5hashselectedMenu,
              id=wxID_MDICHILDIMAGESPOPUPMENUDIRMD5HASHSELECTED)
        self.Bind(wx.EVT_MENU, self.OnPopupMenuDirMd5hashchildrenMenu,
              id=wxID_MDICHILDIMAGESPOPUPMENUDIRMD5HASHCHILDREN)

    def _init_coll_notebookImages_Pages(self, parent):
        # generated method, don't edit

        parent.AddPage(imageId=-1, page=self.panView, select=True, text='View')
        parent.AddPage(imageId=-1, page=self.panel1, select=False,
              text='Timeline')
        parent.AddPage(imageId=-1, page=self.panel2, select=False,
              text='Steganalysis')

    def _init_utils(self):
        # generated method, don't edit
        self.popupMenuDir = wx.Menu(title='')

        self.popupMenuFile = wx.Menu(title='')

        self.popupMenuSHA = wx.Menu(title='')

        self._init_coll_popupMenuDir_Items(self.popupMenuDir)
        self._init_coll_popupMenuFile_Items(self.popupMenuFile)
        self._init_coll_popupMenuSHA_Items(self.popupMenuSHA)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.MDIChildFrame.__init__(self, id=wxID_MDICHILDIMAGES,
              name='MDIChildImages', parent=prnt, pos=wx.Point(470, 259),
              size=wx.Size(1050, 687), style=wx.DEFAULT_FRAME_STYLE,
              title='Image Analyzer')
        self._init_utils()
        self.SetClientSize(wx.Size(1042, 656))
        self.SetBackgroundColour(wx.Colour(125, 152, 221))
        self.SetIcon(wx.Icon('./Images/FNSFIcon.ico',wx.BITMAP_TYPE_ICO))
        self.SetAutoLayout(True)
        self.Bind(wx.EVT_SIZE, self.OnMDIChildImagesSize)

        self.panImages = wx.Panel(id=wxID_MDICHILDIMAGESPANIMAGES,
              name='panImages', parent=self, pos=wx.Point(8, 488),
              size=wx.Size(1024, 152), style=wx.TAB_TRAVERSAL)
        self.panImages.SetBackgroundColour(wx.Colour(225, 236, 255))
        self.panImages.SetConstraints(LayoutAnchors(self.panImages, True, True,
              True, True))

        self.notebookImages = wx.Notebook(id=wxID_MDICHILDIMAGESNOTEBOOKIMAGES,
              name='notebookImages', parent=self.panImages, pos=wx.Point(8, 8),
              size=wx.Size(1007, 0), style=0)
        self.notebookImages.SetAutoLayout(False)
        self.notebookImages.SetConstraints(LayoutAnchors(self.notebookImages,
              True, True, True, True))

        self.panView = wx.Panel(id=wxID_MDICHILDIMAGESPANVIEW, name='panView',
              parent=self.notebookImages, pos=wx.Point(0, 0), size=wx.Size(999,
              0), style=wx.TAB_TRAVERSAL)
        self.panView.SetAutoLayout(False)
        self.panView.SetBackgroundColour(wx.Colour(225, 236, 255))
        self.panView.SetConstraints(LayoutAnchors(self.panView, True, True,
              True, True))

        self.panel1 = wx.Panel(id=wxID_MDICHILDIMAGESPANEL1, name='panel1',
              parent=self.notebookImages, pos=wx.Point(0, 0), size=wx.Size(999,
              0), style=wx.TAB_TRAVERSAL)

        self.panel2 = wx.Panel(id=wxID_MDICHILDIMAGESPANEL2, name='panel2',
              parent=self.notebookImages, pos=wx.Point(0, 0), size=wx.Size(999,
              0), style=wx.TAB_TRAVERSAL)

        self.panThumbnails = wx.Panel(id=wxID_MDICHILDIMAGESPANTHUMBNAILS,
              name='panThumbnails', parent=self, pos=wx.Point(8, 8),
              size=wx.Size(1024, 176), style=wx.TAB_TRAVERSAL)
        self.panThumbnails.SetAutoLayout(True)

        self.panViewFolders = wx.Panel(id=wxID_MDICHILDIMAGESPANVIEWFOLDERS,
              name='panViewFolders', parent=self, pos=wx.Point(8, 176),
              size=wx.Size(200, 304), style=wx.TAB_TRAVERSAL)
        self.panViewFolders.SetBackgroundColour(wx.Colour(225, 236, 255))
        self.panViewFolders.SetAutoLayout(True)

        self.treeViewFolders = wx.TreeCtrl(id=wxID_MDICHILDIMAGESTREEVIEWFOLDERS,
              name='treeViewFolders', parent=self.panViewFolders,
              pos=wx.Point(8, 8), size=wx.Size(184, 288),
              style=wx.HSCROLL | wx.VSCROLL | wx.TR_HAS_BUTTONS)
        self.treeViewFolders.SetConstraints(LayoutAnchors(self.treeViewFolders,
              True, True, True, True))

        self.listThumbnails = wx.ListView(id=wxID_MDICHILDIMAGESLISTTHUMBNAILS,
              name='listThumbnails', parent=self.panThumbnails, pos=wx.Point(8,
              48), size=wx.Size(1008, 120), style=wx.VSCROLL | wx.LC_ICON)
        self.listThumbnails.Bind(wx.EVT_LIST_ITEM_SELECTED,
              self.OnListThumbnailsListItemSelected,
              id=wxID_MDICHILDIMAGESLISTTHUMBNAILS)

        self.btnClose = wx.Button(id=wxID_MDICHILDIMAGESBTNCLOSE, label='Close',
              name='btnClose', parent=self.panImages, pos=wx.Point(936, 16),
              size=wx.Size(75, 23), style=0)
        self.btnClose.SetConstraints(LayoutAnchors(self.btnClose, False, True,
              True, False))
        self.btnClose.Bind(wx.EVT_BUTTON, self.OnBtnCloseButton,
              id=wxID_MDICHILDIMAGESBTNCLOSE)

        self.listCtrl1 = wx.ListCtrl(id=wxID_MDICHILDIMAGESLISTCTRL1,
              name='listCtrl1', parent=self, pos=wx.Point(368, 288),
              size=wx.Size(200, 100), style=wx.LC_ICON)

        self.imgFolder = wx.StaticBitmap(bitmap=wx.Bitmap(u'Images/folder_new.gif',
              wx.BITMAP_TYPE_GIF), id=wxID_MDICHILDIMAGESIMGFOLDER,
              name=u'imgFolder', parent=self.panThumbnails, pos=wx.Point(8, 8),
              size=wx.Size(24, 24), style=0)
        self.imgFolder.SetConstraints(LayoutAnchors(self.imgFolder, True, True,
              False, False))

        self.lblDirectoryName = wx.StaticText(id=wxID_MDICHILDIMAGESLBLDIRECTORYNAME,
              label=u'NMT', name=u'lblDirectoryName', parent=self.panThumbnails,
              pos=wx.Point(40, 16), size=wx.Size(26, 16), style=0)
        self.lblDirectoryName.SetForegroundColour(wx.Colour(0, 0, 187))
        self.lblDirectoryName.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, u'Tahoma'))
        self.lblDirectoryName.SetConstraints(LayoutAnchors(self.lblDirectoryName,
              True, True, False, False))

        self._init_coll_notebookImages_Pages(self.notebookImages)

    def __init__(self, parent):
        self._init_ctrls(parent)
        wx.BeginBusyCursor()
        self.FileInfo = {}
        self.dirPath = ""
        #self.lblDirectoryName.SetLabel(PlatformMethods.Convert(self.dirPath))
        """
        self.CreateListControl()
        self.treeDirView = True
        self.FilesList = []
        if len(Globals.FileInfoList) > 1:
            #if Globals.fileTreeView is None:
            #Globals.fileTreeView = FileTreeView(self, self.treeDirList)
            self.fileTreeView = FileTreeView(self, self.treeDirList)
            self.treeDirList.Show(True)
            self.TreeViewRoot = self.fileTreeView.AddDirectoryTreeNodes()
            self.root = self.TreeViewRoot
            #self.CreateTreeControl()
        """
        
        wx.EndBusyCursor()
        
    def checkStatusRange(self, event):
        return event.GetDragStatus() != wx.SASH_STATUS_OUT_OF_RANGE

    def doLayout(self):
        #wx.LayoutAlgorithm().LayoutWindow(self, self.panel1)
        #self.panel1.Refresh()
        #print 'lay out'
        #if self:
        wx.LayoutAlgorithm().LayoutWindow(self) #, self.remainingSpace)
            #wx.LayoutAlgorithm().LayoutMDIFrame(self)
            #self.GetClientWindow().Refresh()
            #print 'lay out1'
        #return None

    def OnMDIChildImagesSize(self, event):
        self.doLayout()
        event.Skip()


    def OnSashTopSashDragged(self, event):
        if self.checkStatusRange(event):
            self.sashTop.SetDefaultSize(wx.Size(1000, event.GetDragRect().height))
            self.doLayout()
        event.Skip()

    def OnSashLeftSashDragged(self, event):
        if self.checkStatusRange(event):
            self.sashLeft.SetDefaultSize(wx.Size(event.GetDragRect().width, 1000))
            self.doLayout()
        event.Skip()

    def OnSashBottomSashDragged(self, event):
        if self.checkStatusRange(event):
            self.sashBottom.SetDefaultSize(wx.Size(1000, event.GetDragRect().height))
            self.doLayout()
        event.Skip()

    def OnSashRightSashDragged(self, event):
        if self.checkStatusRange(event):
            self.sashRight.SetDefaultSize(wx.Size(event.GetDragRect().width, 1000))
            self.doLayout()
        event.Skip()
        
    def ShowDirectoryTreeView(self):
        #self.ShowProjectProperties(True)
        self.notebookProject.Show(True)
        
    
    def CreateListControl(self):
        listID = wx.NewId()
        self.listFilesDetails = CustomListCtrl(self.panFileList, listID,
                                 pos=wx.Point(8,48), size=wx.Size(800, 584),
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
        """
        self.lstFileList = wx.ListCtrl(id=wxID_MDICHILDFILELISTLSTFILELIST,
              name=u'lstFileList', parent=self.panPluglinList, pos=wx.Point(8,
              48), size=wx.Size(728, 464),
              style=wx.LC_REPORT | wx.HSCROLL | wx.VSCROLL)
        self.lstFileList.SetConstraints(LayoutAnchors(self.lstFileList, True,
              True, True, True))
        self.lstFileList.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, u'Tahoma'))
        """
        
       
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
        
        info.m_format = wx.LIST_FORMAT_LEFT
        info.m_text = "Size"
        self.listFilesDetails.InsertColumnInfo(1, info)
        
        info.m_format = wx.LIST_FORMAT_LEFT
        info.m_text = "Created Time"
        self.listFilesDetails.InsertColumnInfo(2, info)
        
        info.m_text = "Modified Time"
        self.listFilesDetails.InsertColumnInfo(3, info)
        
        info.m_text = "Accessed Time"
        self.listFilesDetails.InsertColumnInfo(4, info)
        info.m_text = "Category"
        self.listFilesDetails.InsertColumnInfo(5, info)
        info.m_text = "File Type"
        self.listFilesDetails.InsertColumnInfo(6, info)
        info.m_text = "Description"
        self.listFilesDetails.InsertColumnInfo(7, info)
        info.m_text = "MD5 Digest"
        self.listFilesDetails.InsertColumnInfo(8, info)
        info.m_text = "SHA1 Digest"
        self.listFilesDetails.InsertColumnInfo(9, info)
        info.m_text = "SHA224 Digest"
        self.listFilesDetails.InsertColumnInfo(10, info)
        info.m_text = "SHA256 Digest"
        self.listFilesDetails.InsertColumnInfo(11, info)
        info.m_text = "SHA384 Digest"
        self.listFilesDetails.InsertColumnInfo(12, info)
        info.m_text = "SHA512 Digest"
        self.listFilesDetails.InsertColumnInfo(13, info)
    
    def AddFileDetailsToListView(self):
        #self.treeDirView = treeDirView
        #self.dirPath = dirPath
        self.SetCursor(wx.HOURGLASS_CURSOR)
        self.FileInfo = {}
        self.listFilesDetails.ClearAll()
        self.AddListColumnHeadings()
        totalFiles = 0
        #iconInfo = {}
        self.imageListSmallIcon = None
        self.imageListSmallIcon = wx.ImageList(16, 16)
        IconDict = {}
        #tbd: get file specific icon and display
        #self.idx1 = self.imageListSmallIcon.Add(images.getSmilesBitmap())
        self.sm_up = self.imageListSmallIcon.Add(images.getSmallUpArrowBitmap())
        self.sm_dn = self.imageListSmallIcon.Add(images.getSmallDnArrowBitmap())
        
        for fileInfo in self.FilesList:
            """
            found = False
            if self.treeDirView:
                if fileInfo.DirectoryPath == self.dirPath:
                    found = True
            else:
                if self.dirPath == "Unknown":
                    if fileInfo.MimeType == "Unknown" and fileInfo.Description == "Unknown":
                        found = True
                else:
                    if fileInfo.MimeType.find(self.dirPath) >= 0:
                        #typeList = fileInfo.MimeType.split("/")
                        #for type in typeList:
                    #if fileInfo.MimeType == self.dirPath:
                        found = True
                    if not found:
                        if fileInfo.Description == self.dirPath and fileInfo.MimeType == "Unknown":
                            found = True
            if found:
            """
            totalFiles += 1
            #print "totalFiles = " + str(totalFiles)
            listItem = []
            if self.treeDirView:
                listItem.append(PlatformMethods.Convert(fileInfo.Name))
            else:
                listItem.append(os.path.join(PlatformMethods.Convert(fileInfo.DirectoryPath), PlatformMethods.Convert(fileInfo.Name)))
            listItem.append(CommonFunctions.ConvertByteToKilobyte(fileInfo.Size))
            listItem.append(CommonFunctions.GetShortDateTime(fileInfo.CreatedTime))
            listItem.append(CommonFunctions.GetShortDateTime(fileInfo.ModifiedTime))
            listItem.append(CommonFunctions.GetShortDateTime(fileInfo.AccessedTime))
            listItem.append(fileInfo.Category)
            listItem.append(PlatformMethods.Convert(fileInfo.MimeType))
            listItem.append(PlatformMethods.Convert(fileInfo.Description))
            listItem.append(fileInfo.MD5Digest)
            listItem.append(fileInfo.SHA1Digest)
            listItem.append(fileInfo.SHA224Digest)
            listItem.append(fileInfo.SHA256Digest)
            listItem.append(fileInfo.SHA384Digest)
            listItem.append(fileInfo.SHA512Digest)
            #self.listFilesDetails.Append(listItem)
            #print listItem
            self.FileInfo[totalFiles] = tuple(listItem)
            #print self.FileInfo
            iconFound = False
            if not (fileInfo.Name.rfind('.') == -1):
                fileExtension = fileInfo.Name[fileInfo.Name.rfind('.'):]
                fileType = wx.TheMimeTypesManager.GetFileTypeFromExtension(fileExtension)
                if fileType:
                    #fullFileName = os.path.join(self.dirPath, data[0])
                    try:
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
                    except:
                        print 'error occured'
                        
            if not iconFound:
                bmp = images.getNoFile16Bitmap()
                #bmp.SetSize(wx.Size(16, 16))
                #iconInfo[totalFiles] = bmp
                IconDict[totalFiles] = self.imageListSmallIcon.Add(bmp)

                
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
            self.listFilesDetails.SetItemData(index, key)
            #except:
            #    continue
            
        """
        items = musicdata.items()
        for key, data in items:
            index = self.list.InsertImageStringItem(sys.maxint, data[0], self.sm_dn)
            self.list.SetStringItem(index, 1, data[1])
            self.list.SetStringItem(index, 2, data[2])
            self.list.SetItemData(index, key)
        """
           
        self.listFilesDetails.SetColumnWidth(0, 250)
        self.listFilesDetails.SetColumnWidth(1, 50)
        self.listFilesDetails.SetColumnWidth(2, 100)
        self.listFilesDetails.SetColumnWidth(3, 100)
        self.listFilesDetails.SetColumnWidth(4, 100)
        self.listFilesDetails.SetColumnWidth(5, 50)
        self.listFilesDetails.SetColumnWidth(6, 100)
        self.listFilesDetails.SetColumnWidth(7, 100)
        self.listFilesDetails.SetColumnWidth(8, 125)
        value = "file"
        if totalFiles > 0:
            value = "files"
        self.lblDirectoryName.SetLabel(PlatformMethods.Convert(self.dirPath) + " (" + str(totalFiles) + " " + value + " )")
        self.SetCursor(wx.STANDARD_CURSOR)
    
    
    def UpdateFilesInDirectory(self):
        self.FilesList = []
        for fileInfo in Globals.FileInfoList:
            found = False
            if self.treeDirView:
                if fileInfo.DirectoryPath == self.dirPath:
                    found = True
            else:
                if self.dirPath == "Unknown":
                    if fileInfo.MimeType == "Unknown" and fileInfo.Description == "Unknown":
                        found = True
                else:
                    if fileInfo.MimeType.find(self.dirPath) >= 0:
                        #typeList = fileInfo.MimeType.split("/")
                        #for type in typeList:
                    #if fileInfo.MimeType == self.dirPath:
                        found = True
                    if not found:
                        if fileInfo.Description == self.dirPath and fileInfo.MimeType == "Unknown":
                            found = True
            if found:
                self.FilesList.append(fileInfo)
        
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
        for fileInfo in self.FilesList:
            totalFiles += 1
            #print "totalFiles = " + str(totalFiles)
            #listItem = []
            if self.treeDirView:
                #listItem.append(PlatformMethods.Convert(fileInfo.Name))
                fileName = PlatformMethods.Convert(fileInfo.Name)
            else:
                #listItem.append(os.path.join(PlatformMethods.Convert(fileInfo.DirectoryPath), PlatformMethods.Convert(fileInfo.Name)))
                fileName = os.path.join(PlatformMethods.Convert(fileInfo.DirectoryPath), PlatformMethods.Convert(fileInfo.Name))
            iconFound = False
            if not (fileInfo.Name.rfind('.') == -1):
                fileExtension = fileInfo.Name[fileInfo.Name.rfind('.'):]
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
                    #except:
                    #    iconFound = False
                        
            if not iconFound:
                bmp = images.getSmileBitmap()
                #iconInfo[totalFiles] = bmp
                ilMax = self.imageListLargeIcon.Add(bmp)
                    
            self.listFilesIcons.InsertImageStringItem(sys.maxint, fileName, ilMax)
       
        value = "file"
        if totalFiles > 0:
            value = "files"
        self.lblDirectoryName.SetLabel(PlatformMethods.Convert(self.dirPath) + " (" + str(totalFiles) + " " + value + " )")
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

        
    def IsFileSelected(self):
        if  Globals.frmGlobalMainForm.GetViewsCheckedMenu() == 'Details':
            self.index = self.listFilesDetails.GetFirstSelected()
        else:
            self.index = self.listFilesIcons.GetFirstSelected()
            
        if self.index >=0:
            if self.treeDirView:
                if  Globals.frmGlobalMainForm.GetViewsCheckedMenu() == 'Details':
                    self.selectedFileName = PlatformMethods.Convert(self.listFilesDetails.GetItem(self.index).GetText())
                    self.fullFilePath = os.path.join(PlatformMethods.Convert(self.dirPath), self.selectedFileName)
                else:
                    self.selectedFileName = PlatformMethods.Convert(self.listFilesIcons.GetItem(self.index).GetText())
                    self.fullFilePath = os.path.join(PlatformMethods.Convert(self.dirPath), self.selectedFileName)
            else:
                if  Globals.frmGlobalMainForm.GetViewsCheckedMenu() == 'Details':
                    self.fullFilePath = PlatformMethods.Convert(self.listFilesDetails.GetItem(self.index).GetText())
                else:
                    self.fullFilePath = PlatformMethods.Convert(self.listFilesIcons.GetItem(self.index).GetText())
                
                self.dirPath = self.fullFilePath[:self.fullFilePath.rfind(PlatformMethods.GetDirSeparator())]
                self.selectedFileName = self.fullFilePath[self.fullFilePath.rfind(PlatformMethods.GetDirSeparator())+1:]
                #print "fileName%s"%self.selectedFileName
                #print 'filePath%s'%self.fullFilePath
                #print 'dirPath=%s'%self.dirPath
            return True
        else:
            dlg = wx.MessageDialog(self, 'Please select a file from the list.',
              'Error', wx.OK | wx.ICON_ERROR)
            try:
                dlg.ShowModal()
            finally:
                dlg.Destroy()
                return False
            
            
    def OnListFilesDoubleClick(self, event):
        if self.IsFileSelected():
            self.OpenFile()
        event.Skip()

           
    def OpenFile(self):
        """
        for fileInfo in Globals.FileInfoList:
            if self.fullFilePath == os.path.join(PlatformMethods.Convert(fileInfo.DirectoryPath), PlatformMethods.Convert(fileInfo.Name)):
                cmd = PlatformMethods.Convert(fileInfo.OpenCommand)
        """
        fileExtension = self.fullFilePath[self.fullFilePath.rfind('.'):]
        fileType = wx.TheMimeTypesManager.GetFileTypeFromExtension(fileExtension)
        if fileType:
            mimeType = fileType.GetMimeType() or ""
            #newFile.MimeType = mimeType
            #newFile.Description = fileType.GetDescription() or "Unknown"
            cmd = fileType.GetOpenCommand(self.fullFilePath, mimeType)
            os.system('start '+cmd)
        #break
        
    def GetTreeItemText(self, treeCtrl, item):
        if item:
            #return self.treeDirList.GetItemText(item)
            return treeCtrl.GetItemText(item)
        else:
            return ""
        
    def GetAncestorsName(self, item, treeCtrl):
        parentsName = []
        #parentItem = self.treeDirList.GetItemParent(item)
        parentItem = treeCtrl.GetItemParent(item)
        while not (parentItem == self.root):
            if self.treeDirView:
                parentsName.insert(0, PlatformMethods.GetDirSeparator())
            else:
                parentsName.insert(0, "/")
            parentsName.insert(0, self.GetTreeItemText(treeCtrl, parentItem))
            #parentItem = self.treeDirList.GetItemParent(parentItem)
            parentItem = treeCtrl.GetItemParent(parentItem)
        return ''.join(parentsName)
    
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
            self.dirPath = self.GetAncestorsName(item, treeCtrl)
            #dirPath += self.treeDirList.GetItemText(item)
            self.dirPath += self.GetTreeItemText(treeCtrl, item)
            #print dirPath
            if self.treeDirView:
                if self.dirPath.count(PlatformMethods.GetDirSeparator()) == 0:
                     self.dirPath += PlatformMethods.GetDirSeparator()

                self.dirPath = PlatformMethods.ConvertFilePath(self.dirPath)
           
            """
            if not Globals.frmGlobalFileList:
                #GlobalMethods.PRINT("Network Scanner Loaded...")
                import MDIChildFileList
                Globals.frmGlobalFileList = MDIChildFileList.create(self)
            """
            self.UpdateFilesInDirectory()
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
        if len(Globals.FileInfoList) > 1:
            self.ShowDirectoryTreeView()
            self.root = self.TreeViewRoot
        event.Skip()

    def OnBtnCategoryViewButton(self, event):
        self.btnDirTreeView.Enable(True)
        self.btnDirTreeView.SetValue(False)
        self.btnCategoryView.Enable(False)
        self.treeDirView = False
        if len(Globals.FileInfoList) > 1:
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
        if Globals.fileCategoryView is None:
            Globals.fileCategoryView = FileCategoryView(self, self.treeCatList)
            self.CategoryViewRoot = Globals.fileCategoryView.AddCategoryTreeNodes()
        
        self.treeCatList.Show(True)
        self.treeDirList.Show(False)
        

    def OnTreeCatListTreeSelChanged(self, event):
        self.OnTreeDirListTreeSelChanged(event, self.treeCatList)
        event.Skip()


    def OnTreeDirListRightUp(self, event):
        self.treeDirList.PopupMenu(self.popupMenuDir)
        event.Skip()

    def OnPopupMenuDirMd5hashselectedMenu(self, event):
        if self.dirPath == "":
            return
        files = os.listdir(self.dirPath)
        self.db = SqliteDatabase(Globals.MACFileName)
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
        md5Digest = CommonFunctions.GetMD5HexDigest(filePath)
        values = self.db.SqlSQuote(md5Digest) + " where DirectoryPath='" + dirPath
        values += "'  and FileName= '" + fileName + "';"
        #print query + values
        self.db.ExecuteNonQuery("update " + Constants.FileInfoTable + " set MD5Digest = " + values)
        for file in Globals.FileInfoList:
            if filePath == file.DirectoryPath + PlatformMethods.GetDirSeparator() + file.Name:
                file.MD5Digest = md5Digest
                break
        """
        for fileInfo in self.FilesList:
            if filePath == fileInfo.DirectoryPath + PlatformMethods.GetDirSeparator() + fileInfo.Name:
                fileInfo.MD5Digest = md5Digest
                break
        """
        
    def UpdateSHA224Digest(self, dirPath, fileName):
        filePath = dirPath + PlatformMethods.GetDirSeparator() + fileName
        digest = CommonFunctions.GetSHA224Digest(filePath)
        values = self.db.SqlSQuote(digest) + " where DirectoryPath='" + dirPath
        values += "'  and FileName= '" + fileName + "';"
        #print query + values
        self.db.ExecuteNonQuery("update " + Constants.FileInfoTable + " set SHA224Digest = " + values)
        for file in Globals.FileInfoList:
            if filePath == file.DirectoryPath + PlatformMethods.GetDirSeparator() + file.Name:
                file.SHA224Digest = digest
                break
            
        if  Globals.frmGlobalMainForm.GetViewsCheckedMenu() == 'Details':  
            self.AddFileDetailsToListView()
        
    def UpdateSHA1Digest(self, dirPath, fileName):
        filePath = dirPath + PlatformMethods.GetDirSeparator() + fileName
        sha1 = CommonFunctions.GetSHA1Digest(filePath)
        values = self.db.SqlSQuote(sha1) + " where DirectoryPath='" + dirPath
        values += "'  and FileName= '" + fileName + "';"
        #print query + values
        self.db.ExecuteNonQuery("update " + Constants.FileInfoTable + " set SHA1Digest = " + values)
        for file in Globals.FileInfoList:
            if filePath == file.DirectoryPath + PlatformMethods.GetDirSeparator() + file.Name:
                file.SHA1Digest = sha1
                break
            
        if  Globals.frmGlobalMainForm.GetViewsCheckedMenu() == 'Details':  
            self.AddFileDetailsToListView()
            
    def UpdateSHA256Digest(self, dirPath, fileName):
        filePath = dirPath + PlatformMethods.GetDirSeparator() + fileName
        digest = CommonFunctions.GetSHA256Digest(filePath)
        values = self.db.SqlSQuote(digest) + " where DirectoryPath='" + dirPath
        values += "'  and FileName= '" + fileName + "';"
        #print query + values
        self.db.ExecuteNonQuery("update " + Constants.FileInfoTable + " set SHA256Digest = " + values)
        for file in Globals.FileInfoList:
            if filePath == file.DirectoryPath + PlatformMethods.GetDirSeparator() + file.Name:
                file.SHA256Digest = digest
                break
            
        if  Globals.frmGlobalMainForm.GetViewsCheckedMenu() == 'Details':  
            self.AddFileDetailsToListView()
            
    def UpdateSHA384Digest(self, dirPath, fileName):
        filePath = dirPath + PlatformMethods.GetDirSeparator() + fileName
        digest = CommonFunctions.GetSHA384Digest(filePath)
        values = self.db.SqlSQuote(digest) + " where DirectoryPath='" + dirPath
        values += "'  and FileName= '" + fileName + "';"
        #print query + values
        self.db.ExecuteNonQuery("update " + Constants.FileInfoTable + " set SHA384Digest = " + values)
        for file in Globals.FileInfoList:
            if filePath == file.DirectoryPath + PlatformMethods.GetDirSeparator() + file.Name:
                file.SHA384Digest = digest
                break
            
        if  Globals.frmGlobalMainForm.GetViewsCheckedMenu() == 'Details':  
            self.AddFileDetailsToListView()
            
    def UpdateSHA512Digest(self, dirPath, fileName):
        filePath = dirPath + PlatformMethods.GetDirSeparator() + fileName
        digest = CommonFunctions.GetSHA512Digest(filePath)
        values = self.db.SqlSQuote(digest) + " where DirectoryPath='" + dirPath
        values += "'  and FileName= '" + fileName + "';"
        #print query + values
        self.db.ExecuteNonQuery("update " + Constants.FileInfoTable + " set SHA512Digest = " + values)
        for file in Globals.FileInfoList:
            if filePath == file.DirectoryPath + PlatformMethods.GetDirSeparator() + file.Name:
                file.SHA512Digest = digest
                break
            
        if  Globals.frmGlobalMainForm.GetViewsCheckedMenu() == 'Details':  
            self.AddFileDetailsToListView()
            
    def OnPopupMenuDirMd5hashchildrenMenu(self, event):
        if self.dirPath == "":
            return
        self.db = SqliteDatabase(Globals.MACFileName)
        if not self.db.OpenConnection():
            return
        
        sums = [0, 1] # 0 files 1 directory so far
        self.SetCursor(wx.HOURGLASS_CURSOR)
        try:
            os.path.walk(self.dirPath, self.UpdateGroupMD5Digest, sums)
        except Exception, value:
            print "Failed to walk directories. Error: %s"%(value)
        
        self.db.CloseConnection()
        if  Globals.frmGlobalMainForm.GetViewsCheckedMenu() == 'Details':
            self.AddFileDetailsToListView()
        self.SetCursor(wx.STANDARD_CURSOR)
        event.Skip()


    def UpdateGroupMD5Digest(self, sms, dirName, fileList):
        query = "update " + Constants.FileInfoTable + " set MD5Digest = "
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
        if not self.IsFileSelected():
            return
        self.db = SqliteDatabase(Globals.MACFileName)
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
        if self.IsFileSelected():
            self.OpenFile()
        event.Skip()

    def OnPopupMenuFileMenuitemopenfileMenu(self, event):
        if self.IsFileSelected():
            self.OpenFile()
        event.Skip()
        
    def GetSelectedFileInfo(self):
        self.fileInfo = None
        for fileinfo in self.FilesList:
            if PlatformMethods.Convert(fileinfo.Name) == self.selectedFileName and PlatformMethods.Convert(fileinfo.DirectoryPath) == self.dirPath:
                    self.fileInfo = fileinfo
        
        return self.fileInfo

    def OnPopupMenuFileMenuitemfilepropertiesMenu(self, event):
        if not self.IsFileSelected():
            return
        
        if not self.GetSelectedFileInfo():
            return
        
        import frmFileViewer
        fileProp = frmFileViewer.frmFileViewer(self, self.fileInfo)
        fileProp.Show()
        event.Skip()

    def OnPopupMenuFileMenuitemviewfileMenu(self, event):
        if not self.IsFileSelected():
            return
        
        if not self.GetSelectedFileInfo():
            return
        
        import frmFileViewer
        fileProp = frmFileViewer.frmFileViewer(self, self.fileInfo)
        fileProp.Show()
        event.Skip()

    def OnPopupMenuFileGensha1Menu(self, event):
        event.Skip()

    def OnPopupMenuSHASha1digestMenu(self, event):
        self.GenerateHashes(self.UpdateSHA1Digest)
            
        event.Skip()

    def OnPopupMenuSHASha224digestMenu(self, event):
        self.GenerateHashes(self.UpdateSHA224Digest)
        event.Skip()

    def OnPopupMenuSHASha256digestMenu(self, event):
        self.GenerateHashes(self.UpdateSHA256Digest)
        event.Skip()

    def OnPopupMenuSHASha384digestMenu(self, event):
        self.GenerateHashes(self.UpdateSHA384Digest)
        event.Skip()

    def OnPopupMenuSHASha512digestMenu(self, event):
        self.GenerateHashes(self.UpdateSHA512Digest)
        event.Skip()

    def OnListThumbnailsListItemSelected(self, event):
        event.Skip()


        
class WindowHolder(wx.MDIParentFrame):
    def __init__(self, prnt, id, title, CentralID = ""):
		# First, call the base class' __init__ method to create the frame
        wx.MDIParentFrame.__init__(self, id=id, name='', parent=prnt,
            pos=wx.Point(0, 0), size=wx.Size(1280, 1024),
            style=wx.DEFAULT_FRAME_STYLE, title=title)
              
        self.imageViewer = create(self)

    
# Every wxWidgets application must have a class derived from wx.App
class MyApp(wx.App):

	# wxWindows calls this method to initialize the application
	def OnInit(self):

		# Create an instance of our customized Frame class
		frame = WindowHolder(None, -1, "Image Viewer")
		frame.Show(True)

		# Tell wxWindows that this is our main window
		self.SetTopWindow(frame)

		# Return a success flag
		return True


if __name__ == "__main__":
    app = MyApp(0)	# Create an instance of the application class
    app.MainLoop()	# Tell it to start processing events
        
