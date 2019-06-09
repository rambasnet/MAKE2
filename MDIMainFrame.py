#Boa:MDIParent:frmMainFrame

#-----------------------------------------------------------------------------
# Name:        MainFrame.py
# Purpose:     
#
# Author:      Ram Basnet
#
# Created:     2006/03/10
# RCS-ID:      $Id: MDIMainFrame.py,v 1.15 2008/03/12 04:04:03 rbasnet Exp $
# Copyright:   (c) 2004
# Licence:     All Rights Reserved.
# New field:   Whatever
#-----------------------------------------------------------------------------

import wx
import wx.lib.buttons
import re, string
import time
import os, sys
#import thread
import wx.aui

from wx.lib.anchors import LayoutAnchors
#from MySqlDatabase import *
import Globals
import DBFunctions
import Constants
import PlatformMethods
from DirectoryViewStyle import *
from FileCategoryView import *
from CommonFunctions import __InitWx__
import MDIChildFileList
import images

import frmCustomizeKeywordSearch
import MDIChildImage
import CommonFunctions

def create(parent):
    return frmMainFrame(parent)

[wxID_FRMMAINFRAME, wxID_FRMMAINFRAMEBTNPROJPROPERTIES, 
 wxID_FRMMAINFRAMEBTNREPORTKNOWNFILES, wxID_FRMMAINFRAMENOTEBOOKCASE, 
 wxID_FRMMAINFRAMEPANBUTTONBAR, wxID_FRMMAINFRAMEPANHOME, 
 wxID_FRMMAINFRAMEPANLEFTMOST, wxID_FRMMAINFRAMEPANPROJPROPERTIES, 
 wxID_FRMMAINFRAMEPANREPORT, wxID_FRMMAINFRAMEPANREPORTFRONT, 
 wxID_FRMMAINFRAMEPANTOPMOST, wxID_FRMMAINFRAMESASHBOTTOMMOST, 
 wxID_FRMMAINFRAMESASHLEFTMOST, wxID_FRMMAINFRAMESASHTOPMOST, 
 wxID_FRMMAINFRAMESTATUSBARMAIN, wxID_FRMMAINFRAMETOOLBARMAIN, 
 wxID_FRMMAINFRAMETXTSYSTEMOUTPUT, 
] = [wx.NewId() for _init_ctrls in range(17)]

[wxID_FRMMAINFRAMEMENUFILEITEMSITEMWRITEDDTODISK, 
 wxID_FRMMAINFRAMEMENUFILEMENUEXIT, 
 wxID_FRMMAINFRAMEMENUFILEMENUITEMCREATEDISKIMAGE, 
 wxID_FRMMAINFRAMEMENUFILEMENUNEWCASE, wxID_FRMMAINFRAMEMENUFILEMENUOPENCASE, 
] = [wx.NewId() for _init_coll_menuFile_Items in range(5)]

[wxID_FRMMAINFRAMESUBMENUTOOLSKWFREQMENUCUSTOMIZESEARCH, 
 wxID_FRMMAINFRAMESUBMENUTOOLSKWFREQMENUSELECTDIR, 
 wxID_FRMMAINFRAMESUBMENUTOOLSKWFREQMENUSELECTFILE, 
] = [wx.NewId() for _init_coll_subMenuToolsKwFreq_Items in range(3)]

[wxID_FRMMAINFRAMEMENUTOOLSITEMHEXVIEWER, 
 wxID_FRMMAINFRAMEMENUTOOLSITEMRESUMESCANDISK, 
 wxID_FRMMAINFRAMEMENUTOOLSITEMSSCANDISK, 
 wxID_FRMMAINFRAMEMENUTOOLSMENUITEMUPDATENSRL, 
] = [wx.NewId() for _init_coll_menuTools_Items in range(4)]

[wxID_FRMMAINFRAMETOOLBARMAINTOOLNEWCASE, 
 wxID_FRMMAINFRAMETOOLBARMAINTOOLS7, 
] = [wx.NewId() for _init_coll_ToolBarMain_Tools in range(2)]

[wxID_FRMMAINFRAMEMENUVIEWSVIEWDETAILS, wxID_FRMMAINFRAMEMENUVIEWSVIEWICONS, 
] = [wx.NewId() for _init_coll_menuViews_Items in range(2)]

[wxID_FRMMAINFRAMESUBMENUREPORTSKEYWORDSFREQUENCY] = [wx.NewId() for _init_coll_subMenuReports_Items in range(1)]

[wxID_FRMMAINFRAMEMENUHELPABOUT] = [wx.NewId() for _init_coll_menuHelp_Items in range(1)]

[wxID_FRMMAINFRAMETIMERMAIN] = [wx.NewId() for _init_utils in range(1)]

class frmMainFrame(wx.MDIParentFrame):
    def _init_coll_menuFile_Items(self, parent):
        # generated method, don't edit

        parent.Append(help='', id=wxID_FRMMAINFRAMEMENUFILEMENUNEWCASE,
              kind=wx.ITEM_NORMAL, text=u'&New Case...')
        parent.Append(help='', id=wxID_FRMMAINFRAMEMENUFILEMENUOPENCASE,
              kind=wx.ITEM_NORMAL, text=u'&Open Case...')
        parent.AppendSeparator()
        parent.Append(help='',
              id=wxID_FRMMAINFRAMEMENUFILEMENUITEMCREATEDISKIMAGE,
              kind=wx.ITEM_NORMAL, text='Create Disk Image...')
        parent.Append(help='',
              id=wxID_FRMMAINFRAMEMENUFILEITEMSITEMWRITEDDTODISK,
              kind=wx.ITEM_NORMAL, text=u'Write DD Image To Disk...')
        parent.AppendSeparator()
        parent.Append(help='', id=wxID_FRMMAINFRAMEMENUFILEMENUEXIT,
              kind=wx.ITEM_NORMAL, text='&Exit')
        self.Bind(wx.EVT_MENU, self.OnMenuFileMenuexitMenu,
              id=wxID_FRMMAINFRAMEMENUFILEMENUEXIT)
        self.Bind(wx.EVT_MENU, self.OnMenuFileMenunewCaseMenu,
              id=wxID_FRMMAINFRAMEMENUFILEMENUNEWCASE)
        self.Bind(wx.EVT_MENU, self.OnMenuFileMenuopenCaseMenu,
              id=wxID_FRMMAINFRAMEMENUFILEMENUOPENCASE)
        self.Bind(wx.EVT_MENU, self.OnMenuFileMenuitemcreatediskimageMenu,
              id=wxID_FRMMAINFRAMEMENUFILEMENUITEMCREATEDISKIMAGE)
        self.Bind(wx.EVT_MENU, self.OnMenuFileItemsitemwriteddtodiskMenu,
              id=wxID_FRMMAINFRAMEMENUFILEITEMSITEMWRITEDDTODISK)

    def _init_coll_menuBarMain_Menus(self, parent):
        # generated method, don't edit

        parent.Append(menu=self.menuFile, title='&File')
        parent.Append(menu=self.menuViews, title=u'View')
        parent.Append(menu=self.menuTools, title='Tools')
        parent.Append(menu=self.menuHelp, title='Help')

    def _init_coll_menuTools_Items(self, parent):
        # generated method, don't edit

        parent.Append(help='', id=wxID_FRMMAINFRAMEMENUTOOLSITEMSSCANDISK,
              kind=wx.ITEM_NORMAL, text=u'Scan Disk/Directories')
        parent.Append(help='', id=wxID_FRMMAINFRAMEMENUTOOLSITEMRESUMESCANDISK,
              kind=wx.ITEM_NORMAL, text='Resume Scan Disk/Directories')
        parent.AppendSeparator()
        parent.Append(help='', id=wxID_FRMMAINFRAMEMENUTOOLSMENUITEMUPDATENSRL,
              kind=wx.ITEM_NORMAL, text='Update NSRL Hashes')
        parent.AppendSeparator()
        parent.Append(help='', id=wxID_FRMMAINFRAMEMENUTOOLSITEMHEXVIEWER,
              kind=wx.ITEM_NORMAL, text=u'Hex Viewer')
        self.Bind(wx.EVT_MENU, self.OnMenuToolsItemsscandiskMenu,
              id=wxID_FRMMAINFRAMEMENUTOOLSITEMSSCANDISK)
        self.Bind(wx.EVT_MENU, self.OnMenuToolsMenuitemupdatensrlMenu,
              id=wxID_FRMMAINFRAMEMENUTOOLSMENUITEMUPDATENSRL)
        self.Bind(wx.EVT_MENU, self.OnMenuToolsItemresumescandiskMenu,
              id=wxID_FRMMAINFRAMEMENUTOOLSITEMRESUMESCANDISK)
        self.Bind(wx.EVT_MENU, self.OnMenuToolsItemhexviewerMenu,
              id=wxID_FRMMAINFRAMEMENUTOOLSITEMHEXVIEWER)

    def _init_coll_menuHelp_Items(self, parent):
        # generated method, don't edit

        parent.AppendSeparator()
        parent.Append(help='', id=wxID_FRMMAINFRAMEMENUHELPABOUT,
              kind=wx.ITEM_NORMAL, text='&About')
        parent.AppendSeparator()
        self.Bind(wx.EVT_MENU, self.OnMenuHelpAboutMenu,
              id=wxID_FRMMAINFRAMEMENUHELPABOUT)

    def _init_coll_menuViews_Items(self, parent):
        # generated method, don't edit

        parent.Append(help='', id=wxID_FRMMAINFRAMEMENUVIEWSVIEWDETAILS,
              kind=wx.ITEM_CHECK, text=u'Details')
        parent.Append(help=u'', id=wxID_FRMMAINFRAMEMENUVIEWSVIEWICONS,
              kind=wx.ITEM_CHECK, text=u'Icons')
        self.Bind(wx.EVT_MENU, self.OnMenuViewsViewdetailsMenu,
              id=wxID_FRMMAINFRAMEMENUVIEWSVIEWDETAILS)
        self.Bind(wx.EVT_MENU, self.OnMenuViewsViewiconsMenu,
              id=wxID_FRMMAINFRAMEMENUVIEWSVIEWICONS)

    def _init_coll_notebookCase_Pages(self, parent):
        # generated method, don't edit

        parent.AddPage(imageId=-1, page=self.panHome, select=False,
              text=u'Case')
        parent.AddPage(imageId=-1, page=self.panReport, select=True,
              text='Report')

    def _init_coll_statusBarMain_Fields(self, parent):
        # generated method, don't edit
        parent.SetFieldsCount(3)

        parent.SetStatusText(number=0, text='Ready')
        parent.SetStatusText(number=1, text='')
        parent.SetStatusText(number=2, text='DateTime')

        parent.SetStatusWidths([-1, -1, -1])

    def _init_utils(self):
        # generated method, don't edit
        self.menuBarMain = wx.MenuBar()

        self.menuFile = wx.Menu(title='')

        self.menuTools = wx.Menu(title='')

        self.menuHelp = wx.Menu(title='')

        self.timerMain = wx.Timer(id=wxID_FRMMAINFRAMETIMERMAIN, owner=self)
        self.Bind(wx.EVT_TIMER, self.OnTimerMainTimer,
              id=wxID_FRMMAINFRAMETIMERMAIN)

        self.menuViews = wx.Menu(title=u'')

        self._init_coll_menuBarMain_Menus(self.menuBarMain)
        self._init_coll_menuFile_Items(self.menuFile)
        self._init_coll_menuTools_Items(self.menuTools)
        self._init_coll_menuHelp_Items(self.menuHelp)
        self._init_coll_menuViews_Items(self.menuViews)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.MDIParentFrame.__init__(self, id=wxID_FRMMAINFRAME,
              name='frmMainFrame', parent=prnt, pos=wx.Point(334, -47),
              size=wx.Size(1032, 775), style=wx.DEFAULT_FRAME_STYLE,
              title='MAKE2')
        self._init_utils()
        self.SetToolTipString('')
        self.SetMenuBar(self.menuBarMain)
        self.Center(wx.BOTH)
        self.SetAutoLayout(True)
        self.SetBackgroundColour(wx.Colour(236, 233, 216))
        self.SetClientSize(wx.Size(1016, 737))
        self.Bind(wx.EVT_SIZE, self.OnFrmMainFrameSize)
        self.Bind(wx.EVT_ACTIVATE, self.OnFrmMainFrameActivate)

        self.statusBarMain = wx.StatusBar(id=wxID_FRMMAINFRAMESTATUSBARMAIN,
              name='statusBarMain', parent=self,
              style=wx.ST_SIZEGRIP | wx.CLIP_CHILDREN)
        self.statusBarMain.SetToolTipString('Status Bar')
        self.statusBarMain.SetExtraStyle(0)
        self._init_coll_statusBarMain_Fields(self.statusBarMain)
        self.SetStatusBar(self.statusBarMain)

        self.sashTopMost = wx.SashLayoutWindow(id=wxID_FRMMAINFRAMESASHTOPMOST,
              name='sashTopMost', parent=self, pos=wx.Point(-270, -20),
              size=wx.Size(1048, 85), style=wx.SW_3D)
        self.sashTopMost.SetBackgroundColour(wx.Colour(4, 56, 85))
        self.sashTopMost.SetOrientation(wx.LAYOUT_HORIZONTAL)
        self.sashTopMost.SetAlignment(wx.LAYOUT_TOP)
        self.sashTopMost.SetSashVisible(wx.SASH_BOTTOM, False)
        self.sashTopMost.SetDefaultSize(wx.Size(1048, 100))
        self.sashTopMost.SetDefaultBorderSize(0)
        self.sashTopMost.SetAutoLayout(True)
        self.sashTopMost.SetSashVisible(wx.SASH_RIGHT, True)
        self.sashTopMost.SetConstraints(LayoutAnchors(self.sashTopMost, False,
              False, False, False))
        self.sashTopMost.Bind(wx.EVT_SASH_DRAGGED,
              self.OnSashTopMostSashDragged, id=wxID_FRMMAINFRAMESASHTOPMOST)

        self.sashLeftMost = wx.SashLayoutWindow(id=wxID_FRMMAINFRAMESASHLEFTMOST,
              name='sashLeftMost', parent=self, pos=wx.Point(0, 80),
              size=wx.Size(128, 608),
              style=wx.SW_BORDER | wx.SW_3DSASH | wx.CLIP_CHILDREN | wx.SW_3D)
        self.sashLeftMost.SetBackgroundColour(wx.Colour(125, 152, 221))
        self.sashLeftMost.SetExtraBorderSize(0)
        self.sashLeftMost.SetAlignment(wx.LAYOUT_LEFT)
        self.sashLeftMost.SetOrientation(wx.LAYOUT_VERTICAL)
        self.sashLeftMost.SetSashVisible(wx.SASH_RIGHT, True)
        self.sashLeftMost.SetDefaultSize(wx.Size(125, 600))
        self.sashLeftMost.Bind(wx.EVT_SASH_DRAGGED,
              self.OnSashLeftMostSashDragged, id=wxID_FRMMAINFRAMESASHLEFTMOST)

        self.sashBottomMost = wx.SashLayoutWindow(id=wxID_FRMMAINFRAMESASHBOTTOMMOST,
              name='sashBottomMost', parent=self, pos=wx.Point(152, 630),
              size=wx.Size(776, 50), style=wx.SW_3D)
        self.sashBottomMost.SetBackgroundColour(wx.Colour(125, 152, 221))
        self.sashBottomMost.SetAlignment(wx.LAYOUT_BOTTOM)
        self.sashBottomMost.SetSashVisible(wx.SASH_TOP, True)
        self.sashBottomMost.SetOrientation(wx.LAYOUT_HORIZONTAL)
        self.sashBottomMost.SetDefaultSize(wx.Size(776, 50))
        self.sashBottomMost.SetExtraBorderSize(5)
        self.sashBottomMost.SetAutoLayout(False)
        self.sashBottomMost.Bind(wx.EVT_SASH_DRAGGED,
              self.OnSashBottomMostSashDragged,
              id=wxID_FRMMAINFRAMESASHBOTTOMMOST)

        self.panTopMost = wx.Panel(id=wxID_FRMMAINFRAMEPANTOPMOST,
              name='panTopMost', parent=self.sashTopMost, pos=wx.Point(0, 0),
              size=wx.Size(1048, 85),
              style=wx.RAISED_BORDER | wx.CLIP_CHILDREN | wx.TAB_TRAVERSAL)
        self.panTopMost.SetAutoLayout(True)
        self.panTopMost.SetBackgroundColour(wx.Colour(243, 248, 253))
        self.panTopMost.SetBackgroundStyle(wx.BG_STYLE_COLOUR)

        self.txtSystemOutput = wx.TextCtrl(id=wxID_FRMMAINFRAMETXTSYSTEMOUTPUT,
              name='txtSystemOutput', parent=self.sashBottomMost,
              pos=wx.Point(4, 4), size=wx.Size(768, 42),
              style=wx.TE_RICH | wx.TE_MULTILINE | wx.HSCROLL | wx.TE_READONLY | wx.VSCROLL | wx.TE_WORDWRAP,
              value='')

        self.ToolBarMain = wx.ToolBar(id=wxID_FRMMAINFRAMETOOLBARMAIN,
              name=u'ToolBarMain', parent=self.panTopMost, pos=wx.Point(0, 0),
              size=wx.Size(1042, 28), style=wx.TB_HORIZONTAL | wx.NO_BORDER)
        self.ToolBarMain.SetConstraints(LayoutAnchors(self.ToolBarMain, True,
              True, True, False))
        self.ToolBarMain.SetToolBitmapSize(wx.Size(24, 24))
        self.ToolBarMain.SetBackgroundColour(wx.Colour(183, 183, 255))

        self.panButtonBar = wx.Panel(id=wxID_FRMMAINFRAMEPANBUTTONBAR,
              name=u'panButtonBar', parent=self.panTopMost, pos=wx.Point(0, 28),
              size=wx.Size(1042, 56), style=wx.TAB_TRAVERSAL)
        self.panButtonBar.SetBackgroundColour(wx.Colour(244, 0, 0))
        self.panButtonBar.SetAutoLayout(True)
        self.panButtonBar.SetConstraints(LayoutAnchors(self.panButtonBar, True,
              False, True, False))
        self.panButtonBar.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, u'MS Shell Dlg 2'))

        self.panLeftMost = wx.Panel(id=wxID_FRMMAINFRAMEPANLEFTMOST,
              name=u'panLeftMost', parent=self.sashLeftMost, pos=wx.Point(0, 0),
              size=wx.Size(125, 608), style=wx.TAB_TRAVERSAL)
        self.panLeftMost.SetBackgroundColour(wx.Colour(125, 152, 221))
        self.panLeftMost.SetAutoLayout(True)
        self.panLeftMost.SetBackgroundStyle(wx.BG_STYLE_SYSTEM)

        self.notebookCase = wx.Notebook(id=wxID_FRMMAINFRAMENOTEBOOKCASE,
              name=u'notebookCase', parent=self.panLeftMost, pos=wx.Point(0, 0),
              size=wx.Size(128, 608), style=0)
        self.notebookCase.SetConstraints(LayoutAnchors(self.notebookCase, True,
              True, True, True))
        self.notebookCase.SetBackgroundColour(wx.Colour(125, 152, 221))
        self.notebookCase.SetForegroundColour(wx.Colour(0, 0, 0))
        self.notebookCase.SetToolTipString('')
        self.notebookCase.SetAutoLayout(False)
        self.notebookCase.Show(False)

        self.panReport = wx.Panel(id=wxID_FRMMAINFRAMEPANREPORT,
              name='panReport', parent=self.notebookCase, pos=wx.Point(0, 0),
              size=wx.Size(120, 582), style=wx.TAB_TRAVERSAL)
        self.panReport.SetAutoLayout(True)

        self.panHome = wx.Panel(id=wxID_FRMMAINFRAMEPANHOME, name='panHome',
              parent=self.notebookCase, pos=wx.Point(0, 0), size=wx.Size(120,
              582), style=wx.TAB_TRAVERSAL)
        self.panHome.SetAutoLayout(True)

        self.panProjProperties = wx.Panel(id=wxID_FRMMAINFRAMEPANPROJPROPERTIES,
              name=u'panProjProperties', parent=self.panHome, pos=wx.Point(4,
              4), size=wx.Size(112, 574), style=wx.TAB_TRAVERSAL)
        self.panProjProperties.SetBackgroundColour(wx.Colour(225, 225, 255))
        self.panProjProperties.SetConstraints(LayoutAnchors(self.panProjProperties,
              True, True, True, True))
        self.panProjProperties.Show(True)

        self.btnProjProperties = wx.Button(id=wxID_FRMMAINFRAMEBTNPROJPROPERTIES,
              label=u'Properties', name=u'btnProjProperties',
              parent=self.panProjProperties, pos=wx.Point(8, 8),
              size=wx.Size(75, 23), style=0)
        self.btnProjProperties.Show(True)
        self.btnProjProperties.Bind(wx.EVT_BUTTON,
              self.OnBtnProjPropertiesButton,
              id=wxID_FRMMAINFRAMEBTNPROJPROPERTIES)

        self.panReportFront = wx.Panel(id=wx.NewId(), name='panel1',
              parent=self.panReport, pos=wx.Point(4, 4), size=wx.Size(112, 574),
              style=wx.TAB_TRAVERSAL)
        self.panReportFront.SetBackgroundColour(wx.Colour(225, 225, 255))
        self.panReportFront.SetConstraints(LayoutAnchors(self.panReportFront,
              True, True, True, True))
        self.panReportFront.Show(True)

        self.btnReportKnownFiles = wx.Button(id=wxID_FRMMAINFRAMEBTNREPORTKNOWNFILES,
              label=u'Known Files', name=u'btnReportKnownFiles',
              parent=self.panReportFront, pos=wx.Point(8, 8), size=wx.Size(88,
              23), style=0)
        self.btnReportKnownFiles.Bind(wx.EVT_BUTTON,
              self.OnBtnReportKnownFilesButton,
              id=wxID_FRMMAINFRAMEBTNREPORTKNOWNFILES)

        self._init_coll_notebookCase_Pages(self.notebookCase)

    def __init__(self, parent):
        __InitWx__()
        self._init_ctrls(parent)
        self.SetIcon(images.getMAKE2Icon())
        self.timerMain.Start(1000)
        self.AddToolbarTools()
        self.CreateTopButtonPanel()
        self.SetStatuBarTime()
        #self.fldrImg = wx.ArtProvider.GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, (16,16))
        #self.InitDynamicControls(self.panHome)
        self.Maximize(True)
        self.treeDirView = True
        self.menuViews.Check(wxID_FRMMAINFRAMEMENUVIEWSVIEWDETAILS, True)
        
     
    def AddToolbarTools(self):
        tsize = (24,24)
        new_bmp =  wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_TOOLBAR, tsize)
        open_bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR, tsize)
        toolNewId = wx.NewId()
        toolOpenId = wx.NewId()
   
        #tb.AddSimpleTool(10, new_bmp, "New", "Long help for 'New'")
        self.ToolBarMain.AddLabelTool(toolNewId, "New", new_bmp, shortHelp="New", longHelp="Long help for 'New'")
        self.Bind(wx.EVT_TOOL, self.OnToolNewCaseClick, id=toolNewId)
        #self.Bind(wx.EVT_TOOL_RCLICKED, self.OnToolNewCaseRClick, id=toolNewId)

        #tb.AddSimpleTool(20, open_bmp, "Open", "Long help for 'Open'")
        self.ToolBarMain.AddLabelTool(toolOpenId, "Open", open_bmp, shortHelp="Open", longHelp="Long help for 'Open'")
        self.Bind(wx.EVT_TOOL, self.OnToolOpenCaseClick, id=toolOpenId)
        
        self.ToolBarMain.AddSeparator()
        self.ToolBarMain.Realize()
        #self.Bind(wx.EVT_TOOL_RCLICKED, self.OnToolRClick, id=toolOpenId)
       
                
    def CreateTopButtonPanel(self):
        import wx.lib.buttonpanel as bp
        self.Freeze()
        self.alignment = bp.BP_ALIGN_LEFT
        self.style = bp.BP_USE_GRADIENT
        self.buttonBar = bp.ButtonPanel(self.panButtonBar, -1, "MAKE2::Digital Forensic Toolbox",
                                       style=self.style, alignment=self.alignment)
        self.buttonBar.SetBestSize(wx.Size(1042, 56))
        self.buttonBar.SetConstraints(LayoutAnchors(self.buttonBar, True,
              False, True, False))
                  
                  
        """
        -a -u -i -n folderExplorer Images/Bitmaps/folderExplorer1.png images.py",
                "-a -u -i -n search Images/Bitmaps/Search.png images.py",
                "-a -u -i -n registryViewer Images/Bitmaps/RegistryViewer.png images.py",
                "-a -u -i -n textCat Images/Bitmaps/TextCat.png images.py",
                "-a -u -i -n timelines Images/Bitmaps/Timelines.png images.py",
                "-a -u -i -n logViewer Images/Bitmaps/LogViewer.png images.py",
                "-a -u -i -n imageViewer Images/Bitmaps/ImageViewer.png images.py",
                "-a -u -i -n emailViewer Images/Bitmaps/EmailViewer.png images.py"
        """
        
        self.pngs =[(images.gettimelinesBitmap(), ''),
                    (images.getsearchBitmap(), ""),
                    (images.gettextCatBitmap(), ""),
                    (images.getemailViewerBitmap(), ""),
                    (images.getfolderExplorerBitmap(), ""),
                    (images.getimageViewerBitmap(), ""),
                    (images.getlogViewerBitmap(), ""),
                    (images.getregistryViewerBitmap(), "")
                    ]
        """         
        self.pngs =[(images.gettimelinesBitmap(), ' Timelines  '),
                    (images.getsearchBitmap(), "  Search  "),
                    (images.gettextCatBitmap(), " Text Mining  "),
                    (images.getemailViewerBitmap(), " Emails  "),
                    (images.getfolderExplorerBitmap(), " Explorer  "),
                    (images.getimageViewerBitmap(), " Images  "),
                    (images.getlogViewerBitmap(), " Logs  "),
                    (images.getregistryViewerBitmap(), " Registry  ")
                    ]
        """
        
        
        #explorer button
        self.buttonBar.AddSeparator()
        self.btnExplorer = bp.ButtonInfo(self.buttonBar, wx.NewId(),
                            self.pngs[4][0], kind=wx.ITEM_NORMAL,
                            shortHelp='Folder Explorer', longHelp='Click to view Folder Explorer')
            
        self.btnExplorer.SetText(self.pngs[4][1])
        #self.btnTimeline.SetRect(wx.Rect(0, 0, 100, 100))
        #print self.btnTimeline.Rect
        self.btnExplorer.SetTextAlignment(bp.BP_BUTTONTEXT_ALIGN_RIGHT)
        self.buttonBar.AddButton(self.btnExplorer)
        self.Bind(wx.EVT_BUTTON, self.OnExplorerButton, id=self.btnExplorer.GetId())
       
        
        #timeline button
        self.buttonBar.AddSeparator()
        self.btnTimeline = bp.ButtonInfo(self.buttonBar, wx.NewId(),
                            self.pngs[0][0], kind=wx.ITEM_NORMAL,
                            shortHelp='Timelines Viewer', longHelp='Click to view Timelines')
            
        self.btnTimeline.SetText(self.pngs[0][1])
        #self.btnTimeline.SetRect(wx.Rect(0, 0, 100, 100))
        #print self.btnTimeline.Rect
        self.btnTimeline.SetTextAlignment(bp.BP_BUTTONTEXT_ALIGN_RIGHT)
        self.buttonBar.AddButton(self.btnTimeline)
        self.Bind(wx.EVT_BUTTON, self.OnTimelineButton, id=self.btnTimeline.GetId())
        self.buttonBar.AddSeparator()
        
        #ImageViewer button
        self.btnImageViewer = bp.ButtonInfo(self.buttonBar, wx.NewId(),
                    self.pngs[5][0], kind=wx.ITEM_NORMAL,
                    shortHelp='Image Analysis', longHelp='Click to perform Image Analysis...')
        
        self.btnImageViewer.SetText(self.pngs[5][1])
        self.btnImageViewer.SetTextAlignment(bp.BP_BUTTONTEXT_ALIGN_RIGHT)
        self.buttonBar.AddButton(self.btnImageViewer)
        self.Bind(wx.EVT_BUTTON, self.OnImageViewerButton, id=self.btnImageViewer.GetId())
        self.buttonBar.AddSeparator()
        
                
        #Text Mining button
        self.btnTextCat = bp.ButtonInfo(self.buttonBar, wx.NewId(),
                    self.pngs[2][0], kind=wx.ITEM_NORMAL,
                    shortHelp='Text Mining', longHelp='Click to perform Text Mining...')
        
        self.btnTextCat.SetText(self.pngs[2][1])
        self.btnTextCat.SetTextAlignment(bp.BP_BUTTONTEXT_ALIGN_RIGHT)
        self.buttonBar.AddButton(self.btnTextCat)
        self.Bind(wx.EVT_BUTTON, self.OnTextCategorizationButton, id=self.btnTextCat.GetId())
        self.buttonBar.AddSeparator()
        
        #Search Keywords button
        self.btnKeywordsSearch = bp.ButtonInfo(self.buttonBar, wx.NewId(),
                    self.pngs[1][0], kind=wx.ITEM_NORMAL,
                    shortHelp='Keywords Search', longHelp='Click to Search for keywords...')
            
        self.btnKeywordsSearch.SetText(self.pngs[1][1])
        self.btnKeywordsSearch.SetTextAlignment(bp.BP_BUTTONTEXT_ALIGN_RIGHT)
        self.buttonBar.AddButton(self.btnKeywordsSearch)
        self.Bind(wx.EVT_BUTTON, self.OnKeywordsSearchButton, id=self.btnKeywordsSearch.GetId())
        self.buttonBar.AddSeparator()
        
        
        #Emails button
        self.btnEmails = bp.ButtonInfo(self.buttonBar, wx.NewId(),
                    self.pngs[3][0], kind=wx.ITEM_NORMAL,
                    shortHelp='Email Analysis', longHelp='Click to perform Email Analysis...')
        
        self.btnEmails.SetText(self.pngs[3][1])
        self.btnEmails.SetTextAlignment(bp.BP_BUTTONTEXT_ALIGN_RIGHT)
        self.buttonBar.AddButton(self.btnEmails)
        self.Bind(wx.EVT_BUTTON, self.OnEmailsButton, id=self.btnEmails.GetId())
        self.buttonBar.AddSeparator()
        
       
        """
        #LogViewer button
        self.btnLogViewer = bp.ButtonInfo(self.buttonBar, wx.NewId(),
                    self.pngs[6][0], kind=wx.ITEM_NORMAL,
                    shortHelp='Log Analysis', longHelp='Click to perform Log Analysis...')
        
        self.btnLogViewer.SetText(self.pngs[6][1])
        self.btnLogViewer.SetTextAlignment(bp.BP_BUTTONTEXT_ALIGN_RIGHT)
        self.buttonBar.AddButton(self.btnLogViewer)
        self.Bind(wx.EVT_BUTTON, self.OnLogViewerButton, id=self.btnLogViewer.GetId())
        self.buttonBar.AddSeparator()
        
        
        #LogViewer button
        self.btnRegistryViewer = bp.ButtonInfo(self.buttonBar, wx.NewId(),
                    self.pngs[7][0], kind=wx.ITEM_NORMAL,
                    shortHelp='Registry Analysis', longHelp='Click to perform Registry Analysis...')
        
        self.btnRegistryViewer.SetText(self.pngs[7][1])
        self.btnRegistryViewer.SetTextAlignment(bp.BP_BUTTONTEXT_ALIGN_RIGHT)
        self.buttonBar.AddButton(self.btnRegistryViewer)
        self.Bind(wx.EVT_BUTTON, self.OnRegistryViewerButton, id=self.btnRegistryViewer.GetId())
        self.buttonBar.AddSeparator()
        """
        
        bpArt = self.buttonBar.GetBPArt()
        # set the color the text is drawn with
        bpArt.SetColor(bp.BP_TEXT_COLOR, wx.Color(244, 0, 0))
        bpArt.SetFont(bp.BP_TEXT_FONT, wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, u'MS Shell Dlg 2'))
              
        bpArt.SetColor(bp.BP_BORDER_COLOR, wx.Colour(174,174,255))
        bpArt.SetColor(bp.BP_GRADIENT_COLOR_FROM, wx.Colour(125,152,221))
        bpArt.SetColor(bp.BP_GRADIENT_COLOR_TO, wx.Colour(217, 217, 255))
        bpArt.SetColor(bp.BP_BUTTONTEXT_COLOR, wx.Colour(28,28,255))
        bpArt.SetColor(bp.BP_SEPARATOR_COLOR,
                       bp.BrightenColour(wx.Colour(0, 0, 0), 0.85))
        bpArt.SetColor(bp.BP_SELECTION_BRUSH_COLOR, wx.Color(225, 225, 255))
        bpArt.SetColor(bp.BP_SELECTION_PEN_COLOR, wx.SystemSettings_GetColour(wx.SYS_COLOUR_ACTIVECAPTION))
        bpArt.SetFont(bp.BP_BUTTONTEXT_FONT, wx.Font(9, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, u'MS Shell Dlg 2'))
        
        #self.ChangeLayout()              
        self.Thaw()
        self.buttonBar.DoLayout()
        #self.CreatePanelButtons()

                
    def InitDynamicControls(self, parent):
        self.cp = wx.CollapsiblePane(parent, label='Case Properties')
        #self.cp.SetConstraints(LayoutAnchors(self.cp,
        #      True, True, True, True))
        self.cp.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self.OnCasePaneChanged)
        
        self.Init_CasePane(self.cp.GetPane())
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        parent.SetSizer(sizer)
        #sizer.Add(title, 0, wx.ALL, 25)
        
        
        self.cpDirList = wx.CollapsiblePane(parent, label='Folders List')
        self.cpDirList.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self.OnDirListPaneChanged)
        self.Init_CasePane(self.cpDirList.GetPane())

        #dirListSizer = wx.BoxSizer(wx.VERTICAL)
        #self.SetSizer(sizer)
        #sizer.Add(title, 0, wx.ALL, 25)
        sizer.Add(self.cp, 0, wx.RIGHT|wx.LEFT|wx.EXPAND, 25)
        sizer.Add(self.cpDirList, 0, wx.RIGHT|wx.LEFT|wx.EXPAND, 25)
        
        self.btn = btn = wx.Button(parent, label="Hello")
        #self.Bind(wx.EVT_BUTTON, self.OnToggle, btn)
        sizer.Add(btn, 0, wx.ALL, 25)
        
        """
        self.btn = btn = wx.Button(self, label=btnlbl1)
        self.Bind(wx.EVT_BUTTON, self.OnToggle, btn)
        sizer.Add(btn, 0, wx.ALL, 25)
        """
    
    def Init_CasePane(self, pane):
              
        self.lblCaseProperties = wx.StaticText(id=wx.NewId(),
              label=u'Properties', name=u'lblCaseProperties',
              parent=pane, size=wx.Size(79, 18),
              style=0)
        self.lblCaseProperties.SetFont(wx.Font(11, wx.SWISS, wx.NORMAL,
              wx.BOLD, False, 'Tahoma'))
        self.lblCaseProperties.SetForegroundColour(wx.Colour(255, 255, 255))
        #self.Add(lblCaseProperties, 0, wx.ALL, 25)
        
        self.btnCaseProperties = wx.BitmapButton(bitmap=wx.ArtProvider.GetBitmap(wx.ART_FOLDER,
              wx.ART_OTHER, (32, 32)), id=wx.NewId(),
              name=u'btnCaseProperties', parent=pane, size=wx.Size(48, 40), style=wx.BU_AUTODRAW)
        self.btnCaseProperties.SetBackgroundColour(wx.Colour(125, 152, 225))
        self.btnCaseProperties.Bind(wx.EVT_BUTTON,
              self.OnBtnCasePropertiesButton)
        
        CasePropSizer = wx.FlexGridSizer(cols=2, hgap=5, vgap=5)
        CasePropSizer.AddGrowableCol(1)
        CasePropSizer.Add(self.btnCaseProperties, 0, wx.EXPAND)
        CasePropSizer.Add(self.lblCaseProperties, 0, wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
            
        border = wx.BoxSizer()
        border.Add(CasePropSizer, 1, wx.EXPAND|wx.ALL, 5)
        pane.SetSizer(border)
        self.Layout()
        #self.Add(btnCaseProperties, 0, wx.ALL, 25)
                    
   
    def OnCasePaneChanged(self, event): 
        #self.doLayout()  
        #if evt:
            #self.log.write('wx.EVT_COLLAPSIBLEPANE_CHANGED: %s' % evt.Collapsed)
            # redo the layout
        self.Layout()

        # and also change the labels
        if self.cp.IsExpanded():
            self.cp.SetLabel("Case Properties1")
            #self.btn.SetLabel(btnlbl2)
        
        else:
            self.cp.SetLabel("Case Properties")
            
        #self.Layout()
        self.doLayout()
        self.doLayout()
        self.btn.SetInitialSize()
        #self.cpDirList.SetInitialSize()
        #self.OnSashLeftMostSashDragged(event)
            
    def OnDirListPaneChanged(self, event):
        self.doLayout()
        #if evt:
            #self.log.write('wx.EVT_COLLAPSIBLEPANE_CHANGED: %s' % evt.Collapsed)
            # redo the layout
        self.doLayout()

        # and also change the labels
        if self.cpDirList.IsExpanded():
            self.cpDirList.SetLabel("Folders List1")
        else:
            self.cpDirList.SetLabel("Folders List")
        self.Layout()
        #self.doLayout()
        #self.doLayout()
        self.btn.SetInitialSize()
        #self.OnSashLeftMostSashDragged(event)
        #self.cp.SetInitialSize()
        
    def checkStatusRange(self, event):
        return event.GetDragStatus() != wx.SASH_STATUS_OUT_OF_RANGE

    def doLayout(self):
        #wx.LayoutAlgorithm().LayoutWindow(self, self.panReportFront)
        #self.panReportFront.Refresh()
        #print 'lay out'
        if self:
            wx.LayoutAlgorithm().LayoutMDIFrame(self)
            self.GetClientWindow().Refresh()
            #print 'lay out1'
            return None

   
    def OnSashTopMostSashDragged(self, event):
        if self.checkStatusRange(event):
            self.sashTopMost.SetDefaultSize(wx.Size(1000, event.GetDragRect().height))
            self.doLayout()

    def OnSashLeftMostSashDragged(self, event):
        if self.checkStatusRange(event):
            self.sashLeftMost.SetDefaultSize(wx.Size(event.GetDragRect().width, 1000))
            self.doLayout()

    def OnSashSecondLeftSashDragged(self, event):
        if self.checkStatusRange(event):
            self.sashSecondLeft.SetDefaultSize(wx.Size(event.GetDragRect().width, 1000))
            self.doLayout()

    def OnFrmMainFrameSize(self, event):
        self.doLayout()

    def OnSashBottomMostSashDragged(self, event):
        if self.checkStatusRange(event):
            self.sashBottomMost.SetDefaultSize(wx.Size(1000, event.GetDragRect().height))
            self.doLayout()

    def OnSashSecondTopSashDragged(self, event):
        if self.checkStatusRange(event):
            self.sashSecondTop.SetDefaultSize(wx.Size(1000, event.GetDragRect().height))
            self.doLayout()

    def OnMenuToolsSetdbMenu(self, event):
        event.Skip()
       

    def OnTimerMainTimer(self, event):
        #self.doLayout()
        self.SetStatuBarTime()
        
    def SetStatuBarTime(self):
        currTimeList = time.ctime().split()
        currTime = currTimeList[1] + " " + currTimeList[2] + ", " + currTimeList[4] + "  " + currTimeList[3]
        self.statusBarMain.SetStatusText(number=2, text=currTime)
        

    def OnFrmMainFrameActivate(self, event):
        event.Skip()
        #if Globals.GlobalMainForm:
        #    Globals.GlobalMainForm.doLayout()

    def OnFrmMainFrameSetFocus(self, event):
        self.doLayout()

    def SetSystemOutput(self, msg):
        self.txtSystemOutput.SetValue(self.txtSystemOutput.GetValue() + "\n" + msg)
        self.txtSystemOutput.Refresh()


    def OnBtnExecutiveReportButton(self, event):
        event.Skip()


    def OnMenuToolsReportsMenu(self, event):
        event.Skip()

    def OnMenuHelpAboutMenu(self, event):
        import dlgAbout
        about = dlgAbout.create(self)
        about.ShowModal()


    def OnMenuFileMenunewCaseMenu(self, event):
        import dlgCaseProperties
        newCase = dlgCaseProperties.create(self)
        newCase.ShowModal()
        self.SetTitle("MAKE2::Digital Forensics Toolbox- " + Globals.CurrentCaseFile)
        
    def OnSubMenuToolsKwFreqMenuselectfileMenu(self, event):
        event.Skip()

    def OnSubMenuToolsKwFreqMenuselectdirMenu(self, event):
        event.Skip()

    def OnSubMenuToolsKwFreqMenucustomizesearchMenu(self, event):
        event.Skip()

    def OnSubMenuToolsKwFreqItems3Menu(self, event):
        event.Skip()

    def OnSubMenuReportsKeywordsfrequencyMenu(self, event):
        event.Skip()

    def OnBtnProjPropertiesButton(self, event):
        import dlgCaseProperties
        newCase = dlgCaseProperties.create(self, Globals.CurrentCase)
        newCase.ShowModal()

    def OnMenuFileMenuexitMenu(self, event):
        self.Close()

    def OnToolNewCaseClick(self, event):
        self.OnMenuFileMenunewCaseMenu(event)
        
    def OnToolOpenCaseClick(self, event):
        self.OnMenuFileMenuopenCaseMenu(event)
        
    def ShowOpenCaseMessage(self):
        msg = "Please Open an existing a Case file or create a new Case first!"
        dlg = wx.MessageDialog(self, msg ,
          'Error', wx.OK | wx.ICON_ERROR)
        try:
            dlg.ShowModal()
            return
        finally:
            dlg.Destroy()
        
    def OnMenuFileMenuopenCaseMenu(self, event):
        import Init
        import dlgDataSource
        self.SetCursor(wx.HOURGLASS_CURSOR)
        Init.InitGlobals()
        dlg = wx.FileDialog(self, "Open Case", ".", "", "*.cfi", wx.OPEN)
        try:
            if dlg.ShowModal() == wx.ID_OK:
                success = True
                msg = ""
                Globals.CurrentCaseFile = dlg.GetPath().encode('utf-8', 'replace')
                busy = wx.BusyInfo("It might take some good few minutes depending on the evidence size...")
                wx.Yield()
                
                if DBFunctions.GetCaseSettings(Globals.CurrentCaseFile):
                    Init.InitAllDBFileNames()
                    DBFunctions.GetCaseEvidences(Globals.CurrentCaseFile)
                    
                    for key in Globals.EvidencesDict:
                        dlg = dlgDataSource.create(self, key)
                        dlg.ShowModal()
                        #print 'wait'
                    #Globals.MACFileName = Globals.CurrentCase.CaseName + Constants.MACExtension
                    #Globals.KeywordsFileName = Globals.CurrentCase.CaseName + Constants.KeywordsExtension
                    #Globals.TextCatFileName = Globals.CurrentCase.CaseName + Constants.TextCatExtension
                    
                    DBFunctions.LoadMACMinMaxValues()
                    
                    DBFunctions.UpdateDatabaseTables()
                        
                else:
                    msg = "Couldn't open Case File: %s!"%Globals.CurrentCaseFile
                    success = False
                    
                if not success:
                    dlg = wx.MessageDialog(self, msg ,
                      'Error', wx.OK | wx.ICON_ERROR)
                    try:
                        #Globals.CaseOpen = False
                        #self.ShowCaseProperties(False)
                        dlg.ShowModal()
                        #return
                    finally:
                        dlg.Destroy()
                else:
                    Globals.CaseOpen = True
                    self.SetTitle("MAKE2 - " + Globals.CurrentCaseFile)
                    #self.ShowDirectoryTreeView()
                    self.notebookCase.Show(True)
                    self.ShowCaseProperties(True)
                    
                    
        finally:
            dlg.Destroy()
        self.SetCursor(wx.STANDARD_CURSOR)
        
  
    def ShowDirectoryTreeView(self):
        #self.ShowCaseProperties(True)
        self.notebookCase.Show(True)
        self.ShowFileListView()


    def ShowCaseProperties(self, value):
        self.btnProjProperties.Show(value)
        self.panProjProperties.Show(value)
        self.notebookCase.Show(value)



    def OnToolBarMainToolnewCaseTool(self, event):
        event.Skip()

    def OnMenuToolsItemsscandiskMenu(self, event):
        if not Globals.CaseOpen:
            self.ShowOpenCaseMessage()
            return
        dlg = wx.DirDialog(self)
        try:
            if dlg.ShowModal() == wx.ID_OK:
                dir = dlg.GetPath()
                # Your code
                import dlgScanProgress
                scanMAC = dlgScanProgress.create(self, dir)
                #scanMAC.StartScan(dir)
                scanMAC.ShowModal()
                
        finally:
            dlg.Destroy()
        event.Skip()
    
        
    def ShowFileListView(self):
        if Globals.CaseOpen:
            busy = wx.BusyInfo("Loading Folders and Files...")
            wx.Yield()
            if not Globals.frmGlobalFileList:
                #GlobalMethods.PRINT("Network Scanner Loaded...")
                Globals.frmGlobalFileList = MDIChildFileList.create(self)
            
            #Globals.frmGlobalFileList.AddFilesToListView(dirPath, self.treeDirView)
            Globals.frmGlobalFileList.SetPosition(wx.Point(0, 0))
            Globals.frmGlobalFileList.Show(True)
            Globals.frmGlobalFileList.Activate()
            Globals.frmGlobalFileList.Maximize(True)
        
    def OnTreeDirListTreeSelChanged(self, event):
        item = self.treeDirList.GetSelection()
        if not item == self.root:
            #
            dirPath = self.GetAncestorsName(item)
            dirPath += self.treeDirList.GetItemText(item)
            #print dirPath
            if self.treeDirView:
                if dirPath.count(PlatformMethods.GetDirSeparator()) == 0:
                     dirPath += PlatformMethods.GetDirSeparator()

                dirPath = PlatformMethods.ConvertFilePath(dirPath)
            if not Globals.frmGlobalFileList:
                #GlobalMethods.PRINT("Network Scanner Loaded...")
                import MDIChildFileList
                Globals.frmGlobalFileList = MDIChildFileList.create(self)
            
            Globals.frmGlobalFileList.AddFilesToListView(dirPath, self.treeDirView)
            Globals.frmGlobalFileList.SetPosition(wx.Point(0, 0))
            Globals.frmGlobalFileList.Show(True)
            Globals.frmGlobalFileList.Activate()
            Globals.frmGlobalFileList.Maximize(True)

        event.Skip()

    def OnKeywordsSearchButton(self, event):
        if Globals.CaseOpen:
            #self.notebookCase.Show(False)
            #self.InitKeywordSearchControls()
            #self.notebook1.Show(False)
            wx.BeginBusyCursor()
            #self.InitKeywordSearchControls()
            #self.notebookKeywords.Show(True)
            if not Globals.frmGlobalKeywords:
                import MDIChildKeywords
                Globals.frmGlobalKeywords = MDIChildKeywords.create(self)
            
            Globals.frmGlobalKeywords.Show(True)
            Globals.frmGlobalKeywords.Activate()
            Globals.frmGlobalKeywords.Maximize(True)
            wx.EndBusyCursor()
            #print 'cliked'
        event.Skip()    
            
       
    def OnTimelineButton(self, event):
        if Globals.CaseOpen:
            wx.BeginBusyCursor()
            busy = wx.BusyInfo("Creating MAC Timelines...")
            wx.Yield()
            if not Globals.frmGlobalTimeline:
                import MDIChildTimeline
                #import MDIChildFileListTimeline
                Globals.frmGlobalTimeline = MDIChildTimeline.create(self)
            Globals.frmGlobalTimeline.SetPosition(wx.Point(0, 0))
            Globals.frmGlobalTimeline.Show(True)
            Globals.frmGlobalTimeline.Activate()
            Globals.frmGlobalTimeline.Maximize(True)
            wx.EndBusyCursor()
            #print 'cliked'
        event.Skip() 
        
        
    def OnTextCategorizationButton(self, event):
        if Globals.CaseOpen:
            #self.notebookCase.Show(False)
            #self.InitKeywordSearchControls()
            #self.notebook1.Show(False)
            wx.BeginBusyCursor()
            #self.InitKeywordSearchControls()
            #self.notebookKeywords.Show(True)
            if not Globals.frmGlobalTextCat:
                import MDIChildTextMining
                Globals.frmGlobalTextCat = MDIChildTextMining.create(self)
            
            Globals.frmGlobalTextCat.Show(True)
            Globals.frmGlobalTextCat.Activate()
            Globals.frmGlobalTextCat.Maximize(True)
            wx.EndBusyCursor()
            #print 'cliked'
        event.Skip() 

      

    def OnBtnKeywordsExReportButton(self, event):
        event.Skip()
        
    def OnBtnBackToCaseButton(self, event):
        self.notebookKeywords.Show(False)
        self.notebookCase.Show(True)
        Globals.frmGlobalKeywords.Show(False)
        if Globals.frmGlobalFileList:
            Globals.frmGlobalFileList.Show(True)
            Globals.frmGlobalFileList.Maximize(True)
        event.Skip()
    

    def OnBtnCategoryViewButton(self, event):
        self.btnDirTreeView.Enable(True)
        self.btnDirTreeView.SetValue(False)
        self.btnCategoryView.Enable(False)
        self.treeDirView = False
        self.ShowFileCategoryView()
        event.Skip()

    def OnMenuViewsViewdetailsMenu(self, event):
        self.menuViews.Check(wxID_FRMMAINFRAMEMENUVIEWSVIEWDETAILS, True)
        self.menuViews.Check(wxID_FRMMAINFRAMEMENUVIEWSVIEWICONS, False)
        event.Skip()

    def OnMenuViewsViewiconsMenu(self, event):
        self.menuViews.Check(wxID_FRMMAINFRAMEMENUVIEWSVIEWDETAILS, False)
        self.menuViews.Check(wxID_FRMMAINFRAMEMENUVIEWSVIEWICONS, True)
        event.Skip()
    
    #return 'Details', 'Icons'
    def GetViewsCheckedMenu(self):
        if self.menuViews.IsChecked(wxID_FRMMAINFRAMEMENUVIEWSVIEWDETAILS):
            return 'Details'
        else:
            return 'Icons'

    def OnMenuToolsMenuitemupdatensrlMenu(self, event):
        dlg = wx.MessageDialog(self, "Please select the folder that contains NSRL text files",
          'Message', wx.OK | wx.ICON_INFORMATION)
        try:
            self.ShowCaseProperties(False)
            dlg.ShowModal()
        finally:
            dlg.Destroy()
            
        dlg = wx.DirDialog(self)
        try:
            if dlg.ShowModal() == wx.ID_OK:
                dir = dlg.GetPath()
                # Your code
                import dlgNSRLProgress
                nsrlProgress = dlgNSRLProgress.create(self, dir)
                nsrlProgress.ShowModal()
        finally:
            dlg.Destroy()
        event.Skip()

    def OnMenuFileMenuitemcreatediskimageMenu(self, event):
        import dlgCreateDD
        createDD = dlgCreateDD.create(self)
        createDD.ShowModal()
        event.Skip()

    def OnEmailsButton(self, event):
        if Globals.CaseOpen:
            busy = wx.BusyInfo("Please wait! Loading Email Module...")
            wx.Yield()
            #wx.BeginBusyCursor()
            if not Globals.frmGlobalEmails:
                import MDIChildEmails
                Globals.frmGlobalEmails = MDIChildEmails.create(self)
            
            Globals.frmGlobalEmails.Show(True)
            Globals.frmGlobalEmails.Activate()
            Globals.frmGlobalEmails.Maximize(True)
            #wx.EndBusyCursor()
            #print 'cliked'
        event.Skip() 

    def OnExplorerButton(self, event):
        busy = wx.BusyInfo("Please wait! Loading Explorer...")
        wx.Yield()
        self.ShowFileListView()
            #print 'cliked'
        event.Skip() 
        
    def OnImageViewerButton(self, event):
        if Globals.CaseOpen:
            busy = wx.BusyInfo("Please wait! Loading ImageViewer...")
            wx.Yield()
            wx.BeginBusyCursor()
            if not Globals.frmGlobalImages:
                import MDIChildImage
                Globals.frmGlobalImages = MDIChildImage.create(self)
            #Globals.frmGlobalImages.Show(True)
            #Globals.frmGlobalImages.Activate()
            Globals.frmGlobalImages.Maximize(True)
            wx.EndBusyCursor()
        event.Skip()
        
    def OnLogViewerButton(self, event):
        event.Skip()
        
    def OnRegistryViewerButton(self, event):
        event.Skip()
        
    def OnMenuToolsItemresumescandiskMenu(self, event):
        if not Globals.CaseOpen:
            self.ShowOpenCaseMessage()
            return
        dlg = wx.DirDialog(self)
        try:
            if dlg.ShowModal() == wx.ID_OK:
                dir = dlg.GetPath()
                # Your code
                import dlgResumeScanProgress
                scanMAC = dlgResumeScanProgress.create(self, dir)
                #scanMAC.StartScan(dir)
                scanMAC.ShowModal()
                
        finally:
            dlg.Destroy()
        event.Skip()
       
        
    def OnBtnReportKnownFilesButton(self, event):
        import dlgKnownFilesReport
        knownFiles = dlgKnownFilesReport.create(self)
        knownFiles.ShowModal()
        event.Skip()
        

    def OnMenuToolsItemhexviewerMenu(self, event):
        import frmFileViewer
        fileProp = frmFileViewer.frmFileViewer(self)
        fileProp.Show()
        event.Skip()

    def OnMenuFileItemsitemwriteddtodiskMenu(self, event):
        import dlgWriteImageToDisk
        writeDisk = dlgWriteImageToDisk.create(self)
        writeDisk.ShowModal()
        event.Skip()
        
        
        
class MyApp(wx.App):
    # Every wxWidgets application must have a class derived from wx.App  
	# wxWindows calls this method to initialize the application
    def OnInit(self):
        # Create an instance of our customized Frame class
        Globals.ImagesFileName = "caseNew.ima"
        frame = create(None)
        import MDIChildImage
        Globals.frmGlobalImages = MDIChildImage.create(frame)
        Globals.frmGlobalImages.Show(True)
        Globals.frmGlobalImages.Activate()
        Globals.frmGlobalImages.Maximize(True)
        frame.Show(True)

        # Tell wxWindows that this is our main window
        self.SetTopWindow(frame)

        # Return a success flag
        return True



if __name__ == "__main__":
    app = MyApp(0)	# Create an instance of the application class
    app.MainLoop()	# Tell it to start processing events
