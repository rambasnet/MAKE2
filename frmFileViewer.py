#-----------------------------------------------------------------------------
# Name:        frmFileViewer.py
# Purpose:     
#
# Author:      Ram Basnet
#
# Created:     2007/11/12
# RCS-ID:      $Id: frmFileViewer.py,v 1.5 2007/11/13 19:52:48 rbasnet Exp $
# Copyright:   (c) 2006
# Licence:     <your licence>
# New field:   Whatever
#-----------------------------------------------------------------------------
#Boa:MDIChild:frmFileViewer

import wx
from wx.lib.anchors import LayoutAnchors
import wx.grid
import wx.html
import wx.aui
import time
import re, string
import os.path, sys
#import wx.lib.delayedresult as delayedresult
import wx.lib.newevent
import  thread
import cStringIO
from stat import *

from SqliteDatabase import *
import Globals
import Constants
import CommonFunctions
import DBFunctions
import Classes
import PlatformMethods
import images
import codecs
from HexViewWindow import *
from TextViewWindow import *
import hexedit

if sys.platform == 'win32':
    wildcard = "All files (*.*)|*.*|"\
               "Text files (*.txt)|*.txt"
else:
    wildcard = "All files|*|"\
               "Text files (*.txt)|*.txt"

class frmFileViewer(wx.Frame):
    
    def __init__(self, parent, fileInfo=None):

        wx.Frame.__init__(self, id=wx.NewId(), name='frmFileViewer', title='File Viewer',
              parent=parent, pos=wx.DefaultPosition, size=wx.Size(965, 789),
              style=wx.DEFAULT_FRAME_STYLE |wx.SUNKEN_BORDER |wx.CLIP_CHILDREN)
              
        self.Center(wx.BOTH)
        # tell FrameManager to manage this frame        
        self.auiManager = wx.aui.AuiManager()
                
        self.auiManager.SetManagedWindow(self)
        
        self._perspectives = []
        self.n = 0
        self.x = 0
        
        self.SetIcon(images.getMAKE2Icon())
        # min size for the frame itself isn't completely done.
        # see the end up FrameManager::Update() for the test
        # code. For now, just hard code a frame minimum size
        self.SetMinSize(wx.Size(400, 300))
        self.Bind(wx.EVT_CLOSE, self.OnExit)
        self.InitMenuBar()
        self.InitToolBar()
        self.InitPanes()
        # "commit" all changes made to FrameManager   
        
        #self.auiManager.GetArtProvider().SetMetric(wx.aui.AUI_DOCKART_CAPTION_FONT, 10)
        self.auiManager.GetArtProvider().SetMetric(wx.aui.AUI_DOCKART_CAPTION_SIZE, 20)
        self.auiManager.GetArtProvider().SetColor(wx.aui.AUI_DOCKART_BACKGROUND_COLOUR, wx.Colour(125, 152, 221))
        self.auiManager.GetArtProvider().SetColor(wx.aui.AUI_DOCKART_SASH_COLOUR, wx.Colour(125, 152, 221))
        self.auiManager.GetArtProvider().SetColor(wx.aui.AUI_DOCKART_INACTIVE_CAPTION_COLOUR, wx.Colour(183, 183, 255))
        self.auiManager.GetArtProvider().SetColor(wx.aui.AUI_DOCKART_INACTIVE_CAPTION_GRADIENT_COLOUR, wx.Colour(125, 152, 221))
        self.auiManager.Update()
        
        self.fileInfo = fileInfo
        if not self.fileInfo is None:
            self.LoadFileProperties()
        
        self. AttachSearchEvents()
        self.HexViewCenterPane = True
        
    # create menu
    def InitMenuBar(self):
        mb = wx.MenuBar()
        self.fileMenu = wx.Menu()
        self.fileMenu.Append(wx.ID_OPEN, ("&Open...\tCtrl+O"), "", wx.ITEM_NORMAL)
        #self.menu_file.Append(ID_OPENDEVICE, _("Open &Device..."), "", wx.ITEM_NORMAL)
        #self.fileMenu.Append(wx.ID_REVERT, _("&Reload\tCtrl+R"), "", wx.ITEM_NORMAL)
        self.fileMenu.Append(wx.ID_CLOSE, ("&Close\tCtrl+W"), "", wx.ITEM_NORMAL)
        self.fileMenu.AppendSeparator()
        self.fileMenu.Append(wx.ID_EXIT, ("&Quit"), "", wx.ITEM_NORMAL)
        #fileMenu.Append(wx.ID_EXIT, "Exit")
        self.Bind(wx.EVT_MENU, self.OnOpenFile, id=wx.ID_OPEN)
        self.Bind(wx.EVT_MENU, self.OnCloseFile, id=wx.ID_CLOSE)
        self.Bind(wx.EVT_MENU, self.OnExit, id=wx.ID_EXIT)

        self.viewMenu = wx.Menu()
        self.IDViewFileProperties = wx.NewId()
        self.IDViewHash = wx.NewId()
        self.IDViewText = wx.NewId()
        self.IDViewHex = wx.NewId()
        self.IDViewNative = wx.NewId()
        
        self.viewMenu.AppendCheckItem(self.IDViewFileProperties, "File &Properties")
        self.viewMenu.Check(self.IDViewFileProperties, True)
        self.Bind(wx.EVT_MENU, self.OnShowFileProperties, id=self.IDViewFileProperties)
        self.viewMenu.AppendCheckItem(self.IDViewHash, "Ha&shes")
        self.viewMenu.Check(self.IDViewHash, True)
        self.Bind(wx.EVT_MENU, self.OnShowHash, id=self.IDViewHash)
        
        self.viewMenu.AppendSeparator()
        
        self.viewMenu.AppendCheckItem(self.IDViewHex, "&Hex View")
        self.viewMenu.Check(self.IDViewHex, True)
        self.Bind(wx.EVT_MENU, self.OnShowHexView, id=self.IDViewHex)
        
        self.viewMenu.AppendCheckItem(self.IDViewText, "&Text View")
        self.viewMenu.Check(self.IDViewText, True)
        self.Bind(wx.EVT_MENU, self.OnShowTextView, id=self.IDViewText)
        
        self.viewMenu.AppendCheckItem(self.IDViewNative, "&Native View")
        self.viewMenu.Check(self.IDViewNative, True)
        self.Bind(wx.EVT_MENU, self.OnShowNativeView, id=self.IDViewNative)
        
        self.viewMenu.AppendSeparator()
           
        mb.Append(self.fileMenu, "&File")
        mb.Append(self.viewMenu, "&View")
                
        self.SetMenuBar(mb)

        self.statusBar = self.CreateStatusBar(1, wx.ST_SIZEGRIP)
        self.statusBar.SetStatusText("Ready", 0)
        
        
    def InitToolBar(self):
        # create some toolbars
        self.toolBarMain = wx.ToolBar(self, wx.NewId(), wx.DefaultPosition, wx.DefaultSize,
            style=wx.TB_FLAT | wx.TB_NODIVIDER)
        self.toolBarMain.SetToolBitmapSize(wx.Size(32, 32))
        #self.toolBarMain.SetConstraints(LayoutAnchors(self.toolBarMain, True,
        #      True, True, False))
        self.toolBarMain.SetBackgroundColour(wx.Colour(183, 183, 255))
        
        self.searchUpID = wx.NewId()
        self.searchDownID = wx.NewId()
        self.toolBarMain.AddLabelTool(self.searchUpID, "SearchUp", images.getSearchUpBitmap(), shortHelp="Search Up")
        self.Bind(wx.EVT_TOOL, self.OnToolSearchUpClick, id=self.searchUpID)
        
        #add search control box
        self.searchCtrlID = wx.NewId()
        self.ctrlSearch = MySearchCtrl(self.toolBarMain, id=self.searchCtrlID, size=(150,-1), doSearch=self.DoSearch)
        self.toolBarMain.AddControl(self.ctrlSearch)
        
        self.toolBarMain.AddLabelTool(self.searchDownID, "SearchDown", images.getSearchDownBitmap(), shortHelp="Search Down")
        self.Bind(wx.EVT_TOOL, self.OnToolSearchDownClick, id=self.searchDownID)
        
        self.toolBarMain.AddSeparator()
        self.hexViewID = wx.NewId()
        tool = self.toolBarMain.AddCheckLabelTool(self.hexViewID, "HexView", images.getHexViewBitmap(),
                                    shortHelp="Click to view file in HEX (0x00) format")
        self.Bind(wx.EVT_TOOL, self.OnToolHexViewClick, id=self.hexViewID)
        
        self.toolBarMain.AddSeparator()

        self.textViewID = wx.NewId()
        tool = self.toolBarMain.AddCheckLabelTool(self.textViewID, "TextView", images.getTextViewBitmap(),
                                    shortHelp="Click to view file as Text")
        self.Bind(wx.EVT_TOOL, self.OnToolTextViewClick, id=self.textViewID)
        
        self.toolBarMain.AddSeparator()
        self.nativeViewID = wx.NewId()
        tool = self.toolBarMain.AddCheckLabelTool(self.nativeViewID, "NativeView", images.getNativeViewBitmap(),
                                    shortHelp="Click to view file using IE")
        self.Bind(wx.EVT_TOOL, self.OnToolNativeViewClick, id=self.nativeViewID)        
        self.toolBarMain.Realize()
        
        self.toolBarMain.ToggleTool(self.hexViewID, True)
        self.auiManager.AddPane(self.toolBarMain, wx.aui.AuiPaneInfo().
                      Name("tb2").Caption("Toolbar 2").
                      ToolbarPane().Top().Row(1).
                      LeftDockable(False).RightDockable(False))
        
    def InitPanes(self):
        # add bunch of floatable panes
        self.auiManager.AddPane(self.CreateFileProperties(), wx.aui.AuiPaneInfo().
                        Name("Property").Caption("File Properties").
                        Left().Layer(1).Position(1).CloseButton(True).PinButton(True))
                        
        self.auiManager.AddPane(self.CreateHashValuesView(), wx.aui.AuiPaneInfo().
                        Name("Hash").Caption("Hash Values").
                        Left().Layer(1).Position(2).CloseButton(True))
                        
        self.auiManager.AddPane(self.CreateHTMLCtrl(), wx.aui.AuiPaneInfo().Name("NativeView").
                        Caption("IE View").Bottom().Layer(1).Position(1).CloseButton(True).MaximizeButton(True))
                
        self.auiManager.AddPane(self.CreateTextViewWindow(), wx.aui.AuiPaneInfo().Name("TextView").
                        Caption("Text View").Bottom().Layer(1).Position(2).CloseButton(True).MaximizeButton(True))
        
        self.auiManager.AddPane(self.CreateHexViewWindow(), wx.aui.AuiPaneInfo().Name("HexView").
                          CenterPane())
        # Show How To Use The Closing Panes Event
        self.Bind(wx.aui.EVT_AUI_PANE_CLOSE, self.OnPaneClose)
        
        
    def OnPaneClose(self, event):
        name = event.GetPane().name
        if name == "Property":
            self.viewMenu.Check(self.IDViewFileProperties, False)
        elif name == "Hash":
            self.viewMenu.Check(self.IDViewHash, False)
        elif name== "FloatHexView":
            self.viewMenu.Check(self.IDViewHex, False)
        elif name == "FloatTextView":
            self.viewMenu.Check(self.IDViewText, False)
        elif name == "FloatNativeView":
            self.viewMenu.Check(self.IDViewNative, False)
        event.GetPane().Hide()
        #event.Veto()

    def OnExit(self, event):
        self.auiManager.UnInit()
        self.Destroy()
        event.Skip()        
 

    def OnShowFileProperties(self, event):
        #if event.IsChecked():
        self.auiManager.GetPane("Property").Show(self.viewMenu.IsChecked(self.IDViewFileProperties))
        self.auiManager.Update()
        event.Skip()
        
    def OnShowHash(self, event):
        self.auiManager.GetPane("Hash").Show(self.viewMenu.IsChecked(self.IDViewHash))
        self.auiManager.Update()
        event.Skip()
        
    def OnShowTextView(self, event):
        #if event.IsChecked():
        #if not self.auiManager.GetPane("TextView").IsShown():
        self.auiManager.GetPane("TextView").Caption("Text View").Bottom().Layer(1).Position(2).CloseButton(True).MaximizeButton(True).Show(self.viewMenu.IsChecked(self.IDViewText))
        self.auiManager.Update()
        event.Skip()
        
    def OnShowHexView(self, event):
        #if not self.auiManager.GetPane("HexView").IsShown():
        self.auiManager.GetPane("HexView").Dockable(True).Caption("Hex View").Bottom().Layer(1).Position(1).CloseButton(True).MaximizeButton(True).Show(self.viewMenu.IsChecked(self.IDViewHex))
            #self.auiManager.GetPane("HexView").Show(self.viewMenu.IsChecked(self.IDViewHex))
        self.auiManager.Update()
        event.Skip()
        
        
    def OnShowNativeView(self, event):
        #if not self.auiManager.GetPane("NativeView").IsShown():
        self.auiManager.GetPane("NativeView").Caption("Native View").Bottom().Layer(1).Position(3).CloseButton(True).MaximizeButton(True).Show(self.viewMenu.IsChecked(self.IDViewNative))
            #self.auiManager.GetPane("FloatNativeView").
        self.auiManager.Update()
        event.Skip()
        

    def CreateFileProperties(self):
        self.panProperties = wx.Panel(id=wx.NewId(),
              name='panProperties', parent=self, pos=wx.Point(0,0), size=wx.Size(250, 424),
              style=wx.CLIP_CHILDREN | wx.TAB_TRAVERSAL)
        self.panProperties.SetAutoLayout(True)
        self.panProperties.SetBackgroundColour(wx.Colour(225, 236, 255))
        
        self.lblFileName = wx.StaticText(id=wx.NewId(),
              label=u'File Name', name=u'lblFileName',
              parent=self.panProperties, pos=wx.Point(48, 32), size=wx.Size(46,
              13), style=0)

        self.bitmapIcon = wx.StaticBitmap(bitmap=wx.NullBitmap,
              id=wx.NewId(), name=u'bitmapIcon',
              parent=self.panProperties, pos=wx.Point(8, 8), size=wx.Size(32,
              32), style=0)

        self.staticText17 = wx.StaticText(id=wx.NewId(),
              label=u'File name:', name='staticText17',
              parent=self.panProperties, pos=wx.Point(48, 8), size=wx.Size(49,
              13), style=0)

              
        self.listCtrlFileProperties = wx.ListCtrl(id=wx.NewId(),
              name='listCtrlFileProperties', parent=self.panProperties,
              pos=wx.Point(8, 56), size=wx.Size(234, 360),
              style=wx.VSCROLL | wx.LC_VRULES | wx.HSCROLL | wx.LC_HRULES | wx.LC_REPORT)
        self.listCtrlFileProperties.SetConstraints(LayoutAnchors(self.listCtrlFileProperties, True,
              True, True, True))
        self.listCtrlFileProperties.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL,
              wx.NORMAL, False, 'Tahoma'))
        self.listCtrlFileProperties.InsertColumn(col=0, format=wx.LIST_FORMAT_LEFT,
              heading='Property', width=75)
        self.listCtrlFileProperties.InsertColumn(col=1, format=wx.LIST_FORMAT_LEFT, heading='Value',
              width=150)
        return self.panProperties
    
    def CreateHTMLCtrl(self):
        self.panIEView = wx.Panel(id=wx.NewId(), parent=self, pos=wx.Point(0, 0), size=wx.Size(416, 316))
        self.panIEView.SetBackgroundColour(wx.Colour(225, 236, 255))
        self.panIEView.SetAutoLayout(True)
        
        self.htmlCtrl = wx.html.HtmlWindow(self.panIEView, -1, wx.Point(8,8), wx.Size(400, 300))
        if "gtk2" in wx.PlatformInfo:
            self.htmlCtrl.SetStandardFonts()
        self.htmlCtrl.SetConstraints(LayoutAnchors(self.htmlCtrl, True,
              True, True, True))
              
        """
        self.auiManager.AddPane(self.CreateHTMLCtrl(), wx.aui.AuiPaneInfo().
                          Caption("HTML Content").
                          Float().FloatingPosition(self.GetStartPosition()).
                          FloatingSize(wx.Size(300, 200)).CloseButton(True).MaximizeButton(True))
        self.auiManager.Update()
        """
        return self.panIEView
        
    def CreateHashValuesView(self):
        self.panHashValues = wx.Panel(id=wx.NewId(),
              name='panHashValues', parent=self, pos=wx.Point(0, 0),size=wx.Size(250, 376),
              style=wx.CLIP_CHILDREN | wx.TAB_TRAVERSAL)
        self.panHashValues.SetBackgroundColour(wx.Colour(225, 236, 255))
        self.panHashValues.SetAutoLayout(True)
             
        self.listCtrlHashValues = wx.ListCtrl(id=wx.NewId(),
              name='listCtrlHashValues', parent=self.panHashValues,
              pos=wx.Point(8, 8), size=wx.Size(234, 360),
              style=wx.VSCROLL | wx.LC_VRULES | wx.HSCROLL | wx.LC_HRULES | wx.LC_REPORT)
        self.listCtrlHashValues.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL,
              wx.NORMAL, False, 'Tahoma'))
        self.listCtrlHashValues.SetConstraints(LayoutAnchors(self.listCtrlHashValues, True,
              True, True, True))
        self.listCtrlHashValues.InsertColumn(col=0, format=wx.LIST_FORMAT_LEFT,
              heading='Algorithm', width=75)
        self.listCtrlHashValues.InsertColumn(col=1, format=wx.LIST_FORMAT_LEFT, heading='Value',
              width=150)
        return self.panHashValues
        

    def CreateHexViewWindow(self):
        self.panHexView = wx.Panel(id=wx.NewId(), parent=self, pos=wx.Point(0, 0), size=wx.Size(672, 600))
        self.panHexView.SetBackgroundColour(wx.Colour(225, 236, 255))
        self.panHexView.SetAutoLayout(True)
        self.lblStatus = wx.StaticText(id=wx.NewId(),
              label='Staus', name='lblStatus',
              parent=self.panHexView, pos=wx.Point(8, 572),
              size=wx.Size(656, 20), style=wx.ST_NO_AUTORESIZE | wx.SUNKEN_BORDER)
        self.lblStatus.SetConstraints(LayoutAnchors(self.lblStatus, True,
              False, True, True))
              
        self.hexView = HexViewWindow(self.panHexView, self.lblStatus, id=wx.NewId(), pos=wx.Point(8, 8), size=wx.Size(656, 555))
        self.hexView.SetConstraints(LayoutAnchors(self.hexView,
              True, True, True, True))
        self.hexView.Bind(wx.EVT_CONTEXT_MENU, self.OnHexViewRightUp)
        self.hexView.Bind(wx.EVT_LEFT_UP, self.OnHexViewLeftUp)
    
              
        self.hexViewer = hexedit.HexEdit()
        self.hexView.setModel(self.hexViewer)
        self.hexViewer.attach(self)
        return self.panHexView
    
    def CreateTextViewWindow(self):
        self.panTextView = wx.Panel(id=wx.NewId(), parent=self, pos=wx.Point(0, 0), size=wx.Size(672, 600))
        self.panTextView.SetBackgroundColour(wx.Colour(225, 236, 255))
        self.panTextView.SetAutoLayout(True)
        self.lblTextViewStatus = wx.StaticText(id=wx.NewId(),
              label='Staus', parent=self.panTextView, pos=wx.Point(8, 572),
              size=wx.Size(656, 20), style=wx.ST_NO_AUTORESIZE | wx.SUNKEN_BORDER)
        self.lblTextViewStatus.SetConstraints(LayoutAnchors(self.lblTextViewStatus, True,
              False, True, True))
              
        self.textView = TextViewWindow(self.panTextView, self.lblTextViewStatus, id=wx.NewId(), pos=wx.Point(8, 8), size=wx.Size(656, 555))
        self.textView.SetConstraints(LayoutAnchors(self.textView,
              True, True, True, True))
        self.textView.Bind(wx.EVT_CONTEXT_MENU, self.OnTextViewRightUp)
        self.textView.Bind(wx.EVT_LEFT_UP, self.OnTextViewLeftUp)
    
              
        self.textViewer = hexedit.HexEdit()
        self.textView.setModel(self.textViewer)
        self.textViewer.attach(self)
        return self.panTextView
            

    def LoadFileProperties(self):
        iconFound = False
        """select Name, DirPath, Size, Created, Modified, Accessed, Category, MimeType, 
        Description, MD5,  KnownFile, NewPath, SHA1, SHA224, SHA256, SHA384, SHA512
        """
        if not (self.fileInfo[0].rfind('.') == -1):
            #if self.fileInfo.Extension:
            fileExtension = self.fileInfo[0][self.fileInfo[0].rfind('.'):]
            fileType = wx.TheMimeTypesManager.GetFileTypeFromExtension(fileExtension)
            if fileType:
                info = fileType.GetIconInfo()
                if info:
                    icon, fileName, idx = info
                    if icon.Ok():
                        self.imageListLargeIcon = wx.ImageList(32, 32)
                        self.imageListLargeIcon.AddIcon(icon)
                        self.bitmapIcon.SetBitmap(self.imageListLargeIcon.GetBitmap(0))
                        iconFound = True
                        
        if not iconFound:
            self.bitmapIcon.SetBitmap(images.getNoFile32Bitmap())
        
        self.lblFileName.SetLabel(PlatformMethods.Decode(self.fileInfo[0]))
        
        index = self.listCtrlFileProperties.InsertStringItem(sys.maxint, "Type")
        self.listCtrlFileProperties.SetStringItem(index, 1, PlatformMethods.Decode(self.fileInfo[7]))
        
        index = self.listCtrlFileProperties.InsertStringItem(sys.maxint, "Location")
        if self.fileInfo[11]:
            filePath = PlatformMethods.Decode(os.path.join(Globals.CasePath, self.fileInfo[11]))
            self.listCtrlFileProperties.SetStringItem(index, 1, filePath)
            #filePath = os.path.join(PlatformMethods.Decode(newPath), PlatformMethods.Decode(self.fileInfo.Name))
        else:
            filePath = self.fileInfo[1]
            if Globals.EvidencesDict:
                if Globals.EvidencesDict[Globals.CurrentEvidenceID]['NewLocation']:
                    filePath = filePath.replace(Globals.EvidencesDict[Globals.CurrentEvidenceID]['Location'], Globals.EvidencesDict[Globals.CurrentEvidenceID]['NewLocation'])
                
            filePath = PlatformMethods.Decode(os.path.join(filePath, self.fileInfo[0]))
            self.listCtrlFileProperties.SetStringItem(index, 1, filePath)
            
            
        
        index = self.listCtrlFileProperties.InsertStringItem(sys.maxint, "Size")
        self.listCtrlFileProperties.SetStringItem(index, 1, CommonFunctions.ConvertByteToKilobyte(self.fileInfo[2]))
        
        index = self.listCtrlFileProperties.InsertStringItem(sys.maxint, "Description")
        self.listCtrlFileProperties.SetStringItem(index, 1, PlatformMethods.Decode(self.fileInfo[8]))
        
        index = self.listCtrlFileProperties.InsertStringItem(sys.maxint, "Created")
        self.listCtrlFileProperties.SetStringItem(index, 1, CommonFunctions.GetShortDateTime(self.fileInfo[3]))
        index = self.listCtrlFileProperties.InsertStringItem(sys.maxint, "Modified")
        self.listCtrlFileProperties.SetStringItem(index, 1, CommonFunctions.GetShortDateTime(self.fileInfo[4]))
        index = self.listCtrlFileProperties.InsertStringItem(sys.maxint, "Accessed")
        self.listCtrlFileProperties.SetStringItem(index, 1, CommonFunctions.GetShortDateTime(self.fileInfo[5]))
        
        index = self.listCtrlHashValues.InsertStringItem(sys.maxint, "MD5")
        self.listCtrlHashValues.SetStringItem(index, 1, PlatformMethods.Decode(self.fileInfo[9]))
        
        index = self.listCtrlHashValues.InsertStringItem(sys.maxint, "SHA1")
        self.listCtrlHashValues.SetStringItem(index, 1, PlatformMethods.Decode(self.fileInfo[12]))
        
        index = self.listCtrlHashValues.InsertStringItem(sys.maxint, "SHA224")
        self.listCtrlHashValues.SetStringItem(index, 1, PlatformMethods.Decode(self.fileInfo[13]))
        index = self.listCtrlHashValues.InsertStringItem(sys.maxint, "SHA256")
        self.listCtrlHashValues.SetStringItem(index, 1, PlatformMethods.Decode(self.fileInfo[14]))
        
        index = self.listCtrlHashValues.InsertStringItem(sys.maxint, "SHA384")
        self.listCtrlHashValues.SetStringItem(index, 1, PlatformMethods.Decode(self.fileInfo[15]))
        index = self.listCtrlHashValues.InsertStringItem(sys.maxint, "SHA512")
        self.listCtrlHashValues.SetStringItem(index, 1, PlatformMethods.Decode(self.fileInfo[16]))
        
        
        #filePath = os.path.join(PlatformMethods.Decode(self.fileInfo.DirPath), PlatformMethods.Decode(self.fileInfo.Name))
        
        if not os.path.exists(filePath):
            CommonFunctions.ShowErrorMessage(self, "File %s doesn't exists!"%filePath, error=True)
            return
        
            
        self.OpenFileInHexView(filePath)
        self.OpenFileInHTMLView(filePath)
        self.OpenFileInTextView(filePath)
        
    def OpenFileInHTMLView(self, path):
        try:
            self.htmlCtrl.LoadPage(path)
        except Exception, e:
            wx.MessageBox(
                'HTML Viewer could not open the file: "%s"\n Error: %s' % (path, e),
                "Error",
                wx.ICON_ERROR
            )
        
    def OpenFileInHexView(self, path, changedir=False):
        try:
            self.hexViewer.load(path, readonly=True)
        except IOError, e:
            wx.MessageBox(
                'Could not open the file: "%s"\n Error: %s' % (path, e),
                "Error",
                wx.ICON_ERROR
            )
    
    def OpenFileInTextView(self, path):
        try:
            self.textViewer.load(path)
        except IOError, e:
            wx.MessageBox(
                'Could not open the file: "%s"\n Error: %s' % (path, e),
                "Error",
                wx.ICON_ERROR
            )
    
    def AttachSearchEvents(self):
        #find dialog
        wx.EVT_COMMAND_FIND(self, -1, self.OnFind)
        wx.EVT_COMMAND_FIND_NEXT(self, -1, self.OnFind)
        wx.EVT_COMMAND_FIND_REPLACE(self, -1, self.OnFind)
        wx.EVT_COMMAND_FIND_REPLACE_ALL(self, -1, self.OnFind)
        wx.EVT_COMMAND_FIND_CLOSE(self, -1, self.onFindClose)
        
       
        
    def OnFind(self, evt):
        et = evt.GetEventType()
        findstring = codecs.escape_decode(evt.GetFindString())[0]
        case = bool(evt.GetFlags() & 4)
        
        def abortcheck():
            wx.Yield()
            return self._abort_find
        
        def find_next():
            self._searching = True
            self._abort_find = False
            try:
                offset = self.hexViewer.bin.find(
                    self.hexView.offset + 1,
                    findstring,
                    casesensitive=case,
                    wrap = True,
                    abortcheck=abortcheck
                )
            except StopIteration:
                self.statusBar.SetStatusText("Search aborted", 0)
                self._find_start = None
            else:
                if offset is not None:
                    self.hexView.setSelection(offset, offset+len(findstring)-1, offset=offset)
                    self.statusBar.SetStatusText("String found at offset 0x%08x"% offset, 0)
                    self._find_start = offset
                else:
                    wx.Bell()
                    self.statusBar.SetStatusText("String not found", 0)
                    self._find_start = None
            self._searching = False
        
        if et == wx.wxEVT_COMMAND_FIND or et == wx.wxEVT_COMMAND_FIND_NEXT:
            self.statusBar.SetStatusText("Searching...", 0)
            find_next()
        

        
    def onGoto(self, event):        
        dlg = wx.TextEntryDialog(
            self, 
            "Enter offset as decimal or heaxdecimal (0x123) number",
            "Goto offset"
        )
        if dlg.ShowModal() == wx.ID_OK:
            try:
                offset = long(dlg.GetValue(), 0)
            except ValueError:
                wx.MessageBox("Expected a number in decimal (123) or hex (0x123) format", "Error", wx.ICON_ERROR)
            else:
                if offset < self.hexView.model.size():
                    self.hexView.setSelection(offset, offset, offset)
                else:
                    wx.MessageBox("Can't position after file end", "Error", wx.ICON_ERROR)
        dlg.Destroy()
        
    def OnToolSearchDownClick(self, evt):
        findString = codecs.escape_decode(self.ctrlSearch.GetSearchString())[0]
        if len(findString) == 0:
            wx.MessageBox("Please enter string to search", "Error", wx.ICON_ERROR)
            return
        self.DoSearch(findString)
        
    def OnToolSearchUpClick(self, evt):
        findString = codecs.escape_decode(self.ctrlSearch.GetSearchString())[0]
        if len(findString) == 0:
            wx.MessageBox("Please enter string to search", "Error", wx.ICON_ERROR)
            return
        self.DoSearch(findString, False)
        
   
    def DoSearch(self, findString, forward=True):
        #et = evt.GetEventType()
        findString = findString.encode('latin-1')
        #case = bool(evt.GetFlags() & 4)
        self.statusBar.SetStatusText("Searching...", 0)
        #self._searching = True
        #self._abort_find = False
        try:
            if forward:
                if self.HexViewCenterPane:
                    offset = self.hexViewer.bin.find(
                        self.hexView.offset + 1,
                        findString,
                        casesensitive=False,
                        wrap = True,
                        abortcheck=None,
                        reverse=False
                    )
                else:
                    #must be Text View, no search allowed on native yet
                    offset = self.textViewer.bin.find(
                        self.textView.offset + 1,
                        findString,
                        casesensitive=False,
                        wrap = True,
                        abortcheck=None,
                        reverse=False
                    )
                    
            else:
                if self.HexViewCenterPane:
                    offset = self.hexViewer.bin.find(
                        self.hexView.offset - 1,
                        findString,
                        casesensitive=False,
                        wrap = True,
                        abortcheck=None,
                        reverse=True
                    )
                else:
                    offset = self.textViewer.bin.find(
                        self.textView.offset - 1,
                        findString,
                        casesensitive=False,
                        wrap = True,
                        abortcheck=None,
                        reverse=True
                    )
        except Exception, msg:
            wx.MessageBox(unicode(msg), "Error", wx.ICON_ERROR) 
            self.statusBar.SetStatusText("Search Failed!", 0)
            self.HexFindStart = None
            self.TextFindStart = None
        else:
            if offset is not None:
                if self.HexViewCenterPane:
                    self.hexView.setSelection(offset, offset+len(findString)-1, offset=offset)
                    self.HexFindStart = offset
                else:
                    self.textView.setSelection(offset, offset+len(findString)-1, offset=offset)
                    self.TextFindStart = offset
                    
                self.statusBar.SetStatusText("String found at offset 0x%08x" % offset, 0)
                
                return True
            else:
                wx.Bell()
                self.statusBar.SetStatusText("String not found", 0)
                self.HexFindStart = None
                self.TextFindStart = None
                return False
            
    def EnableToolbarSearchTools(self, enable=True):
        self.toolBarMain.EnableTool(self.searchUpID, enable)
        self.toolBarMain.EnableTool(self.searchDownID, enable)
        #self.toolBarMain.EnableTool(self.searchCtrlID, enable)
        self.ctrlSearch.Enable(enable)
        
        
    def OnChangeContentPane(self, event):
        """
        self.auiManager.GetPane("HexView").Show(event.GetId() == self.hexViewID)
        self.auiManager.GetPane("TextView").Show(event.GetId() == self.textViewID)
        self.auiManager.GetPane("NativeView").Show(event.GetId() == self.nativeViewID)
        """
        self.auiManager.GetPane("HexView").Show(False)
        self.auiManager.GetPane("TextView").Show(False)
        self.auiManager.GetPane("NativeView").Show(False)
        if event.GetId() == self.hexViewID:
            self.EnableToolbarSearchTools(True)
            self.HexViewCenterPane = True
            self.auiManager.GetPane("HexView").CenterPane().Show(True)
            #self.auiManager.GetPane("HexView").Hide()
            self.OnShowTextView(event)
            self.OnShowNativeView(event)
        elif event.GetId() == self.textViewID:
            self.EnableToolbarSearchTools(True)
            self.HexViewCenterPane = False
            self.auiManager.GetPane("TextView").CenterPane().Show(True)
            #self.auiManager.GetPane("HexView").Hide()
            #self.auiManager.GetPane("FloatTextView").Hide()
            self.OnShowHexView(event)
            self.OnShowNativeView(event)
        elif event.GetId() == self.nativeViewID:
            self.EnableToolbarSearchTools(False)
            self.HexViewCenterPane = True
            self.auiManager.GetPane("NativeView").CenterPane().Show(True)
            self.OnShowHexView(event)
            self.OnShowTextView(event)
            #self.OnShowHexView(event)
            #self.OnShowTextView(event)
            #OnShowNativeView
        self.auiManager.Update()
        
    def OnToolHexViewClick(self, evt):
        """
        if self.toolBarMain.GetToolState(self.hexViewID):
            self.toolBarMain.ToggleTool(self.hexViewID, True)
            self.toolBarMain.ToggleTool(self.textViewID, False)
        else:
        """
            #self.toolBarMain.EnableTool(self.hexViewID, False)
        self.toolBarMain.ToggleTool(self.hexViewID, True)
        self.toolBarMain.ToggleTool(self.textViewID, False)
        self.toolBarMain.ToggleTool(self.nativeViewID, False)
        self.OnChangeContentPane(evt)
        evt.Skip()
        
    def OnToolTextViewClick(self, evt):
        self.toolBarMain.ToggleTool(self.textViewID, True)
        self.toolBarMain.ToggleTool(self.nativeViewID, False)
        self.toolBarMain.ToggleTool(self.hexViewID, False)
        self.OnChangeContentPane(evt)
        evt.Skip()
        
    def OnToolNativeViewClick(self, evt):
        self.toolBarMain.ToggleTool(self.nativeViewID, True)
        self.toolBarMain.ToggleTool(self.textViewID, False)
        self.toolBarMain.ToggleTool(self.hexViewID, False)
        self.OnChangeContentPane(evt)
        evt.Skip()
        
    def CreateHexPopupMenu(self):
        if not hasattr(self, "IDPopupHexMenuItemSelectAll"):
            self.IDPopupHexMenuItemSelectAll = wx.NewId()
            self.IDPopupHexMenuItemCopy = wx.NewId()
            self.IDPopupHexMenuItemGoTo = wx.NewId()
            self.IDPopupHexMenuItemFind = wx.NewId()
            self.IDPopupHexMenuItemSaveSelection = wx.NewId()
            
            self.Bind(wx.EVT_MENU, self.OnHexPopupMenuItemSelectAll,
              id=self.IDPopupHexMenuItemSelectAll)
            self.Bind(wx.EVT_MENU, self.OnHexPopupMenuItemCopy,
              id=self.IDPopupHexMenuItemCopy)
              
            self.Bind(wx.EVT_MENU, self.onGoto,
              id=self.IDPopupHexMenuItemGoTo)
            self.Bind(wx.EVT_MENU, self.OnHexPopupMenuItemFind,
              id=self.IDPopupHexMenuItemFind)
            self.Bind(wx.EVT_MENU, self.OnHexPopupMenuItemSaveSelection,
              id=self.IDPopupHexMenuItemSaveSelection)
            
        popupMenu = wx.Menu()
           
        popupMenu.Append(id=self.IDPopupHexMenuItemSelectAll, kind=wx.ITEM_NORMAL, text='Select &All\tCtrl+A')
        popupMenu.AppendSeparator()
        popupMenu.Append(id=self.IDPopupHexMenuItemCopy, kind=wx.ITEM_NORMAL, text='&Copy Text\tCtrl+C')
        popupMenu.AppendSeparator()
        
        popupMenu.Append(id=self.IDPopupHexMenuItemGoTo, kind=wx.ITEM_NORMAL, text='&Go To Offset...\tCtrl+G')
        popupMenu.Append(id=self.IDPopupHexMenuItemFind, kind=wx.ITEM_NORMAL, text='&Find...\tCtrl+F')
        popupMenu.AppendSeparator()
        popupMenu.Append(id=self.IDPopupHexMenuItemSaveSelection, kind=wx.ITEM_NORMAL, text='Save Selection As...')
        
        self.hexView.PopupMenu(popupMenu)
        popupMenu.Destroy()
        
    def CreateTextPopupMenu(self):
        if not hasattr(self, "IDPopupTextMenuItemSelectAll"):
            self.IDPopupTextMenuItemSelectAll = wx.NewId()
            self.IDPopupTextMenuItemCopy = wx.NewId()
            self.IDPopupTextMenuItemGoTo = wx.NewId()
            self.IDPopupTextMenuItemFind = wx.NewId()
            self.IDPopupTextMenuItemSaveSelection = wx.NewId()
            
            self.Bind(wx.EVT_MENU, self.OnTextPopupMenuItemSelectAll,
              id=self.IDPopupTextMenuItemSelectAll)
            self.Bind(wx.EVT_MENU, self.OnTextPopupMenuItemCopy,
              id=self.IDPopupTextMenuItemCopy)
              
            self.Bind(wx.EVT_MENU, self.OnTextPopupMenuItemFind,
              id=self.IDPopupTextMenuItemFind)
            self.Bind(wx.EVT_MENU, self.OnTextPopupMenuItemSaveSelection,
              id=self.IDPopupTextMenuItemSaveSelection)
            
        popupMenu = wx.Menu()
        popupMenu.Append(id=self.IDPopupTextMenuItemSelectAll, kind=wx.ITEM_NORMAL, text='Select &All\tCtrl+A')
        popupMenu.AppendSeparator()
        popupMenu.Append(id=self.IDPopupTextMenuItemCopy, kind=wx.ITEM_NORMAL, text='&Copy Text\tCtrl+C')
        popupMenu.AppendSeparator()
        popupMenu.Append(id=self.IDPopupTextMenuItemFind, kind=wx.ITEM_NORMAL, text='&Find...\tCtrl+F')
        popupMenu.AppendSeparator()
        popupMenu.Append(id=self.IDPopupTextMenuItemSaveSelection, kind=wx.ITEM_NORMAL, text='Save Selection As...')
        
        self.textView.PopupMenu(popupMenu)
        popupMenu.Destroy()
        
    def OnHexViewRightUp(self, event):
        self.CreateHexPopupMenu()
        event.Skip()
        
    def OnTextViewRightUp(self, event):
        self.CreateTextPopupMenu()
        event.Skip()
        
    def OnHexViewLeftUp(self, event):
        event.Skip()
        
    def OnTextViewLeftUp(self, event):
        event.Skip()
        
    def OnHexPopupMenuItemSelectAll(self, event):
        end = self.hexView.model.size() - 1
        self.hexView.setSelection(0, end, offset=end)
        event.Skip()
    
    def OnTextPopupMenuItemSelectAll(self, event):
        end = self.textView.model.size() - 1
        self.textView.setSelection(0, end, offset=end)
        event.Skip()
        
        
    def OnHexPopupMenuItemCopy(self, event):
        event.Skip()
        
    def OnTextPopupMenuItemCopy(self, event):
        event.Skip()        
        
    def OnHexPopupMenuItemFind(self, event):
        self.HexFindStart = None
        data = wx.FindReplaceData()
        start, end = self.hexView.getSelection()
        if start is not None and end is not None:
            size = min(100, end - start + 1)
            data.SetFindString(codecs.escape_encode(self.hexView.model.bin.read(start, size))[0])
        dlg = wx.FindReplaceDialog(self, data, "Find", wx.FR_NOUPDOWN|wx.FR_NOWHOLEWORD)
        dlg.data = data  # save a reference to it...
        dlg.Show(True)
        event.Skip()
        
    def OnTextPopupMenuItemFind(self, event):
        self.TextFindStart = None
        data = wx.FindReplaceData()
        start, end = self.textView.getSelection()
        if start is not None and end is not None:
            size = min(100, end - start + 1)
            data.SetFindString(codecs.escape_encode(self.textView.model.bin.read(start, size))[0])
        dlg = wx.FindReplaceDialog(self, data, "Find", wx.FR_NOUPDOWN|wx.FR_NOWHOLEWORD)
        dlg.data = data  # save a reference to it...
        dlg.Show(True)
        event.Skip()
        
    def onFindClose(self, evt):
        if self._searching:
            self._abort_find = True
        #~ else:
        evt.GetDialog().Destroy()
        
    def OnHexPopupMenuItemSaveSelection(self, event):
        if self.hexView.selection_start is not None and self.hexView.selection_end is not None:
            selection_start, selection_end = self.hexView.getSelection()
            if selection_start > selection_end: #swap if start > end
                selection_start, selection_end = self.hexView.selection_end, self.hexView.selection_start
            dlg = wx.FileDialog(self, "Save Selection As...", os.getcwd(), "", PlatformMethods.GetWildcard(), wx.SAVE)
            if dlg.ShowModal() == wx.ID_OK:
                path = dlg.GetPath()
                #make a new instance to copy the stuff to
                newmodel = hexedit.HexEdit()
                newmodel.new(path)
                #copy blocks
                t_offset = 0
                for offset, block in self.hexViewer.bin.blockReader(selection_start, 1024*1024, endoffset=selection_end):
                    newmodel.bin.write(t_offset, block)
                    newmodel.bin.commit() #write to disk often to keep history small
                    t_offset += len(block)
                newmodel.close()
            dlg.Destroy()
        event.Skip()
        
    def OnTextPopupMenuItemSaveSelection(self, event):
        if self.textView.selection_start is not None and self.textView.selection_end is not None:
            selection_start, selection_end = self.textView.getSelection()
            if selection_start > selection_end: #swap if start > end
                selection_start, selection_end = self.textView.selection_end, self.textView.selection_start
            dlg = wx.FileDialog(self, "Save Selection As...", os.getcwd(), "", PlatformMethods.GetWildcard(), wx.SAVE)
            if dlg.ShowModal() == wx.ID_OK:
                path = dlg.GetPath()
                #make a new instance to copy the stuff to
                newmodel = hexedit.HexEdit()
                newmodel.new(path)
                #copy blocks
                t_offset = 0
                for offset, block in self.textViewer.bin.blockReader(selection_start, 1024*1024, endoffset=selection_end):
                    newmodel.bin.write(t_offset, block)
                    newmodel.bin.commit() #write to disk often to keep history small
                    t_offset += len(block)
                newmodel.close()
            dlg.Destroy()
        event.Skip()

    def OnFrmFileViewerClose(self, event):
        self.auiManager.UnInit()
        self.Destroy()

        event.Skip()   
        
    
    def update(self, subject=None):
        pass
    
    def OnOpenFile(self, event):
        dlg = wx.FileDialog(self, ("Open..."), os.getcwd(), "", wildcard, wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.OpenFile(path)
        dlg.Destroy()
      
    def OpenFile(self, filePath):
        if (filePath.rfind('.') >= 0):
            Extension = filePath[filePath.rfind('.'):]
            fileType = wx.TheMimeTypesManager.GetFileTypeFromExtension(Extension)
            if fileType:
                MimeType = PlatformMethods.Encode(fileType.GetMimeType()) or "unknown"
                if MimeType == "None":
                    MimeType = "unknown"
                 
                Description = PlatformMethods.Encode(fileType.GetDescription()) or "unknown"
                if Description == "None":
                    Description = "unknown"
                    
                Category = CommonFunctions.GetFileCategory(MimeType)
            else:
                MimeType = "unknown"
                Description = "unknown"
                Category = "unknown"
            
        else:
            Extension = "None"
            MimeType = "unknown"
            Description = "unknown"
            Category = "unknown"
                    
        try:
            st = os.stat(filePath)
            Modified = st[ST_MTIME]
            Size = st[ST_SIZE]
            Created = st[ST_CTIME]
            Accessed = st[ST_ATIME]
            
        except Exception, value:
                
            Modified = 'None'
            Size = 'None'
            Created = 'None'
            Accessed = 'None'
            
        """select Name, DirPath, Size, Created, Modified, Accessed, Category, MimeType, 
        Description, MD5,  KnownFile, NewPath, SHA1, SHA224, SHA256, SHA384, SHA512
        """
        hashes = CommonFunctions.GetFileHashesAsDict(filePath, bufferSize=1024*1024*16, MD5=True, SHA1=False)
        KnownFile = 0
        NewPath = ""
        if hashes:
            MD5 = hashes['MD5']
        else:
            MD5 = "None"
            
        fileName = PlatformMethods.Encode(os.path.basename(filePath))
        dirPath = PlatformMethods.Encode(os.path.dirname(filePath))
        self.fileInfo = [fileName, dirPath, Size, Created, Modified, Accessed, Category, MimeType, Description,
                        MD5, KnownFile, NewPath, "","","","",""]
        self.LoadFileProperties()
      
    def OnCloseFile(self, event):
        self.hexViewer.close()
        self.textViewer.close()
        self.hexView.reset()
        try:
            self.htmlCtrl.LoadPage("")
        except Exception, e:
            pass
            
        self.update()
        event.Skip()
   
    
class MySearchCtrl(wx.SearchCtrl):
    maxSearches = 10
    def __init__(self, parent, id=-1, value="",
                 pos=wx.DefaultPosition, size=wx.DefaultSize, style=0,
                 doSearch=None):
        style |= wx.TE_PROCESS_ENTER
        wx.SearchCtrl.__init__(self, parent, id, value, pos, size, style)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnTextEntered)
        self.Bind(wx.EVT_MENU_RANGE, self.OnMenuItem, id=1, id2=self.maxSearches)
        self.doSearch = doSearch
        self.searches = []

    def OnTextEntered(self, evt):
        text = self.GetValue()
        if self.doSearch(text):
            self.searches.append(text)
            if len(self.searches) > self.maxSearches:
                del self.searches[0]
            #self.SetMenu(self.MakeMenu())            
        self.SetValue("")

    def OnMenuItem(self, evt):
        text = self.searches[evt.GetId()-1]
        self.doSearch(text)
        
    def MakeMenu(self):
        menu = wx.Menu()
        item = menu.Append(-1, "Recent Searches")
        item.Enable(False)
        for idx, txt in enumerate(self.searches):
            menu.Append(1+idx, txt)
        return menu
    
    def GetSearchString(self):
        return self.GetValue()

    
        

if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = frmFileViewer(None, None)
    frame.Show(True)
    app.MainLoop()