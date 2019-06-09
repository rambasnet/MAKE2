#Boa:MiniFrame:MDIChildFileList

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
    return MDIChildFileList(parent)

class CustomListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, ID, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        
        
[wxID_MDICHILDFILELIST, wxID_MDICHILDFILELISTBTNATIMEVIEWFILES, 
 wxID_MDICHILDFILELISTBTNATIMEZOOM, wxID_MDICHILDFILELISTBTNCTIMEZOOM, 
 wxID_MDICHILDFILELISTBTNCTVIEWFILES, wxID_MDICHILDFILELISTBTNMACVIEWFILES, 
 wxID_MDICHILDFILELISTBTNMACZOOM, wxID_MDICHILDFILELISTBTNMTIMEVIEWFILES, 
 wxID_MDICHILDFILELISTBTNMTIMEZOOM, wxID_MDICHILDFILELISTBTNSHOWTIMELINES, 
 wxID_MDICHILDFILELISTBUTTON1, wxID_MDICHILDFILELISTBUTTON2, 
 wxID_MDICHILDFILELISTBUTTON3, wxID_MDICHILDFILELISTBUTTON4, 
 wxID_MDICHILDFILELISTBUTTON5, wxID_MDICHILDFILELISTGENTOGGLEBUTTON1, 
 wxID_MDICHILDFILELISTGENTOGGLEBUTTON2, wxID_MDICHILDFILELISTLISTVIEW1, 
 wxID_MDICHILDFILELISTPANEL1, wxID_MDICHILDFILELISTPANEL2, 
 wxID_MDICHILDFILELISTPANEL3, wxID_MDICHILDFILELISTPANEL4, 
 wxID_MDICHILDFILELISTPANTEXTTIMELINE, wxID_MDICHILDFILELISTSPLITTERWINDOW1, 
 wxID_MDICHILDFILELISTSTATICBITMAP1, wxID_MDICHILDFILELISTSTATICBITMAP2, 
 wxID_MDICHILDFILELISTSTATICBITMAP3, wxID_MDICHILDFILELISTSTATICBITMAP4, 
 wxID_MDICHILDFILELISTSTATICBITMAP5, wxID_MDICHILDFILELISTSTATICBITMAP6, 
 wxID_MDICHILDFILELISTSTATICBOX1, wxID_MDICHILDFILELISTSTATICBOX2, 
 wxID_MDICHILDFILELISTSTATICBOX3, wxID_MDICHILDFILELISTSTATICBOX4, 
 wxID_MDICHILDFILELISTSTATICTEXT1, wxID_MDICHILDFILELISTSTATICTEXT10, 
 wxID_MDICHILDFILELISTSTATICTEXT11, wxID_MDICHILDFILELISTSTATICTEXT12, 
 wxID_MDICHILDFILELISTSTATICTEXT13, wxID_MDICHILDFILELISTSTATICTEXT2, 
 wxID_MDICHILDFILELISTSTATICTEXT3, wxID_MDICHILDFILELISTSTATICTEXT4, 
 wxID_MDICHILDFILELISTSTATICTEXT5, wxID_MDICHILDFILELISTSTATICTEXT6, 
 wxID_MDICHILDFILELISTSTATICTEXT7, wxID_MDICHILDFILELISTSTATICTEXT8, 
 wxID_MDICHILDFILELISTSTATICTEXT9, wxID_MDICHILDFILELISTTEXTCTRL2, 
 wxID_MDICHILDFILELISTTEXTCTRL4, wxID_MDICHILDFILELISTTREECTRL1, 
 wxID_MDICHILDFILELISTTXTATIMEFROM, wxID_MDICHILDFILELISTTXTATIMETO, 
 wxID_MDICHILDFILELISTTXTCRFROM, wxID_MDICHILDFILELISTTXTCTIMEFROM, 
 wxID_MDICHILDFILELISTTXTCTIMTO, wxID_MDICHILDFILELISTTXTMTIMEFROM, 
 wxID_MDICHILDFILELISTTXTMTIMETO, 
] = [wx.NewId() for _init_ctrls in range(57)]

[wxID_MDICHILDFILELISTPOPUPMENUDIRMD5HASHCHILDREN, 
 wxID_MDICHILDFILELISTPOPUPMENUDIRMD5HASHSELECTED, 
] = [wx.NewId() for _init_coll_popupMenuDir_Items in range(2)]

[wxID_MDICHILDFILELISTPOPUPMENUFILEGENMD5FILES, 
 wxID_MDICHILDFILELISTPOPUPMENUFILEGENSHA, 
 wxID_MDICHILDFILELISTPOPUPMENUFILEMENUITEMOPENFILE, 
 wxID_MDICHILDFILELISTPOPUPMENUFILEMENUITEMVIEWFILE, 
] = [wx.NewId() for _init_coll_popupMenuFile_Items in range(4)]

[wxID_MDICHILDFILELISTPOPUPMENUSHASHA1DIGEST, 
 wxID_MDICHILDFILELISTPOPUPMENUSHASHA224DIGEST, 
 wxID_MDICHILDFILELISTPOPUPMENUSHASHA256DIGEST, 
 wxID_MDICHILDFILELISTPOPUPMENUSHASHA384DIGEST, 
 wxID_MDICHILDFILELISTPOPUPMENUSHASHA512DIGEST, 
] = [wx.NewId() for _init_coll_popupMenuSHA_Items in range(5)]

class MDIChildFileList(wx.MDIChildFrame, listmix.ColumnSorterMixin):

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.MDIChildFrame.__init__(self, id=wxID_MDICHILDFILELIST,
              name=u'MDIChildFileList', parent=prnt, pos=wx.Point(333, 169),
              size=wx.Size(1198, 742), style=wx.DEFAULT_FRAME_STYLE,
              title=u'File List')
        self.SetClientSize(wx.Size(1190, 711))
        self.SetBackgroundColour(wx.Colour(125, 152, 221))
        self.SetIcon(wx.Icon('./Images/FNSFIcon.ico',wx.BITMAP_TYPE_ICO))
        self.SetAutoLayout(True)

        self.panel1 = wx.Panel(id=wxID_MDICHILDFILELISTPANEL1, name='panel1',
              parent=self, pos=wx.Point(16, 24), size=wx.Size(928, 160),
              style=wx.TAB_TRAVERSAL)
        self.panel1.SetBackgroundColour(wx.Colour(128, 128, 255))
        self.panel1.SetAutoLayout(True)

        self.panel2 = wx.Panel(id=wxID_MDICHILDFILELISTPANEL2, name='panel2',
              parent=self.panel1, pos=wx.Point(0, 0), size=wx.Size(928, 120),
              style=wx.TAB_TRAVERSAL)
        self.panel2.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.panel2.SetConstraints(LayoutAnchors(self.panel2, True, True, True,
              False))
        self.panel2.SetAutoLayout(False)
        self.panel2.Bind(wx.EVT_SIZE, self.OnPanel2Size)
        self.panel2.Bind(wx.EVT_MOVE, self.OnPanel2Move)
        self.panel2.Bind(wx.EVT_PAINT, self.OnPanel2Paint)

        self.button1 = wx.Button(id=wxID_MDICHILDFILELISTBUTTON1,
              label='View Selected', name='button1', parent=self.panel1,
              pos=wx.Point(8, 126), size=wx.Size(88, 23), style=0)
        self.button1.Bind(wx.EVT_BUTTON, self.OnButton1Button,
              id=wxID_MDICHILDFILELISTBUTTON1)

        self.button2 = wx.Button(id=wxID_MDICHILDFILELISTBUTTON2,
              label='View All', name='button2', parent=self.panel1,
              pos=wx.Point(112, 128), size=wx.Size(64, 24), style=0)
        self.button2.Bind(wx.EVT_BUTTON, self.OnButton2Button,
              id=wxID_MDICHILDFILELISTBUTTON2)

        self.button3 = wx.Button(id=wxID_MDICHILDFILELISTBUTTON3,
              label='Zoom Selection', name='button3', parent=self.panel1,
              pos=wx.Point(192, 128), size=wx.Size(88, 23), style=0)
        self.button3.Bind(wx.EVT_BUTTON, self.OnButton3Button,
              id=wxID_MDICHILDFILELISTBUTTON3)

        self.button4 = wx.Button(id=wxID_MDICHILDFILELISTBUTTON4,
              label='Zoom All', name='button4', parent=self.panel1,
              pos=wx.Point(296, 128), size=wx.Size(64, 23), style=0)
        self.button4.Bind(wx.EVT_BUTTON, self.OnButton4Button,
              id=wxID_MDICHILDFILELISTBUTTON4)

        self.staticText3 = wx.StaticText(id=wxID_MDICHILDFILELISTSTATICTEXT3,
              label='Timpe Span:', name='staticText3', parent=self.panel1,
              pos=wx.Point(408, 136), size=wx.Size(69, 13), style=0)
        self.staticText3.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'Tahoma'))

        self.staticText4 = wx.StaticText(id=wxID_MDICHILDFILELISTSTATICTEXT4,
              label='00/00/0000 00:00:00', name='staticText4',
              parent=self.panel1, pos=wx.Point(480, 136), size=wx.Size(103, 13),
              style=0)

        self.staticText5 = wx.StaticText(id=wxID_MDICHILDFILELISTSTATICTEXT5,
              label='Mouse At:', name='staticText5', parent=self.panel1,
              pos=wx.Point(608, 136), size=wx.Size(56, 13), style=0)
        self.staticText5.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'Tahoma'))

        self.staticText6 = wx.StaticText(id=wxID_MDICHILDFILELISTSTATICTEXT6,
              label='00/00/0000 00:00:00  ', name='staticText6',
              parent=self.panel1, pos=wx.Point(672, 136), size=wx.Size(109, 13),
              style=0)

        self.staticText7 = wx.StaticText(id=wxID_MDICHILDFILELISTSTATICTEXT7,
              label='File Stats:', name='staticText7', parent=self.panel1,
              pos=wx.Point(784, 136), size=wx.Size(55, 13), style=0)
        self.staticText7.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'Tahoma'))

        self.staticText8 = wx.StaticText(id=wxID_MDICHILDFILELISTSTATICTEXT8,
              label='staticText8', name='staticText8', parent=self.panel1,
              pos=wx.Point(848, 136), size=wx.Size(54, 13), style=0)

        self.splitterWindow1 = wx.SplitterWindow(id=wxID_MDICHILDFILELISTSPLITTERWINDOW1,
              name='splitterWindow1', parent=self, pos=wx.Point(16, 488),
              size=wx.Size(600, 200), style=wx.SP_3D)
        self.splitterWindow1.SetBackgroundColour(wx.Colour(128, 0, 255))

        self.panel3 = wx.Panel(id=wxID_MDICHILDFILELISTPANEL3, name='panel3',
              parent=self.splitterWindow1, pos=wx.Point(0, 0), size=wx.Size(200,
              200), style=wx.TAB_TRAVERSAL)

        self.panel4 = wx.Panel(id=wxID_MDICHILDFILELISTPANEL4, name='panel4',
              parent=self.splitterWindow1, pos=wx.Point(204, 0),
              size=wx.Size(396, 200), style=wx.TAB_TRAVERSAL)
        self.splitterWindow1.SplitVertically(self.panel3, self.panel4, 200)

        self.treeCtrl1 = wx.TreeCtrl(id=wxID_MDICHILDFILELISTTREECTRL1,
              name='treeCtrl1', parent=self.panel3, pos=wx.Point(8, 48),
              size=wx.Size(184, 144), style=wx.TR_HAS_BUTTONS)

        self.button5 = wx.Button(id=wxID_MDICHILDFILELISTBUTTON5,
              label='button5', name='button5', parent=self.panel4,
              pos=wx.Point(312, 8), size=wx.Size(75, 23), style=0)

        self.genToggleButton1 = wx.lib.buttons.GenToggleButton(id=wxID_MDICHILDFILELISTGENTOGGLEBUTTON1,
              label='genToggleButton1', name='genToggleButton1',
              parent=self.panel3, pos=wx.Point(8, 16), size=wx.Size(80, 24),
              style=0)

        self.genToggleButton2 = wx.lib.buttons.GenToggleButton(id=wxID_MDICHILDFILELISTGENTOGGLEBUTTON2,
              label='genToggleButton2', name='genToggleButton2',
              parent=self.panel3, pos=wx.Point(96, 16), size=wx.Size(96, 25),
              style=0)

        self.listView1 = wx.ListView(id=wxID_MDICHILDFILELISTLISTVIEW1,
              name='listView1', parent=self.panel4, pos=wx.Point(8, 40),
              size=wx.Size(376, 152), style=wx.LC_ICON)

        self.panTextTimeline = wx.Panel(id=wxID_MDICHILDFILELISTPANTEXTTIMELINE,
              name='panTextTimeline', parent=self, pos=wx.Point(16, 133),
              size=wx.Size(1168, 88),
              style=wx.CLIP_CHILDREN | wx.TAB_TRAVERSAL)
        self.panTextTimeline.SetBackgroundColour(wx.Colour(192, 192, 192))
        self.panTextTimeline.SetConstraints(LayoutAnchors(self.panTextTimeline,
              True, False, True, False))

        self.txtCrFrom = wx.StaticText(id=wxID_MDICHILDFILELISTTXTCRFROM,
              label='From:', name='txtCrFrom', parent=self.panTextTimeline,
              pos=wx.Point(616, 24), size=wx.Size(28, 13), style=0)

        self.staticText10 = wx.StaticText(id=wxID_MDICHILDFILELISTSTATICTEXT10,
              label='To:', name='staticText10', parent=self.panTextTimeline,
              pos=wx.Point(624, 48), size=wx.Size(16, 13), style=0)

        self.txtATimeTo = wx.TextCtrl(id=wxID_MDICHILDFILELISTTXTATIMETO,
              name='txtATimeTo', parent=self.panTextTimeline, pos=wx.Point(648,
              48), size=wx.Size(120, 21), style=0, value='00/00/0000 00:00:00')

        self.txtATimeFrom = wx.TextCtrl(id=wxID_MDICHILDFILELISTTXTATIMEFROM,
              name='txtATimeFrom', parent=self.panTextTimeline,
              pos=wx.Point(648, 24), size=wx.Size(120, 21), style=0,
              value='00/00/0000 00:00:00')

        self.btnATimeZoom = wx.Button(id=wxID_MDICHILDFILELISTBTNATIMEZOOM,
              label='Zoom', name='btnATimeZoom', parent=self.panTextTimeline,
              pos=wx.Point(784, 48), size=wx.Size(80, 23), style=0)
        self.btnATimeZoom.Bind(wx.EVT_BUTTON, self.OnBtnATimeZoomButton,
              id=wxID_MDICHILDFILELISTBTNATIMEZOOM)

        self.staticBox2 = wx.StaticBox(id=wxID_MDICHILDFILELISTSTATICBOX2,
              label='Created Time', name='staticBox2',
              parent=self.panTextTimeline, pos=wx.Point(8, 8), size=wx.Size(280,
              72), style=0)

        self.staticText11 = wx.StaticText(id=wxID_MDICHILDFILELISTSTATICTEXT11,
              label='From:', name='staticText11', parent=self.panTextTimeline,
              pos=wx.Point(24, 24), size=wx.Size(28, 13), style=0)

        self.staticText9 = wx.StaticText(id=wxID_MDICHILDFILELISTSTATICTEXT9,
              label='To:', name='staticText9', parent=self.panTextTimeline,
              pos=wx.Point(32, 48), size=wx.Size(16, 13), style=0)

        self.txtCTimeFrom = wx.TextCtrl(id=wxID_MDICHILDFILELISTTXTCTIMEFROM,
              name='txtCTimeFrom', parent=self.panTextTimeline, pos=wx.Point(56,
              24), size=wx.Size(120, 21), style=0, value='00/00/0000 00:00:00')

        self.txtCTimTo = wx.TextCtrl(id=wxID_MDICHILDFILELISTTXTCTIMTO,
              name='txtCTimTo', parent=self.panTextTimeline, pos=wx.Point(56,
              48), size=wx.Size(120, 21), style=0, value='00/00/0000 00:00:00')

        self.btnCTimeZoom = wx.Button(id=wxID_MDICHILDFILELISTBTNCTIMEZOOM,
              label='Zoom', name='btnCTimeZoom', parent=self.panTextTimeline,
              pos=wx.Point(192, 48), size=wx.Size(80, 23), style=0)
        self.btnCTimeZoom.Bind(wx.EVT_BUTTON, self.OnBtnCTimeZoomButton,
              id=wxID_MDICHILDFILELISTBTNCTIMEZOOM)

        self.staticBox1 = wx.StaticBox(id=wxID_MDICHILDFILELISTSTATICBOX1,
              label='Accessed Time', name='staticBox1',
              parent=self.panTextTimeline, pos=wx.Point(600, 8),
              size=wx.Size(280, 72), style=0)

        self.btnCTViewFiles = wx.Button(id=wxID_MDICHILDFILELISTBTNCTVIEWFILES,
              label='View Files', name='btnCTViewFiles',
              parent=self.panTextTimeline, pos=wx.Point(192, 24),
              size=wx.Size(80, 23), style=0)
        self.btnCTViewFiles.Bind(wx.EVT_BUTTON, self.OnBtnCTViewFilesButton,
              id=wxID_MDICHILDFILELISTBTNCTVIEWFILES)

        self.btnATimeViewFiles = wx.Button(id=wxID_MDICHILDFILELISTBTNATIMEVIEWFILES,
              label='View Files', name='btnATimeViewFiles',
              parent=self.panTextTimeline, pos=wx.Point(784, 24),
              size=wx.Size(80, 23), style=0)
        self.btnATimeViewFiles.Bind(wx.EVT_BUTTON,
              self.OnBtnATimeViewFilesButton,
              id=wxID_MDICHILDFILELISTBTNATIMEVIEWFILES)

        self.txtMTimeTo = wx.TextCtrl(id=wxID_MDICHILDFILELISTTXTMTIMETO,
              name='txtMTimeTo', parent=self.panTextTimeline, pos=wx.Point(352,
              48), size=wx.Size(120, 21), style=0, value='00/00/0000 00:00:00')

        self.staticBox3 = wx.StaticBox(id=wxID_MDICHILDFILELISTSTATICBOX3,
              label='Modified Time', name='staticBox3',
              parent=self.panTextTimeline, pos=wx.Point(304, 8),
              size=wx.Size(280, 72), style=0)

        self.staticText13 = wx.StaticText(id=wxID_MDICHILDFILELISTSTATICTEXT13,
              label='To:', name='staticText13', parent=self.panTextTimeline,
              pos=wx.Point(328, 48), size=wx.Size(16, 16), style=0)

        self.btnMTimeZoom = wx.Button(id=wxID_MDICHILDFILELISTBTNMTIMEZOOM,
              label='Zoom', name='btnMTimeZoom', parent=self.panTextTimeline,
              pos=wx.Point(488, 48), size=wx.Size(80, 23), style=0)
        self.btnMTimeZoom.Bind(wx.EVT_BUTTON, self.OnBtnMTimeZoomButton,
              id=wxID_MDICHILDFILELISTBTNMTIMEZOOM)

        self.btnMTimeViewFiles = wx.Button(id=wxID_MDICHILDFILELISTBTNMTIMEVIEWFILES,
              label='View Files', name='btnMTimeViewFiles',
              parent=self.panTextTimeline, pos=wx.Point(488, 24),
              size=wx.Size(80, 23), style=0)
        self.btnMTimeViewFiles.Bind(wx.EVT_BUTTON,
              self.OnBtnMTimeViewFilesButton,
              id=wxID_MDICHILDFILELISTBTNMTIMEVIEWFILES)

        self.txtMTimeFrom = wx.TextCtrl(id=wxID_MDICHILDFILELISTTXTMTIMEFROM,
              name='txtMTimeFrom', parent=self.panTextTimeline,
              pos=wx.Point(352, 24), size=wx.Size(120, 21), style=0,
              value='00/00/0000 00:00:00')

        self.staticBox3 = wx.StaticBox(id=wxID_MDICHILDFILELISTSTATICBOX3,
              label='Modified Time', name='staticBox3',
              parent=self.panTextTimeline, pos=wx.Point(304, 8),
              size=wx.Size(280, 72), style=0)

        self.staticText12 = wx.StaticText(id=wxID_MDICHILDFILELISTSTATICTEXT12,
              label='From:', name='staticText12', parent=self.panTextTimeline,
              pos=wx.Point(320, 24), size=wx.Size(28, 13), style=0)

        self.textCtrl4 = wx.TextCtrl(id=wxID_MDICHILDFILELISTTEXTCTRL4,
              name='textCtrl4', parent=self.panTextTimeline, pos=wx.Point(928,
              24), size=wx.Size(128, 21), style=0, value='00/00/0000 00:00:00')

        self.staticText1 = wx.StaticText(id=wxID_MDICHILDFILELISTSTATICTEXT1,
              label='From:', name='staticText1', parent=self.panTextTimeline,
              pos=wx.Point(896, 32), size=wx.Size(28, 13), style=0)

        self.staticText2 = wx.StaticText(id=wxID_MDICHILDFILELISTSTATICTEXT2,
              label='To:', name='staticText2', parent=self.panTextTimeline,
              pos=wx.Point(904, 56), size=wx.Size(16, 13), style=0)

        self.textCtrl2 = wx.TextCtrl(id=wxID_MDICHILDFILELISTTEXTCTRL2,
              name='textCtrl2', parent=self.panTextTimeline, pos=wx.Point(928,
              48), size=wx.Size(128, 21), style=0,
              value='"00/00/0000 00:00:00"')

        self.staticBitmap3 = wx.StaticBitmap(bitmap=wx.Bitmap(u'C:/NMT/Research/ForensicsTool/DigitalForensics/TimelineImages/create_line.gif',
              wx.BITMAP_TYPE_GIF), id=wxID_MDICHILDFILELISTSTATICBITMAP3,
              name='staticBitmap3', parent=self.panTextTimeline,
              pos=wx.Point(88, 8), size=wx.Size(184, 16), style=0)

        self.staticBitmap5 = wx.StaticBitmap(bitmap=wx.Bitmap(u'C:/NMT/Research/ForensicsTool/DigitalForensics/TimelineImages/modify_line.gif',
              wx.BITMAP_TYPE_GIF), id=wxID_MDICHILDFILELISTSTATICBITMAP5,
              name='staticBitmap5', parent=self.panTextTimeline,
              pos=wx.Point(384, 8), size=wx.Size(184, 16), style=0)

        self.staticBox4 = wx.StaticBox(id=wxID_MDICHILDFILELISTSTATICBOX4,
              label='MAC Timelines', name='staticBox4',
              parent=self.panTextTimeline, pos=wx.Point(888, 8),
              size=wx.Size(272, 72), style=0)

        self.staticBitmap2 = wx.StaticBitmap(bitmap=wx.Bitmap(u'C:/NMT/Research/ForensicsTool/DigitalForensics/TimelineImages/modify_line.gif',
              wx.BITMAP_TYPE_GIF), id=wxID_MDICHILDFILELISTSTATICBITMAP2,
              name='staticBitmap2', parent=self.panTextTimeline,
              pos=wx.Point(1032, 8), size=wx.Size(56, 16), style=0)

        self.staticBitmap4 = wx.StaticBitmap(bitmap=wx.Bitmap(u'C:/NMT/Research/ForensicsTool/DigitalForensics/TimelineImages/create_line.gif',
              wx.BITMAP_TYPE_GIF), id=wxID_MDICHILDFILELISTSTATICBITMAP4,
              name='staticBitmap4', parent=self.panTextTimeline,
              pos=wx.Point(968, 8), size=wx.Size(64, 16), style=0)

        self.staticBitmap6 = wx.StaticBitmap(bitmap=wx.Bitmap(u'C:/NMT/Research/ForensicsTool/DigitalForensics/TimelineImages/access_line.gif',
              wx.BITMAP_TYPE_GIF), id=wxID_MDICHILDFILELISTSTATICBITMAP6,
              name='staticBitmap6', parent=self.panTextTimeline,
              pos=wx.Point(688, 8), size=wx.Size(176, 16), style=0)

        self.staticBitmap1 = wx.StaticBitmap(bitmap=wx.Bitmap(u'C:/NMT/Research/ForensicsTool/DigitalForensics/TimelineImages/access_line.gif',
              wx.BITMAP_TYPE_GIF), id=wxID_MDICHILDFILELISTSTATICBITMAP1,
              name='staticBitmap1', parent=self.panTextTimeline,
              pos=wx.Point(1088, 8), size=wx.Size(64, 16), style=0)

        self.btnMACViewFiles = wx.Button(id=wxID_MDICHILDFILELISTBTNMACVIEWFILES,
              label='View Files', name='btnMACViewFiles',
              parent=self.panTextTimeline, pos=wx.Point(1072, 24),
              size=wx.Size(80, 23), style=0)
        self.btnMACViewFiles.Bind(wx.EVT_BUTTON, self.OnBtnMACViewFilesButton,
              id=wxID_MDICHILDFILELISTBTNMACVIEWFILES)

        self.btnMACZoom = wx.Button(id=wxID_MDICHILDFILELISTBTNMACZOOM,
              label='Zoom', name='btnMACZoom', parent=self.panTextTimeline,
              pos=wx.Point(1072, 48), size=wx.Size(80, 23), style=0)
        self.btnMACZoom.Bind(wx.EVT_BUTTON, self.OnBtnMACZoomButton,
              id=wxID_MDICHILDFILELISTBTNMACZOOM)

        self.btnShowTimelines = wx.Button(id=wxID_MDICHILDFILELISTBTNSHOWTIMELINES,
              label='Show Timelines', name='btnShowTimelines',
              parent=self.panel4, pos=wx.Point(200, 8), size=wx.Size(99, 23),
              style=0)
        self.btnShowTimelines.Bind(wx.EVT_BUTTON, self.OnBtnShowTimelinesButton,
              id=wxID_MDICHILDFILELISTBTNSHOWTIMELINES)

    def __init__(self, parent):
        self._init_ctrls(parent)
        #self.CreateTreeControl()
        #self.CreateScrolledWinTimeline()
        """
    def CreateFileListsCtrl(self):
        self.splitterWindow1 = wx.SplitterWindow(id=-1,
              name='splitterWindow1', parent=self, size=wx.Size(600, 200), style=wx.SP_3D)
              
        self.splitterWindow1.SetBackgroundColour(wx.Colour(225, 236, 255))
        self.splitterWindow1.SetConstraints(LayoutAnchors(self.splitterWindow1,
              True, True, True, True))
        self.splitterWindow1.SetMinimumPaneSize(20)
        
        self.panFileType = wx.Panel(id=-1, name='panel3',
              parent=self.splitterWindow1, pos=wx.Point(0, 0), size=wx.Size(200,
              200), style=wx.TAB_TRAVERSAL)
        self.panFileType.SetBackgroundColour(wx.Colour(225, 236, 255))
        self.panFileType.SetAutoLayout(True)
        
        self.panFileList = wx.Panel(id=-1, name='panel4',
              parent=self.splitterWindow1, pos=wx.Point(204, 0),
              size=wx.Size(400, 200), style=wx.TAB_TRAVERSAL)
              
        self.splitterWindow1.SplitVertically(self.panFileType, self.panFileList, 200)

        self.panFileList.SetBackgroundColour(wx.Colour(225, 236, 255))
        self.panFileList.SetAutoLayout(True)
        
        self.treeFileType = wx.TreeCtrl(id=wx.NewId(),
              name='treeCtrl1', parent=self.panFileType, pos=wx.Point(8, 8),
              size=wx.Size(184, 184), style=wx.TR_HAS_BUTTONS)
        self.treeFileType.SetConstraints(LayoutAnchors(self.treeFileType, True,
              True, True, True))
        self.treeFileType.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL, False, 'Tahoma'))

        self.lstFiles = wx.ListCtrl(id=wx.NewId(),
              name='listCtrl1', parent=self.panFileList, pos=wx.Point(8, 8),
              size=wx.Size(380, 184), style=wx.LC_AUTOARRANGE | wx.LC_ICON)
        self.lstFiles.SetConstraints(LayoutAnchors(self.lstFiles, True,
              True, True, True))
        self.lstFiles.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL, False, 'Tahoma'))
        
        return self.splitterWindow1
    """
    
        
    def CreateScrolledWinTimeline(self):
        self.panTextTimeline = wx.ScrolledWindow(id=-1,
              name='panTextTimeline', parent=self, pos=wx.Point(16, 440),
              size=wx.Size(896, 88), style=wx.CLIP_CHILDREN | wx.TAB_TRAVERSAL)
        self.panTextTimeline.SetConstraints(LayoutAnchors(self.panTextTimeline, True, True, True,
              True))
        self.panTextTimeline.EnableScrolling(True, True)
        """
        self.panTextTimeline = wx.Panel(id=-1,
              name='panTextTimeline', parent=self, pos=wx.Point(16, 216),
              size=wx.Size(896, 88), style=wx.CLIP_CHILDREN | wx.TAB_TRAVERSAL)
        """
        self.panTextTimeline.SetBackgroundColour(wx.Colour(192, 192, 192))

        self.txtCrFrom = wx.StaticText(id=-1,
              label='From:', name='txtCrFrom', parent=self.panTextTimeline,
              pos=wx.Point(616, 24), size=wx.Size(28, 13), style=0)

        self.staticText10 = wx.StaticText(id=-1,
              label='To:', name='staticText10', parent=self.panTextTimeline,
              pos=wx.Point(624, 48), size=wx.Size(16, 13), style=0)

        self.txtCreatedStartTime = wx.TextCtrl(id=-1,
              name='txtCreatedStartTime', parent=self.panTextTimeline,
              pos=wx.Point(648, 48), size=wx.Size(120, 21), style=0,
              value='00/00/0000 00:00:00')

        self.textCtrl1 = wx.TextCtrl(id=-1,
              name='textCtrl1', parent=self.panTextTimeline, pos=wx.Point(648,
              24), size=wx.Size(120, 21), style=0, value='00/00/0000 00:00:00')

        self.button6 = wx.Button(id=-1, label='Zoom',
              name='button6', parent=self.panTextTimeline, pos=wx.Point(784,
              48), size=wx.Size(80, 23), style=0)

        self.staticBox2 = wx.StaticBox(id=-1,
              label='Created Time', name='staticBox2',
              parent=self.panTextTimeline, pos=wx.Point(8, 8), size=wx.Size(280,
              72), style=0)

        self.staticBitmap4 = wx.StaticBitmap(bitmap=wx.Bitmap(u'C:/NMT/Research/ForensicsTool/DigitalForensics/TimelineImages/create_line.gif',
              wx.BITMAP_TYPE_GIF), id=-1,
              name='staticBitmap4', parent=self.panTextTimeline,
              pos=wx.Point(88, 8), size=wx.Size(184, 16), style=0)

        self.staticText11 = wx.StaticText(id=-1,
              label='From:', name='staticText11', parent=self.panTextTimeline,
              pos=wx.Point(24, 24), size=wx.Size(28, 13), style=0)

        self.staticText9 = wx.StaticText(id=-1,
              label='To:', name='staticText9', parent=self.panTextTimeline,
              pos=wx.Point(32, 48), size=wx.Size(16, 13), style=0)

        self.textCtrl5 = wx.TextCtrl(id=-1,
              name='textCtrl5', parent=self.panTextTimeline, pos=wx.Point(56,
              24), size=wx.Size(120, 21), style=0, value='00/00/0000 00:00:00')

        self.textCtrl3 = wx.TextCtrl(id=-1,
              name='textCtrl3', parent=self.panTextTimeline, pos=wx.Point(56,
              48), size=wx.Size(120, 21), style=0, value='00/00/0000 00:00:00')

        self.button7 = wx.Button(id=-1, label='Zoom',
              name='button7', parent=self.panTextTimeline, pos=wx.Point(192,
              48), size=wx.Size(80, 23), style=0)

        self.staticBox1 = wx.StaticBox(id=-1,
              label='Created Time', name='staticBox1',
              parent=self.panTextTimeline, pos=wx.Point(600, 8),
              size=wx.Size(280, 72), style=0)

        self.button8 = wx.Button(id=-1,
              label='View Files', name='button8', parent=self.panTextTimeline,
              pos=wx.Point(192, 24), size=wx.Size(80, 23), style=0)

        self.button9 = wx.Button(id=-1,
              label='View Files', name='button9', parent=self.panTextTimeline,
              pos=wx.Point(784, 24), size=wx.Size(80, 23), style=0)

        self.staticBitmap1 = wx.StaticBitmap(bitmap=wx.Bitmap(u'C:/NMT/Research/ForensicsTool/DigitalForensics/TimelineImages/access_line.gif',
              wx.BITMAP_TYPE_GIF), id=-1,
              name='staticBitmap1', parent=self.panTextTimeline,
              pos=wx.Point(680, 8), size=wx.Size(184, 16), style=0)

        self.textCtrl6 = wx.TextCtrl(id=-1,
              name='textCtrl6', parent=self.panTextTimeline, pos=wx.Point(352,
              48), size=wx.Size(120, 21), style=0, value='00/00/0000 00:00:00')

        self.staticBox3 = wx.StaticBox(id=-1,
              label='Created Time', name='staticBox3',
              parent=self.panTextTimeline, pos=wx.Point(304, 8),
              size=wx.Size(280, 72), style=0)

        self.staticText13 = wx.StaticText(id=-1,
              label='To:', name='staticText13', parent=self.panTextTimeline,
              pos=wx.Point(328, 48), size=wx.Size(16, 16), style=0)

        self.button10 = wx.Button(id=-1,
              label='Zoom', name='button10', parent=self.panTextTimeline,
              pos=wx.Point(488, 48), size=wx.Size(80, 23), style=0)

        self.button11 = wx.Button(id=-1,
              label='View Files', name='button11', parent=self.panTextTimeline,
              pos=wx.Point(488, 24), size=wx.Size(80, 23), style=0)

        self.textCtrl7 = wx.TextCtrl(id=-1,
              name='textCtrl7', parent=self.panTextTimeline, pos=wx.Point(352,
              24), size=wx.Size(120, 21), style=0, value='00/00/0000 00:00:00')

        self.staticBitmap3 = wx.StaticBitmap(bitmap=wx.Bitmap(u'C:/NMT/Research/ForensicsTool/DigitalForensics/TimelineImages/modify_line.gif',
              wx.BITMAP_TYPE_GIF), id=-1,
              name='staticBitmap3', parent=self.panTextTimeline,
              pos=wx.Point(384, 8), size=wx.Size(184, 16), style=0)

        self.staticBox3 = wx.StaticBox(id=-1,
              label='Created Time', name='staticBox3',
              parent=self.panTextTimeline, pos=wx.Point(304, 8),
              size=wx.Size(280, 72), style=0)

        self.staticText12 = wx.StaticText(id=-1,
              label='From:', name='staticText12', parent=self.panTextTimeline,
              pos=wx.Point(320, 24), size=wx.Size(28, 13), style=0)

        self.staticBitmap2 = wx.StaticBitmap(bitmap=wx.Bitmap(u'C:/NMT/Research/ForensicsTool/DigitalForensics/TimelineImages/modify_line.gif',
              wx.BITMAP_TYPE_GIF), id=-1,
              name='staticBitmap2', parent=self.panTextTimeline,
              pos=wx.Point(384, 8), size=wx.Size(184, 16), style=0)
    
    
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
        
        info.m_format = wx.LIST_FORMAT_RIGHT
        info.m_text = "Size"
        self.listFilesDetails.InsertColumnInfo(1, info)
        
        info.m_format = wx.LIST_FORMAT_LEFT
        info.m_text = "Created Time"
        self.listFilesDetails.InsertColumnInfo(2, info)
        
        info.m_text = "Last Modified Time"
        self.listFilesDetails.InsertColumnInfo(3, info)
        
        info.m_text = "Last Accessed Time"
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
        if Globals.fileTreeView is None:
            Globals.fileTreeView = FileTreeView(self, self.treeDirList)
            self.TreeViewRoot = Globals.fileTreeView.AddDirectoryTreeNodes()
        
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

    def OnButton1Button(self, event):
        event.Skip()

    def OnButton2Button(self, event):
        event.Skip()

    def OnButton3Button(self, event):
        event.Skip()

    def OnButton4Button(self, event):
        event.Skip()

    def OnPanel2Size(self, event):
        event.Skip()

    def OnPanel2Move(self, event):
        event.Skip()

    def OnPanel2Paint(self, event):
        event.Skip()

    def OnBtnATimeZoomButton(self, event):
        event.Skip()

    def OnBtnCTimeZoomButton(self, event):
        event.Skip()

    def OnBtnCTViewFilesButton(self, event):
        event.Skip()

    def OnBtnATimeViewFilesButton(self, event):
        event.Skip()

    def OnBtnMTimeZoomButton(self, event):
        event.Skip()

    def OnBtnMTimeViewFilesButton(self, event):
        event.Skip()

    def OnBtnMACViewFilesButton(self, event):
        event.Skip()

    def OnBtnMACZoomButton(self, event):
        event.Skip()

    def OnBtnShowTimelinesButton(self, event):
        event.Skip()

        
        
class PanelHolder(wx.MDIParentFrame):
	def __init__(self, parent, id, title):
		# First, call the base class' __init__ method to create the frame
		wx.MDIParentFrame.__init__(self, parent, id, title)
		#self.panel = TimeLines(self,-1)
		self.panel = create(self)

# Every wxWidgets application must have a class derived from wx.App
class MyApp(wx.App):

	# wxWindows calls this method to initialize the application
	def OnInit(self):

		# Create an instance of our customized Frame class
		frame = PanelHolder(None, -1, "TimeLines")
		frame.Show(True)

		# Tell wxWindows that this is our main window
		self.SetTopWindow(frame)

		# Return a success flag
		return True


if __name__ == "__main__":
    app = MyApp(0)	# Create an instance of the application class
    app.MainLoop()	# Tell it to start processing events     
